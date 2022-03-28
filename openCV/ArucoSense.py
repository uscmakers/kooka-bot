# open a camera stream that detects ArUco markers
# and displays the id of the detected markers

def main():
  import cv2
  import numpy as np
  import time
  import sys
  
  # create the marker dictionary
  markerDictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
  
  # create the detector parameters
  parameters = cv2.aruco.DetectorParameters_create()
  
  # create the camera stream
  cap = cv2.VideoCapture(0)
  
  # set the camera resolution
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
  
  # loop until the camera stream is open
  while not cap.isOpened():
    print('failed to open camera')
    time.sleep(1)
    cap = cv2.VideoCapture(0)
    
  # loop until a key is pressed
  while True:
    # read the camera frame
    ret, frame = cap.read()
    
    # detect the markers
    markers = cv2.aruco.detectMarkers(frame, markerDictionary, parameters=parameters)
    
    # if there are markers
    if len(markers[0]) > 0:
      # draw the detected markers
      cv2.aruco.drawDetectedMarkers(frame, markers)
    
    # display the frame
    cv2.imshow('frame', frame)
    
    # if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
  
  # release the camera stream
  cap.release()
  cv2.destroyAllWindows()