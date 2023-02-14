#! /usr/bin/env python
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


	  self.cv_image_m = []
	  rospy.init_node('middle_sensor', anonymous=True)
	  self.pub = rospy.Publisher('/middle', String, queue_size=1)

	  self.bridge = CvBridge()
	  self.image_m= rospy.Subscriber("/lfw/camera_middle/image_raw",Image,self.callback)


	def callback(self,data):
	  try:
	    self.cv_image_m= self.bridge.imgmsg_to_cv2(data, "bgr8")
	    self.cv_image_m= cv2.resize(self.cv_image_m,(192,108))
	    self.cv_image_m= cv2.cvtColor(self.cv_image_m, cv2.COLOR_BGR2GRAY) 
	    _,self.cv_image_m= cv2.threshold(self.cv_image_m,200,255,cv2.THRESH_BINARY)
	    edges_m = cv2.Canny(self.cv_image_m, 50,150)

	    lines_m = cv2.HoughLines(edges_m,1,np.pi/180,10)
	    
	    number_of_black_pix = np.sum(self.cv_image_m == 0) 
	    
	    
	    if number_of_black_pix  > len(self.cv_image_m)*0.3:
	    	self.pub.publish("0")
	    	
	    else:
	    	self.pub.publish("1")

	    lines_m = None
	
	    cv2.imshow("middle_sensor", self.cv_image_m)
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
