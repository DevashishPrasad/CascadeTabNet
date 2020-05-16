import numpy as np
import cv2
from Functions.borderFunc import extract_table
## Input : roi of one cell
## Output : bounding box for the text in that cell
def extractTextBless(img):
    return_arr = []
    h,w=img.shape[0:2]
    base_size=h+14,w+14,3
    img_np = np.zeros(base_size,dtype=np.uint8)
    cv2.rectangle(img_np,(0,0),(w+14,h+14),(255,255,255),30)
    img_np[7:h+7,7:w+7]=img
    # cv2_imshow(img_np)
    gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY) 
    # blur = cv2.GaussianBlur(gray,(5,5),0)
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 1))
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 2)
    # cv2_imshow(dilation)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in (contours): 
        if cv2.contourArea(cnt) < 20:
          continue
        x, y, w, h = cv2.boundingRect(cnt) 
        if(h<6) or w<4 or h/img.shape[0]>0.95 or h>30: 
          continue
        return_arr.append([x-7, y-7, w, h])
    return return_arr

## Input : Roi of Table , Orignal Image, Cells Detected
## Output : Returns XML element which has contains bounding box of textchunks
def borderless(table, image, res_cells):
    cells = []
    x_lines = []
    y_lines = []
    table[0],table[1],table[2],table[3] = table[0]-15,table[1]-15,table[2]+15,table[3]+15
    for cell in res_cells:
        if cell[0]>table[0]-50 and cell[1]>table[1]-50 and cell[2]<table[2]+50 and cell[3]<table[3]+50:
            cells.append(cell)
            # print(cell)
    cells = sorted(cells,key=lambda x: x[3])
    row = []
    last = -1111
    row.append(table[1])
    y_lines.append([table[0],table[1],table[2],table[1]])
    temp = -1111
    prev = None
    im2 = image.copy()
    for i, cell in enumerate(cells):
        if i == 0:
            last = cell[1]
            temp = cell[3]
        elif (cell[1]<last+15 and cell[1]>last-15) or (cell[3]<temp+15 and cell[3]>temp-15):
            if cell[3]>temp:
                temp = cell[3]
        else:
            last = cell[1]
            if last > temp:
              row.append((last+temp)//2)
            if prev is not None:
                if ((last+temp)//2) < prev + 10 or ((last+temp)//2) < prev - 10:
                    row.pop()
            prev = (last+temp)//2
            temp = cell[3]
      
    row.append(table[3]+50)
    i=1
    rows = []
    for r in range(len(row)):
        rows.append([])
    final_rows = rows
    maxr = -111
    # print(len(row))
    for cell in cells:
        if cell[3]<row[i]:
            rows[i-1].append(cell)
        else:
            i+=1
            rows[i-1].append(cell)

    # print(row)
    for n,r1 in enumerate(rows):
        if n==len(rows):
            r1 = r1[:-1]
        # print(r1)
        r1 = sorted(r1,key=lambda x:x[0])
        prevr = None
        for no,r in enumerate(r1):
            if prevr is not None:
                # print(r[0],prevr[0])
                if (r[0]<=prevr[0]+5 and r[0]>=prevr[0]-5) or (r[2]<=prevr[2]+5 and r[2]>=prevr[2]-5):
                    if r[4]<prevr[4]:
                        r1.pop(no)
                    else:
                        r1.pop(no-1)
            prevr = r
          # print(len(r1))

        final_rows[n] = r1
    lasty = []
    for x in range(len(final_rows)):
      lasty.append([99999999,0])

    prev = None
    for n,r1 in enumerate(final_rows):
      for r in r1:
         if prev is None:
            prev = r
         else:
            if r[1]<prev[3]:
              continue

         if r[1]<lasty[n][0]:
           lasty[n][0] = r[1]
         if r[3]>lasty[n][1]:
           lasty[n][1] = r[3]
    # print("last y:",lasty)
    row = []
    row.append(table[1])
    prev = None
    pr = None
    for x in range(len(lasty)-1):
      if x==0 and prev==None:
        prev = lasty[x]
      else:
        if pr is not None:
          if abs(((lasty[x][0]+prev[1])//2)-pr)<=10:
            row.pop()
            row.append((lasty[x][0]+prev[1])//2)
          else:
            row.append((lasty[x][0]+prev[1])//2)
        else:
          row.append((lasty[x][0]+prev[1])//2)
        pr = (lasty[x][0]+prev[1])//2
        prev = lasty[x]
    row.append(table[3])
    maxr = 0
    for r2 in final_rows:
        print(r2)
        if len(r2)>maxr:
            maxr = len(r2)
        

    lastx = []

    for n in range(maxr):
        lastx.append([999999999,0])

    for r2 in final_rows:
        if len(r2)==maxr:
          for n,col in enumerate(r2):
              # print(col)
              if col[2]>lastx[n][1]:
                  lastx[n][1] = col[2]
              if col[0]<lastx[n][0]:
                  lastx[n][0] = col[0]

    print(lastx)
    for r2 in final_rows:
      if len(r2)!=0:
        r=0
        for n,col in enumerate(r2):
          while r!=len(r2)-1 and (lastx[n][0]>r2[r][0]):
              r +=1
          if n != 0:
            if r2[r-1][0] > lastx[n-1][1]:
              if r2[r-1][0]<lastx[n][0]:
                  lastx[n][0] = r2[r-1][0]
    for r2 in final_rows:
        for n,col in enumerate(r2):
          if n != len(r2)-1:  
            if col[2] < lastx[n+1][0]:
              if col[2]>lastx[n][1]:
                  lastx[n][1] = col[2]


    print(lastx)
    col = np.zeros(maxr+1)
    col[0] = table[0]
    prev = 0
    i = 1
    for x in range(len(lastx)):
      if x==0:
        prev = lastx[x]
      else:
        col[i] = (lastx[x][0]+prev[1])//2
        i+=1 
        prev = lastx[x]
    col = col.astype(int)
    col[maxr] = table[2]

    _row_ = sorted(row, key=lambda x:x)
    _col_ = sorted(col, key=lambda x:x)

    for no,c in enumerate(_col_):
        x_lines.append([c,table[1],c,table[3]])
        cv2.line(im2,(c,table[1]),(c,table[3]),(255,0,0),1)
    for no,c in enumerate(_row_):
      y_lines.append([table[0],c,table[2],c])
      cv2.line(im2,(table[0],c),(table[2],c),(255,0,0),1)
    
    # cv2_imshow(im2)
    print("table:",table)
    # for r in row:
    #   cv2.line(im2,(r,table[1]),(r,table[3]),(0,255,0),1)
    # for c in col:
    #   cv2.line(im2,(c,table[1]),(c,table[3]),(0,255,0),1)
    final = extract_table(image[table[1]:table[3],table[0]:table[2]],0,(y_lines,x_lines))

    cellBoxes = []
    img4 = image.copy()
    for box in final:
        cellBox = extractTextBless(image[box[1]:box[3],box[0]:box[4]])
        for cell in cellBox:
            cellBoxes.append([box[0]+cell[0], box[1]+cell[1], cell[2], cell[3]])
            cv2.rectangle(img4, (box[0]+cell[0], box[1]+cell[1]), (box[0]+cell[0]+cell[2], box[1]+cell[1]+cell[3]), (255,0,0), 2)
    # cv2_imshow(img4)

    the_last_y = -1
    cellBoxes = sorted(cellBoxes,key=lambda x: x[1])
    cellBoxes2BeMerged = [] 
    cellBoxes2BeMerged.append([])
    rowCnt = 0
    for cell in cellBoxes:
        if(the_last_y == -1):
          the_last_y = cell[1]
          cellBoxes2BeMerged[rowCnt].append(cell)
          continue
        if(abs(cell[1]-the_last_y) < 8):
          cellBoxes2BeMerged[rowCnt].append(cell)
        else:
          the_last_y=cell[1]
          rowCnt+=1
          cellBoxes2BeMerged.append([])
          cellBoxes2BeMerged[rowCnt].append(cell)

    MergedBoxes = []
    for cellrow in cellBoxes2BeMerged:
      cellrow = sorted(cellrow,key=lambda x: x[0])
      cur_cell = -1
      for c,cell in enumerate(cellrow):
        if(cur_cell == -1):
          cur_cell = cell
          continue
        if(len(cellrow)==1):
          MergedBoxes.append(cell)
          break
        if(abs((cur_cell[0]+cur_cell[2])-cell[0]) < 10):
          cur_cell[2] = cur_cell[2] + cell[2] + (cell[0]- (cur_cell[0]+cur_cell[2]))
          if(cur_cell[3]<cell[3]):
            cur_cell[3]=cell[3]
        else:
          cur_cell[2] = cur_cell[0]+cur_cell[2]
          cur_cell[3] = cur_cell[1]+cur_cell[3]
          MergedBoxes.append(cur_cell)
          cur_cell = cell
      cur_cell[2] = cur_cell[0]+cur_cell[2]
      cur_cell[3] = cur_cell[1]+cur_cell[3]
      MergedBoxes.append(cur_cell)  

    im3 = image.copy()
    for bx in MergedBoxes:
      cv2.rectangle(im3, (bx[0], bx[1]), (bx[2], bx[3]), (255,0,0), 2)
    # cv2_imshow(im3)
    TextChunks = []
    TextChunks.append([])
    rcnt = 0
    ycnt = -1

    final = sorted(final,key=lambda x:x[1])
    for box in final:
      if(ycnt == -1):
        ycnt = box[1]
      tcurcell = []
      mcurcell = []
      for mbox in MergedBoxes:
        if(mbox[0] >= box[0] and mbox[1] >= box[1] and mbox[2] <= box[4] and mbox[3] <= box[3]):
          if(len(tcurcell) == 0):
            tcurcell = mbox
          else:
            if(mbox[0] < tcurcell[0]):
              tcurcell[0] = mbox[0]
            if(mbox[1] < tcurcell[1]):
              tcurcell[1] = mbox[1]  
            if(mbox[2] > tcurcell[2]):
              tcurcell[2] = mbox[2]
            if(mbox[3] > tcurcell[3]):
              tcurcell[3] = mbox[3]  

      for i,frow in enumerate(final_rows):
        for j,fbox in enumerate(frow):
          if(fbox[0] >= box[0] and fbox[0] <= box[4] and fbox[1] >= box[1] and fbox[1] <= box[3]):
            mcurcell = fbox
            final_rows[i].pop(j)
            break  

      if(abs(ycnt-box[1])>10):
        rcnt+=1
        TextChunks.append([])
        ycnt = box[1]

      if(len(tcurcell)==0):
        if(len(mcurcell)==0):
          continue
        else:
          TextChunks[rcnt].append(mcurcell)
      else:
        if(len(mcurcell)==0):
          TextChunks[rcnt].append(tcurcell)
        else:
          if(abs(mcurcell[0] - tcurcell[0])<=20 and abs(mcurcell[1] - tcurcell[1])<=20 and abs(mcurcell[2] - tcurcell[2])<=20 and abs(mcurcell[3] - tcurcell[3])<=20):
            TextChunks[rcnt].append(tcurcell)
          elif((abs(mcurcell[0] - tcurcell[0])<=20 and abs(mcurcell[2] - tcurcell[2])<=20) or (abs(mcurcell[1] - tcurcell[1])<=20 or abs(mcurcell[3] - tcurcell[3])<=20)):
            TextChunks[rcnt].append(mcurcell)
          else:
            TextChunks[rcnt].append(tcurcell)

    colors = [(255,0,0),(0,255,0),(0,0,255),(125,125,0),(0,255,255)]
    for no,r in enumerate(TextChunks):
      for tbox in r:
        cv2.rectangle(im2, (tbox[0], tbox[1]), (tbox[2], tbox[3]), colors[no%len(colors)], 1)
        # print(tbox)

    cv2.imshow("text chunks", im2)
    cv2.waitKey(0)

    def rowstart(val):
      r = 0
      while(val > _row_[r]):
        r += 1  
      if r-1 == -1:
        return r
      else:
        return r-1
        
    def rowend(val):
      r = 0
      while(val > _row_[r]):
        r += 1  
      if r-1 == -1:
        return r
      else:
        return r-1

    def colstart(val):
      r = 0
      while(r < len(_col_) and val > _col_[r]):
        r += 1
      if r-1 == -1:
        return r
      else:
        return r-1
    
    def colend(val):
      r = 0
      while(r < len(_col_) and val > _col_[r]):
        r += 1
      if r-1 == -1:
        return r
      else:
        return r-1
    
    tableXML = etree.Element("table")
    Tcoords = etree.Element("Coords", points=str(table[0])+","+str(table[1])+" "+str(table[0])+","+str(table[3])+" "+str(table[2])+","+str(table[3])+" "+str(table[2])+","+str(table[1]))
    tableXML.append(Tcoords)
    for final in TextChunks:
      for box in final:
        cell = etree.Element("cell")
        end_col,end_row,start_col,start_row = colend(box[2]),rowend(box[3]),colstart(box[0]),rowstart(box[1])
        cell.set("end-col",str(end_col))
        cell.set("end-row",str(end_row))
        cell.set("start-col",str(start_col))
        cell.set("start-row",str(start_row))

        # print(cellBox)
        one = str(box[0])+","+str(box[1])
        two = str(box[0])+","+str(box[3])
        three = str(box[2])+","+str(box[3])
        four = str(box[2])+","+str(box[1])
        # print(one)
        coords = etree.Element("Coords", points=one+" "+two+" "+three+" "+four)

        cell.append(coords)
        tableXML.append(cell)

    return tableXML
