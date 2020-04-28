from border import border
from mmdet.apis import inference_detector, show_result, init_detector
import cv2
import lxml.etree as etree
import glob


config_fname = "path to config file of model" 
checkpoint_path = "path to checkpoint directory"
epoch = 'epoch_file.name'
model = init_detector(config_fname, checkpoint_path+epoch)

imgs = glob.glob('path to directory of images')
for i in imgs:
    print(i)
    result = inference_detector(model, i)
    res_border = []
    res_bless = []
    res_cell = []
    root = etree.Element("document")
    for r in result[0][0]:
        if r[4]>.85:
            res_border.append(r[:4].astype(int))
    for r in result[0][1]:
        if r[4]>.85:
            r[4] = r[4]*100
            res_cell.append(r.astype(int))
    for r in result[0][2]:
        if r[4]>.85:
            res_bless.append(r[:4].astype(int))

    if len(res_border) != 0:
        ## call border script
        for res in res_border:
            root.append(border(res,cv2.imread(i)))  
    # if len(res_bless) != 0:
    #     if len(res_cell) != 0:
    #         for no,res in enumerate(res_bless):
    #             # borderless(res,cv2.imread(i),res_cell)
    #             root.append(borderless(res,cv2.imread(i),res_cell))

    myfile = open('path to save the xml file', "w")
    myfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    myfile.write(etree.tostring(root, pretty_print=True,encoding="unicode"))
    myfile.close()