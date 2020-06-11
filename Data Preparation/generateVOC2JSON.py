## Script for Converting Pascal VOC annotations to Coco Json format
## This script shows and example conversion of our table dataset pascal voc
## annotations conversion to coco annotations  

## Usage :
# You need to first create a txt file containing names of all pascal voc files
# You can use following linux command
# ls -1 | sed -e 's/\.xml$//' | sort -n > "/path/to/folder/coco.txt"
# And then read the comments in this script to understand its working

import os
import xml.etree.ElementTree as ET
import xmltodict
import json
from xml.dom import minidom
from collections import OrderedDict

def generateVOC2Json(rootDir,xmlFiles):
  attrDict = dict()
  # Add categories according to you Pascal VOC annotations
  attrDict["categories"]=[{"supercategory":"none","id":1,"name":"Table"},
                          {"supercategory":"none","id":2,"name":"cell"},
                          {"supercategory":"none","id":3,"name":"borderless"}
        # {"supercategory":"none","id":4,"name":"item_name"},
        # {"supercategory":"none","id":5,"name":"item_desc"},
        # {"supercategory":"none","id":6,"name":"price"},
        # {"supercategory":"none","id":7,"name":"total_price_text"},
        # {"supercategory":"none","id":8,"name":"total_price"},
        # {"supercategory":"none","id":9,"name":"footer"}
            ]
  images = list()
  annotations = list()
  id1 = 1

  # Some random variables
  cnt_bor = 0
  cnt_cell = 0
  cnt_bless = 0

  # Main execution loop
  for root, dirs, files in os.walk(rootDir):
    image_id = 0
    for file in xmlFiles:
      image_id = image_id + 1
      if file in files:
        annotation_path = os.path.abspath(os.path.join(root, file))
        image = dict()
        doc = xmltodict.parse(open(annotation_path).read())
        image['file_name'] = str(doc['annotation']['filename'])
        image['height'] = int(doc['annotation']['size']['height'])
        image['width'] = int(doc['annotation']['size']['width'])
        image['id'] = image_id
        print("File Name: {} and image_id {}".format(file, image_id))
        images.append(image)
        if 'object' in doc['annotation']:
          for key,vals in doc['annotation'].items():
            if(key=='object'):
              for value in attrDict["categories"]:
                if(not isinstance(vals, list)):
                  vals = [vals]
                for val in vals:
                  if str(val['name']) == value["name"]:
                    annotation = dict()
                    annotation["iscrowd"] = 0
                    annotation["image_id"] = image_id
                    x1 = int(val["bndbox"]["xmin"])  - 1
                    y1 = int(val["bndbox"]["ymin"]) - 1
                    x2 = int(val["bndbox"]["xmax"]) - x1
                    y2 = int(val["bndbox"]["ymax"]) - y1
                    annotation["bbox"] = [x1, y1, x2, y2]
                    annotation["area"] = float(x2 * y2)
                    annotation["category_id"] = value["id"]

                    # Tracking the count
                    if(value["id"] == 1):
                      cnt_bor += 1
                    if(value["id"] == 2):
                      cnt_cell += 1
                    if(value["id"] == 3):
                      cnt_bless += 1

                    annotation["ignore"] = 0
                    annotation["id"] = id1
                    annotation["segmentation"] = [[x1,y1,x1,(y1 + y2), (x1 + x2), (y1 + y2), (x1 + x2), y1]]
                    id1 +=1
                    annotations.append(annotation)
        else:
          print("File: {} doesn't have any object".format(file))
      else:
        print("File: {} not found".format(file))

  attrDict["images"] = images	
  attrDict["annotations"] = annotations
  attrDict["type"] = "instances"

  # Printing out some statistics
  print(len(images))
  print("Bordered : ",cnt_bor," Cell : ",cnt_cell," Bless : ",cnt_bless)
  print(len(annotations))

  # Save the final JSON file
  # jsonString = json.dumps(attrDict)
  jsonString = json.dumps(attrDict, indent = 4, sort_keys=True)
  with open("/content/drive/My Drive/ICDAR 13 dataset/coco.json", "w") as f:
    f.write(jsonString)

# Path to the txt file (see at the top of this script)
trainFile = "/content/drive/My Drive/ICDAR 13 dataset/coco.txt"
trainXMLFiles = list()
with open(trainFile, "r") as f:
	for line in f:
		fileName = line.strip()
		print(fileName)
		trainXMLFiles.append(fileName + ".xml")

# Path to the pascal voc xml files 
rootDir = "/content/drive/My Drive/ICDAR 13 dataset/2Be Fine Tuned"

# Start execution
generateVOC2Json(rootDir, trainXMLFiles)
