# Drone_simulation
Drone simulation using ROS, Gazebo and PX4

Drone landing on an AR marker

## Using this repo

Add the package to your work space and `catkin_make`.

Don't forget to set the environment variables

### Launch the simulation world

`roslaunch basics AR_detect.launch`

### Run the node

`rosrun basics arming.py`

Make sure this file is executable `chmod +x arming.py` 

## Environment variables

```
px4_dir=~/Firmware
source /opt/ros/noetic/setup.bash
source ~/drone_ws/devel/setup.bash
source $px4_dir/Tools/setup_gazebo.bash $px4_dir $px4_dir/build/px4_sitl_default
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$px4_dir
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$px4_dir/Tools/sitl_gazebo
export GAZEBO_PLUGIN_PATH=$GAZEBO_PLUGIN_PATH:/usr/lib/x86_64-linux-gnu/gazebo-11/plugins
```
