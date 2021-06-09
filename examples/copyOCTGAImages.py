import os
import sys
from glob import glob
from shutil import copy2 as copy2, copy as copy
from shutil import copytree
import cv2
import pandas as pd

import numpy as np
from skimage import data
from skimage import exposure
from skimage.exposure import match_histograms
import rolling_ball
import fourier
import pandas as pd
print('Hello')

split = 497

def splitImg(img):
    imgOCT = img[0:-1, split:-1].copy()
    imgR = img[0:-1, 0:split].copy()
    imgOCT = cv2.resize(imgOCT, (imgR.shape[1], imgR.shape[0]))

    return imgR, imgOCT

ga_eyes = pd.read_excel('GA eyes_extra.xlsx')

indir = r'C:\data\AMDAnnoSetAll'
outdirBase = r'D:\data\AMD\OCTSetGA_extra'

#wetcases
cases = ga_eyes['eye'].values

selectedfiles=[]

for c in cases:
    outdir = os.path.join(outdirBase, c)
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    d = os.path.join(indir,c)
    OCTdir = d = os.path.join(indir,c,c.replace('_','-').upper()+'_ALL_OCT')
    OCTTimeDirs = os.listdir(OCTdir)

    for d in OCTTimeDirs:
        od = os.path.join(outdirBase,c,c.replace('_','-').upper()+'_ALL_OCT',d)
        refimage = glob(os.path.join(OCTdir, d,'*000.jpg'))
        imgR_OCT = cv2.imread(refimage[0])
        imgR, imgOCT = splitImg(imgR_OCT)
        outref = os.path.join(outdirBase,c,c+'_'+d+'.jpg')
        cv2.imwrite(outref, imgR)
        selectedRef = os.path.join(c,c+'_'+d+'.jpg')
        selectedfiles.append(selectedRef)
        copytree(os.path.join(OCTdir,d),od)

        #
        #
        # dateDirs = os.listdir(os.path.join(indir,d,'org'))
        # for dd in dateDirs:
        #     files = glob(os.path.join(indir,d,'org',dd,'*.png'))
        #     outdd = os.path.join(outdir,d,dd)
        #
        #     for file in files:
        #         basename = os.path.basename(file)
        #         outfile = os.path.join(outdd, basename).replace('.png','.jpg')
        #       #  copy2(file, outfile)
        #
        #         if d in cases:
        #             times = cases[d]
        #             if dd in times:
        #                 if not os.path.exists(outdd):
        #                     os.makedirs(outdd)
        #                 selectedfiles.append(os.path.join(d,dd, basename).replace('.png','.jpg'))
        #                 copy2(file, outfile)
        #                 print(d,dd)

with open(os.path.join(outdir,'selected_ga_oct_files.txt'), 'w') as file:  # Use file to refer to the file object
    for f in selectedfiles:
        file.write(f+'\n')

