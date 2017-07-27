#!/usr/bin/env python

# KUKA API for ROS

# Marhc 2016 Saeid Mokaram  saeid.mokaram@gmail.com
# Sheffield Robotics    http://www.sheffieldrobotics.ac.uk/
# The university of sheffield   http://www.sheffield.ac.uk/

# This script generats a ROS node for comunicating with KUKA iiwa
# Dependencies: conf.txt, ROS server, Rospy, KUKA iiwa java SDK, KUKA iiwa robot.

#######################################################################################################################
from client_lib import *
from paint import paint
import time


######################################################################################################################
if __name__ == '__main__':
    global stableFT

    my_client = kuka_iiwa_ros_client()   # Making a connection object.l

    while (not my_client.isready): pass    # Wait until iiwa is connected zzz!

    if my_client.OperationMode[0] != 'T1':
        print 'The robot is in', my_client.OperationMode[0], 'mode.'
        print 'This demo is safe to work at T1 modes only.'
        exit()

    print 'Started'

    # Initializing Tool 1
    my_client.send_command('setTool tool1')

    lines = paint()

    import matplotlib.pyplot as plt
    for aa in lines:
        plt.plot([x[0] for x in aa], [x[1] for x in aa], '.-')
    #plt.show()

    print lines

    # Go to start position
    my_client.send_command('setPosition 0 52.59 0 -54.53 0 72.86 0')
    while (not my_client.isReadyToMove): pass
    #while Dist.euclidean(my_client.JointPosition[0], [0, 49.43, 0, -48.5, 0, 82.08, 0]) > 0.5: pass  # this is in radians

    if len(lines):
        for line in lines:
            #while (not my_client.isReadyToMove[0]): pass

            # Go start of a line
            my_client.send_command('setPositionXYZABC ' + str(line[0][0]) + ' ' + str(line[0][1]) + ' 180 -180 0 -180 ptp')

            my_client.send_command('setCartImpCtrl 5000 5000 10 300 300 300 1')
            my_client.send_command('setJointAcceleration 0.4')
            my_client.send_command('setJointVelocity 0.2')
            my_client.send_command('setCartVelocity 100')
            # Go down
            my_client.send_command('setPositionXYZABC ' + str(line[0][0]) + ' ' + str(line[0][1]) + ' 176 -180 0 -180 ptp')

            #my_client.send_command('resetCartImpCtrl')
            my_client.send_command('setJointAcceleration 1.0')
            my_client.send_command('setJointVelocity 1.0')
            my_client.send_command('setCartVelocity 1000')
            for point in line:
                # Plot
                my_client.send_command('setPositionXYZABC ' + str(point[0]) + ' ' + str(point[1]) + ' 176 -180 0 -180 lin')

            my_client.send_command('setCartImpCtrl 5000 5000 5000 300 300 300 1')
            # Go up
            my_client.send_command('setPositionXYZABC ' + str(line[-1][0]) + ' ' + str(line[-1][1]) + ' 180 -180 0 -180 ptp')

        # Go to start position
        my_client.send_command('setPosition 0 49.65 0 -49.26 0 81.08 0')

## MAIN #
