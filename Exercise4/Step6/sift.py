"""
Step 6
Daniel Lindberg
"""

import numpy as np
import cv2
from matplotlib import pyplot as plt

img1 = cv2.imread('First.jpg',0)          # queryImage
img2 = cv2.imread('Second.jpg',0)         # same image

# Initiate the Scale Invariant Feature Transformation
sift = cv2.xfeatures2d.SIFT_create()

# find the keypoints and descriptors using the SIFt
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

# Parameters for fast approximate nearest neighbor search
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50)   # or pass empty dictionary

#Use the flann search paramters
flann = cv2.FlannBasedMatcher(index_params,search_params)

#Find all of the matches between the two
matches = flann.knnMatch(des1,des2,k=2)

# Need to draw only good matches, so create a mask
matchesMask = [[0,0] for i in xrange(len(matches))]

# Do a ratio test between all of the masks, check for the vary best features. 
#Chose a default variable as .7
for i,(m,n) in enumerate(matches):
    if m.distance < 0.7*n.distance:
        matchesMask[i]=[1,0]

#Draw the paramters , red will be single point color
#Green is the matching colors
#Use the matches previously deteceted
draw_params = dict(matchColor = (0,255,0),
                   singlePointColor = (255,0,0),
                   matchesMask = matchesMask,
                   flags = 0)

#Draw the links between the images using the green lines
#Draw all of the features with the red circles
img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)

#Show the image
plt.imshow(img3,),plt.show()