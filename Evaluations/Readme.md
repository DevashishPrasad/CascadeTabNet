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
3. Provided JAR file need to be placed in you java jre dictory, inside the lib/ext

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

