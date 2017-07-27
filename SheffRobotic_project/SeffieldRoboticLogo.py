#!/usr/bin/env python

# KUKA API for ROS

# Marhc 2016 Saeid Mokaram  saeid.mokaram@gmail.com
# Sheffield Robotics    http://www.sheffieldrobotics.ac.uk/
# The university of sheffield   http://www.sheffield.ac.uk/

# This script generats a ROS node for comunicating with KUKA iiwa
# Dependencies: conf.txt, ROS server, Rospy, KUKA iiwa java SDK, KUKA iiwa robot.

#######################################################################################################################
from client_lib import *
import time


def FastSpeed(my_client):
    my_client.send_command('setJointAcceleration 1.0')
    my_client.send_command('setJointVelocity 1.0')
    my_client.send_command('setCartVelocity 300')

def SlowSpeed(my_client):
    my_client.send_command('setJointAcceleration 1.0')
    my_client.send_command('setJointVelocity 1.0')
    my_client.send_command('setCartVelocity 30')

def PaintSpeed(my_client):
    my_client.send_command('setJointAcceleration 1.0')
    my_client.send_command('setJointVelocity 1.0')
    my_client.send_command('setCartVelocity 150')


######################################################################################################################
if __name__ == '__main__':

    my_client = kuka_iiwa_ros_client()   # Making a connection object.

    while (not my_client.isready): pass    # Wait until iiwa is connected zzz!

    if my_client.OperationMode[0] == 'T1':
        print 'Hello Sheffield Robotics!'
    else:
        print 'The robot is in', my_client.OperationMode[0], 'mode.'
        print 'This demo works at T1 mode only.'
        exit()


    FastSpeed(my_client)
    # Go to start position
    my_client.send_command('setPosition 0 25.14 0 -99.27 0 55.56 0')
    time.sleep(0.1)

    my_client.send_command('setTool tool2')
    X = 700.0
    Y = -100.0
    x = 0.4
    y = 0.4

    time.sleep(0.1)

    Zdown = 0
    Zup = 20


    # Go start of a line
    my_client.send_command('setPositionXYZABC ' + str(X-(20*x)) + ' ' + str(Y+(-100*y)) + ' ' + str(Zup) + ' -180 0 -180 lin')
    time.sleep(0.1)


    # Go down
    SlowSpeed(my_client)
    my_client.send_command('setCartImpCtrl 5000 5000 100 300 300 300 1')
    my_client.send_command('setPositionXYZABC - - ' + str(Zdown) + ' - - - lin')

    PaintSpeed(my_client)

    [y1, x1] = [Y+(-10*y), X-(20*x)]
    my_client.send_command('setPositionXYZABC ' + str(x1) + ' ' + str(y1) + ' - - - - lin')

    [y1, x1, y2, x2] = [Y+(15*y), X-(28*x), Y+(20*y), X-(30*x)]
    my_client.send_command('MoveCirc ' + str(x1) + ' ' + str(y1) + ' ' + str(Zdown) + ' -180 0 -180 ' + str(x2) + ' ' + str(y2) + ' ' + str(Zdown) + ' -180 0 -180 0.00')  # MoveCirc motion move with CartVelocity

    [y1, x1] = [Y + (145 * y), X - (210 * x)]
    my_client.send_command('setPositionXYZABC ' + str(x1) + ' ' + str(y1) + ' - - - - lin')

    [y1, x1, y2, x2] = [Y + (165 * y), X - (225 * x), Y + (185 * y), X - (210 * x)]
    my_client.send_command('MoveCirc ' + str(x1) + ' ' + str(y1) + ' ' + str(Zdown) + ' -180 0 -180 ' + str(x2) + ' ' + str(y2) + ' ' + str(Zdown) + ' -180 0 -180 0.00')  # MoveCirc motion move with CartVelocity

    [y1, x1] = [Y + (305 * y), X - (20 * x)]
    my_client.send_command('setPositionXYZABC ' + str(x1) + ' ' + str(y1) + ' - - - - lin')

    [y1, x1, y2, x2] = [Y + (340 * y), X - (20 * x), Y + (365 * y), X - (40 * x)]
    my_client.send_command('MoveCirc ' + str(x1) + ' ' + str(y1) + ' ' + str(Zdown) + ' -180 0 -180 ' + str(x2) + ' ' + str(y2) + ' ' + str(Zdown) + ' -180 0 -180 0.00')  # MoveCirc motion move with CartVelocity

    [y1, x1] = [Y + (405 * y), X - (235 * x)]
    my_client.send_command('setPositionXYZABC ' + str(x1) + ' ' + str(y1) + ' - - - - lin')

    [y1, x1, y2, x2] = [Y + (415 * y), X - (260 * x), Y + (445 * y), X - (270 * x)]
    my_client.send_command('MoveCirc ' + str(x1) + ' ' + str(y1) + ' ' + str(Zdown) + ' -180 0 -180 ' + str(x2) + ' ' + str(y2) + ' ' + str(Zdown) + ' -180 0 -180 0.00')  # MoveCirc motion move with CartVelocity

    [y1, x1] = [Y + (590 * y), X - (270 * x)]
    my_client.send_command('setPositionXYZABC ' + str(x1) + ' ' + str(y1) + ' - - - - lin')

    [y1, x1, y2, x2] = [Y + (615 * y), X - (260 * x), Y + (630 * y), X - (225 * x)]
    my_client.send_command('MoveCirc ' + str(x1) + ' ' + str(y1) + ' ' + str(Zdown) + ' -180 0 -180 ' + str(x2) + ' ' + str(y2) + ' ' + str(Zdown) + ' -180 0 -180 0.00')  # MoveCirc motion move with CartVelocity

    [y1, x1] = [Y + (655 * y), X - (45 * x)]
    my_client.send_command('setPositionXYZABC ' + str(x1) + ' ' + str(y1) + ' - - - - lin')

    [y1, x1, y2, x2] = [Y + (665 * y), X - (30 * x), Y + (690 * y), X - (20 * x)]
    my_client.send_command('MoveCirc ' + str(x1) + ' ' + str(y1) + ' ' + str(Zdown) + ' -180 0 -180 ' + str(x2) + ' ' + str(y2) + ' ' + str(Zdown) + ' -180 0 -180 0.00')  # MoveCirc motion move with CartVelocity

    [y1, x1] = [Y + (750 * y), X - (20 * x)]
    my_client.send_command('setPositionXYZABC ' + str(x1) + ' ' + str(y1) + ' - - - - lin')

    #######################################################################################
    my_client.send_command('resetCartImpCtrl')
    FastSpeed(my_client)
    # Go up
    my_client.send_command('setPositionXYZABC - - ' + str(Zup) + ' - - - lin')
    # Go start of a line
    [y1, x1] = [Y + (80 * y), X - (270 * x)]
    my_client.send_command('setPositionXYZABC ' + str(x1) + ' ' + str(y1) + ' - - - - lin')
    #######################################################################################
    my_client.send_command('setCartImpCtrl 5000 5000 100 300 300 300 1')
    SlowSpeed(my_client)
    # Go down
    my_client.send_command('setPositionXYZABC - - ' + str(Zdown) + ' - - - lin')

    PaintSpeed(my_client)

    #######################################################################################
    [y1, x1] = [Y + (245 * y), X - (270 * x)]
    my_client.send_command('setPositionXYZABC ' + str(x1) + ' ' + str(y1) + ' - - - - lin')

    [y1, x1, y2, x2] = [Y + (275 * y), X - (280 * x), Y + (285 * y), X - (310 * x)]
    my_client.send_command('MoveCirc ' + str(x1) + ' ' + str(y1) + ' ' + str(Zdown) + ' -180 0 -180 ' + str(x2) + ' ' + str(y2) + ' ' + str(Zdown) + ' -180 0 -180 0.00')  # MoveCirc motion move with CartVelocity

    [y1, x1] = [Y + (285 * y), X - (405 * x)]
    my_client.send_command('setPositionXYZABC ' + str(x1) + ' ' + str(y1) + ' - - - - lin')

    [y1, x1, y2, x2] = [Y + (275 * y), X - (435 * x), Y + (245 * y), X - (445 * x)]
    my_client.send_command('MoveCirc ' + str(x1) + ' ' + str(y1) + ' ' + str(Zdown) + ' -180 0 -180 ' + str(x2) + ' ' + str(y2) + ' ' + str(Zdown) + ' -180 0 -180 0.00')  # MoveCirc motion move with CartVelocity

    [y1, x1] = [Y + (80 * y), X - (445 * x)]
    my_client.send_command('setPositionXYZABC ' + str(x1) + ' ' + str(y1) + ' - - - - lin')

    [y1, x1, y2, x2] = [Y + (50 * y), X - (435 * x), Y + (40 * y), X - (405 * x)]
    my_client.send_command('MoveCirc ' + str(x1) + ' ' + str(y1) + ' ' + str(Zdown) + ' -180 0 -180 ' + str(x2) + ' ' + str(y2) + ' ' + str(Zdown) + ' -180 0 -180 0.00')  # MoveCirc motion move with CartVelocity

    [y1, x1] = [Y + (40 * y), X - (310 * x)]
    my_client.send_command('setPositionXYZABC ' + str(x1) + ' ' + str(y1) + ' - - - - lin')

    [y1, x1, y2, x2] = [Y + (50 * y), X - (280 * x), Y + (80 * y), X - (270 * x)]
    my_client.send_command('MoveCirc ' + str(x1) + ' ' + str(y1) + ' ' + str(Zdown) + ' -180 0 -180 ' + str(x2) + ' ' + str(y2) + ' ' + str(Zdown) + ' -180 0 -180 0.00')  # MoveCirc motion move with CartVelocity
    #######################################################################################
    my_client.send_command('resetCartImpCtrl')
    FastSpeed(my_client)
    # Go up
    my_client.send_command('setPositionXYZABC - - ' + str(Zup) + ' - - - lin')
    # Go start of a line
    [y1, x1] = [Y + (510 * y), X - (320 * x)]
    my_client.send_command('setPositionXYZABC ' + str(x1) + ' ' + str(y1) + ' - - - - lin')
    #######################################################################################
    my_client.send_command('setCartImpCtrl 5000 5000 100 300 300 300 1')
    SlowSpeed(my_client)
    # Go down
    my_client.send_command('setPositionXYZABC - - ' + str(Zdown) + ' - - - lin')

    PaintSpeed(my_client)

    #######################################################################################
    [y1, x1, y2, x2] = [Y + (635 * y), X - (445 * x), Y + (510 * y), X - (570 * x)]
    my_client.send_command('MoveCirc ' + str(x1) + ' ' + str(y1) + ' ' + str(Zdown) + ' -180 0 -180 ' + str(x2) + ' ' + str(y2) + ' ' + str(Zdown) + ' -180 0 -180 0.00')  # MoveCirc motion move with CartVelocity

    [y1, x1, y2, x2] = [Y + (390 * y), X - (445 * x), Y + (510 * y), X - (320 * x)]
    my_client.send_command('MoveCirc ' + str(x1) + ' ' + str(y1) + ' ' + str(Zdown) + ' -180 0 -180 ' + str(x2) + ' ' + str(y2) + ' ' + str(Zdown) + ' -180 0 -180 0.00')  # MoveCirc motion move with CartVelocity




    my_client.send_command('resetCartImpCtrl')
    FastSpeed(my_client)
    # Go up
    my_client.send_command('setPositionXYZABC - - ' + str(Zup) + ' - - - lin')

    # Go to start position
    my_client.send_command('setPosition 0 25.14 0 -99.27 0 55.56 0')

## MAIN #
