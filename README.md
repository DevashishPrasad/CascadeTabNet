# CascadeTabNet

## License
The code of CascadeTabNet is released under the MIT License. There is no limitation for both acadmic and commercial usage.

## Paper
<a href="https://arxiv.org/abs/2004.12629">Preprint Link of Paper</a> : The paper has been accepted at <b>CVPR 2020 Workshop </b>

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
  <td>Table Bank Word table detection</td><td><a href="https://drive.google.com/open?id=1-ZnV84t61IrkAfQH7dOATpo_T4C1J4Qa">Checkpoint</a></td>
  </tr>    
  <tr>
  <td>Table Bank Latex table detection</td><td><a href="https://drive.google.com/open?id=1-9EzU_LfD6fE8iJFjOZ3nBsCObqhpNUa">Checkpoint</a></td>
  </tr>    
  <tr>
  <td>Table Bank Both table detection</td><td><a href="https://drive.google.com/open?id=1-vjfGRhF8kqvKwZPPFNwiTaOoonJlGgv">Checkpoint</a></td>
  </tr>      
  <tr>
  <td>ICDAR 19 (Track B2 Modern) table structure recognition</td><td><a href="https://drive.google.com/open?id=1-QieHkR1Q7CXuBu4fp3rYrvDG9j26eFT">Checkpoint</a></td>
  </tr>      
</table>

## Additional Results
<a href="results.pdf">Supplementary file</a>

Whole code will be released soon in this repository !

## Contact
Devashish Prasad : devashishkprasad [at] gmail [dot] com <br>
Ayan Gadpal : ayangadpal2 [at] gmail [dot] com <br>
Kshitij Kapadni : kshitij.kapadni [at] gmail [dot] com <br>
Manish Visave : manishvisave149 [at] gmail [dot] com <br>

## Acknowledgement
The initial work was inspired from the Automatic Invoice Parsing system we developed for Akshay Navalakha (AP Analytica)

## Cite as
<pre>
@misc{ cascadetabnet2020,
    title={CascadeTabNet: An approach for end to end table detection and structure recognition from image-based documents},
    author={Devashish Prasad and Ayan Gadpal and Kshitij Kapadni and Manish Visave and Kavita Sultanpure},
    year={2020},
    eprint={2004.12629},
    archivePrefix={arXiv},
    primaryClass={cs.CV}
}
</pre>
