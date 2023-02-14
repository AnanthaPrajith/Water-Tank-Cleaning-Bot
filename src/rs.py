#!/usr/bin/env python
from __future__ import print_function
 
import roslib

import sys
import rospy
import cv2
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist

class image_converter:

	def __init__(self):

	  rospy.init_node('right_sensor', anonymous=True)
	  self.cv_image_r = []
	  self.pub = rospy.Publisher('/right', String, queue_size=1)
	  self.bridge = CvBridge()
	  self.image_r = rospy.Subscriber("/lfw/camera_right/image_rawr",Image,self.callback_r)


	def callback_r(self,data):
	  try:
	    self.cv_image_r = self.bridge.imgmsg_to_cv2(data, "bgr8")
	    self.cv_image_r = cv2.resize(self.cv_image_r,(192,108))
	    self.cv_image_r = cv2.cvtColor(self.cv_image_r, cv2.COLOR_BGR2GRAY) 
	    _,self.cv_image_r = cv2.threshold(self.cv_image_r,200,255,cv2.THRESH_BINARY)
	    edges_r = cv2.Canny(self.cv_image_r, 50,150)

	    lines_r = cv2.HoughLines(edges_r,1,np.pi/180,10)

	    number_of_black_pix = np.sum(self.cv_image_r == 0) 

	    if number_of_black_pix  > len(self.cv_image_r)*0.3:
	    	self.pub.publish("0")
	    
	    else:
	    	self.pub.publish("1")
	    lines_r = None

	    cv2.imshow("right_sensor", self.cv_image_r)
	    cv2.waitKey(3)

	  except CvBridgeError as e:
	    print(e)

  

def main(args):
  ic = image_converter()
  
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)