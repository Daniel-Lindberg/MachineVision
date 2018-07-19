#Author:Daniel Lindberg

import time
import cv2
import numpy as np
from skimage.morphology import skeletonize
import weave
import sys

#obtain the capture image
cap = cv2.VideoCapture(0)

#Used for the erode function
kernel = np.ones((3,3),np.uint8)

done=False

#get the start time
start_time = time.clock()

#iterator for number of frames 
i = 0

def _thinningIteration(im, iter):
    I, M = im, np.zeros(im.shape, np.uint8)
    expr = """
    for (int i = 1; i < NI[0]-1; i++) {
        for (int j = 1; j < NI[1]-1; j++) {
            int p2 = I2(i-1, j);
            int p3 = I2(i-1, j+1);
            int p4 = I2(i, j+1);
            int p5 = I2(i+1, j+1);
            int p6 = I2(i+1, j);
            int p7 = I2(i+1, j-1);
            int p8 = I2(i, j-1);
            int p9 = I2(i-1, j-1);
            int A  = (p2 == 0 && p3 == 1) + (p3 == 0 && p4 == 1) +
                     (p4 == 0 && p5 == 1) + (p5 == 0 && p6 == 1) +
                     (p6 == 0 && p7 == 1) + (p7 == 0 && p8 == 1) +
                     (p8 == 0 && p9 == 1) + (p9 == 0 && p2 == 1);
            int B  = p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9;
            int m1 = iter == 0 ? (p2 * p4 * p6) : (p2 * p4 * p8);
            int m2 = iter == 0 ? (p4 * p6 * p8) : (p2 * p6 * p8);
            if (A == 1 && B >= 2 && B <= 6 && m1 == 0 && m2 == 0) {
                M2(i,j) = 1;
            }
        }
    } 
    """

    weave.inline(expr, ["I", "iter", "M"])
    return (I & ~M)


def thinning(src):
    dst = src.copy() / 255
    prev = np.zeros(src.shape[:2], np.uint8)
    diff = None

    while True:
        dst = _thinningIteration(dst, 0)
        dst = _thinningIteration(dst, 1)
        diff = np.absolute(dst - prev)
        prev = dst.copy()
        if np.sum(diff) == 0:
            break
    return dst * 255

#Do this loop for 100 second
while(time.clock()-start_time <= 100):
    #obtain the frames
    ret, frame = cap.read()
    frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _,frame = cv2.threshold(frame, 70,255,cv2.THRESH_BINARY)
    frame = thinning(frame)

    #write the frame to be made into a MPEG via ffmpeg
    path_name = str("Frame"+str("{0:0=4d}".format(i))+".png")
    cv2.imwrite(path_name,frame)
    i = i +1
    #wait a hot second
    k= cv2.waitKey(1);
    if k==27:
        break
cap.release()
cv2.destroyAllWindows()
