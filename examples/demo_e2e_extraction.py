from oct_converter.readers import E2E
import cv2
import os


indir = r'C:\data\e2e'
#filepath = os.path.join(indir,'OCT exsample 1.E2E')
filepath = os.path.join(indir,'PATIE013.E2E')
#
# filepath = '/Users/mark/Downloads/TRALO01R.E2E'
file = E2E(filepath)
cslo_imgs = file.read_clso_image()  # returns an OCT volume with additional metadata if available
# cv2.imshow('img1',cslo_imgs[0])
# cv2.imshow('img2',cslo_imgs[1])
# cv2.waitKey()

for idx in range(len(cslo_imgs)):
    cv2.imwrite(os.path.join(indir,'out','out_{0}.png'.format(idx)),cslo_imgs[idx])



# oct_volumes = file.read_oct_volume()  # returns an OCT volume with additional metadata if available
#
# for volume in oct_volumes:
#     volume.peek() # plots a montage of the volume
#     volume.save(os.path.join(indir,'{}.avi'.format(volume.patient_id)))
