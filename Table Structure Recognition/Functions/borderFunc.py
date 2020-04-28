import cv2
import numpy as np

##################  Functions required for Border table Recognition #################
# Input : Image
# Output : hor,ver 
def line_detection(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    bw = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 17, 1)
    bw = cv2.bitwise_not(bw)
    ## To visualize image after thresholding ##
    # cv2.imshow(bw)
    # cv2.waitKey(0)
    ###########################################
    horizontal = bw.copy()
    vertical = bw.copy()

    # [horizontal lines]
    # Create structure element for extracting horizontal lines through morphology operations
    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 1))

    # Apply morphology operations
    horizontal = cv2.erode(horizontal, horizontalStructure)
    horizontal = cv2.dilate(horizontal, horizontalStructure)

    horizontal = cv2.dilate(horizontal, (1,1), iterations=5)
    horizontal = cv2.erode(horizontal, (1,1), iterations=5)

    # HoughlinesP function to detect horizontal lines
    hor_lines = cv2.HoughLinesP(horizontal,rho=1,theta=np.pi/180,threshold=100,minLineLength=30,maxLineGap=3)
    if hor_lines is None:
        return None,None
    temp_line = []
    for line in hor_lines:
        for x1,y1,x2,y2 in line:
            temp_line.append([x1,y1-5,x2,y2-5])

    # Sorting the list of detected lines by Y1
    hor_lines = sorted(temp_line,key=lambda x: x[1])

    ## Uncomment this part to visualize the lines detected on the image ##
    # print(len(hor_lines))
    # for x1, y1, x2, y2 in hor_lines:
    #     cv2.line(image, (x1,y1), (x2,y2), (0, 255, 0), 1)

    
    # print(image.shape)
    # cv2.imshow("image",image)
    # cv2.waitKey(0)
    ####################################################################

    ## Selection of best lines from all the horizontal lines detected ##
    lasty1 = -111111
    lines_x1 = []
    lines_x2 = []
    hor = []
    i=0
    for x1,y1,x2,y2 in hor_lines:
        if y1 >= lasty1 and y1 <= lasty1 + 10:
            lines_x1.append(x1)
            lines_x2.append(x2)
        else:
            if (i != 0 and len(lines_x1) is not 0):
                hor.append([min(lines_x1),lasty1,max(lines_x2),lasty1])
                cv2.line(image, (min(lines_x1), lasty1), (max(lines_x2), lasty1), (0, 255, 0), 1)
            lasty1 = y1
            lines_x1 = []
            lines_x2 = []
            lines_x1.append(x1)
            lines_x2.append(x2)
            i+=1
    cv2.line(image, (min(lines_x1), lasty1), (max(lines_x2), lasty1), (0, 255, 0), 1)
    hor.append([min(lines_x1),lasty1,max(lines_x2),lasty1])
    #####################################################################


    # [vertical lines]
    # Create structure element for extracting vertical lines through morphology operations
    verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 15))

    # Apply morphology operations
    vertical = cv2.erode(vertical, verticalStructure)
    vertical = cv2.dilate(vertical, verticalStructure)

    vertical = cv2.dilate(vertical, (1,1), iterations=8)
    vertical = cv2.erode(vertical, (1,1), iterations=7)

    # cv2_imshow(vertical)
    # cv2.waitKey(0)

    # HoughlinesP function to detect vertical lines
    ver_lines = cv2.HoughLinesP(vertical,rho=1,theta=np.pi/180,threshold=20,minLineLength=15,maxLineGap=2)
    #ver_lines = cv2.HoughLinesP(vertical, 1, np.pi/180, 20, np.array([]), 15, 2)
    if ver_lines is None:
        return None,None
    temp_line = []
    for line in ver_lines:
        for x1,y1,x2,y2 in line:
            temp_line.append([x1,y1,x2,y2])

    # Sorting the list of detected lines by X1
    ver_lines = sorted(temp_line,key=lambda x: x[0])

    ## Uncomment this part to visualize the lines detected on the image ##
    # print(len(ver_lines))
    # for x1, y1, x2, y2 in ver_lines:
    #     cv2.line(image, (x1,y1-5), (x2,y2-5), (0, 255, 0), 2)

    
    # print(image.shape)
    # cv2.imshow("image",image)
    # cv2.waitKey(0)
    ####################################################################

    ## Selection of best lines from all the vertical lines detected ##
    lastx1 = -111111
    lines_y1 = []
    lines_y2 = []
    ver = []
    count = 0
    lasty1 = -11111
    lasty2 = -11111
    for x1,y1,x2,y2 in ver_lines:
        if x1 >= lastx1 and x1 <= lastx1 + 15 and not (((min(y1,y2)<min(lasty1,lasty2)-20 or min(y1,y2)<min(lasty1,lasty2)+20)) and ((max(y1,y2)<max(lasty1,lasty2)-20 or max(y1,y2)<max(lasty1,lasty2)+20))):
            lines_y1.append(y1)
            lines_y2.append(y2)
            # lasty1 = y1
            # lasty2 = y2
        else:
            if (count != 0 and len(lines_y1) is not 0):
                ver.append([lastx1,min(lines_y2)-5,lastx1,max(lines_y1)-5])
                cv2.line(image, (lastx1, min(lines_y2)-5), (lastx1, max(lines_y1)-5), (0, 255, 0), 1)
            lastx1 = x1
            lines_y1 = []
            lines_y2 = []
            lines_y1.append(y1)
            lines_y2.append(y2)
            count += 1
            lasty1 = -11111
            lasty2 = -11111
    cv2.line(image, (lastx1,min(lines_y2)-5), (lastx1,max(lines_y1)-5), (0, 255, 0), 1)
    ver.append([lastx1,min(lines_y2)-5,lastx1,max(lines_y1)-5])
    #################################################################

    # cv2_imshow(image)
    # cv2.waitKey(0)

    return hor,ver

