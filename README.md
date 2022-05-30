# kooka-bot
Kookabot is a 4 degree-of-freedom (DOF) robotic manipulator designed to assist humans in cooking activities such as stirring and chopping food.

## Overview
This project is designed to develop a manipulator-based robotic system that can be used as a cooking assistant robot. The project objective focused on enabling a robot to mimic a human's stirring motions, and it required working on different subsystems in mechanical, electrical, and software areas. This repository provides a system software that was developed to enable rapid prototyping and testing of the robot hardware. The core functionalities of the software are: interative graphical user interface (GUI) for users, computer vision, motion planning, motor controls. Details regarding software workflow and codes can be found [here](scripts/). Also, [here](https://www.youtube.com/watch?v=a38A9QeRUQw) is a vido that shows the progress and work involved in developing the Kookabot.

## Grapical User Interface (GUI)

<img width="842" alt="guidiagram" src="https://user-images.githubusercontent.com/42167077/170895252-ad72d4ab-f7a7-4f58-a7d4-d1ed52a96300.png">

The purpose of the GUI shown above is to provide users with intuitive understanding of the robot's status and options for different controls modes needed to test the robot's various features. The GUI can be broken down into 8 modules as shown above, and the purpose of each module is explained in a corresponding below:

1. Joint position control module: This module accepts joint position commands for all of the robot's joints. Based on the commands the robot receives, the module displays the amount of angle each joint has to move.
2. USB connection module: In order to carry out the commands in the physical robot hardware, the software needs to establish communication with Arduino microcontrollers that controls the motors embedded in the robot hardware. This module receives the USB port numbers of the microcontrollers used in this project.
3. Visualizaton module: Testing of the robot's motions required verifying that the mathematical computation done in software and real hardware match almost perfectly. To do so, a visualization module was created to show a 3D rendering that estimates all of the robot's links' positions.
4. Terminal: Terminal outputs throws necessary error messages in case the user has not provided parameters needed to enable the robot's particular feature.
5. Execution button for a whole stirring action: Upon clicking this button, the robot will carry out the entire process of localizing a pot, generating stirring trajectories, and execute motions of following the generated trajectories.
6. Different buttons: There are different buttons embedded in this GUI needed to provide users with different control modes. Details regarding each button can be found [here](scripts/).
7. Goal assignment slots: The slots accept x, y, z position commands that the robot's end effector must reach.
8. Robot's trajectory parameter slots: There are different parameters that the users must provide to the GUI to generate cooking motions of the robot. Along with details of the software work flow and different buttons, details of the parameters is provided [here](scripts/).

## Accomplished Tasks
1. The robot is fully assembled.
2. The robot is fully capable of planning and executing circular trajectories needed to generate stirring motions.
3. The robot is capable of detecting a pot and its location using a camera.

## Future Work
1. The computer vision's capability to detect different foods can be expanded to cook different foods.
2. Different trajectory planning schemes can be designed to mimic different cooking motions.

## Contributors
* Anokhi Kholwadwala (mechanical)
* Grace True (mechanical)
* Isaac Gerstmann (software)
* Matt Liberson (electrical & software)
* Misha Kuznetsov (mechanical)
* Sam Jeon (software)
* Spencer Lin (software)
* Will Stewart (software)
