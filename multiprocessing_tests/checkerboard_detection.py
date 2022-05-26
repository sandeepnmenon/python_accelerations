import random
import time
import cv2
import os
import numpy as np
from glob import glob
import sys
import multiprocessing as mp


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
            return img_corners
        else:
            return np.array([])
    except Exception as e:
        print(e)
        # print(f'Corners ({corners_x}x{corners_y}) could not be found for image file at {image_file_path}')
        return np.array([])


if __name__ == "__main__":
    # Compare checkerboard detection on all files in a directory using serial python loop and multiprocessing
    dir_path = "/home/menonsandu/stereo-callibration/camodocal/data/images/png_files"
    corners_x = 9
    corners_y = 6

    # Python
    files = glob(os.path.join(dir_path , "*.png"))
    start = time.time()
    img_corners_list = {}
    for image_file in files:
        img_corners = py_get_checkerboard_corners(image_file, corners_x, corners_y)
        img_corners_list[image_file] = img_corners
    end = time.time()
    print("Time taken by python checkerboard detection on all files in a directory:", end - start)

    # Multiprocessing
    start = time.time()
    img_corners_list_mp = {}
    num_processes = max(1, mp.cpu_count() - 2)
    pool = mp.Pool(num_processes)
    for image_file in files:
        img_corners_mp = pool.apply_async(py_get_checkerboard_corners, (image_file, corners_x, corners_y))
        img_corners_list_mp[image_file] = img_corners_mp
    pool.close()
    pool.join()
    end = time.time()
    print(f"Time taken by multiprocessing {num_processes} processes checkerboard detection on all files in a directory:", end - start)

    # Compare results
    compare_flag = True
    for image_file in files:
        img_corners = np.array(img_corners_list[image_file])
        img_corners_mp= np.array(img_corners_list_mp[image_file].get())
        if not np.array_equal(img_corners, img_corners_mp):
            print(f'Corners ({corners_x}x{corners_y}) did not match for image file at {image_file}')
            compare_flag = False
            
    # Check for a random image if results are same
    if compare_flag:
        print("Results are same for all images")
    else:
        print("Results are not same for some images")