# def map(ver, hor, table_lines):
#     mapping = []
#     ver = sorted(ver, key=lambda x: x[0])
#     hor = sorted(hor, key=lambda x: x[1])
#     for i in range(len(ver)):
#         for j in range(len(hor)):
#             mp = []
#             for idx in range(len(table_lines)):
#                 if i + 1 == len(ver) or j + 1 == len(hor):
#                     continue

#                 if (table_lines[idx][0] < ver[i + 1][0] and table_lines[idx][1] < hor[j + 1][1]):
#                     mp.append(table_lines[idx])
#                     print(table_lines[idx])
#             sorted(mp, key=lambda x: [x[0],x[1]])
#             mapping.append(mp)
#     return mapping

## Return the intersection of lines only if intersection is present ##
# Input : x1, y1, x2, y2, x3, y3, x4, y4 (1: vertical, 2: horizontal)
# Output : (x,y) Intersection point
def line_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    # print(x1, y1, x2, y2)
    # print(x3, y3, x4, y4)
    
    if((x1>= x3-5 or x1>= x3+5) and (x1 <= x4+5 or x1 <= x4-5) and (y3+8>=min(y1,y2) or y3-5>=min(y1,y2)) and y3<=max(y1,y2)+5):
        return x1,y3


## main extraction function ##
# Input : Image, Decision parameter(1/0),lines for borderless (only of decision parameter is 0)
#
def extract_table(table_body,__line__,lines=None):
    # Deciding variable
    if(__line__ == 1 ):
    # Check if table image is  bordered or borderless
        temp_lines_hor, temp_lines_ver = line_detection(table_body)
    else:
        temp_lines_hor, temp_lines_ver = lines

    # table = table_body.copy()		
    x = 0
    y = 0
    k = 0
    points = []
    print("[Table status] : Processing table with lines")
    # Remove same lines detected closer
    for x1, y1, x2, y2 in temp_lines_ver:
        point = []
        for x3, y3, x4, y4 in temp_lines_hor:
            try:
                k += 1
                x, y = line_intersection(x1, y1, x2, y2, x3, y3, x4, y4)
                point.append([x, y])
            except:
                continue
        points.append(point)

    # boxno = -1
    box = []
    flag = 1
    lastCache = []
    ## creating bounding boxes of cells from the points detected 
    ## This is still under work and might fail on some images
    for i, row in enumerate(points):
        limitj = len(row)
        currentVala = []
        for j, col in enumerate(row):

            if (j == limitj-1):
                break
            if (i == 0):
                nextcol = row[j+1]
                lastCache.append([col[0], col[1], nextcol[0], nextcol[1],9999,9999,9999,9999])
            else:
                nextcol = row[j+1]
                currentVala.append([col[0], col[1], nextcol[0], nextcol[1], 9999, 9999, 9999, 9999])
                # Matching 
                flag = 1
                index = []                
                for k, last in enumerate(lastCache):

                    if (col[1] == last[1]) and lastCache[k][4] == 9999:
                        lastCache[k][4] = col[0]
                        lastCache[k][5] = col[1]
                        if lastCache[k][4] != 9999 and lastCache[k][6] != 9999:    
                            box.append(lastCache[k])
                            index.append(k)
                            flag = 1

                    if (nextcol[1] == last[3]) and lastCache[k][6] == 9999:
                        lastCache[k][6] = nextcol[0]
                        lastCache[k][7] = nextcol[1]
                        if lastCache[k][4] != 9999 and lastCache[k][6] != 9999:    
                            box.append(lastCache[k])
                            index.append(k)
                            flag = 1
                    
                    if len(lastCache) !=0:
                        if lastCache[k][4] == 9999 or lastCache[k][6] == 9999:
                            flag = 0
                # print(index)
                for k in index:
                      lastCache.pop(k)
                # tranfsering
                if flag == 0:
                    for last in lastCache:
                        if last[4] == 9999 or last[6] == 9999:
                            currentVala.append(last)

        if(i!=0):
            lastCache = currentVala

                
    ## Visualizing the cells ##
    # count = 1
    # for i in box:
    #     cv2.rectangle(table_body, (i[0], i[1]), (i[6], i[7]), (int(i[7]%255),0,int(i[0]%255)), 2)
    # #     count+=1
    # cv2.imshow("cells",table_body)
    # cv2.waitKey(0)
    ############################
    return box



