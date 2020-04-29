# Table Structure Recognition(TSR)

### **For Bordered Tables code is released. We will update the borderless soon

## TSR Pipeline
![TSR Pipeline](https://github.com/DevashishPrasad/CascadeTabNet/blob/master/Table%20Structure%20Recognition/Pipeline.PNG)

## Bordered Pipeline
For bordered table images, the most important feature is that it contains lines to segregate rows and columns due to which a human can easily understand the structure and its information. So, We took advantage of this feature and used line detection methods to detect the lines in an image by which it was easy to separate the rows and columns of the table. For this we divided the Bordered Pipeline into 3 Steps: 

            1. Line Detection
                1. Horizontal line
                2. Vertical line
            2. Cell Formation
                1. Find Intersection points in lines
                2. Identify cells from points
            3. Text Detection in cells 




