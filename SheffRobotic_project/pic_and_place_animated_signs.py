#!/usr/bin/env python

# KUKA API for ROS

# Marhc 2016 Saeid Mokaram  saeid.mokaram@gmail.com
# Sheffield Robotics    http://www.sheffieldrobotics.ac.uk/
# The university of sheffield   http://www.sheffield.ac.uk/

# This script generats a ROS node for comunicating with KUKA iiwa
# Dependencies: conf.txt, ROS server, Rospy, KUKA iiwa java SDK, KUKA iiwa robot.

#######################################################################################################################
import time
import scipy.spatial.distance as Dist
import numpy as np

from client_lib import *

import gtk
import cv2.cv as cv
import thread

##########################
def goToStart(client): # Go to start position
    global stableFT
    
    my_sign.NoTouch()

    # Initializing Tool 1
    my_client.send_command('setTool tool1')
    
    client.send_command('setJointAcceleration 0.1')
    client.send_command('setJointVelocity 1.0')
    client.send_command('setJointJerk 0.1')
    my_client.send_command('setCartVelocity 100')
    
    client.send_command('setPosition 0 49.43 0 -48.5 0 82.08 0')
    while Dist.euclidean(client.JointPosition[0], np.deg2rad([0, 49.43, 0, -48.5, 0, 82.08, 0]) ) > 0.5 : pass # this is in radians
    #print client.JointPosition[0], np.deg2rad([0, 20, 0, -90, 0, 70, 0])

    client.send_command('setPositionXYZABC 700 0 290 -180 0 -180 ptp')
    while Dist.euclidean(client.ToolPosition[0][0:3], [700, 0, 290] ) > 10 : pass
    print client.ToolPosition[0][0:3], [700, 0, 290]
    time.sleep(0.5)
    print 'In home possition'
    my_sign.Touch()

    stableFT = client.ToolForce[0]
    while ( Dist.cosine(stableFT, client.ToolForce[0]) < 0.2 ) and not my_sign.newExp: pass

    if my_sign.newExp:
        client.send_command('resetCompliance')  # Compliance OFF
    else:
        client.send_command('setCompliance 10 10 5000 300 300 300') # Compliance ON
        my_sign.TouchForce()
##########################
class tube:
    def __init__(self, x, y, ref, id):
        self.x = x + ref[0]
        self.y = y + ref[1]
        self.id = id

    def isInMyRange(self, client):
        if Dist.euclidean(client.ToolPosition[0][0:3], [self.x, self.y, 290]) < 30:
            print '-->', self.id
            print 'End pos =', client.ToolPosition[0][0:3]
            print 'Tube pos =', [self.x, self.y, 290]
            print 'dist = ', Dist.euclidean(client.ToolPosition[0][0:3], [self.x, self.y, 290])
            return True
        else:
            return False

    def Pick(self, client):
        global stableFT
        print 'Picking the tube'
        client.send_command('resetCompliance')  # Compliance OFF
        my_sign.NoTouch()
        time.sleep(1)
        client.send_command('setPositionXYZABC '+str(self.x)+' '+str(self.y)+' 290 -180 0 -180 ptp') # Stic to the tube
        time.sleep(0.5)
        stableFT = client.ToolForce[0]
        time.sleep(0.5)
        ####################################################
        my_sign.Touch()
        t1 = time.time()
        while (time.time()-t1 < 2): # Can change mind within 3s
            time.sleep(0.1)
            if ( Dist.cosine(stableFT, client.ToolForce[0]) > 0.2 ) :
                client.send_command('setCompliance 10 10 5000 300 300 300') # Compliance On
                my_sign.TouchForce()
                time.sleep(1) # Have time to move out of the tube zone
                print 'User aborted!'
                return
        # Desidion has been made
        print 'Desidion has been made'
        ####################################################
        client.send_command('resetCompliance')  # Compliance OFF
        my_sign.NoTouch()
        time.sleep(0.1)
        client.send_command('setPositionXYZABC '+str(self.x)+' '+str(self.y)+' 290 -180 0 -180 lin') # Stic to the tube
        time.sleep(0.1)
        client.send_command('setPositionXYZABC '+str(self.x)+' '+str(self.y)+' 120 -180 0 -180 ptp') # Go down
        time.sleep(0.1)
        stableFT = client.ToolForce[0]
        client.send_command('setPositionXYZABC '+str(self.x)+' '+str(self.y)+' 290 -180 0 -180 ptp') # Pick the bolt up
        time.sleep(0.1)
        goToStart(client) # move bac to home and wait zzz
##########################
##########################
import matplotlib.pyplot as plt
import Image
from PIL import Image

