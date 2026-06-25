import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    
    # 1. Obtener la ruta del archivo de configuración YAML que acabamos de crear
    pkg_teleop = get_package_share_directory('easybot_teleop')
    config_filepath = os.path.join(pkg_teleop, 'config', 'joystick.yaml')

    # 2. Nodo 'joy': Lee el control por Bluetooth/USB y publica en el tópico /joy
    joy_node = Node(
        package='joy',
        executable='joy_node',
        name='joy_node',
        parameters=[{
            'deadzone': 0.05,        # Ignora movimientos mínimos (útil si la palanca está un poco suelta)
            'autorepeat_rate': 20.0  # Frecuencia de publicación (20 Hz) para un control fluido
        }]
    )

    # 3. Nodo 'teleop_twist_joy': Traduce los botones a comandos de velocidad (/cmd_vel)
    teleop_node = Node(
        package='teleop_twist_joy',
        executable='teleop_node',
        name='teleop_twist_joy_node',
        parameters=[config_filepath],
        # Si en el futuro tu controlador de motores usa otro tópico, lo cambias aquí:
        remappings=[('/cmd_vel', '/cmd_vel')] 
    )

    # 4. Retornar ambos nodos para que se ejecuten simultáneamente
    return LaunchDescription([
        joy_node,
        teleop_node
    ])