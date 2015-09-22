import numpy as np
import cv2
from matplotlib import pyplot as plt

def cvt_contour_to_2d(contour):
    returned_arr = []
    for i in range(0,len(contour)):
      returned_arr.append(contour[i][0])
    return np.array(returned_arr)

def count_sides(slope):
    sides = 0
    average = np.average(map(np.absolute,slope))
    for i in range(0, len(slope)):
        if(np.absolute(slope[i]) > average*1.5):
            sides = sides + 1
    return sides

def slope1d(input_array):
    returned_arr = [input_array[len(input_array)-1] - input_array[0]]
    for i in range(0,len(input_array)-1):
        slope = input_array[i] - input_array[i+1]
        returned_arr.append(slope)
    return np.array(returned_arr)

def slope2d(input_array):
    returned_array = []
    for i in range(0,len(input_array)-80):
        slope = input_array[i] - input_array[i+80]
        returned_array.append(slope[0]/ slope[1])
    return returned_array


im = cv2.imread('sample5.jpg')
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,60,255,cv2.THRESH_BINARY_INV)
img_contour = np.copy(thresh)
contours, heirarchy = cv2.findContours(img_contour,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
# contour = get_relevant_contour(contours)
polydp = [cv2.approxPolyDP(contour, 15, True) for contour in contours]
rectangles = [cv2.boundingRect(contour) for contour in polydp if len(contour) == 3]
# slope_x = slope2d(cvt_contour_to_2d(contour))
# second_diff_slope_x = slope1d(slope_x)
# print count_sides(second_diff_slope_x)
# plt.plot(slope_x)
# plt.show()
im2 = np.copy(im)
for i in range(0, len(polydp)):
    cv2.drawContours(im2, polydp[i], -1, (0,255,255), 3)

for i in range(0, len(rectangles)):
    rect = rectangles[i]
    cv2.rectangle(im2, (rect[0], rect[1]), (rect[0]+rect[2], rect[1] + rect[3]), (255,255,0))

# # cv2.namedWindow('output')
# cv2.imshow('input', im)
cv2.imshow('thresholded', thresh)
cv2.imshow('output', im2)
cv2.waitKey(0)
