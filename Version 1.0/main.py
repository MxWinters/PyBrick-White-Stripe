### Copyright / Licence ###
####################################################################################
#
#MIT Licence
#
#Copyright (c) 2022 Morgan Winters
#Copyright (c) 2021 Tcm0
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
#
#
#This software contains code taken from Tcm0 and their 42140 PyBricks code 
#which was released under the same MIT licence as this code.
#Please see: https://github.com/Tcm0/PybricksRemoteLayouts

####################################################################################


### WHITE STRIPE ###


### Set Up ###
# Import Libraries 
from pybricks.pupdevices import *
from pybricks.parameters import *
from pybricks.hubs import TechnicHub
from pybricks.tools import wait

# Initialize the hub.
hub = TechnicHub()

# Connect to the remote.
remote = Remote()
#change the text inside the "" to set name on remote
#15 character limit 
remote.name("RemoteNameHere")

# Update Console & LED's
print("White Stripe Combat Robot - Version 1.0")
print("\nRunning Setup...")
hub.light.on(Color.RED)
remote.light.on(Color.RED)

# System Varibles
print("declaring variables...")
# Set Startup Controller Mode
#set the controller mode on startup to control mode 1, standby mode
controllerMode = 1
# Dance Mode
#this is used by the dance mode section to run/stop dance mode loop
danceMode = False
# Get orientation of hub
#either up side down or right side up. This is used to invert the controls when flipped
hubOrientation = hub.imu.up() # This line taken and modified from Tcm0's 42140 code


# Motor Varibles
#used by the code, no need to change these
drive_motor1_speed = 0
drive_motor2_speed = 0

# User Definable Variables
# set motor port and direction
drive1 = Motor(Port.A, Direction.CLOCKWISE)
drive2 = Motor(Port.B, Direction.COUNTERCLOCKWISE)

# Update Console & LED's
hub.light.on(Color.GREEN)
remote.light.on(Color.GREEN)
print("\nSetup Complete...")
print("\nBattery voltage: " + str(hub.battery.voltage()) + "mV...")
print("\nBattery current: " + str(hub.battery.current()) + "mA...")
wait(1000)
print("\nSystem Ready")


### System Functions ###
# Sets LED colour depending on if right side up or up-side-down
def SetLEDs():
    if controllerMode == 1:
        hub.light.on(Color.RED)
        remote.light.on(Color.RED)
    elif controllerMode == 2 and hubOrientation == Side.TOP: # This line taken and modified from Tcm0's 42140 code
        hub.light.on(Color.GREEN)
        remote.light.on(Color.GREEN)
    elif controllerMode == 2 and hubOrientation == Side.BOTTOM: # This line taken and modified from Tcm0's 42140 code
        hub.light.on(Color.MAGENTA)
        remote.light.on(Color.MAGENTA)
    elif controllerMode == 3:
        hub.light.on(Color.BLUE)
        remote.light.on(Color.BLUE)


### Main Loop Function ###
while True:
    #check which buttons are pressed
    pressed = remote.buttons.pressed()
    #check hub orientation
    hubOrientation = hub.imu.up() # This line taken and modified from Tcm0's 42140 code
    #set hub/remote LEDs
    SetLEDs()
    
    if controllerMode == 1:
        #mode 1 simply passes and does nothing
        #add commands here if you wish
        pass
    
    
    ### Drive Motors
    # Left Remote Button
    #which motor and its rotation direction is dependent on the hub/robot orientation
    #first we select the speed and direction of the motor
    if controllerMode == 2:
        if hubOrientation == Side.TOP: # This line taken and modified from Tcm0's 42140 code
            if Button.LEFT_PLUS in pressed:
                drive_motor1_speed = 100
            elif Button.LEFT_MINUS in pressed:
                drive_motor1_speed = -100            
            else:
                drive_motor1_speed = 0
        elif hubOrientation == Side.BOTTOM: # This line taken and modified from Tcm0's 42140 code
            if Button.LEFT_PLUS in pressed:
                drive_motor2_speed = -100
            elif Button.LEFT_MINUS in pressed:
                drive_motor2_speed = 100            
            else:
                drive_motor2_speed = 0

    # Right Remote Button
    #which motor and its rotation direction is dependent on the hub/robot orientation
    #first we select the speed and direction of the motor
    if controllerMode == 2:
        if hubOrientation == Side.TOP: # This line taken and modified from Tcm0's 42140 code
            if Button.RIGHT_PLUS in pressed:
                drive_motor2_speed = 100
            elif Button.RIGHT_MINUS in pressed:
                drive_motor2_speed = -100            
            else:
                drive_motor2_speed = 0
        elif hubOrientation == Side.BOTTOM: # This line taken and modified from Tcm0's 42140 code
            if Button.RIGHT_PLUS in pressed:
                drive_motor1_speed = -100
            elif Button.RIGHT_MINUS in pressed:
                drive_motor1_speed = 100            
            else:
                drive_motor1_speed = 0
    #then we apply the selected speed value to drive motors
    drive1.dc(drive_motor1_speed)
    drive2.dc(drive_motor2_speed)


    ### Dance - Spin Left
    #dance mode spins the bot left on the spot when the reed stop button is pressed
    #press red stop button again to stop the robot from dancing
    if Button.LEFT in pressed and controllerMode == 3:
        danceMode = True
        wait(500)
        while (danceMode == True):
            pressed = remote.buttons.pressed()
            if Button.LEFT in pressed:
                drive1.stop()
                drive2.stop()
                danceMode = False           
            drive1.dc(-100)
            drive2.dc(100)
            wait(250)
        
    ### Dance - Spin Right
    #dance mode spins the bot right on the spot when the reed stop button is pressed
    #press red stop button again to stop the robot from dancing
    if Button.RIGHT in pressed and controllerMode == 3:
        danceMode = True
        wait(500)
        while (danceMode == True):
            pressed = remote.buttons.pressed()
            if Button.RIGHT in pressed:
                drive1.dc(0)
                drive2.dc(0)
                danceMode = False      
            drive1.dc(100)
            drive2.dc(-100)
            wait(250)

    
    ### Mode Selector - Centre Green button
    #mode 1 - standby mode
    #mode 2 - run/fight mode
    #mode 3 - dance mode
    if Button.CENTER in pressed:
        if controllerMode == 1:
            controllerMode = 2
            SetLEDs()
            print("Controller mode 2")         
        elif controllerMode == 2:
            controllerMode = 3
            SetLEDs()
            print("Controller mode 3")
        elif controllerMode == 3:
            controllerMode = 1
            SetLEDs()
            print("Controller mode 1")
        wait(250)

    # Wait For 10 Millisecond Before Repeating Loop
    wait(10)
