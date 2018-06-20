
import numpy as np
import cv2

im = cv2.imread('/home/daniel/UnivCol/MachineVision/Exercises/Exercise1/StepFive/Photo-Small.jpg')
row, col = im.shape[:2]
bottom = im[row-2:row, 0:col]
mean = cv2.mean(bottom)[0]

bordersize=4
border=cv2.copyMakeBorder(im,top=bordersize, bottom=bordersize, left=bordersize, right=bordersize, borderType=cv2.BORDER_CONSTANT, value=[mean,mean,mean])

line_down = cv2.line(border, (0,row/2), (col, row/2), (0,255,255),1)
line_side = cv2.line(line_down, (col/2,0) , (col/2, row), (0,255,255), 1)

cv2.imshow('Cross Hairs', line_side)

cv2.waitKey(0)
cv2.destroyAllWindows()