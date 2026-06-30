import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
from launch_ros.actions import Node

def generate_launch_description():

    # ==========================================================
    # 1. RUTAS Y ARCHIVOS
    # ==========================================================
    pkg_description = get_package_share_directory('easybot_description')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    # Obtener ruta al mundo personalizado
    pkg_easybot_launch = get_package_share_directory('easybot_launch')
    world_file = os.path.join(pkg_easybot_launch, 'worlds', 'easybot.world')

    # Ruta al archivo principal Xacro
    xacro_file = os.path.join(pkg_description, 'urdf', 'easybot.urdf.xacro')

    # Usamos ParameterValue para forzar que ROS 2 lea el XML resultante como un simple texto (String)
    robot_description = {
        'robot_description': ParameterValue(Command(['xacro ', xacro_file]), value_type=str)
    }

    # ==========================================================
    # 2. NODOS PRINCIPALES
    # ==========================================================
    
    # Nodo Robot State Publisher: Publica las TFs y usa el tiempo de simulación
    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description, {'use_sim_time': True}]
    )

    # Lanzador de Ignition Gazebo: Iniciamos un mundo vacío por defecto
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': f'-r {world_file}'}.items()
    )

    # Nodo Spawner: Toma el 'robot_description' y lo inyecta en Gazebo
    # Añadimos una ligera altura en Z para que el robot "caiga" y no quede atascado en el piso
    spawn_node = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'easybot',
            '-topic', 'robot_description',
            '-z', '0.1'
        ],
        output='screen'
    )

    # ==========================================================
    # 3. EL PUENTE (ROS <-> IGNITION)
    # ==========================================================
    # Este nodo traduce los mensajes entre el simulador y ROS 2.
    # Sintaxis: /topico@tipo_ros[tipo_ignition
    # ] = De ROS a Ignition (Ej: comandos de velocidad)
    # [ = De Ignition a ROS (Ej: sensores y odometría)
    
    bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            # Reloj de simulación
            '/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock',
            # Comandos de movimiento
            '/cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist',
            # Odometría del Skid-Steer
            '/odom@nav_msgs/msg/Odometry[ignition.msgs.Odometry',
            # Transformaciones (TF)
            '/tf@tf2_msgs/msg/TFMessage[ignition.msgs.Pose_V',
            # Datos del Lidar
            '/scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan',
            # ESTA ES LA LÍNEA NUEVA: Puente para los ángulos de las ruedas
            '/joint_states@sensor_msgs/msg/JointState[ignition.msgs.Model'
        ],
        output='screen'
    )


    # ==========================================================
    # 4. VISUALIZACIÓN EN RVIZ2
    # ==========================================================
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        parameters=[{'use_sim_time': True}],  # <--- ESTA LÍNEA ES LA CLAVE para la sincronizacion de los datos
        arguments=['-d', os.path.join(pkg_description, 'rviz', 'default.rviz')]
    )

    # ==========================================================
    # 5. RETORNAR LA DESCRIPCIÓN
    # ==========================================================
    return LaunchDescription([
        rsp_node,
        gazebo_launch,
        spawn_node,
        bridge_node,
        rviz_node
    ])