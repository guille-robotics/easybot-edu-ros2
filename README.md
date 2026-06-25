# 🤖 easybot-edu-ros2

¡Bienvenido a **easybot-edu-ros2**! Este repositorio es la "Easy Way" (la forma más fácil) de levantar, visualizar y simular un robot móvil en ROS 2. 

Está diseñado con un enfoque educativo, ideal para dar los primeros pasos en la robótica móvil, aprender sobre transformaciones (TF), URDF y simulaciones físicas sin lidiar con configuraciones complejas.

## 📦 Estructura del Repositorio

Este proyecto se compone de dos paquetes principales:

* **`easybot_description`**: Contiene el modelo físico del robot (URDF generado de forma sencilla), las mallas 3D y las configuraciones visuales predeterminadas de RViz2.
* **`easybot_launch`**: Es el orquestador del proyecto. Contiene los scripts de lanzamiento (`launch files`) para levantar los nodos de estado del robot y los visualizadores con un solo comando.

## ⚙️ Requisitos Previos

* **Sistema Operativo:** Ubuntu 22.04
* **ROS 2:** Humble Hawksbill
* **Dependencias de ROS 2:** `xacro`, `joint_state_publisher_gui`, `robot_state_publisher`, `rviz2`

## 🚀 Instalación (The Easy Way)

Sigue estos pasos para clonar y compilar el repositorio en tu propio espacio de trabajo:

1. Crea un espacio de trabajo (si no tienes uno) y navega a la carpeta `src`:
   ```bash
   mkdir -p ~/easybot_ws/src
   cd ~/easybot_ws/src