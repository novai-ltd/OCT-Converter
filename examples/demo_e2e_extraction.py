from oct_converter.readers import E2E
import cv2
import os


indir = r'E:\Novai Dropbox\New Potential Studies Discussed Proposals\Astellas 2020\Primate AF photos'
#filepath = os.path.join(indir,'OCT exsample 1.E2E')
filenames = ['SBL5001A.E2E','SBL5003A.E2E','SBL5004A.E2E','SBL5002A.E2E']#,SBL5004A '026_F016.E2E', '02601C.E2E']
for filename in filenames:
    filepath = os.path.join(indir,filename)
    #
    # filepath = '/Users/mark/Downloads/TRALO01R.E2E'
    file = E2E(filepath)
    cslo_imgs = file.read_clso_image()  # returns an cslo volume with additional metadata if available

    # cv2.imshow('img1',cslo_imgs[0])
    # cv2.imshow('img2',cslo_imgs[1])
    # cv2.waitKey()
    #oct_volumes = file.read_oct_volume()  # returns an OCT volume with additional metadata if available
    #
    # for vi in range(len(oct_volumes) ):
    #     volume = oct_volumes[vi]
    #     os.makedirs(os.path.join(indir, 'out', filename, 'oct', str(vi)), exist_ok=True)
    #     #volume.peek()  # plots a montage of the volume
    #
    #     for i in range(volume.num_slices):
    #         cv2.imwrite(os.path.join(indir, 'out', filename, 'oct', str(vi), '{0}.png'.format(i)), volume.volume[i])
    #
    #         #volume.save(os.path.join(indir,'out',filename,'oct','{}.avi'.format(volume.patient_id)))


    for idx in range(len(cslo_imgs)):
        os.makedirs(os.path.join(indir,'out',filename,'cslo'), exist_ok=True)
        cv2.imwrite(os.path.join(indir,'out',filename,'cslo','{0}.png'.format(idx)),cslo_imgs[idx])
