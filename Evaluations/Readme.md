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

### Train/Test split for ICDAR 13
**Train**
```
eu-003
eu-015
eu-020
us-018
us-019
us-034
us-009
us-015
us-017
us-036
us-033
us-032
us-028
us-022
```
**Test**<br>
Rest of PDFs are used for testing

## ICDAR 19

ICDAR 19 evalution Tool can be found [Here](https://github.com/cndplab-founder/ICDAR2019_cTDaR)
and Dataset [Here](https://github.com/cndplab-founder/ICDAR2019_cTDaR)

## Table Bank

Evaluation is carried out in following steps:

1) Model Loading <br>
2) For each image in test set <br>
   i) Extract ground truth for the corresponding image from annotations <br>
   ii) Pass the image to model to get its predictions <br>
   iii) Correct the predictions using line correction technique <br>
   iv) Map the ground truth bounding box to its appropriate predicted box. This is done using the euclidean distance.<br>
   v) Calculate the IoU for each pair of boxes (Ground-truth vs predicted) <br>
   vi) Using the IoU value calculate the precision and recall per object <br>
   vii) perform step iii) to v) for each table in image <br>
3) Calculate the average precision and recall across all images to get the final result.<br><br>

Above steps are implemented in evaluation.py file.<br>

Download train and test json files for all of the three subsets (Latex, Word, Both) from [Here](https://drive.google.com/open?id=1lxpK4sa4LTSHPFuQEsjFdx87NAlQ8F5O) <br><br>

Set appropriate paths to of Words.json and Latex.json in script.<br><br>

After setting paths run

```
python evaluation.py

```
Evaluation on tablebank is done using line correction on the model predictions.<br>
