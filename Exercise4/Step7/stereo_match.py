import numpy as np
import cv2
from matplotlib import pyplot as plt

imgL = cv2.imread('snapshot_left_1385866691881.1577.jpg',0)
imgR = cv2.imread('snapshot_left_1385875341982.3462.jpg',0)

#stereo = cv2.createStereoBM(numDisparities=16, blockSize=15)
#stereo = cv2.StereoBM(cv2.STEREO_BM_BASIC_PRESET,ndisparities=16, SADWindowSize=15)
stereo=cv2.StereoBM_create(numDisparities=16, blockSize=15)
disparity = stereo.compute(imgL,imgR)
plt.imshow(disparity,'gray')
plt.show()
