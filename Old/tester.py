# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 00:02:23 2017

@author: kshahzada
"""

from cv2 import *
# Initialize the camera
capture = CaptureFromCAM(0)  # 0 -> index of camera
if capture:     # Camera initialized without any errors
   NamedWindow("cam-test",CV_WINDOW_AUTOSIZE)
   f = QueryFrame(capture)     # capture the frame
   if f:
       ShowImage("cam-test",f)
       WaitKey(0)
DestroyWindow("cam-test")