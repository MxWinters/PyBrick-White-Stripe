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
print("White Stripe Combat Robot - Version 2.0")
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
old_drive_motor1_speed = 0
old_drive_motor2_speed = 0
drive_motor1_speed = 0
drive_motor2_speed = 0
stalled_counter = 0

# User Definable Variables
#remote switch debounce time
switch_debounce_time = 150
#set motor port and direction
drive1 = Motor(Port.A, Direction.CLOCKWISE)
drive2 = Motor(Port.B, Direction.COUNTERCLOCKWISE)
#motor control limits
motor_max_speed = 1500
motor_mode_2_acceleration = 5000
motor_mode_3_acceleration = 15000
motor_torque = 260


# Update Console
hub.light.on(Color.GREEN)
remote.light.on(Color.GREEN)
print("Setup Complete...")
print("Battery voltage: " + str(hub.battery.voltage()) + "mV...")
print("Battery current: " + str(hub.battery.current()) + "mA...")
wait(1000)
print("System Ready\n")


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
    elif controllerMode == 3 and hubOrientation == Side.TOP: # This line taken and modified from Tcm0's 42140 code
        hub.light.on(Color.YELLOW)
        remote.light.on(Color.YELLOW)
    elif controllerMode == 3 and hubOrientation == Side.BOTTOM: # This line taken and modified from Tcm0's 42140 code
        hub.light.on(Color.VIOLET)
        remote.light.on(Color.VIOLET)
    elif controllerMode == 4:
        hub.light.on(Color.BLUE)
        remote.light.on(Color.BLUE)

# Emergency Stop 
#stop the motors and flashes hub and remote leds red/blue 5 times
def EmergencyStop():
    drive_motor1_speed = 0
    drive_motor2_speed = 0
    drive1.stop()
    drive2.stop()
    for x in range (0, 5):
        hub.light.on(Color.RED)
        remote.light.on(Color.BLUE)
        wait(150)
        hub.light.on(Color.BLUE)
        remote.light.on(Color.RED)
        wait(150)
    SetLEDs()

# Set Motor Control Limits
def SetControlLimits():
    drive1.stop()
    drive2.stop()
    if controllerMode == 2:
        drive1.control.limits(motor_max_speed, motor_mode_2_acceleration, motor_torque)
        drive2.control.limits(motor_max_speed, motor_mode_2_acceleration, motor_torque)
    elif controllerMode == 3:
        drive1.control.limits(motor_max_speed, motor_mode_3_acceleration, motor_torque)
        drive2.control.limits(motor_max_speed, motor_mode_3_acceleration, motor_torque)


