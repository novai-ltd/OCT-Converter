# Normalize staining
import math
import os

import numpy as np
#import openslide
import cv2
from PIL import Image

from scipy.ndimage.morphology import binary_fill_holes
from skimage.color import rgb2gray
from skimage.feature import canny
from skimage.morphology import binary_closing, binary_dilation, disk
import skimage.io as io
import numpy
import pandas as pd
import json
#

baseDir = r'D:\data\AMD\OCTSetGA'
#jsonfile = r'D:\data\AMD\OCTSet\020520201631.json'
jsonfile = r'D:\data\AMD\OCTSetGA\GA14092020.json'

if os.path.exists(os.path.join(baseDir,'image')) ==False:
    os.makedirs(os.path.join(baseDir, 'image'))

if os.path.exists(os.path.join(baseDir, 'mask')) == False:
    os.makedirs(os.path.join(baseDir, 'mask'))

if os.path.exists(os.path.join(baseDir, 'combined')) == False:
    os.makedirs(os.path.join(baseDir, 'combined'))


colours= {'GA':(0,255,0)}

coloursGray= {'GA':1}


with open(jsonfile) as json_file:
    data = json.load(json_file)
    meta = data['_via_img_metadata']
    for p in meta.keys():
        data = meta[p]
        filename =  data['filename']
        img = cv2.imread(os.path.join(baseDir,filename))
        imgOrg = img.copy()
        mask = np.zeros((img.shape[0],img.shape[1]),'uint8')
        maskCol = np.zeros(img.shape, 'uint8')

        regions = data['regions']
        for region in regions:
            shape = region['shape_attributes']
            x = shape['all_points_x']
            y = shape['all_points_y']

            region = region['region_attributes']
            type='GA'

            pnts = np.stack((x, y), axis=-1)
            pnts = np.int32(pnts)
            #cv2.fillPoly(img,[pnts],colours[fluid_type])
            cv2.fillPoly(maskCol, [pnts], colours[type])
            cv2.fillPoly(mask, [pnts], coloursGray[type])

        overlayImage = cv2.addWeighted(imgOrg, 0.5, maskCol, 0.5, 0)

        comb = np.hstack((imgOrg, maskCol, overlayImage))
        fnameSp = filename.split('\\')
        fname = fnameSp[1]

        cv2.imwrite(os.path.join(baseDir, 'combined',fname.replace('.jpg', '.png')), comb)
        cv2.imwrite(os.path.join(baseDir, 'image', fname.replace('.jpg', '.png')), imgOrg)
        cv2.imwrite(os.path.join(baseDir, 'mask', fname.replace('.jpg', '.png')), mask)

        #        if len(regions)>0:
#            cv2.imshow('img', img)
#            cv2.waitKey()

        print('filename: ' + filename)
        print('regions: ' + str(len(regions)))
        print('')




