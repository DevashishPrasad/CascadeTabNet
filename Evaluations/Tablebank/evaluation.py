#Importing Libraries
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


precision = []
recall = []
tablecount = 0

#Function to implement line detection.
def line_detection(image):

    #Converting Image to Gray color		
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    bw = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 1)
    bw = cv2.bitwise_not(bw)
    horizontal = bw.copy()
    vertical = bw.copy()

    # [horiz]
    # Create structure element for extracting horizontal lines through morphology operations
    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 1))

    # Apply morphology operations
    horizontal = cv2.erode(horizontal, horizontalStructure)
    horizontal = cv2.dilate(horizontal, horizontalStructure)

    horizontal = cv2.dilate(horizontal, (1,1), iterations=5)
    horizontal = cv2.erode(horizontal, (1,1), iterations=5)

    # cv2.imshow("hori",horizontal)
    # cv2.waitKey(0)
    #Apply HoughLinesP to detect horizontal lines
    hor_lines = cv2.HoughLinesP(horizontal,rho=1,theta=np.pi/180,threshold=100,minLineLength=150,maxLineGap=10)
    if hor_lines is None:
        return None,None
    temp_line = []
    for line in hor_lines:
        for x1,y1,x2,y2 in line:
            temp_line.append([x1,y1-5,x2,y2-5])
    #Sorted lines according to y values
    hor_lines = sorted(temp_line,key=lambda x: x[1])
    print(len(hor_lines))
    for x1, y1, x2, y2 in hor_lines:
        cv2.line(image, (x1,y1-5), (x2,y2-5), (0, 255, 0), 1)

    # cv2.imshow("image",image)
    # cv2.waitKey(0)
    
    # [vert]
    # Create structure element for extracting vertical lines through morphology operations
    verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 15))

    # Apply morphology operations
    vertical = cv2.erode(vertical, verticalStructure)
    vertical = cv2.dilate(vertical, verticalStructure)

    vertical = cv2.dilate(vertical, (1,1), iterations=5)
    vertical = cv2.erode(vertical, (1,1), iterations=5)

    #Detecting vertical lines using HoughLinesP() function
    ver_lines = cv2.HoughLinesP(vertical,rho=1,theta=np.pi/180,threshold=110,minLineLength=150,maxLineGap=10)
    if ver_lines is None:
        return None,None
    temp_line = []
    for line in ver_lines:
        for x1,y1,x2,y2 in line:
            temp_line.append([x1,y1-5,x2,y2-5])

    #Sorting vertical lines according to x values		
    ver_lines = sorted(temp_line,key=lambda x: x[0])
    print(image.shape)
    for x1, y1, x2, y2 in ver_lines:
        cv2.line(image, (x1,y1-5), (x2,y2-5), (0, 255, 0), 2)
    #return the list of horizontal and vertical lines 	
    return hor_lines,ver_lines


#Function to calculate IoU between two boxes
def bb_intersection_over_union(ground_truth, detection):
	
	global tablecount
	
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
	#Calculate iou , precision and recall and append precision and recall to global lists
	iou = interArea / float(gtArea + detectionArea - interArea)
	precision_iou = interArea / float(detectionArea)
	recall_iou = interArea / float(gtArea)
	precision.append(precision_iou)
	recall.append(recall_iou)

	# return the intersection over union value
	return iou

#List of epochs to be evaluated
epochs = ['epoch_22.pth','epoch_23.pth','epoch_24.pth','epoch_25.pth','epoch_26.pth']
# Testing Images
# img_files = glob.glob("/content/drive/My Drive/TableBank/tablebank_both_augment/*.*")

#test json for word subset images . If you are using latex test subset then provide path for respective test json file
with open('/content/drive/My Drive/TableBank/word_test.json') as f:
	data = json.load(f)