def findX(X,x):
    return X.index(x)
def findY(Y,y):
    return Y.index(y)

def span(box,X,Y):
    start_col = findX(X,box[0])     ## x1
    end_col = findX(X,box[4])-1     ## x3
    start_row = findY(Y,box[1])     ## y1
    end_row = findY(Y,box[3])-1     ## y2
    # print(end_col,end_row,start_col,start_row)
    return end_col,end_row,start_col,start_row



def extractText(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    _, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    # cv2_imshow(thresh1)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 2)
    contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    im2 = img.copy()
    mx,my,mw,mh = float('Inf'),float('Inf'),-1,-1
    for cnt in contours: 
        x, y, w, h = cv2.boundingRect(cnt) 
        # print(im2.shape)
        if x<2 or y<2 or (x+w>=im2.shape[1]-1 and y+h>=im2.shape[0]-1) or w>=im2.shape[1]-1 or h>=im2.shape[0]-1:
            continue  
        if x<mx:
            mx = x
        if y<my:
            my = y
        if x+w>mw:
            mw = x+w
        if y+h>mh:
            mh = y+h
        # print(x, y, w, h)

    if mx !=float('Inf') and my !=float('Inf'):
        # Drawing a rectangle on copied image 
        # rect = cv2.rectangle(im2, (mx+1, my), (mw-2, mh-2), (0, 255, 0), 1)
        # cv2_imshow(im2)
        return mx,my,mw,mh
    else :
        return None