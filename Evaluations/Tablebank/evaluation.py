
#import libraries
from collections import namedtuple
import numpy as np
import cv2
import glob
import time
import matplotlib
import matplotlib.pylab as plt
import glob
import mmcv
from mmcv.runner import load_checkpoint
import mmcv.visualization.image as mmcv_image
import lxml.etree as etree
import numpy as np
import os
import subprocess
import sys
from mmdet.models import build_detector
from mmdet.apis import inference_detector, show_result, init_detector
import cv2
import json


# Path to images.txt file
both_images_file = open("/content/drive/My Drive/TableBank/both_images.txt","w")

#reading json file for latex
latex_file = open("/content/drive/My Drive/TableBank/Latex.json","r")

#Loading json file for latex
latex_json = json.load(latex_file)

#reading json file for Word
word_file = open("/content/drive/My Drive/TableBank/Word.json","r")

#Loading json file for Word
word_json = json.load(word_file)

#Adding latex Images path to both_images.txt file
total = 0
for idx,i in enumerate(latex_json['images']):
  if(idx < 500):
    continue
  if(idx > 1500):
    break
  total+=1
  both_images_file.write("/content/drive/My Drive/TableBank/tablebank_latex/"+str(i['file_name']))
  both_images_file.write("\n")

#Adding Word Images path to both_images.txt file
for idx,i in enumerate(word_json['images']):
  if(idx < 500):
    continue
  if(idx > 1500):
    break
  total+=1
  both_images_file.write("/content/drive/My Drive/TableBank/tablebank_word/"+str(i['file_name']))
  both_images_file.write("\n")

print(total)
both_images_file.close()
latex_file.close()
word_file.close()

#Reading both_images.txt file
both_images_file = open("/content/drive/My Drive/TableBank/both_images.txt","r")
#checking content of .txt file
for i in both_images_file:
  print(i)
both_images_file.close()

#Word Images 
with open('/content/drive/My Drive/TableBank/Word.json') as f1:
	data1 = json.load(f1)
eval_images = open("/content/drive/My Drive/TableBank/both_images.txt","r")
e_images = []
for i in eval_images:
  e_images.append(i[:-1])
# e_images = e_images[:2000] 
# print(e_images) 
idx = 0
for i in data1['images']:
      image_name = "/content/drive/My Drive/TableBank/tablebank_both_augment/"+str(i['file_name'])
      if(image_name in e_images):
        print(image_name)
        idx+=1
print(idx)


tablecount = 0

#Function to calculate IoU
def bb_intersection_over_union(ground_truth, detection):
  global tablecount
  # print(tablecount)
  # determine the (x, y)-coordinates of the intersection rectangle
  tablecount+=1	
  xA = max(ground_truth[0], detection[0])
  yA = max(ground_truth[1], detection[1])
  xB = min(ground_truth[2], detection[2])
  yB = min(ground_truth[3], detection[3])
  # compute the area of intersection rectangle
  interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
  # compute the area of both the prediction and ground-truth
  # rectangles
  gtArea = (ground_truth[2] - ground_truth[0] + 1) * (ground_truth[3] - ground_truth[1] + 1)
  detectionArea = (detection[2] - detection[0] + 1) * (detection[3] - detection[1] + 1)
  # compute the intersection over union by taking the intersection
  # area and dividing it by the sum of prediction + ground-truth
  # areas - the interesection area
  iou = interArea / float(gtArea + detectionArea - interArea)
  precision_iou = interArea / float(detectionArea)
  recall_iou = interArea / float(gtArea)
  #Adding precision and recall for each image in lists precision  and recall
  precision.append(precision_iou)
  recall.append(recall_iou)

  # return the intersection over union value
  return iou

eval_images = open("/content/drive/My Drive/TableBank/both_images.txt","r")
e_images = []
for i in eval_images:
  e_images.append(i[:-1])
print(e_images)  

#Best Epoch of Model
epochs = ['epoch_15.pth']
# Testing Images
# img_files = glob.glob("/content/drive/My Drive/TableBank/tablebank_both_augment/*.*")

#Loading both json file for latex and word images
with open('/content/drive/My Drive/TableBank/Latex.json') as f1:
	data1 = json.load(f1)
with open('/content/drive/My Drive/TableBank/Word.json') as f2:
	data2 = json.load(f2)


