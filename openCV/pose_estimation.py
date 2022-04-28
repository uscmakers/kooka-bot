import math

import numpy as np
import cv2
import sys
from utils import ARUCO_DICT
import argparse
import time

def pose_estimation(frame, aruco_dict_type, matrix_coefficients, distortion_coefficients):
    '''
    frame - Frame from the video stream
    matrix_coefficients - Intrinsic matrix of the calibrated camera
    distortion_coefficients - Distortion coefficients associated with your camera
    return:-
    frame - The frame with the axis drawn on it
    '''

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.aruco_dict = cv2.aruco.Dictionary_get(aruco_dict_type)
    parameters = cv2.aruco.DetectorParameters_create()

    corners, ids, rejected_img_points = cv2.aruco.detectMarkers(gray, cv2.aruco_dict, parameters=parameters,
                                                                cameraMatrix=matrix_coefficients,
                                                                distCoeff=distortion_coefficients)

    # If markers are detected
    if len(corners) > 0:
        # check if both 23 and 24 is in ids
        if 23 in ids and 24 in ids:
            # draw a line between the two markers
            x1_sum = corners[0][0][0][0] + corners[0][0][1][0] + corners[0][0][2][0] + corners[0][0][3][0]
            y1_sum = corners[0][0][0][1] + corners[0][0][1][1] + corners[0][0][2][1] + corners[0][0][3][1]
            x1_centerPixel = (x1_sum * .25).astype(np.int64)
            y1_centerPixel = (y1_sum * .25).astype(np.int64)
            x2_sum = corners[1][0][0][0] + corners[1][0][1][0] + corners[1][0][2][0] + corners[1][0][3][0]
            y2_sum = corners[1][0][0][1] + corners[1][0][1][1] + corners[1][0][2][1] + corners[1][0][3][1]
            x2_centerPixel = (x2_sum * .25).astype(np.int64)
            y2_centerPixel = (y2_sum * .25).astype(np.int64)
            
            displacement = returnDistance(x1_centerPixel, y1_centerPixel, x2_centerPixel, y2_centerPixel)

            cv2.line(frame, (x1_centerPixel, y1_centerPixel), (x2_centerPixel, y2_centerPixel), (0, 255, 0), 2)
            
            # calculate the midpoint of the line
            midpoint = (((x1_centerPixel + x2_centerPixel) / 2).astype(np.int64), ((y1_centerPixel + y2_centerPixel) / 2).astype(np.int64))
            cv2.circle(frame, midpoint, 5, (0, 0, 255), -1)

        for i in range(0, len(ids)):
            # Estimate pose of each marker and return the values rvec and tvec---(different from those of camera coefficients)
            rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.02, matrix_coefficients,
                                                                           distortion_coefficients)
            # Draw a square around the markers
            cv2.aruco.drawDetectedMarkers(frame, corners)

            # Draw Axis
            cv2.aruco.drawAxis(frame, matrix_coefficients, distortion_coefficients, rvec, tvec, 0.01)
            

    return frame

def returnDistance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def main():
    #--K_Matrix calibration_matrix.npy --D_Coeff distortion_coefficients.npy --type DICT_5X5_100
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-k", "--K_Matrix", required=True, help="Path to calibration matrix (numpy file)")
    # ap.add_argument("-d", "--D_Coeff", required=True, help="Path to distortion coefficients (numpy file)")
    # ap.add_argument("-t", "--type", type=str, default="DICT_ARUCO_ORIGINAL", help="Type of ArUCo tag to detect")
    # args = vars(ap.parse_args())

    if ARUCO_DICT.get("DICT_5X5_100", None) is None:
        print(f"ArUCo tag type is not supported")
        sys.exit(0)

    aruco_dict_type = ARUCO_DICT["DICT_5X5_100"]
    calibration_matrix_path = "calibration_matrix.npy"
    distortion_coefficients_path = "distortion_coefficients.npy"

    k = np.load(calibration_matrix_path)
    d = np.load(distortion_coefficients_path)

    video = cv2.VideoCapture(1)
    time.sleep(2.0)

    while True:
        ret, frame = video.read()

        if not ret:
            break

        output = pose_estimation(frame, aruco_dict_type, k, d)

        cv2.imshow('Estimated Pose', output)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()
    return output

if __name__ == '__main__':
    main()