import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    # 1. Obtener el directorio de instalación de easybot_description
    pkg_description = get_package_share_directory('easybot_description')

    # 2. Construir la ruta completa al archivo URDF descargado de tu web
    urdf_file = os.path.join(pkg_description, 'urdf', 'easybot.urdf')

    # 3. Leer el contenido del URDF para pasarlo como parámetro
    with open(urdf_file, 'r') as infp:
        robot_description_content = infp.read()

    # 4. Configurar el nodo Robot State Publisher (esencial para las TFs)
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_content}]
    )

    # 5. Configurar el nodo Joint State Publisher con GUI (crea los sliders para las ruedas)
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )

    # 6. Configurar el nodo de RViz2 para la visualización 3D
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', os.path.join(pkg_description, 'rviz', 'default.rviz')]
    )

    # 7. Retornar la descripción del lanzamiento con todos los nodos
    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node
    ])