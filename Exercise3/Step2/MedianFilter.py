#Author: Daniel Lindberg

#apply the Median filter as documented in our Lecture-Week-5
#to the G band only in a graymap and provide an image of before 
#and after filter images in your report - did this help enhance
#the laser spot edge boundary at all?

import cv2
import argparse
 
image_path = "image.png"
# read the image in grayscale
image = cv2.imread(image_path, 0)
# apply the 3x3 median filter on the image
processed_image = cv2.medianBlur(image, 3)
# display image
cv2.imshow('Median Filter Processing', processed_image)
# save image to disk
cv2.imwrite('processed_image.png', processed_image)
# pause the execution of the script until a key on the keyboard is pressed
cv2.waitKey(0)