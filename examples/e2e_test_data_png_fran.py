from oct_converter.readers import E2E
import cv2
import os


#indir = r'Y:\Backup\data\data\Phase2\Phase2_E2E\E2E darc2 imaging\Glaucuma_single\All'

base = r'Z:\data\Phase2\E2E darc2 imaging\Glaucuma_single\from fran'
#filepath = os.path.join(indir,'OCT exsample 1.E2E')
#filenames = ['OCT exsample 1.E2E','OCT exsample 2.E2E','OCT exsample.E2E','PATIE013.E2E','Unknow Patient OCT Data.E2E']#,SBL5004A '026_F016.E2E', '02601C.E2E']
indirs = os.listdir(base)
for indir in indirs:
    if os.path.isdir(os.path.join(base,indir)):
        filenames = os.listdir(os.path.join(base,indir))#,'OCT exsample 2.E2E','OCT exsample.E2E','PATIE013.E2E','Unknow Patient OCT Data.E2E']#,SBL5004A '026_F016.E2E', '02601C.E2E']
        for filename in filenames:
            if filename.endswith('.E2E'):
                filepath = os.path.join(base,indir,filename)
                #
                # filepath = '/Users/mark/Downloads/TRALO01R.E2E'
                file = E2E(filepath)
                cslo_imgs = file.read_clso_image()  # returns an cslo volume with additional metadata if available

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


                for idx in range(len(cslo_imgs)):
                    os.makedirs(os.path.join(base, indir,'out'), exist_ok=True)
                    cv2.imwrite(os.path.join(base, indir,'out',filename.replace('E2E','tiff')),cslo_imgs[idx])
