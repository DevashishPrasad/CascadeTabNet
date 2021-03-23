# CascadeTabNet
[![PWC](https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/cascadetabnet-an-approach-for-end-to-end/table-detection-on-icdar2013-1)](https://paperswithcode.com/sota/table-detection-on-icdar2013-1?p=cascadetabnet-an-approach-for-end-to-end)
[![PWC](https://img.shields.io/badge/PyTorch-v1.4-blue)](https://pytorch.org/)
[![PWC](https://img.shields.io/badge/%20mmdetection%20-v1.2-blue)](https://github.com/open-mmlab/mmdetection)

> **CascadeTabNet: An approach for end to end table detection and structure recognition from image-based documents**<br>
> [Devashish Prasad](https://github.com/DevashishPrasad),
> [Ayan Gadpal](https://github.com/ayangadpal),
> [Kshitij Kapadni](https://github.com/kshitijkapadni),
> [Manish Visave](https://github.com/ManishDV),
> <br>
> [CVPR Link of Paper](http://openaccess.thecvf.com/content_CVPRW_2020/papers/w34/Prasad_CascadeTabNet_An_Approach_for_End_to_End_Table_Detection_and_CVPRW_2020_paper.pdf)<br>
> [arXiv Link of Paper](https://arxiv.org/abs/2004.12629)<br>
> <a href="results.pdf">Supplementary file</a> <br>
> The paper was presented (Orals) at [CVPR 2020 Workshop on Text and Documents in the Deep Learning Era](https://cvpr2020text.wordpress.com/)<br>
> Virtual Oral Presentation [YOUTUBE VIDEO](https://www.youtube.com/watch?v=6rovEyWKZw8)
<img align="right" src="imgs/CVPR Teaser.gif" />

## 1. Introduction
CascadTabNet is an automatic table recognition method for interpretation of tabular data in document images. We present an improved deep learning-based end to end approach for solving both problems of table detection and structure recognition using a single Convolution Neural Network (CNN) model. CascadeTabNet is a Cascade mask Region-based CNN High-Resolution Network (Cascade mask R-CNN HRNet) based model that detects the regions of tables and recognizes the structural body cells from the detected tables at the same time. We evaluate our results on ICDAR 2013, ICDAR 2019 and TableBank public datasets. We achieved 3rd rank in ICDAR 2019 post-competition results for table detection while attaining the best accuracy results for the ICDAR 2013 and TableBank dataset. We also attain the highest accuracy results on the ICDAR 2019 table structure recognition dataset. 

<img src="imgs/main_res.png"/>

## 2. Setup
<b>Models are developed in Pytorch based <a href="https://github.com/open-mmlab/mmdetection">MMdetection</a> framework (Version 1.2)</b>
<br>

<pre>
pip install -q mmcv terminaltables
git clone --branch v1.2.0 'https://github.com/open-mmlab/mmdetection.git'
cd "mmdetection"
pip install -r "/content/mmdetection/requirements/optional.txt"
python setup.py install
python setup.py develop
pip install -r {"requirements.txt"}
pip install pillow==6.2.1 
pip install mmcv==0.4.3
</pre>

<b>Code is developed under following library dependencies</b> <br>

PyTorch = 1.4.0<br>
Torchvision = 0.5.0<br>
Cuda = 10.0<br>

<pre>
pip install torch==1.4.0+cu100 torchvision==0.5.0+cu100 -f https://download.pytorch.org/whl/torch_stable.html
</pre>

**If you are using Google Colaboratory (Colab), Then you need add**
```
from google.colab.patches import cv2_imshow
```
and replace all the `cv2.imshow` with `cv2_imshow`

## 3. Model Architecture
<img src="imgs/model arch.png" width="550"/>
<a href="imgs/theonnx.onnx.svg">Model Computation Graph</a>

## 4. Image Augmentation
<img src="imgs/3imgs.png" width="750"/><br>
Codes: <a href="https://github.com/DevashishPrasad/CascadeTabNet/blob/master/Data%20Preparation/Dilation.py">Code for dilation transform</a> <a href="https://github.com/DevashishPrasad/CascadeTabNet/blob/master/Data%20Preparation/Smudge.py">Code for smudge transform</a>

## 5. Benchmarking
### 5.1. Table Detection
#### 1. ICDAR 13
<img src="imgs/ICDAR 13.png" width="450"/>

#### 2. ICDAR 19 (Track A Modern)
<img src="imgs/icdar 19.png" width="450"/>

#### 3. TableBank
<img src="imgs/tablebank.png" width="450"/>

#### TableBank Benchmarking : <a href="https://doc-analysis.github.io/"> <b>Official Leaderboard</b></a><br>
TableBank Dataset Divisions : <a href="https://drive.google.com/open?id=1lxpK4sa4LTSHPFuQEsjFdx87NAlQ8F5O">TableBank</a>

### 5.2. Table Structure Recognition
#### 1. ICDAR 19 (Track B2)
<img src="imgs/TSR.png" width="450"/>

## 6. Model Zoo
Checkout our demo notebook for loading checkpoints and performing inference <br>[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1lzjbBQsF4X2C2WZhxBJz0wFEQor7F-fv?usp=sharing)<br>
[Config file](Config/cascade_mask_rcnn_hrnetv2p_w32_20e.py) for the Models<br>
*Note: Config paths are only required to change during training*<br>
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

## 7. Datasets

1) End to End Table Recognition Dataset <br>
We manually annotated some of the <a href="http://sac.founderit.com/">ICDAR 19 table competition (cTDaR)</a> dataset images for cell detection in the borderless tables. More details about the dataset are mentioned in the paper. <br>
<a href="https://drive.google.com/drive/folders/1mNDbbhu-Ubz87oRDjdtLA4BwQwwNOO-G?usp=sharing">dataset link</a>

2) General Table Detection Dataset (ICDAR 19 + Marmot + Github)<br>
We manually corrected the annotations of Marmot and <a href="https://github.com/sgrpanchal31/table-detection-dataset">Github</a> and combined them with ICDAR 19 dataset to create a general and robust dataset. <br>
<a href="https://drive.google.com/open?id=1RuEACireEqPnQrYqghEqsOPRE-CkGSUd">dataset link</a>

## 8. Training
You may refer this <a href="https://www.dlology.com/blog/how-to-train-an-object-detection-model-with-mmdetection/">tutorial</a> for training Mmdetection models on your custom datasets in colab.<br>

You may refer this <a href="/Data Preparation/generateVOC2JSON.py">script</a> to convert your Pascal VOC XML annotation files to a single COCO Json file.

## 9. Docker

The docker image of this project can be found at <a href="https://hub.docker.com/repository/docker/akadirpamukcu/tabnet">docker hub</a> 

It currently contains three models from model zoo. For details you can check the readme file at the docker hub.

## Contact
Devashish Prasad : devashishkprasad [at] gmail [dot] com <br>
Ayan Gadpal : ayangadpal2 [at] gmail [dot] com <br>
Kshitij Kapadni : kshitij.kapadni [at] gmail [dot] com <br>
Manish Visave : manishvisave149 [at] gmail [dot] com <br>

## Acknowledgements

We thank the following contributions because of which
the paper was made possible

1. The **MMdetection** project team for creating the amazing framework to push the state of the art computer vision
research and which enabled us to experiment and build state of the art models very easily.

2. Our college **”Pune Institute of Computer Technology”** for funding our research and giving us the opportunity to work and publish our research at an international conference.

3. **<a href="http://chenkai.site/">Kai Chen</a>** for endorsing our paper on the arXiv to publish a pre-print of the paper and also for maintaining the Mmdetection repository along with the team.

4. **Google Colaboratory** team for providing free high end GPU resources for research and development. All of the code base was developed using Google colab and couldn't be possible without it.

5. **AP Analytica** for making us aware about a similar problem statement and giving us an opportunity to work on the same.

6. **Overleaf.com** for open sourcing the wonderful project which enabled us to write the research paper easily in the latex format

## License
The code of CascadeTabNet is Open Source under the [MIT License](LICENSE.md). There is no limitation for both acadmic and commercial usage.

## Cite as
If you find this work useful for your research, please cite our paper:

```
@misc{ cascadetabnet2020,
    title={CascadeTabNet: An approach for end to end table detection and structure recognition from image-based documents},
    author={Devashish Prasad and Ayan Gadpal and Kshitij Kapadni and Manish Visave and Kavita Sultanpure},
    year={2020},
    eprint={2004.12629},
    archivePrefix={arXiv},
    primaryClass={cs.CV}
}
```
