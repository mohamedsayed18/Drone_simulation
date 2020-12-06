#!/usr/bin/env python
"""
change the mode of the flight and set arming on
Before entering Offboard mode, you must have already started streaming setpoints.
 Otherwise the mode switch will be rejected.
"""

# libraries and messages 
import rospy
from mavros_msgs.srv import SetMode
from mavros_msgs.srv import CommandBool
from geometry_msgs.msg import PoseStamped
from ar_track_alvar_msgs.msg import AlvarMarkers
from mavros_msgs.msg import PositionTarget
from nav_msgs.msg import Odometry
from mavros_msgs.srv import CommandTOL

glo_pos_z = 0
glo_pos_x = 0
glo_pos_y = 0
marker_x = 0
marker_y = 0
detected = 0

def landing(data):
	global target_pose
	global marker_sub
	global glo_pos_x
	global glo_pos_y
	global marker_x
	global marker_y
	global detected
	#print("landing callback")
	#rospy.loginfo(len(data.markers))
	#print (data)
	try:
		if data.markers[0].id == 50:
			### to get the position of the tag
			print("x-position ", data.markers[0].pose.pose.position.x, "y-postion", data.markers[0].pose.pose.position.y)
			print("global-x ",glo_pos_x, "global-y", glo_pos_y )
			marker_x = data.markers[0].pose.pose.position.x
			marker_y = data.markers[0].pose.pose.position.y
			target_pose.pose.position.x = glo_pos_x - marker_y-0.2
			target_pose.pose.position.y = glo_pos_y - marker_x-0.2
			detected = 1
			#marker_sub.unregister()
			
	except:
		pass
		
"""
		while(glo_pos_x <= target_pose.pose.position.x and glo_pos_y <= target_pose.pose.position.y):
			pub.publish(target_pose)
			rate.sleep()

		print("ended the while")
		marker_sub.unregister()
		rospy.wait_for_service('/mavros/cmd/land')
   		try:
			landService = rospy.ServiceProxy('/mavros/cmd/land', CommandTOL)
			#http://wiki.ros.org/mavros/CustomModes for custom modes
			isLanding = landService(altitude = 0, latitude = 0.8, longitude = 0.8, min_pitch = 0, yaw = 0)
		except rospy.ServiceException, e:
			print "service land call failed: %s. The vehicle cannot land "%e
			rospy.loginfo("detected")		
"""
def glo_pos(data):
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
	
	"""
	target_pose.pose.position.x = .3
	target_pose.pose.position.y = 0.3
	target_pose.pose.position.z = 2
	"""
	pub = rospy.Publisher('mavros/setpoint_position/local', PoseStamped, queue_size=10)  # publisher
	#pub = rospy.Publisher('/mavros/setpoint_raw/local', PositionTarget, queue_size=10)  # publisher
	#marker_sub	= rospy.Subscriber("/ar_pose_marker", AlvarMarkers, landing) #subscriber
	suby = rospy.Subscriber("/mavros/local_position/pose", PoseStamped, glo_pos) #subscriber
	rospy.init_node('arming', anonymous=True)    # regulator node
	rate = rospy.Rate(100) # 10hz

	for i in range(100):
		pub.publish(target_pose)
		rate.sleep()
	print("done setting")
    
	# OFF board mode
	rospy.wait_for_service('/mavros/set_mode')  # block until service is available 
	mode_srv = rospy.ServiceProxy("/mavros/set_mode", SetMode)
	response = mode_srv.call(custom_mode="OFFBOARD")
	print(response)

	# Arming ON
	rospy.wait_for_service("mavros/cmd/arming")
	arming_srv = rospy.ServiceProxy("mavros/cmd/arming", CommandBool)
	arm_response = arming_srv.call(True)
	print(arm_response)
	flagy = 0
	
	while not rospy.is_shutdown():
		# publishing 
		pub.publish(target_pose)

		if (glo_pos_z >= 1.9 and flagy==0):
			marker_sub	= rospy.Subscriber("/ar_pose_marker", AlvarMarkers, landing) #subscriber
			#suby.unregister()
			print("subscriber created")
			flagy=1
			#marker_sub	= rospy.Subscriber("/ar_pose_marker", AlvarMarkers, landing) #subscriber
		if (detected == 1 and -0.23<marker_x<-0.2 and -0.23<marker_y<-0.2):
			marker_sub.unregister()
			rospy.wait_for_service('/mavros/cmd/land')
			try:
				landService = rospy.ServiceProxy('/mavros/cmd/land', CommandTOL)
				#http://wiki.ros.org/mavros/CustomModes for custom modes
				isLanding = landService(altitude = 0, latitude = 0.8, longitude = 0.8, min_pitch = 0, yaw = 0)
			except rospy.ServiceException, e:
				print "service land call failed: %s. The vehicle cannot land "%e
