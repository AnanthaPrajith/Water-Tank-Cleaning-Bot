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

	  rospy.init_node('Line_follower_controller', anonymous=True)
	  
	  self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
	  self.vel = Twist()

#_____Defining intial velocity as zero for robot. You should change 
#	  self.vel.linear.x and self.vel.angular.z  for controlling the robot
#     self.vel.linear.x should be less than 1 and 
#	  self.vel.angular.z should be between 2 and -2

	  self.vel.linear.x = 0
	  self.vel.linear.y = 0
	  self.vel.linear.z = 0
	  self.vel.angular.x = 0
	  self.vel.angular.y = 0
	  self.vel.angular.z = 0

#_____Setting Sensor values as 1 as intial condition for left, right and middle sensor
#_____If the line is detected, the sensor gives output as 0
#_____else it gives output as 1

	  self.left = "1"
	  self.middle = "1"
	  self.right = "1"
	  
	  self.publish_vel()

#________________________for subscribing sensor data___________________________
	  
	  self.sensor_middle = rospy.Subscriber("/middle",String,self.callback_m)
	  self.sensor_right = rospy.Subscriber("/right",String,self.callback_r)
	  self.sensor_left = rospy.Subscriber("/left",String,self.callback_l)

#_________________callback function for sensor data ___________

	def callback_l(self,data):
	  if data.data == "0":
	  	self.left = "0"

	  else:
	  	self.left = "1"
	  self.publish_vel()

# Create Callback function for right and middle sensor 	

	def callback_m(self,data):
	  if data.data == "0":
	  	self.middle = "0"

	  	
	  else:
	  	self.middle = "1"
	  self.publish_vel()

	def callback_r(self,data):
	  if data.data == "0":
	  	self.right = "0"

	  else:
	  	self.right = "1"
	  self.publish_vel()

#_____________for publishing Velocity___________________
    


	def publish_vel(self) :



	  	if self.middle  == "0":
			self.vel.linear.x = 0.2
			self.vel.linear.y = 0
			self.vel.linear.z = 0
			self.vel.angular.x = 0
			self.vel.angular.y = 0
			self.vel.angular.z = 0.0
			rospy.loginfo("Going straight")

	  	if self.right == "0":
			self.vel.linear.x = 0.1
			self.vel.linear.y = 0
			self.vel.linear.z = 0
			self.vel.angular.x = 0
			self.vel.angular.y = 0
			self.vel.angular.z = -1.30
			rospy.loginfo("Turning right")

	  	if self.left == "0":
			self.vel.linear.x = 0.1
			self.vel.linear.y = 0
			self.vel.linear.z = 0
			self.vel.angular.x = 0
			self.vel.angular.y = 0
			self.vel.angular.z = 1.30
			rospy.loginfo("Turning left")





		self.pub.publish(self.vel)
	  

# ______________________________________________________________________________________________________________________

#	Create algorithm for line follower robot based on the sensor data (self.left, self.right and self.middle).
#	Based on your decision set value for self.vel.linear.x (for moving robot forward) and self.vel.angular.y (for turning robot
#	left or right)

#	self.vel.linear.x should be less than 1. You can set any value for stable movement of robot  
#	self.vel.angular.z should be between 2 and -2 
#	(negative direction makes the robot tur opposite direction)
# ______________________________________________________________________________________________________________________

		# self.pub.publish(self.vel)
 
	  

def main(args):
  ic = image_converter()
  
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
