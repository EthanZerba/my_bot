import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessStart

from launch_ros.actions import Node


def generate_launch_description():

    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name='my_bot' #<--- CHANGE ME


    Slam_toolbox = Node(
    package='slam_toolbox',
    executable='/usr/bin/python3',
    arguments=['/opt/ros/foxy/share/slam_toolbox/launch/online_async_launch.py'],
    parameters=[{'params_file': './src/my_bot/config/mapper_params_online_async.yaml', 'use_sim_time': False}],
    remappings=[('/odom', '/rtabmap/odom')]
)

    twist_mux = Node(
        package='twist_mux',
        executable='twist_mux',
        arguments=['--ros-args', '--params-file', './src/my_bot/config/twist_mux.yaml', '-r', 'cmd_vel_out:=diff_cont/cmd_vel_unstamped']
    )

    Rtabmap = Node(
    package='rtabmap_ros',
    executable='rtabmap',
    output='screen',
    parameters=[{
        'RGBD/Enabled': 'false',
        'subscribe_depth': False,
        'rgb/camera_info_topic': '/camera_info',
        'queue_size': 10,
        'subscribe_scan': True,
        'rgb/image_topic': '/image_raw', # modify this line to subscribe to the /image_raw topic
        'Mem/STMSize': '2048', # optional, adjust the memory size as needed
        'Mem/UseOdomFeatures': 'True', # optional, enable odometry features for better loop closure detection
        'Mem/IncrementalMemory': 'True', # optional, enable incremental loop closure detection
        'Mem/InitWMWithAllNodes': 'True', # optional, initialize the word map with all nodes for better localization
    }],
    remappings=[
        ('/image_raw', '/rgb/image'),
        ('/camera_info', '/rgb/camera_info')
    ]
)







    return LaunchDescription([
        Slam_toolbox,
        twist_mux,
        Rtabmap,
    ])
