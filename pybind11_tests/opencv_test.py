import random
import time
import cv2
import os
import numpy as np
from glob import glob
import sys

# Add parent directory path in import
sys.path.append('../')
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


if __name__ == "__main__":
    # Compare checkerboard detection using python and C++ with pybind11
    img_path = "/home/menonsandu/Downloads/checkerboad.jpeg"
    corners_x = 9
    corners_y = 7

    start = time.time()
    img_corners = get_checkerboard_corners(img_path, corners_x, corners_y)
    end = time.time()
    print(img_corners.shape, img_corners[3])
    print("Time taken by cpp checkerboard detection:", end - start)

    start = time.time()
    img_corners, gray_img = py_get_checkerboard_corners(img_path, corners_x, corners_y)
    end = time.time()
    print(img_corners.shape, img_corners[3])
    print("Time taken by python checkerboard detection:", end - start)

    # Compare checkerboard detection on all files in a directory using python and C++ with pybind11
    dir_path = "/home/menonsandu/stereo-callibration/camodocal/data/images/png_files"
    corners_x = 9
    corners_y = 6

    # Python
    files = glob(os.path.join(dir_path , "*.png"))
    start = time.time()
    img_corners_list = []
    for image_file in files:
        img_corners, gray_img = py_get_checkerboard_corners(image_file, corners_x, corners_y)
        img_corners_list.append(img_corners)
    end = time.time()
    print("Time taken by python checkerboard detection on all files in a directory:", end - start)

    # C++
    start = time.time()
    img_corners_list = []
    for image_file in files:
        img_corners = get_checkerboard_corners(image_file, corners_x, corners_y)
        img_corners_list.append(img_corners)
    end = time.time()
    print("Time taken by cpp checkerboard detection on all files in a directory:", end - start)