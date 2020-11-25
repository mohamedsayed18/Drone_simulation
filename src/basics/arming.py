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

if __name__ == '__main__':

    # position message
    target_pose = PoseStamped()
    target_pose.pose.position.x = 0
    target_pose.pose.position.y = 0
    target_pose.pose.position.z = 2

    pub = rospy.Publisher('mavros/setpoint_position/local', PoseStamped, queue_size=10)  # publisher
    rospy.init_node('arming', anonymous=True)    # regulator node
    rate = rospy.Rate(15) # 10hz

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

    while not rospy.is_shutdown():
    # publishing 
        pub.publish(target_pose)


