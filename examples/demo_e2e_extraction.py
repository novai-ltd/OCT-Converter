from oct_converter.readers import E2E
import cv2
import os


indir = r'C:\data\e2e\wetransfer-66d068\E2E Exsample'
filepath = os.path.join(indir,'OCT exsample 1.E2E')
#
# filepath = '/Users/mark/Downloads/TRALO01R.E2E'
file = E2E(filepath)
cslo_img = file.read_clso_image()  # returns an OCT volume with additional metadata if available
cv2.imshow('img',cslo_img)
cv2.waitKey()
# oct_volumes = file.read_oct_volume()  # returns an OCT volume with additional metadata if available
#
# for volume in oct_volumes:
#     volume.peek() # plots a montage of the volume
#     volume.save(os.path.join(indir,'{}.avi'.format(volume.patient_id)))
