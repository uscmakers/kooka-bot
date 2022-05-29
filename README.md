# kooka-bot

Run GUI with "python exe.py" from the "gui" directory.

![image](https://user-images.githubusercontent.com/77693398/170552111-343891e5-4f75-439f-8e20-cb78d92801e8.png)

First thing to do is connect the 3 stepper joints to the proper USB ports (one port per joint due to having one arduino per stepper motor).
Once USB ports are entered, user should press "connect". Upon success, the maximum joint velocity can be specified in the "Vel (deg/sec)" field.

Now the robot is ready to be controlled:

To the right is a view where the robot arm is visualized in yellow. Sliders for the different joints can be manipulated to move the arm. 
The future orientation post-movement is visualized in red so user can see expected result of motion.
After moving sliders as desired, the user can press "command", and the arm will move all joints at once to end the motion of all joints at the same instant.

"Stir" can be pressed to execute a stirring motion with the robot.

![image](https://user-images.githubusercontent.com/77693398/170552668-d8d80b9c-8c39-4724-ae2c-c5bff58a46c8.png)