### Main Loop Function ###
while True:
    #check which buttons are pressed
    pressed = remote.buttons.pressed()
    #check hub orientation
    hubOrientation = hub.imu.up() # This line taken from Tcm0's 42140 code
    #set hub/remote LEDs
    SetLEDs()
    
    ### Entering Controller Mode 1 - Stand By Mode
    #executed when entering controllerMode 1
    #here to stop the motors being powered while holding when entering into standby mode
    if controllerMode == 1:
        drive_motor1_speed = 0
        drive_motor2_speed = 0
        drive1.stop()
        drive2.stop()

    ### Entering Controller Mode 2 - Run Mode
    #executed when entering controllerMode 2
    if controllerMode == 2:
        #you can add commands here if you wish something to happen when entering controllerMode 2
        #this currently passed and does nothing. Remove or comment out pass below if you add code here
        pass

    ### Drive Motors
    # Remote Left +/- Buttons
    #pressing the left +/- buttons on the remote activates with left side motor
    #which motor and its rotation direction is dependent on the hub/robot orientation
    #first we select the speed and direction of the motor
    if controllerMode == 2 or controllerMode == 3:
        if hubOrientation == Side.TOP: # This line taken from Tcm0's 42140 code
            if Button.LEFT_PLUS in pressed:
                drive_motor1_speed = motor_max_speed
            elif Button.LEFT_MINUS in pressed:
                drive_motor1_speed = -motor_max_speed         
            else:
                drive_motor1_speed = 0
        elif hubOrientation == Side.BOTTOM: # This line taken from Tcm0's 42140 code
            if Button.LEFT_PLUS in pressed:
                drive_motor2_speed = -motor_max_speed
            elif Button.LEFT_MINUS in pressed:
                drive_motor2_speed = motor_max_speed            
            else:
                drive_motor2_speed = 0

    # Remote right +/- Buttons
    #pressing the right +/- buttons on the remote activates with right side motor
    #which motor and its rotation direction is dependent on the hub/robot orientation
    #first we select the speed and direction of the motor
    if controllerMode == 2 or controllerMode == 3:
        if hubOrientation == Side.TOP: # This line taken from Tcm0's 42140 code
            if Button.RIGHT_PLUS in pressed:
                drive_motor2_speed = motor_max_speed
            elif Button.RIGHT_MINUS in pressed:
                drive_motor2_speed = -motor_max_speed            
            else:
                drive_motor2_speed = 0
        elif hubOrientation == Side.BOTTOM: # This line taken from Tcm0's 42140 code
            if Button.RIGHT_PLUS in pressed:
                drive_motor1_speed = -motor_max_speed
            elif Button.RIGHT_MINUS in pressed:
                drive_motor1_speed = motor_max_speed            
            else:
                drive_motor1_speed = 0
    
    ### Apply Selected Speed
    #split to allow mode 2 to stop motor
    if controllerMode == 2:
        if drive_motor1_speed != 0:
            drive1.run(drive_motor1_speed)
        else:
            drive1.stop()
        if drive_motor2_speed != 0:
            drive2.run(drive_motor2_speed)
        else:
            drive2.stop()
    #and mode 3 to hold motor
    elif controllerMode == 3:
        if drive_motor1_speed == 0:
            drive1.hold()
        else:
            drive1.run(drive_motor1_speed)
        if drive_motor2_speed == 0:
            drive2.hold()
        else:
            drive2.run(drive_motor2_speed)

    
    ### Drive Motor 1 Emergency Stop
    #executed when drive1 motor is stalled, cuts power to motor but only after stall_counter 
    #reaches 50 to prevent it randomly activating
    #un/comment the line below to enable emergency stop in control mode 2 only
    if drive1.control.stalled() == True and controllerMode == 2:
    #un/comment the line below to enable emergency stop in control mode 3
    #if drive1.control.stalled() == True and controllerMode == 2 and controllerMode == 3:
        if stalled_counter == 50:
            stalled_counter = 0
        else:
            stalled_counter = stalled_counter + 1

    ### Drive Motor 2 Emergency Stop
    #executed when drive2 motor is stalled, cuts power to motor but only after stall_counter 
    #reaches 50 to prevent it randomly activating
    #un/comment the line below to enable emergency stop in control mode 2 only
    if drive1.control.stalled() == True and controllerMode == 2:
    #un/comment the line below to enable emergency stop in control mode 3
    #if drive1.control.stalled() == True and controllerMode == 2 and controllerMode == 3:
        if stalled_counter == 50:
            stalled_counter = 0
            EmergencyStop()
        else:
            stalled_counter = stalled_counter + 1

    ### Controller Mode 3 - Dance Mode
    #executed when entering controllerMode 3
    if controllerMode == 3:
        #you can add commands here if you wish something to happen when entering controllerMode 3
        #this currently passed and does nothing. Remove or comment out pass below if you add code here
        pass

    ### Dance - Spin Left
    #dance mode spins the bot left on the spot when the red stop button is pressed
    #press red stop button again to stop the robot from dancing
    if Button.LEFT in pressed and controllerMode == 4:
        danceMode = True
        wait(500)
        while (danceMode == True):
            pressed = remote.buttons.pressed()
            drive1.dc(-100)
            drive2.dc(100)
            if Button.LEFT in pressed:
                danceMode = False
                drive1.dc(0)
                drive2.dc(0)
                hub.light.on(Color.RED)
                remote.light.on(Color.RED)
                wait(1000)      
            wait(switch_debounce_time)
        
    ### Dance - Spin Right
    #dance mode spins the bot right on the spot when the red stop button is pressed
    #press red stop button again to stop the robot from dancing
    if Button.RIGHT in pressed and controllerMode == 4:
        danceMode = True
        wait(500)
        while (danceMode == True):
            pressed = remote.buttons.pressed()
            drive1.dc(100)
            drive2.dc(-100)
            if Button.RIGHT in pressed:
                danceMode = False
                drive1.dc(0)
                drive2.dc(0)
                hub.light.on(Color.RED)
                remote.light.on(Color.RED)
                wait(1000)
            wait(switch_debounce_time)
   
    ### Mode Selector - Centre Green button
    #mode 1 - standby mode
    #mode 2 - run/fight mode
    #mode 3 - dance mode
    if Button.CENTER in pressed:
        if controllerMode == 1:
            controllerMode = 2
            SetLEDs()
            SetControlLimits()
            print("Controller mode 2 - Run Mode (slow motor acceleration)")         
        elif controllerMode == 2:
            controllerMode = 3
            SetLEDs()
            SetControlLimits()
            print("Controller mode 3 - Run Mode (fast motor acceleration)")
        elif controllerMode == 3:
            controllerMode = 4
            SetLEDs()
            print("Controller mode 4 - Dance Mode")
        elif controllerMode == 4:
            controllerMode = 1
            SetLEDs()
            print("Controller mode 1 - Stand-By Mode")
        wait(switch_debounce_time)

    # Wait For 10 Millisecond Before Repeating Loop
    wait(10)
