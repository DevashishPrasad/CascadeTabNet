# Table Structure Recognition(TSR)

### **For Bordered Tables code is released. We will update the borderless soon

## TSR Pipeline
![TSR Pipeline](https://github.com/DevashishPrasad/CascadeTabNet/blob/master/Table%20Structure%20Recognition/Pipeline.PNG)

### Things To Do :- 
If you want run the code directly without understanding how the code works you can simply add all the directory paths into <a href=https://github.com/DevashishPrasad/CascadeTabNet/blob/master/Table%20Structure%20Recognition/main.py> main.py </a> file and execute it with following command:
```
python main.py
```
This will generate XML files for all the bordered tables.

## Bordered Pipeline
For bordered table images, the most important feature is that it contains lines to segregate rows and columns due to which a human can easily understand the structure and its information. So, We took advantage of this feature and used line detection methods to detect the lines in an image by which it was easy to separate the rows and columns of the table. For this we divided the Bordered Pipeline into 3 Steps: 
            
            1. Line Detection
                i.  Horizontal lines
                ii. Vertical lines
            2. Cell Formation
                i.  Find Intersection points in lines
                ii. Identify cells from points
            3. Text Detection in cells 

The <a href=https://github.com/DevashishPrasad/CascadeTabNet/blob/master/Table%20Structure%20Recognition/Functions/BorderFunc.py > BorderFunc.py </a> file contains all the necessary functions that are required for the bordered pipeline. This file is imported in <a href=https://github.com/DevashishPrasad/CascadeTabNet/blob/master/Table%20Structure%20Recognition/border.py> border.py </a> file which is the handler for whole bordered pipeline. This handler returns XML structure of a single table to <a href=https://github.com/DevashishPrasad/CascadeTabNet/blob/master/Table%20Structure%20Recognition/main.py> main.py </a> file which is the handler for TSR Module.

### 1. Line Detection
Refer this Documentation for Line Detection : https://docs.opencv.org/3.4/d9/db0/tutorial_hough_lines.html

Line Detection was performed using the Houghlinesp function of opencv and refering to the original documentaion. We have provided <a href=https://github.com/DevashishPrasad/CascadeTabNet/blob/master/Table%20Structure%20Recognition/Functions/line_detection.py > line detection</a> with all the parameters already set which works better for tables. 
