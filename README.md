# CascadeTabNet

## License
The code of CascadeTabNet is released under the MIT License. There is no limitation for both acadmic and commercial usage.

## Paper
Link of Paper : The paper has been accepted at <b>CVPR2020 Workshop on Text and Documents in the Deep Learning Era</b> and preprint link will be available soon

## End to End Table Recognition Dataset 
We manually annotated some of the <a href="http://sac.founderit.com/">ICDAR 19 table competition (cTDaR)</a> dataset images. Details about the dataset are mentioned in the paper. 
<a href="https://drive.google.com/drive/folders/1mNDbbhu-Ubz87oRDjdtLA4BwQwwNOO-G?usp=sharing">dataset link</a>

## Introduction
CascadTabNet is an automatic table recognition method for interpretation of tabular data in document images. We present an improved deep learning-based end to end approach for solving both problems of table detection and structure recognition using a single Convolution Neural Network (CNN) model. CascadeTabNet is a Cascade mask Region-based CNN High-Resolution Network (Cascade mask R-CNN HRNet) based model that detects the regions of tables and recognizes the structural body cells from the detected tables at the same time. We evaluate our results on ICDAR 2013, ICDAR 2019 and TableBank public datasets. We achieved 3rd rank in ICDAR 2019 post-competition results for table detection while attaining the best accuracy results for the ICDAR 2013 and TableBank dataset. We also attain the highest accuracy results on the ICDAR 2019 table structure recognition dataset. 

We use <a href="https://github.com/open-mmlab/mmdetection">MMdetection</a> framework to implement the model.

## Model Architecture
<img src="imgs/model arch.png" width="550"/>
<a href="imgs/theonnx.onnx.svg">Model Computation Graph</a>

## Image Augmentation
<img src="imgs/3imgs.png" width="750"/><br>
Codes: <a href="">Code for dilation transform</a> <a href="">Code for smudge transform</a>

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

<table>
  <tr>
  <th>Model Name</th><th>Checkpoint File</th>
  </tr>
  <tr>
  <td>General Model table detection</td><td><a href="https://drive.google.com/open?id=1-xfq5hDmFdKgbY9FSFTmhSlcb2p13RPn">Checkpoint</a></td>
  </tr>
  <tr>
  <td>ICDAR 13 table detection</td><td><a href="https://drive.google.com/open?id=1-mVr4UBicFk3mjUz5tsVPjQ4jzRtiT7V">Checkpoint</a></td>
  </tr>
  <tr>
  <td>ICDAR 19 (Track A Modern) table detection</td><td><a href="https://drive.google.com/open?id=1vfUr4pmmI4GICZubAnBeFU8pviMUW_c9">Checkpoint</a></td>
  </tr>  
  <tr>
  <td>Table Bank Word table detection</td><td>-</td>
  </tr>    
  <tr>
  <td>Table Bank Latex table detection</td><td>-</td>
  </tr>    
  <tr>
  <td>Table Bank Both table detection</td><td><a href="https://drive.google.com/open?id=1-nTe0oNOYPMjl_3Zo4CsBN9y4lponvCd">Checkpoint</a></td>
  </tr>      
  <tr>
  <td>ICDAR 19 (Track B2 Modern) table structure recognition</td><td><a href="https://drive.google.com/open?id=1-QieHkR1Q7CXuBu4fp3rYrvDG9j26eFT">Checkpoint</a></td>
  </tr>      
</table>

## Additional Results
<a href="results">Supplementary file</a>

Whole code will be released soon in this repository !

## Contact
Devashish Prasad : devashishkprasad [at] gmail [dot] com <br>
Ayan Gadpal : ayangadpal2 [at] gmail [dot] com <br>
Kshitij Kapadni : kshitij.kapadni [at] gmail [dot] com <br>
Manish Visave : manishvisave149 [at] gmail [dot] com <br>

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
