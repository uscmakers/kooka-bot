import cv2
import cv2.aruco as aruco
    
    
def main():
  import cv2
  import numpy as np
  import cv2.aruco as aruco
  import time

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
        # print(ids)
        #   print()
        x_sum = corners[0][0][0][0]+ corners[0][0][1][0]+ corners[0][0][2][0]+ corners[0][0][3][0]
        y_sum = corners[0][0][0][1]+ corners[0][0][1][1]+ corners[0][0][2][1]+ corners[0][0][3][1]
        
        x_centerPixel = x_sum*.25
        y_centerPixel = y_sum*.25
        
        print(str(x_centerPixel) + ", " + str(y_centerPixel))
    

    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

  cap.release()
  cv2.destroyAllWindows()

if __name__ == '__main__':
  main()