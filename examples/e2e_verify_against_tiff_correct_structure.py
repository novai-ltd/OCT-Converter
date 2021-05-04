from oct_converter.readers import E2E
import cv2
import os
from glob import glob
import numpy as np
from shutil import copy2

TIFFIN = r'Z:\data\Phase2\p2_eye_gl_no_border_no_lowres\NovaiTestSite'
E2EIN = r'Z:\data\Phase2\E2E darc2 imaging\Glaucuma_single\All'
E2EOUTBASE = r'Z:\data\Phase2\E2E darc2 imaging\Glaucuma_single_correctS_new_fname'
E2EOUT = os.path.join(E2EOUTBASE,'Filtered')
E2EOUTPoor = os.path.join(E2EOUTBASE,'FilteredPoorMatch')

os.makedirs(E2EOUT, exist_ok= True)
fout = open(os.path.join(E2EOUTBASE,'dist.txt'),'w')
s = 'filename,mindiff\n'
fout.write(s)
CountryID='GBR'
SiteID ='01'
DateID = '04052021'
visitNums = ['v1']#,'02','03','04','05','06']
sideLUT ={'LE':'OS','RE':'OD'}

#the
folders = os.listdir(TIFFIN)#,'OCT exsample 2.E2E','OCT exsample.E2E','PATIE013.E2E','Unknow Patient OCT Data.E2E']#,SBL5004A '026_F016.E2E', '02601C.E2E']
for folder in folders:
    filenames = os.listdir(os.path.join(TIFFIN, folder,'01'))
    for filename in filenames:
        if filename.endswith('.tiff'):
            filepathTIFF = os.path.join(TIFFIN,folder,'01',filename)
            imgTiffRGB = cv2.imread(filepathTIFF)
            imgTiffB, imgTiffG,imgTiffR = cv2.split(imgTiffRGB)
            imgTiff = imgTiffG

            filenameSplit = os.path.splitext(filename)[0].split('_')
            DARC = filenameSplit[0]
            caseID = filenameSplit[1]
            shortDate = filenameSplit[2]
            eyeSide = sideLUT[filenameSplit[4]]
            timeID=filenameSplit[5]
            imageSeq = filenameSplit[6]
            # filenameE2E = '{0}_{1}_{2}_*_{3}_{4}_*.E2E'.format(
            # DARC,
            # caseID,
            # shortDate,
            # eyeSide,
            # timeID)
            #if caseID != '032':
            #    continue

            filenameE2E = '*{0}_*.E2E'.format(caseID)

            filepathE2ESearch = os.path.join(E2EIN, filenameE2E)
            filepathsE2E2 = glob(filepathE2ESearch)
            if (len(filepathsE2E2)==0):
                continue
            mindiff = 9e99
            mindifffname=''

            for filepathE2E in filepathsE2E2:
                print(filepathE2E)
                file = E2E(filepathE2E)
                cslo_imgs = file.read_clso_image()  # returns an cslo volume with additional metadata if available

                single_cslo =  cslo_imgs[0]

                if imgTiff.shape != single_cslo.shape:
                    continue

                diff = np.sum(cv2.absdiff(imgTiff, single_cslo))

                allbasefname = os.path.basename(filepathE2E)
                outf = os.path.join(E2EOUTBASE, 'test', allbasefname.upper().replace('.E2E', '_all_e2e.png'))
                os.makedirs(os.path.dirname(outf), exist_ok=True)
                print('Write png:{0}'.format(outf))
                cv2.imwrite(outf, single_cslo)
                tiffbase = os.path.basename(filepathTIFF)
                outfTiff = os.path.join(E2EOUTBASE, 'test', tiffbase.replace('.tiff', '_all_tiff.png'))
                cv2.imwrite(outfTiff, imgTiff)

                if diff<mindiff:
                    mindiff = diff
                    mindifffname = filepathE2E

            if len(mindifffname)>0:
                basefname = os.path.basename(mindifffname)

                file = E2E(mindifffname)
                cslo_imgs = file.read_clso_image()  # returns an cslo volume with additional metadata if available
                single_cslo_best = cslo_imgs[0]

                s = '{0},{1}\n'.format(basefname,mindiff)
                print(s)
                fout.write(s)
                for visit in visitNums:
                    #DARCII_AAA_XX_YYYYY_ZZ_00000000_RE/LE_1.x_1
                    patientID3 = '{0:03}'.format(int(caseID))
                    visitID2 = visit
                    imageSeq  = 1
                    outFName = 'DARC_{0}_{1}_{2}_{3}_{4}_{5}_{6}_{7}_O.E2E'.format(CountryID,SiteID,patientID3,eyeSide,visitID2,DateID,timeID, imageSeq)

                    foldersuffix = os.path.join(CountryID, SiteID, patientID3,visitID2)

                    if (mindiff > 100000):
                        OutD = os.path.join(E2EOUTPoor)
                    else:
                        OutD = os.path.join(E2EOUT)

                    os.makedirs(os.path.join(OutD, 'E2EPng_and_TiffPng', foldersuffix), exist_ok=True)

                    os.makedirs(os.path.join(OutD, 'TIFF', foldersuffix), exist_ok=True)
                    os.makedirs(os.path.join(OutD, 'E2E', foldersuffix), exist_ok=True)

                    cv2.imwrite(os.path.join(OutD,'E2EPng_and_TiffPng',foldersuffix,outFName.replace('.E2E','_e2e.png')),single_cslo_best)
                    cv2.imwrite(os.path.join(OutD,'E2EPng_and_TiffPng',foldersuffix, outFName.replace('.E2E', '_tiff.png')), imgTiff)

                    copy2(mindifffname, os.path.join(OutD,'E2E',foldersuffix, outFName))
                    cv2.imwrite(os.path.join(OutD,'TIFF',foldersuffix, outFName.replace('.E2E', '.TIFF')), imgTiff)



fout.close()

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
