#!/usr/bin/env python

# KUKA API for ROS

# Jan 2017 Saeid Mokaram  saeid.mokaram@gmail.com
# Sheffield Robotics    http://www.sheffieldrobotics.ac.uk/
# The university of sheffield   http://www.sheffield.ac.uk/

# This script generats a ROS node for comunicating with KUKA iiwa
# Dependencies: client_lib, time, scipy, KUKA iiwa 7-14 robot.

#######################################################################################################################
from client_lib import *
import time
import scipy.spatial.distance as Dist
#######################################################################################################################
def MaxT1Speed(my_client):
    my_client.send_command('setJointAcceleration 1.0')
    my_client.send_command('setJointVelocity 1.0')
    my_client.send_command('setJointJerk 1.0')
    my_client.send_command('setCartVelocity 1000')

def MaxT2Speed(my_client):
    my_client.send_command('setJointAcceleration 0.1')
    my_client.send_command('setJointVelocity 0.9')
    my_client.send_command('setJointJerk 0.1')
    my_client.send_command('setCartVelocity 1000')


def goToStart(client):  # Go to start position
    global stableFT

    # Initializing Tool 1
    my_client.send_command('setTool tool1')

    if my_client.OperationMode[0] == 'T1':
        MaxT1Speed(my_client)
        print 'T1'
    elif my_client.OperationMode[0] == 'T2':
        MaxT2Speed(my_client)
        print 'T2'
    else:
        print 'The robot is in', my_client.OperationMode[0], 'mode.'
        print 'This demo is safe to work at T1 or T2 modes only.'
        exit()

    client.send_command('setPosition 0 49.65 0 -49.26 0 81.08 0')
    while Dist.euclidean(client.JointPosition[0], [0, 49.65, 0, -49.26, 0, 81.08, 0]) > 0.5: pass  # this is in radians

    client.send_command('setPositionXYZABC 700 0 310 -180 0 -180 ptp')
    while Dist.euclidean(client.ToolPosition[0][0:3], [700, 0, 310]) > 10: pass
    print client.ToolPosition[0][0:3], [700, 0, 310]
    time.sleep(0.5)
    print 'In home possition'

    stableFT = client.ToolForce[0]
    while (Dist.cosine(stableFT, client.ToolForce[0]) < 0.2): pass

    client.send_command('setCompliance 10 10 5000 300 300 300')  # Compliance ON
##########################

##########################
class tube:
    def __init__(self, x, y, ref, id):
        self.x = x + ref[0]
        self.y = y + ref[1]
        self.id = id

    def isInMyRange(self, client):
        if Dist.euclidean(client.ToolPosition[0][0:3], [self.x, self.y, 320]) < 30:
            print '-->', self.id
            print 'End pos =', client.ToolPosition[0][0:3]
            print 'Tube pos =', [self.x, self.y, 320]
            print 'dist = ', Dist.euclidean(client.ToolPosition[0][0:3], [self.x, self.y, 320])
            return True
        else:
            return False

    def Pick(self, client):
        global stableFT
        print 'Picking the tube'
        client.send_command('resetCompliance')  # Compliance OFF
        time.sleep(1)
        client.send_command(
            'setPositionXYZABC ' + str(self.x) + ' ' + str(self.y) + ' 320 -180 0 -180 ptp')  # Stic to the tube
        time.sleep(0.5)
        stableFT = client.ToolForce[0]
        time.sleep(0.5)
        ####################################################
        t1 = time.time()
        while (time.time() - t1 < 1):  # Can change mind within 3s
            time.sleep(0.1)
            if (Dist.cosine(stableFT, client.ToolForce[0]) > 0.2):
                client.send_command('setCompliance 10 10 5000 300 300 300')  # Compliance On
                time.sleep(1)  # Have time to move out of the tube zone
                print 'User aborted!'
                return
        # Desidion has been made
        print 'Desidion has been made'
        ####################################################
        client.send_command('resetCompliance')  # Compliance OFF
        time.sleep(0.1)
        client.send_command(
            'setPositionXYZABC ' + str(self.x) + ' ' + str(self.y) + ' 320 -180 0 -180 ptp')  # Stic to the tube
        time.sleep(0.1)
        client.send_command('setPositionXYZABC ' + str(self.x) + ' ' + str(self.y) + ' 160 -180 0 -180 lin')  # Go down
        time.sleep(0.1)
        stableFT = client.ToolForce[0]
        client.send_command(
            'setPositionXYZABC ' + str(self.x) + ' ' + str(self.y) + ' 320 -180 0 -180 lin')  # Pick the bolt up
        time.sleep(0.1)
        goToStart(client)  # move bac to home and wait zzz
##########################

## MAIN #
######################################################################################################################
if __name__ == '__main__':
    global stableFT

    ref = [400, -225]
    Tubes = [tube(0, 0, ref, 11),    tube(0, 150, ref, 12),   tube(0, 300, ref, 13),   tube(0, 450, ref, 14),
             tube(50, 75, ref, 21),  tube(50, 225, ref, 22),  tube(50, 375, ref, 23),
             tube(100, 0, ref, 31),  tube(100, 150, ref, 32), tube(100, 300, ref, 33), tube(100, 450, ref, 34),
             tube(150, 75, ref, 21), tube(150, 225, ref, 22), tube(150, 375, ref, 23),
             tube(200, 0, ref, 41),  tube(200, 150, ref, 42), tube(200, 300, ref, 43), tube(200, 450, ref, 44)]

    ##########################
    my_client = kuka_iiwa_ros_client()  # Making a connection object.
    while (not my_client.isready): pass  # Wait until iiwa is connected zzz!
    print 'Started'

    while True:

        goToStart(my_client)
        ##########################

        while True:
            for tu in Tubes:
                if tu.isInMyRange(my_client):
                    tu.Pick(my_client)
            time.sleep(0.1)

## MAIN #
