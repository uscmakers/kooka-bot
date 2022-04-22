import math

import numpy as np
import cv2
import sys
from utils import ARUCO_DICT
import argparse
import time


def pose_esitmation(frame, aruco_dict_type, matrix_coefficients, distortion_coefficients):
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
        for i in range(0, len(ids)):
            # Estimate pose of each marker and return the values rvec and tvec---(different from those of camera coefficients)
            rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.02, matrix_coefficients,
                                                                           distortion_coefficients)
            # Draw a square around the markers
            cv2.aruco.drawDetectedMarkers(frame, corners)

            # Draw Axis
            cv2.aruco.drawAxis(frame, matrix_coefficients, distortion_coefficients, rvec, tvec, 0.01)
            
            # print("tvec: ", (abs(tvec[0][0][0]) * 10000).astype(np.int64), ", ", (abs(tvec[0][0][1]) * 10000).astype(np.int64))
            # print("rvec: ", rvec)
            
            # Draw a point 5cm to the right of the marker
            # x = abs(tvec[0][0][0] * 10000).astype(np.int64)
            # y = abs(tvec[0][0][1] * 10000).astype(np.int64)
            # cv2.circle(frame, (x, y), radius=10, color=(0, 0, 255), thickness=-1)
            
            # Vector math stuff
            # displacement = 100
            # rodr = cv2.Rodrigues(rvec)
            # print("potato1", rvec)
            # # print(rodr[0])
            # proj = rvec * displacement + tvec * 900
            # # print("potato2", tvec)
            # x = ((proj[0][0][0]).astype(np.int64))
            # y = ((proj[0][0][1]).astype(np.int64))
            # # print ("proj: ", x, ", ", y)
            
            # use theta
            displacement = 100
            theta = rvec[0][0][0]
            # print(theta)
            x = (displacement * np.cos(theta)).astype(np.int64)
            y = (displacement * np.sin(theta)).astype(np.int64)
            x += -(tvec[0][0][0] * 3000).astype(np.int64)
            y += -(tvec[0][0][1] * 3000).astype(np.int64)
            # x += 200
            # y += 200
            print ("proj: ", x, ", ", y) 
            # print(tvec)
            cv2.circle(frame, (x, y), radius=10, color=(0, 0, 255), thickness=-1)

    return frame


# Checks if a matrix is a valid rotation matrix.
def isRotationMatrix(R) :
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype = R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6

# Calculates rotation matrix to euler angles
# The result is the same as MATLAB except the order
# of the euler angles ( x and z are swapped ).
def rotationMatrixToEulerAngles(R) :

    assert(isRotationMatrix(R))

    sy = math.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])

    singular = sy < 1e-6

    if  not singular :
        x = math.atan2(R[2,1] , R[2,2])
        y = math.atan2(-R[2,0], sy)
        z = math.atan2(R[1,0], R[0,0])
    else :
        x = math.atan2(-R[1,2], R[1,1])
        y = math.atan2(-R[2,0], sy)
        z = 0

    return np.array([x, y, z])


if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-k", "--K_Matrix", required=True, help="Path to calibration matrix (numpy file)")
    ap.add_argument("-d", "--D_Coeff", required=True, help="Path to distortion coefficients (numpy file)")
    ap.add_argument("-t", "--type", type=str, default="DICT_ARUCO_ORIGINAL", help="Type of ArUCo tag to detect")
    args = vars(ap.parse_args())

    if ARUCO_DICT.get(args["type"], None) is None:
        print(f"ArUCo tag type '{args['type']}' is not supported")
        sys.exit(0)

    aruco_dict_type = ARUCO_DICT[args["type"]]
    calibration_matrix_path = args["K_Matrix"]
    distortion_coefficients_path = args["D_Coeff"]

    k = np.load(calibration_matrix_path)
    d = np.load(distortion_coefficients_path)

    video = cv2.VideoCapture(1)
    time.sleep(2.0)

    while True:
        ret, frame = video.read()

        if not ret:
            break

        output = pose_esitmation(frame, aruco_dict_type, k, d)

        cv2.imshow('Estimated Pose', output)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()
