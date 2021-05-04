from oct_converter.readers import E2E
import cv2
import os
import numpy as np

#intiff = r'D:\data\e2e\glucoma\Glaucoma E2e imaging\072_OS_240min.tiff'
#ine2e =r'D:\data\e2e\glucoma\Glaucoma E2e imaging\4hr\out\07201F.E2E\cslo\0.png'

intiff = r'D:\data\e2e\glucoma\Glaucoma E2e imaging\1\out\07201F.E2E\072_OD_BL.tiff'
ine2e =r'D:\data\e2e\glucoma\Glaucoma E2e imaging\1\out\07201F.E2E\cslo\0.png'

intiffImgA = cv2.imread(intiff)
intiffImgG, intiffImgG, intiffImgG = cv2.split(intiffImgA)
ine2eImg = cv2.imread(ine2e, cv2.IMREAD_GRAYSCALE)

diff = intiffImgG.astype('double')- intiffImgG.astype('double') #cv2.subtract(intiffImgG, ine2eImg)
print(np.sum(diff))
#cv2.imshow('e2e', ine2eImg)
#cv2.imshow('tiff', intiffImgG)

#cv2.waitKey()

cv2.imwrite(r'D:\data\e2e\glucoma\Glaucoma E2e imaging\1\out\07201F.E2E\tiff.png', intiffImgG)
cv2.imwrite(r'D:\data\e2e\glucoma\Glaucoma E2e imaging\1\out\07201F.E2E\e1e.png', ine2eImg)