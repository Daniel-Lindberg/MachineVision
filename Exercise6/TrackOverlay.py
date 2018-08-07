#Author: Daniel Lindberg

'''
Pedestrian detection.
Takes in a video file path, the name of the title of the images to be showed
and then finally the 'store' which is the location of the new video

'''
from __future__ import print_function
from imutils.object_detection import non_max_suppression
import argparse
import cv2
import numpy as np
import imutils
import csv
from skimage.morphology import skeletonize
import weave
import sys

######################################################################################
#Top Down Skeleton:
#apply the threshold
def skeletonTopDown(frame):
    ret, frame=cv2.threshold(frame, 70,255,cv2.THRESH_BINARY)

    #Get the negative of the image
    frame = 255-frame
    
    #apply the median blur on replace blurr value of 1
    frame = cv2.medianBlur(frame, 1)

    #Do the skeleton processing loop
    """
    This section of code was adapted from the following post, which was
    based in turn on the Wikipedia description of a morphological skeleton
    http://felix.abecassis.me/2011/09/opencv-morphological-skeleton/
    """
    element=cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
    counter = 0
    while (counter <=100):
        eroded = cv2.erode(frame, element)
        temp = cv2.dilate(eroded, element)
        temp=cv2.subtract(frame, temp)
        skel=cv2.bitwise_or(skel,temp)
        img=eroded.copy()

        counter=counter+1
        zeros= size - cv2.countNonZero(frame)
        if zeros==size:
            done=True

######################################################################################
#Thinning(Bottom up Skeleton) Methods: #
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

##############################################################################3

#Takes in all of the arguments specified
parser = argparse.ArgumentParser()
#Draw the bounding box or not
parser.add_argument("drawBox")
#Specifies the video file input
parser.add_argument("videofilepath", help="send a video file")
#Specifies what the name of the movie will show
parser.add_argument("show")
#Specifies the name of the new video
parser.add_argument("store")
args=parser.parse_args()

#take the video capture frame
cap = cv2.VideoCapture(args.videofilepath)
while not cap.isOpened():
	cap = cv2.VideoCapture(args.videofilepath)
	cv2.waitKey(1000)
	print ("Wait for the header")

#Get total number of frames
pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)

#Use the HOG Descriptor which stands for histogram of oriented gradients
hog = cv2.HOGDescriptor()
#Use the defualt people detector of the historgram of gradients
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
#create a list of total locations in each frame
locations = []
#have an incrementer for the frames
incrementer = 0
#create a list of all of the video frames
frames = []
#Create a list of all of the individual people
#This is done by taking all of the 

while True:
	#read in the frame from the video
    flag, frame = cap.read()
    location = []
    if flag:
        # The frame is ready and already captured
        #create a copy of the original
        orig = frame.copy()

        blank = frame.copy()
        #detect people within the image
        (rects, weights) = hog.detectMultiScale(frame, winStride=(4,4), padding=(8,8), scale=1.05)

       	# draw the original bounding boxes
       	for (x, y, w, h) in rects:
       		cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)

       	# apply non-maxima suppression to the bounding boxes using a
		# fairly large overlap threshold to try to maintain overlapping
		# boxes that are still people
		rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
		pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

		# draw the final bounding boxes
		i = 1
		for (xA, yA, xB, yB) in pick:
			#add in the location bounds of the people
			location.append(str(str(xA)+','+str(yA)+','+str(xB)+','+str(yB)))
			#Draw the rectangle
			cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
			i = i+1

		#add all of the locations of the rectangles
        locations.append(location)
        incrementer = incrementer+1
        #add curent frame to list
        frames.append(frame)
        #Display the image with the title
        if(args.drawBox):
        	cv2.imshow(args.show,frame)
        else:
        	cv2.imshow(args.show,blank)
    else:
        # The next frame is not ready, so we try to read it again
        cap.set(cv2.CAP_PROP_POS_FRAMES, pos_frame-1)
        print ("frame is not ready")
        # It is better to wait for a while for the next frame to be ready
        cv2.waitKey(1000)

    if cv2.waitKey(10) == 27:
        break
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        # If the number of captured frames is equal to the total number of frames,
        # we stop
        break

#get the dimensions of the first image for the video formatting
height, width, layers = frames[1].shape
#create a video based off of the store argument in the avi format, dimension is that of the first image
writer = cv2.VideoWriter(str(args.store)+".avi", cv2.VideoWriter_fourcc(*"MJPG"), 30,(width,height))
#for every single frame in the list, add the frame to the video
j=0
for frame in frames:
	writer.write(frame)
	path_name = str("Frame"+str("{0:0=4d}".format(j))+".png")
	cv2.imwrite(path_name, frame)
	j=j+1
#Write the location of rectangles into a csv file
with open('people.csv', 'w') as csvfile:
	#Use a comma as the delimeter
    spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    i = 1
    #Write the frame number associated with all of the rectangle locations
    for location in locations:
		spamwriter.writerow(['Frame'+str(i), str(location)])
		i=i+1