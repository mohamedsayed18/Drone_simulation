#!/usr/bin/env python
"""
This script detect an AR marker and land on it. the sequence is as follow
1- Set the offboard mode
2- Arming on
3- fly to the target position
4- detect the marker and land on it

Notes:
Before entering Offboard mode, you must have already started streaming setpoints.
 Otherwise the mode switch will be rejected.
"""

# libraries and messages 
import rospy
from mavros_msgs.srv import SetMode
from mavros_msgs.srv import CommandBool
from mavros_msgs.srv import CommandTOL
from geometry_msgs.msg import PoseStamped
from ar_track_alvar_msgs.msg import AlvarMarkers

# Global variables for the drone position, marker_position
glo_pos_z = 0
glo_pos_x = 0
glo_pos_y = 0
marker_x = 0
marker_y = 0
detected = 0	#	true if the marker is detected 

def landing(data):
	"""
	detect the marker and set the new target pose
	"""
	global target_pose
	global marker_sub
	global glo_pos_x
	global glo_pos_y
	global marker_x
	global marker_y
	global detected
	
	try:
		if data.markers[0].id == 50:
			# to get the position of the tag
			print("x-position ", data.markers[0].pose.pose.position.x, "y-postion", data.markers[0].pose.pose.position.y)
			print("global-x ",glo_pos_x, "global-y", glo_pos_y )
			marker_x = data.markers[0].pose.pose.position.x
			marker_y = data.markers[0].pose.pose.position.y
			# set the new target pose
			target_pose.pose.position.x = glo_pos_x - marker_y-0.2
			target_pose.pose.position.y = glo_pos_y - marker_x-0.2
			detected = 1	
	except:
		pass
		
def glo_pos(data):
	"""
	callback for the local position
	it set the drone position to the global values
	"""
	global glo_pos_z
	global glo_pos_x
	global glo_pos_y
	glo_pos_z = data.pose.position.z
	glo_pos_x = data.pose.position.x
	glo_pos_y = data.pose.position.y 

if __name__ == '__main__':
	
	# position message
	target_pose = PoseStamped()
	target_pose.pose.position.x = 1.5
	target_pose.pose.position.y = 0
	target_pose.pose.position.z = 2.5

	# publisher, the target pose of the drone
	pub = rospy.Publisher('mavros/setpoint_position/local', PoseStamped, queue_size=10)
	# subscriber to the pose of the drone
	suby = rospy.Subscriber("/mavros/local_position/pose", PoseStamped, glo_pos)
	rospy.init_node('arming', anonymous=True)    # node initialization
	rate = rospy.Rate(100) # 100hz

	# Publish some set points before entering the offboard mode
	for i in range(100):
		pub.publish(target_pose)
		rate.sleep()
    
	# OFF board mode
	rospy.wait_for_service('/mavros/set_mode')  # block until service is available 
	mode_srv = rospy.ServiceProxy("/mavros/set_mode", SetMode)
	response = mode_srv.call(custom_mode="OFFBOARD")
	print("Offboard mode ", response)

	# Arming ON
	rospy.wait_for_service("mavros/cmd/arming")
	arming_srv = rospy.ServiceProxy("mavros/cmd/arming", CommandBool)
	arm_response = arming_srv.call(True)
	print("Arming ", arm_response.success)
	flagy = 0
	
	while not rospy.is_shutdown():
		# publishing target position
		pub.publish(target_pose)

		if (glo_pos_z >= 2.3 and flagy==0):	# if drone reached the target
			#	Subscriber to the marker
			marker_sub	= rospy.Subscriber("/ar_pose_marker", AlvarMarkers, landing)
			print("subscriber created")
			flagy=1
			
		# if marker is found and the drone is above it, start landing
		if (detected == 1 and -0.23<marker_x<-0.2 and -0.23<marker_y<-0.2):
			marker_sub.unregister()	# no longer need to know the position of the marker
			rospy.wait_for_service('/mavros/cmd/land')
			try:
				landService = rospy.ServiceProxy('/mavros/cmd/land', CommandTOL)
				isLanding = landService(altitude = 0, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
			except rospy.ServiceException, e:
				print "service land call failed"
