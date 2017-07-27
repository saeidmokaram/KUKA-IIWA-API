import cv, gtk
import thread
import time

########################################################################
def play_sign():
    global run
    global vidFile #F, nFrames, waitPerFrameInMillisec]

    while run:
        tmp = vidFile
        for f in xrange( tmp[1] ):
            frameImg = cv.QueryFrame( tmp[0] )

            size = cv.GetSize(frameImg)
            thumbnail = cv.CreateImage((size[0]*gtk.gdk.screen_height()/size[1], gtk.gdk.screen_height() ), frameImg.depth, frameImg.nChannels)
            cv.Resize(frameImg, thumbnail)
            cv.ShowImage("Press esc to close", thumbnail)
            cv.ResizeWindow("Press esc to close", size[0]*gtk.gdk.screen_height()/size[1], gtk.gdk.screen_height())
            #cv.MoveWindow("My Video Window", 0, 0)
            ch = 0xFF & cv.WaitKey(tmp[2])
            if ch == 27:
                run=False
                break
            if tmp != vidFile:
                break
        cv.SetCaptureProperty(vidFile[0], cv.CV_CAP_PROP_POS_FRAMES, 0)
    cv.DestroyWindow( "Press esc to close" )

########################################################################
def OpenMove(file):
    F = cv.CaptureFromFile(file)
    nFrames = int(cv.GetCaptureProperty(F, cv.CV_CAP_PROP_FRAME_COUNT))
    fps = cv.GetCaptureProperty(F, cv.CV_CAP_PROP_FPS)
    waitPerFrameInMillisec = int(1 / fps * 1000 / 1)

    return [F, nFrames, waitPerFrameInMillisec]
########################################################################



########################################################################
File1 = OpenMove('mp4/001_Cobot_General.mp4')
File2 = OpenMove('mp4/002_Direction_of_Movement.mp4')
File3 = OpenMove('mp4/003_Speed.mp4')
File4 = OpenMove('mp4/004_Reach.mp4')
File5 = OpenMove('mp4/005_Force.mp4')
File6 = OpenMove('mp4/006_Touch.mp4')
File7 = OpenMove('mp4/007_Touch_+_Force.mp4')
File9 = OpenMove('mp4/009_No_Touch.mp4')

try:
    run = True
    vidFile = File1
    thread.start_new_thread(play_sign, ())
except:
    print "Error: unable to start SignShow thread"

while run:
    vidFile = File1
    time.sleep(3)
    vidFile = File2
    time.sleep(3)
    vidFile = File3
    time.sleep(3)
    vidFile = File4
    time.sleep(3)
    vidFile = File5
    time.sleep(3)
    vidFile = File6
    time.sleep(3)
    vidFile = File7
    time.sleep(3)
    vidFile = File9
    time.sleep(3)