class Sign:
    def __init__(self):

        self.run = True
        self.newExp = False
        self.SignLoading = self.OpenMove('signs/000_Loading_Screen.mp4')
        self.SignCobotGeneral = self.OpenMove('signs/001_Cobot_General.mp4')
        self.SignDirectionOfMovement = self.OpenMove('signs/002_Direction_of_Movement.mp4')
        self.SignSpeed = self.OpenMove('signs/003_Speed.mp4')
        self.SignReach = self.OpenMove('signs/004_Reach.mp4')
        self.SignForce = self.OpenMove('signs/005_Force.mp4')
        self.SignTouch = self.OpenMove('signs/006_Touch.mp4')
        self.SignTouchForce = self.OpenMove('signs/007_Touch_+_Force.mp4')
        self.SignNoTouch = self.OpenMove('signs/009_No_Touch.mp4')


        try:
            self.vidFile = self.SignLoading
            thread.start_new_thread(self.play_sign, ())
        except:
            print "Error: unable to start SignShow thread"
    
    ###################################
    def Loading(self):
        self.vidFile = self.SignLoading
        
    ###################################
    def CobotGeneral(self):
        self.vidFile = self.SignCobotGeneral

    ###################################
    def DirectionOfMovement(self):
        self.vidFile = self.SignDirectionOfMovement

    ###################################
    def Speed(self):
        self.vidFile = self.SignSpeed

    ###################################
    def Reach(self):
        self.vidFile = self.SignReach

    ###################################
    def Force(self):
        self.vidFile = self.SignForce

    ###################################
    def Touch(self):
        self.vidFile = self.SignTouch

    ###################################
    def TouchForce(self):
        self.vidFile = self.SignTouchForce

    ###################################
    def NoTouch(self):
        self.vidFile = self.SignNoTouch

    ###################################
    def play_sign(self):


        while self.run:
            tmp = self.vidFile # F, nFrames, waitPerFrameInMillisec]
            for f in xrange(tmp[1]):
                frameImg = cv.QueryFrame(tmp[0])

                size = cv.GetSize(frameImg)
                thumbnail = cv.CreateImage((size[0] * gtk.gdk.screen_height() / size[1], gtk.gdk.screen_height()),
                                           frameImg.depth, frameImg.nChannels)
                cv.Resize(frameImg, thumbnail)
                cv.ShowImage("Press esc to close", thumbnail)
                cv.ResizeWindow("Press esc to close", size[0] * gtk.gdk.screen_height() / size[1],
                                gtk.gdk.screen_height())
                # cv.MoveWindow("My Video Window", 0, 0)
                ch = 0xFF & cv.WaitKey(tmp[2])
                if ch == 27:
                    self.run = False
                    break
                if ch == 32:
                    self.newExp = True
                if tmp != self.vidFile:
                    break
            cv.SetCaptureProperty(self.vidFile[0], cv.CV_CAP_PROP_POS_FRAMES, 0)
        cv.DestroyWindow("Press esc to close")

    ###################################
    def OpenMove(self, file):
        F = cv.CaptureFromFile(file)
        nFrames = int(cv.GetCaptureProperty(F, cv.CV_CAP_PROP_FRAME_COUNT))
        fps = cv.GetCaptureProperty(F, cv.CV_CAP_PROP_FPS)
        waitPerFrameInMillisec = int(1 / fps * 1000 / 1)

        return [F, nFrames, waitPerFrameInMillisec]
    ###################################

##########################
##########################

## MAIN #
######################################################################################################################
if __name__ == '__main__':
    global stableFT
    global my_sign
    
    my_sign = Sign()

    ref = [400,-225]
    Tubes = [ tube(0,0,ref, 11), tube(0,150,ref, 12), tube(0,300,ref, 13), tube(0,450,ref, 14) ,
                    tube(50,75,ref, 21), tube(50,225,ref, 22), tube(50,375,ref, 23),
              tube(100,0,ref, 31), tube(100,150,ref, 32), tube(100,300,ref, 33), tube(100,450,ref, 34) ,
                    tube(150,75,ref, 21), tube(150,225,ref, 22), tube(150,375,ref, 23),
              tube(200,0,ref, 41), tube(200,150,ref, 42), tube(200,300,ref, 43), tube(200,450,ref, 44) ]

    ##########################
    my_client = kuka_iiwa_ros_client()   # Making a connection object.
    while (not my_client.isready): pass    # Wait until iiwa is connected zzz!
    print 'Started'


    while my_sign.run:
        my_sign.newExp = False

        my_sign.CobotGeneral()
        time.sleep(4)
        my_sign.DirectionOfMovement()
        time.sleep(4)
        my_sign.Speed()
        time.sleep(4)
        my_sign.Reach()
        time.sleep(4)
        my_sign.Force()
        time.sleep(4)


        goToStart(my_client)
        ##########################

        while not my_sign.newExp:
            for tu in Tubes:
                if tu.isInMyRange(my_client):
                    tu.Pick(my_client)
            time.sleep(0.1)

## MAIN #
