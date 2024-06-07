#!/usr/bin/env python

import rospy
from mavros_msgs.srv import SetMode
from mavros_msgs.srv import CommandBool
from mavros_msgs.srv import CommandTOL
from geometry_msgs.msg import PoseStamped, TwistStamped 
import time

rospy.init_node('mavros_takeoff_python')
rate = rospy.Rate(10)
pose_pub = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped, queue_size=10)
vel_pub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel', TwistStamped, queue_size=10)

def setmode(a):
    rospy.wait_for_service('/mavros/set_mode')
    try:
        change_mode = rospy.ServiceProxy('/mavros/set_mode', SetMode)
        response = change_mode(custom_mode= a)
        rospy.loginfo(response)
    except rospy.ServiceException as e:
        print("Set mode failed: %s" %e)

def arming():
    print ("\nArming")
    rospy.wait_for_service('/mavros/cmd/arming')
    try:
        arming_cl = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
        response = arming_cl(value = True)
        rospy.loginfo(response)
    except rospy.ServiceException as e:
        print("Arming failed: %s" %e)
def takeoff():
    print ("\nTaking off")
    rospy.wait_for_service('/mavros/cmd/takeoff')
    try:
        takeoff_cl = rospy.ServiceProxy('/mavros/cmd/takeoff', CommandTOL)
        response = takeoff_cl(altitude=10, latitude=0, longitude=0, min_pitch=0, yaw=0)
        rospy.loginfo(response)
    except rospy.ServiceException as e:
        print("Takeoff failed: %s" %e)

def land():
    print ("\nLanding")
    rospy.wait_for_service('/mavros/cmd/land')
    try:
        takeoff_cl = rospy.ServiceProxy('/mavros/cmd/land', CommandTOL)
        response = takeoff_cl(altitude=10, latitude=0, longitude=0, min_pitch=0, yaw=0)
        rospy.loginfo(response)
    except rospy.ServiceException as e:
        print("Landing failed: %s" %e)

def disarm():
    print ("\nDisarming")
    rospy.wait_for_service('/mavros/cmd/arming')
    try:
        arming_cl = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
        response = arming_cl(value = False)
        rospy.loginfo(response)
    except rospy.ServiceException as e:
        print("Disarming failed: %s" %e)
def rotate(yaw_rate, duration=5):
    vel = TwistStamped()
    vel.header.stamp = rospy.Time.now()
    vel.twist.angular.z = yaw_rate

    start_time = rospy.Time.now()
    while rospy.Time.now() - start_time < rospy.Duration(duration):
        vel_pub.publish(vel)
        rate.sleep()
def move_to_position(x, y, z, duration=5):
    pose = PoseStamped()
    pose.header.stamp = rospy.Time.now()
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.position.z = z

    start_time = rospy.Time.now()
    while rospy.Time.now() - start_time < rospy.Duration(duration):
        pose_pub.publish(pose)
        rate.sleep()

def move_with_velocity(vx, vy, vz, duration=5):
    vel = TwistStamped()
    vel.header.stamp = rospy.Time.now()
    vel.twist.linear.x = vx
    vel.twist.linear.y = vy
    vel.twist.linear.z = vz
    
    start_time = rospy.Time.now()
    while rospy.Time.now() - start_time < rospy.Duration(duration):
        vel_pub.publish(vel)
        rate.sleep()
def xmove(vx):
    vel = TwistStamped()
    vel.twist.linear.x = vx
    vel_pub.publish(vel)
def ymove(vy):
    vel = TwistStamped()
    vel.twist.linear.y = vy
    vel_pub.publish(vel)
def zmove(vz):
    vel = TwistStamped()
    vel.twist.linear.z = vz
    vel_pub.publish(vel)


 

