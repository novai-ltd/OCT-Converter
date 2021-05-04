from oct_converter.readers import E2E
import cv2
import os
from glob import glob
import numpy as np
from shutil import copy2
import shutil

TESTINBASE = r'Z:\data\Phase2\E2E darc2 imaging\Glaucuma_single_correctS\Filtered'

#the
rendirlist = ['E2E/GBR/00','E2EPng_and_TiffPng/GBR/00','Tiff/GBR/00']
checkdir = os.path.join(TESTINBASE,'E2E/GBR/00')

folders = os.listdir(checkdir)#,'OCT exsample 2.E2E','OCT exsample.E2E','PATIE013.E2E','Unknow Patient OCT Data.E2E']#,SBL5004A '026_F016.E2E', '02601C.E2E']
for folder in folders:
    filenames = os.listdir(os.path.join(checkdir,folder, '01'))
    if len(filenames)!=6:

        for d in rendirlist:
            ff = os.path.join(TESTINBASE,d,folder)
            print('Issue with files:{0}'.format(ff))
           # os.rename(ff,os.path.join(ff+'_issues'))
            shutil.rmtree(ff)


# DARCII_AAA_XX_YYYYY_ZZ_00000000_RE/LE_1_1
#
# Where:
#
# AAA = 3 letter ISO 3166 country code
# AUS = Australia
# NZL = New Zealand
# GBR = United Kingdom
# USA = United States of America
# XX = Site code (starting at 01)
# YYYYY = Patient ID (starting at 00001)
# ZZ = visit number (starting at 01)
# 00000000 = Date in the format DDMMYYYY
# RE/LE= Right/Left Eye,
# 1/2/3/4 = imaging modalities,
# 1 = ICGA
#     1.0 = ICGA baseline
#     1.1 = ICGA 120mins
#     1.2 = ICGA 240mins
# 2 = IR
# 3 = Autofluorescent (488)
# 4 = Red Free
# 1/2/3 = photo number (3 for each modality required)
# The files should be stored locally and transferred to SFTP in the following structure:
# \country code (AAA, e.g., AUS or NZL)
#     \site code (XX, starting at 01)
#     \patient ID (YYYYY, starting at 00001)
#     \visit number (ZZ, starting at 01)
#         DARCII_AAA_XX_YYYYY_ZZ_00000000_RE/LE_1/2/3/4_1/2/3.e2e
