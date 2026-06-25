import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():

    # 1. Obtener los directorios de instalación de ambos paquetes
    pkg_easybot_launch = get_package_share_directory('easybot_launch')
    pkg_easybot_teleop = get_package_share_directory('easybot_teleop')

    # 2. Definir las rutas exactas a los archivos launch que ya creaste
    gazebo_launch_path = os.path.join(pkg_easybot_launch, 'launch', 'gazebo.launch.py')
    joystick_launch_path = os.path.join(pkg_easybot_teleop, 'launch', 'joystick.launch.py')

    # 3. Preparar la inclusión de la simulación base (Gazebo + URDF + Bridge)
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch_path)
    )

    # 4. Preparar la inclusión del control por Bluetooth (Joy + Teleop)
    joystick_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(joystick_launch_path)
    )

    # 5. Ejecutar todo simultáneamente
    return LaunchDescription([
        gazebo_launch,
        joystick_launch
    ])