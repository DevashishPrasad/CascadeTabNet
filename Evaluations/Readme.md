# Evaluation Tools

This folder contain various tool for performing evaluation on various benchmarking Dataset for Table detection and structure
recognition.

## ICDAR 13

Official site : http://www.tamirhassan.com/html/competition.html <br>
Download the Complete Data [Here](http://www.tamirhassan.com/html/files/icdar2013-competition-dataset-with-gt.zip)

### Prerequisites

This tool is tested on Windows 7 only
1. Java Oracle 8
2. Python 3
3. Provided JAR file need to be placed in you java jre directory, inside the lib/ext

### Format of file 

The format for PDF, Ground Truth and Result should be in the same format as specified in ICDAR 13 official site
Also, the naming convention as specified by ICDAR 13 are
file.pdf, file-reg.xml, file-reg-result.xml <br>
Where, file.pdf is the PDF on which the detection is performed, 
file-reg.xml is the Groundthruth XML file used for table Detection
file-reg-result.xml Contains the output Detected coordinate of algorithm.


### Running Evaluation

Evalutation using orignal tool on single PDF can be found [Here](https://github.com/tamirhassan/dataset-tools)

Put all the PDF, their groundtruth and result XML in same directory as 
the eval.py and tool.java

simply run
```
python eval.py
```
to get result 

## ICDAR 19

ICDAR 19 evalution Tool can be found [Here](https://github.com/cndplab-founder/ICDAR2019_cTDaR)
and Dataset [Here](https://github.com/cndplab-founder/ICDAR2019_cTDaR)

## Table Bank




Evaluation is carried out in following steps:

1) Model Loading <br>
2) For each image in test set <br>
   
   2.1) Extract ground truth for the corresponding image from annotations <br>
   2.2) Pass the image to model to get its predictions <br>
   2.3) After getting the predictions correct theses predictions using line correction technique <br>
   2.4) Once the bounding boxes are corrected the necessary step is to map the ground truth bounding box to its appropriate predicted box. This is done using the euclidean distance.<br>
   2.4) After mapping the ground truth to appropriate prediction calculate the IoU for these two boxes <br>
   2.5) Using the IoU value calculate the precision and recall per object <br>
   2.6) perform step 2.3 - 2.5 for each table in image <br>
3) After calculating precision and recall for each table in every image calculate the average precision and recall to get final result.<br><br>

Above steps are coded in evaluation.py file.<br>

Download train and test json files for word subset, latex subset and both_merged subset from [Here](https://drive.google.com/open?id=1lxpK4sa4LTSHPFuQEsjFdx87NAlQ8F5O) <br><br>

Set appropriate paths to of Words.json and Latex.json in script.<br><br>

After setting paths run

```
python evaluation.py

```
Evaluation on tablebank is done using line correction on the model predictions.<br>
