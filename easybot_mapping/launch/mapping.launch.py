import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # 1. Rutas
    pkg_easybot_mapping = get_package_share_directory('easybot_mapping')
    pkg_slam_toolbox = get_package_share_directory('slam_toolbox')

    config_file = os.path.join(pkg_easybot_mapping, 'config', 'mapper_params_online_async.yaml')

    # 2. Configurar el nodo de SLAM Toolbox llamando a su lanzador oficial
    slam_toolbox_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_slam_toolbox, 'launch', 'online_async_launch.py')
        ),
        launch_arguments={
            'slam_params_file': config_file,
            'use_sim_time': 'true'
        }.items()
    )

    # 3. Retornar la ejecución
    return LaunchDescription([
        slam_toolbox_launch
    ])