import cv2
import numpy as np
from math import inf
import time
from PIL import Image, ImageDraw, ImageFilter

def MSE(bloc1, bloc2):
    block1, block2 = np.array(bloc1), np.array(bloc2)
    return np.square(np.subtract(block1, block2)).mean()

def new_mse(old_mse,new_mse):
    if old_mse>new_mse:
        return new_mse
    else:
        return old_mse

def mse_blocks(origin_x, origin_y, step):
    # Block au même endroit
    mse_x, mse_y = origin_x, origin_y
    min_mse = MSE(block1, grayImg1[origin_x:origin_x + 16, origin_y:origin_y + 16])
    A.append((origin_y, origin_x))

    # Blocks autour du block central
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue  # On a déjà traité le block central

            x, y = origin_x + i * step, origin_y + j * step
            block = grayImg1[x:x + 16, y:y + 16]
            new_mse = MSE(block1, block)
            if new_mse < min_mse:
                mse_x, mse_y = x, y
                min_mse = new_mse
            A.append((y, x))

    return min_mse,(mse_x, mse_y)


img1 = cv2.imread("image072.png")
img2 = cv2.imread("image092.png")
img3= cv2.imread('new_image.png') 

# add borders 
image_bordered = cv2.copyMakeBorder(src=img1,top=64, bottom=64, left=64, right=64, borderType=cv2.BORDER_CONSTANT)
# les images sont en gris 
grayImg1 = cv2.cvtColor(image_bordered , cv2.COLOR_BGR2GRAY)
grayImg2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
grayImg3= cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)

file_coordonner=[]
file_coordonner1=[]
A=[]

tps1 = time.time()
for i in range (0,grayImg2.shape[0]-16,16): #colonne with step 16 
    for j in range (0,grayImg2.shape[1]-16,16): #ligne 
           block1 = grayImg2[i:i + 16,j:j + 16]
           min = inf 
           origin_x=i+64
           origin_y=j+64
           step=32
           while(step>=1):
             new_mse,(new_x,new_y)=mse_blocks(origin_x,origin_y,step)
            
             if min>new_mse:
                min=new_mse
                (mse_x,mse_j)=(new_x,new_y)
                origin_x=mse_x 
                origin_y=mse_j

               
             step=step // 2
           if min > 50 : 
            print(min)
            file_coordonner.append((mse_j-64,mse_x-64))
            #print((mse_j-64,mse_x-64))
            file_coordonner1.append((j,i))
            grayImg3[i:i+16, j:j+16]= grayImg1[mse_x:mse_x+16, mse_j:mse_j+16]
            #print("original") 
            #print(j,i)
tps2 = time.time()
# tp =67 projet=19
print("le temps d'execution est"+ str(tps2 - tps1))
for i in range (len(file_coordonner)) :
    cv2.rectangle(img1, (file_coordonner[i][0], file_coordonner[i][1]),
                      (file_coordonner[i][0]+16,file_coordonner[i][1]+16), (0, 0, 255), 2) 

    cv2.rectangle(img2, (file_coordonner1[i][0], file_coordonner1[i][1]),
                      (file_coordonner1[i][0]+16,file_coordonner1[i][1]+16), (0, 255, 0), 2)

    cv2.rectangle(image_bordered, (A[i][0],A[i][1]),
                      (A[i][0]+16,A[i][1]+16), (0, 255, 0), 2)                  
#resize the window pop images 
imS2 = cv2.resize(img2, (960, 540)) 
imS1 = cv2.resize(img1, (960, 540)) 
imS3 = cv2.resize( grayImg3 , (960, 540))

cv2.imshow("image", imS1)
cv2.imshow("image2", imS2)
cv2.imshow("image3",imS3)

cv2.waitKey(0)