for epoch in epochs:
  tablecount = 0
  total = 0
  precision = []
  recall = []
  idx = 0
  try:
  	#Threshold for prediction
    score_thr = 0.92
    #Path to config file of model
    config_fname = "/content/drive/My Drive/cascade_mask_rcnn_hrnetv2p_w32_20e.py"
    #Path to checkpoint file
    checkpoint_file_path = "/content/drive/My Drive/both_cascade_mask_rcnn_hrnetv2p_w32_20e/"+epoch

    # build the model from a config file and a checkpoint file
    model = init_detector(config_fname, checkpoint_file_path)

    #{dict_keys(['info', 'licenses', 'images', 'categories', 'annotations'])}
    #{'file_name': '1401.0007_15.jpg', 'id': 1, 'license': 1, 'width': 596, 'height': 842}
    #{'segmentation': [[85, 396, 85, 495, 510, 495, 510, 396]], 'area': 42075, 'image_id': 1, 'category_id': 1, 'id': 1, 'iscrowd': 0, 'bbox': [85, 396, 425, 99]}

    gt_boxes = []
    t=0
    for i in data1['images']:
      gt_boxes = []		
      #Extracting gt for latex images
      image_name = "/content/drive/My Drive/TableBank/tablebank_latex/"+str(i['file_name'])
      if(image_name not in e_images):
        continue
      if(cv2.imread(image_name) is None):
        print("continued1")
        continue  
      #Taking prediction of model for each image in testing set
      result = inference_detector(model, image_name)
      if(len(result[0][0])==0):
        print("continued1 again")
        continue

      total += 1
      d_bboxes = np.vstack(result)
      for j in data1['annotations']:
        if(j['image_id'] == i['id']):
          for k in j['segmentation']:
            gt_boxes.append(k)
      idx+=1
      print(i['id'],' ',idx,' ',i['file_name'])
      #calculating IoU with respect to gt if it contains multiple tables
      for bbox1 in d_bboxes[0][0]:
        min_dist = 99999 #min dist to find closest predicted bbox according to gt
        min_el = gt_boxes[0][0]
        for bbox2 in gt_boxes:

          dist = np.linalg.norm((bbox1[0]-bbox2[0],bbox1[1]-bbox2[1]))
          if(min_dist > dist):
            min_dist = dist
            min_el = bbox2
        bbox_int1 = bbox1[:-1]
    
        t = t + 1
        total += 1
        bbox_int1 = bbox1.astype(np.int32)
        bbox_int2 = [int(min_el[0]),int(min_el[1]),int(min_el[4]),int(min_el[5])]
        iou = bb_intersection_over_union(bbox_int1,bbox_int2)
        print(" IOU : ",iou)

    #Same Process for Word Images in testing set    
    gt_boxes = []		
    for i in data2['images']:
      gt_boxes = []		
      image_name = "/content/drive/My Drive/TableBank/tablebank_word/"+str(i['file_name'])
      if(image_name not in e_images):
        continue
      if(cv2.imread(image_name) is None):
        continue
      result = inference_detector(model, image_name)
      if(len(result[0][0])==0):
        continue
      total += 1
      d_bboxes = np.vstack(result)
      for j in data2['annotations']:
        if(j['image_id'] == i['id']):
          for k in j['segmentation']:
            gt_boxes.append(k)
      idx+=1
      print(i['id'],' ',idx,' ',i['file_name'])
      for bbox1 in d_bboxes[0][0]:
        min_dist = 99999
        min_el = gt_boxes[0][0]
        for bbox2 in gt_boxes:
          dist = np.linalg.norm((bbox1[0]-bbox2[0],bbox1[1]-bbox2[1]))
          if(min_dist > dist):
            min_dist = dist
            min_el = bbox2
        bbox_int1 = bbox1[:-1]
    
        # img = cv2.imread(image_name)
        # cv2.rectangle(img,(bbox_int1[0],bbox_int1[1]),(bbox_int1[2],bbox_int1[3]),(0,255,0))
        # cv2.imwrite(str(t)+".jpg",img)
        t = t + 1
        bbox_int1 = bbox1.astype(np.int32)
        bbox_int2 = [int(min_el[0]),int(min_el[1]),int(min_el[4]),int(min_el[5])]
        # bbox_int2 = bbox_int2.astype(np.int32)
        iou = bb_intersection_over_union(bbox_int1,bbox_int2)
        print(" IOU : ",iou)

  except Exception as e:
    print(str(e))

  # global tablecount
  print("total",total)

  #Calculating average precision and recall
  sum_precision = sum(precision)
  sum_recall = sum(recall)

  avg_precision = sum_precision / tablecount
  avg_recall = sum_recall / tablecount

  #Calculating F1 Score
  f1_score = 2 * ((avg_precision * avg_recall) / (avg_precision + avg_recall))
  print("====================================================")
  print("Precision : ",avg_precision)
  print("Recall : ",avg_recall)
  print("F1 : ",f1_score)
  saver = "{} Paste in excel : {} {} {}".format(epoch,avg_precision,avg_recall,f1_score)
  print(saver)
  my_file = open("/content/file.txt", "w")
  my_file.write(saver)
  my_file.close()

