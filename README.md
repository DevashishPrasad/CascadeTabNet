# CascadeTabNet

## License
The code of CascadeTabNet is released under the MIT License. There is no limitation for both acadmic and commercial usage.

## Paper
Link of Paper : The paper has been accepted at <b>CVPR2020 Workshop on Text and Documents in the Deep Learning Era</b> and preprint link will be available soon

## End to End Dataset 
We manually annotated some of the <a href="http://sac.founderit.com/">ICDAR 19 table competition (cTDaR)</a> dataset images for table cell detection in borderless tables while also categorizing tables into two classes (bordered and borderless) and will be releasing the annotations to the community. 
<a href="https://drive.google.com/drive/folders/1mNDbbhu-Ubz87oRDjdtLA4BwQwwNOO-G?usp=sharing">dataset link</a>

## Introduction
CascadTabNet is an automatic table recognition method for interpretation of tabular data in document images. We present an improved deep learning-based end to end approach for solving both problems of table detection and structure recognition using a single Convolution Neural Network (CNN) model. CascadeTabNet is a Cascade mask Region-based CNN High-Resolution Network (Cascade mask R-CNN HRNet) based model that detects the regions of tables and recognizes the structural body cells from the detected tables at the same time. We evaluate our results on ICDAR 2013, ICDAR 2019 and TableBank public datasets. We achieved 3rd rank in ICDAR 2019 post-competition results for table detection while attaining the best accuracy results for the ICDAR 2013 and TableBank dataset. We also attain the highest accuracy results on the ICDAR 2019 table structure recognition dataset.

## Model Architecture
<img src="imgs/model arch.png" width="550"/>
<a href="imgs/theonnx.onnx.svg">Model Computation Graph</a>

## Image Augmentation
### 1. Original Image
<img src="imgs/orig.jpg" width="350"/>

### 2. Dilation Transform
<a href="">Code for dilation transform</a>

<img src="imgs/dilate.jpg" width="350"/>

### 3. Smudge Transform
<a href="">Code for smudge transform</a>

<img src="imgs/smudge.jpg" width="350"/>


## Benchmarking
### Table Detection
#### 1. ICDAR 13
<img src="imgs/ICDAR 13.png" width="450"/>

#### 2. ICDAR 19 (Track A Modern)
<img src="imgs/icdar 19.png" width="450"/>

#### 3. TableBank
<img src="imgs/tablebank.png" width="450"/>

### Table Structure Recognition
#### 1. ICDAR 19 (Track B2)
<img src="imgs/TSR.png" width="450"/>

## Model Zoo
Checkpoints of the Models we have trained : 

<ol>
  <a<li>General Model table detection</li>
  <li>ICDAR 13 table detection</li>
  <li>ICDAR 19 (Track A Modern) table detection </li>
  <li>Table Bank Word table detection</li>
  <li>Table Bank Latex table detection</li> 
  <li>Table Bank Both table detection</li>
  <li>ICDAR 19 (Track B2 Modern) table structure recognition</li>
</ol>

Whole code will be released soon in this repository


<!--## Citing
<pre>
@article{
  cascacadetabnet2020
  authors = ""
  title = ""
  journal = ""
  year = ""
}
</pre>-->
