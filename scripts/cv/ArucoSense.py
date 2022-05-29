import cv2
import cv2.aruco as aruco
import numpy as np
  
def GetCoords():
    
    cap = cv2.VideoCapture(1)
    cap.set(4, 480)
    
    # dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)
    parameters = aruco.DetectorParameters_create()
        
    while True:
        ret, frame = cap.read()
        if not ret:
            break
    
        # detect aruco markers
        corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, dictionary, parameters=parameters)
    
        # draw markers
        frame = aruco.drawDetectedMarkers(frame, corners, ids, (0, 255, 0))
    
        # print id
        if ids is not None:
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

                cv2.line(frame, (x1_centerPixel, y1_centerPixel), (x2_centerPixel, y2_centerPixel), (0, 255, 0), 2)

                # calculate the midpoint of the line
                midpoint = (((x1_centerPixel + x2_centerPixel) / 2).astype(np.int64),
                            ((y1_centerPixel + y2_centerPixel) / 2).astype(np.int64))

                cv2.circle(frame, midpoint, 5, (0, 0, 255), -1)
                cap.release()
                cv2.destroyAllWindows()
                return midpoint
    
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
  GetCoords()