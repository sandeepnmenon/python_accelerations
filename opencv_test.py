import random
import time
import cv2
import os
import numpy as np
from build.py_opencv import get_checkerboard_corners

def py_get_checkerboard_corners(image_file_path, corners_x, corners_y):
    if not os.path.isfile(image_file_path):
        return None, None
    try:
        img = cv2.imread(image_file_path, cv2.IMREAD_COLOR)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, img_corners = cv2.findChessboardCorners(gray_img, (corners_x, corners_y), None)
        if ret:
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            cv2.cornerSubPix(gray_img, img_corners, (5, 5), (-1, -1), criteria)
            return img_corners, gray_img
        else:
            raise Exception()
    except Exception as e:
        print(e)
        print(f'Corners ({corners_x}x{corners_y}) could not be found for image file at {image_file_path}')
        return np.array([]), gray_img

img_path = "/home/menonsandu/Downloads/checkerboad.jpeg"
corners_x = 9
corners_y = 7

# Compare time taken by python checkerboard detection with cpp
start = time.time()
img_corners, gray_img = py_get_checkerboard_corners(img_path, corners_x, corners_y)
print(img_corners.shape, img_corners[3])
end = time.time()
print("Time taken by python checkerboard detection:", end - start)

start = time.time()
img_corners = get_checkerboard_corners(img_path, corners_x, corners_y)
print(img_corners.shape, img_corners[3])
end = time.time()
print("Time taken by cpp checkerboard detection:", end - start)