#Iterating over the list of epochs
for epoch in epochs:
	#Setting to default at the start of each epoch
	tablecount = 0
	precision =[]
	recall = []
	try:
		#cofig file path and checkpoint file path provide appropriate paths
		score_thr = 0.9
		config_fname = "/content/drive/My Drive/cascade_mask_rcnn_hrnetv2p_w32_20e.py"
		checkpoint_file_path = "/content/drive/My Drive/Mmdetection/word_cascade_mask_rcnn_hrnetv2p_w32_20e/"+epoch

		# build the model from a config file and a checkpoint file
		model = init_detector(config_fname, checkpoint_file_path)
		
		#List to store ground truth values	
		gt_boxes = []
		idx = 0
		t=0
		#Iterating over all the images
		for i in data['images']:
			idx+=1        
		
			image_name = "/content/drive/My Drive/TableBank/tablebank_word/"+str(i['file_name'])
			#Reading Image
			iii = cv2.imread(image_name)
			#If image is invalid then continue
			if(iii is None):
				print("continued")
				continue
			#If image is valid then get prediction from model	
			result = inference_detector(model, image_name)
			#If no table detected then continue to next image
			if(len(result[0][0])==0):
				print("continued again")
				continue

			#Detecting horizontal and vertical lines in table image 	
			hor,ver = line_detection(iii)

			# =================== APPLY LINE CORRECTION ==================
			if(hor is not None and ver is not None):
				#For each detected table in image correct the lines
				for r in result[0][0]:
					xmin = 9999
					ymin = 9999
					xmax = 9999
					ymax = 9999
					#For each horizontal line detected by line detection
					for h in hor:
						# print(h)
						diff1 = abs(h[1] - r[1])
						if(diff1 < abs(r[1]-ymin) and abs(h[0]-r[0])<25 and abs(h[2]-r[2])<25):
							ymin = h[1]
						diff2 = abs(h[3] - r[3])
						if(diff2 < abs(r[3]-ymax) and abs(h[0]-r[0])<25 and abs(h[2]-r[2])<25):
							ymax = h[3]    
					if(ymin != 9999):      
						r[1] = ymin
					if(ymax != 9999):      
						r[3] = ymax
					for v in ver:
						diff1 = abs(v[0] - r[0])
						if(diff1 < abs(r[0]-xmin) and abs(h[1]-r[1])<25 and abs(h[3]-r[3])<25):
							xmin = v[0]
						diff2 = abs(v[2] - r[2])
						if(diff2 < abs(r[2]-xmax) and abs(h[1]-r[1])<25 and abs(h[3]-r[3])<25):
							xmax = v[2]       
					if(xmin != 9999):        
						r[0] = xmin
					if(xmax != 9999):        
						r[2] = xmax    

				# ============== LINE CORRECTION END ================ 

			d_bboxes = np.vstack(result)
			#Getting ground truth for tables in image 
			for j in data['annotations']:
				if(j['image_id'] == i['id']):
					for k in j['segmentation']:
						gt_boxes.append(k)

			print(i['id'],' ',idx,' ',i['file_name'])
			# print(gt_boxes)
			# print(d_bboxes[0][0])
			# print("Image : {}".format(i))
			#Calculating minimum distance ground truth from prediction in case of multiple tables in the image
			#For each prediction 
			for bbox1 in d_bboxes[0][0]:
				min_dist = 99999
				#setting minimum distance gt box to first box in Extracted Ground truths for images
				min_el = gt_boxes[0][0]
				#For each box in ground truth
				for bbox2 in gt_boxes:
					#Calculating minimum distance Ground truth from prediction
					#Subtract starting X and Y values of predicted box and ground truth box
					dist = np.linalg.norm((bbox1[0]-bbox2[0],bbox1[1]-bbox2[1]))
					#If minimum distance is grater than calculated distance
					#Set calculated distance to min_dist and the corresponding box to closest ground truth i.e., min_el
					if(min_dist > dist):
						min_dist = dist
						min_el = bbox2
				#Avoiding confidence score from predicted box so that only coordinates are remained
				bbox_int1 = bbox1[:-1]
		
				# img = cv2.imread(image_name)
				# cv2.rectangle(img,(bbox_int1[0],bbox_int1[1]),(bbox_int1[2],bbox_int1[3]),(0,255,0))
				# cv2.imwrite(str(t)+".jpg",img)
				t = t + 1
				#Converting coordinates to int
				bbox_int1 = bbox1.astype(np.int32)
				bbox_int2 = [int(min_el[0]),int(min_el[1]),int(min_el[4]),int(min_el[5])]
				# bbox_int2 = bbox_int2.astype(np.int32)
				#Calculating IoU of ground truth and predicted region
				iou = bb_intersection_over_union(bbox_int1,bbox_int2)
				print(" IOU : ",iou)
			#Resetting gt_boxes for next image
			gt_boxes = []		

	except Exception as e:
		print("ERROR : ",str(e))

	# global tablecount

	#Sum over all the precision and recall of every table in all images
	sum_precision = sum(precision)
	sum_recall = sum(recall)

	#Calculating average precision and recall
	avg_precision = sum_precision / tablecount
	avg_recall = sum_recall / tablecount

	#Calculating F1 score
	f1_score = 2 * ((avg_precision * avg_recall) / (avg_precision + avg_recall))


	print("====================================================")
	print("Precision : ",avg_precision)
	print("Recall : ",avg_recall)
	print("F1 : ",f1_score)
	
	#Saving the results in file
	saver = "\n {} {} {}".format(avg_precision,avg_recall,f1_score)
	print(saver)
	my_file = open("path-to-random-log-file.txt", "a")
	my_file.write(saver)
	my_file.close()
