# Drone_simulation
Drone simulation using ROS, Gazebo and PX4

# Using this repo

Add the package to your work space and `catkin_make`

## Launch the Iris_fpv_model

`roslaunch basics mylaunch.launch`

to show images in rviz

open rviz by typing `rviz`

then Add->By topic->/image_raw/image

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
