from oct_converter.readers import E2E
import cv2
import os
from glob import glob
import numpy as np
from shutil import copy2

TIFFIN = r'D:\data\p2_eye_gl_no_border_no_lowres\NovaiTestSite'
E2EIN = r'Y:\Backup\data\data\Phase2\Phase2_E2E\E2E darc2 imaging\Glaucuma_single\All'
E2EOUT = r'Y:\Backup\data\data\Phase2\Phase2_E2E\E2E darc2 imaging\Glaucuma_single\Filtered'
E2EOUTPoor = r'Y:\Backup\data\data\Phase2\Phase2_E2E\E2E darc2 imaging\Glaucuma_single\FilteredPoorMatch'

os.makedirs(E2EOUT, exist_ok= True)
fout = open(os.path.join(E2EOUT,'dist.txt'),'w')
s = 'filename,mindiff\n'
fout.write(s)

#filepath = os.path.join(indir,'OCT exsample 1.E2E')
#filenames = ['OCT exsample 1.E2E','OCT exsample 2.E2E','OCT exsample.E2E','PATIE013.E2E','Unknow Patient OCT Data.E2E']#,SBL5004A '026_F016.E2E', '02601C.E2E']
folders = os.listdir(TIFFIN)#,'OCT exsample 2.E2E','OCT exsample.E2E','PATIE013.E2E','Unknow Patient OCT Data.E2E']#,SBL5004A '026_F016.E2E', '02601C.E2E']
for folder in folders:
    filenames = os.listdir(os.path.join(TIFFIN, folder,'01'))
    for filename in filenames:
        if filename.endswith('.tiff'):
            filepathTIFF = os.path.join(TIFFIN,folder,'01',filename)
            imgTiff = cv2.imread(filepathTIFF, cv2.IMREAD_GRAYSCALE)
            filenameSplit = os.path.splitext(filename)[0].split('_')
            filenameE2E = '{0}_{1}_{2}_*_{3}_{4}_*.E2E'.format(
            filenameSplit[0],
            filenameSplit[1],
            filenameSplit[2],
            filenameSplit[4],
            filenameSplit[5])

            filepathE2ESearch = os.path.join(E2EIN, filenameE2E)
            filepathsE2E2 = glob(filepathE2ESearch)
            if (len(filepathsE2E2)==0):
                continue
            mindiff = 9e9
            mindifffname=''

            for filepathE2E in filepathsE2E2:
                print(filepathE2E)
                file = E2E(filepathE2E)
                cslo_imgs = file.read_clso_image()  # returns an cslo volume with additional metadata if available

                single_cslo =  cslo_imgs[0]

                diff = np.sum(cv2.absdiff(imgTiff, single_cslo))

                allbasefname = os.path.basename(filepathE2E)
                cv2.imwrite(os.path.join(E2EOUT, 'test', allbasefname.replace('.E2E', '_all_e2e.png')), single_cslo)

                if diff<mindiff:
                    mindiff = diff
                    mindifffname = filepathE2E

            if len(mindifffname)>0:
                basefname = os.path.basename(mindifffname)
                s = '{0},{1}\n'.format(basefname,mindiff)
                print(s)
                fout.write(s)

                copy2(mindifffname,os.path.join(E2EOUT,basefname.replace('.E2E','_O.E2E')))

                if (mindiff > 100000):
                    OutD = E2EOUTPoor
                else:
                    OutD = E2EOUT


                os.makedirs(os.path.join(OutD,'test'),exist_ok=True)

                cv2.imwrite(os.path.join(OutD,'test',basefname.replace('.E2E','_e2e.png')),single_cslo)
                cv2.imwrite(os.path.join(OutD,'test', basefname.replace('.E2E', '_tiff.png')), imgTiff)

                #for idx in range(len(cslo_imgs)):
                #    os.makedirs(os.path.join(indir,'out'), exist_ok=True)
                #    cv2.imwrite(os.path.join(indir,'out',filename.replace('E2E','tiff')),cslo_imgs[idx])


                # cv2.imshow('img1',cslo_imgs[0])
                # cv2.imshow('img2',cslo_imgs[1])
                # cv2.waitKey()
                # oct_volumes = file.read_oct_volume()  # returns an OCT volume with additional metadata if available
                # #
                # for vi in range(len(oct_volumes) ):
                #     volume = oct_volumes[vi]
                #     os.makedirs(os.path.join(indir, 'out', filename, 'oct', str(vi)), exist_ok=True)
                #     #volume.peek()  # plots a montage of the volume
                #
                #     for i in range(volume.num_slices):
                #         cv2.imwrite(os.path.join(indir, 'out', filename, 'oct', str(vi), '{0}.png'.format(i)), volume.volume[i])

                        #volume.save(os.path.join(indir,'out',filename,'oct','{}.avi'.format(volume.patient_id)))

fout.close()