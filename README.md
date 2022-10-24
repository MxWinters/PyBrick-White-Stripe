# PyBricks Software For White Stripe

Pybricks software for using the PoweredUp Remote with the Technic hub. This has been written for use with my combat robot White Stripe but can be used on any model that has 2 or 4 wheel skid steering such as tanks, robots or perhaps the LEGO Technic 42140 Transformation Vehicle set.

# Version 1:
This verison has 3 different control modes, Stand-by Mode, Run Mode and Dance Mode. Stand-by Mode disables the remote's button to prevent movement of the robot when handling or not in use. Run mode which allow one to drive the robot as normal. Dance Mode spins the robot around on the spot, left button spins left, right button spins right, then press the same button to stop it spinning. 

Switching between modes is done with the centre green button on the remote.

While in Run Mode, the hub continuously checks the orientation and if it detects that the robot is up-side-down, which motor is powered and its rotation direction are both inverted so that forward on the remote remains drive forward, left remains turn left.

# Version 2
Functionally, Version 2 acts similar to Version 1 but is a more advanced version with 4 different control modes, Stand-by Mode, Run Mode (slow acceleration), Run Mode (fast acceleration) and Dance Mode.
The version uses the .run() function to control the motors instead of .dc(). This allow for better control of the motors and ensures both motors spin at the same speed, allows for adjustable motor acceleration/deceleration and the use of the .control.stalled() function to detect when the motor is stalled, it then cuts the power to the motors to prevent any hub cutout issues mid-fight/battle.

# Install

Simply download to your device, open <Version 1/main.py> or <Version 2/main.py> with the PyBricks app or PyBricks website with Chrome, configure it as per below and then flash the code to the Technic Hub in the normal way.

# Configuration

Set which Controller Mode you want the hub to start with in the Set Startup Controller Mode section, then set the user definable settings in the "User Definable Variables" section (detailed info on each setting is included in the comments next to each setting in the main.py file).

# Bugs / Issues

Should you have any issue with it, send me a message on Facebook or submit an issue on the Issues tab on GitHub and Ill look into it. 
My Facebook page is: https://www.facebook.com/MxWintersAFOL

# Contributions

Being an open source project, if you have any changes/bug fixes/improvements, feel free to fork this repo and submit a pull request. I welcome any contributions to this project.

# Copyright / Licence

The project has been published under the MIT licence, you are free to download, run, edit and/or publish derivatives of this software but the top copyright notice MUST remain. See LICENCE file for more information.

This software contains code taken from Tcm0 and their 42140 PyBricks code which was released under the same MIT licence as this project. I have credited them in my code and have clearly specified which lines that were copied from their code.
Please see: https://github.com/Tcm0/PybricksRemoteLayouts
