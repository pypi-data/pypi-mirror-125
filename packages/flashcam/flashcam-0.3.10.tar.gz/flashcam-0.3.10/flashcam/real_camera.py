import cv2
from flashcam.base_camera2 import BaseCamera

from flashcam.usbcheck import recommend_video
# import base_camera  #  Switches: slowrate....

import datetime
import time
import socket

import glob

import subprocess as sp
import numpy as np

import flashcam.config as config

from  flashcam.stream_enhancer import Stream_Enhancer

class Camera(BaseCamera):
    video_source = 0

    @staticmethod
    def init_cam(  ):
        """
        should return videocapture device
        but also sould set Camerare.video_source
        """

        # ----------------------------
        #    we need to get in into the thread.....
        #  NOT NOW - all is taken from BaseCam
        # def __init__(self, target_frame = "direct" , average = 0, blur = 0 , threshold = 0):


        res = "640x480"
        print("D... init_cam caleld with:", res )
        print("i... init_cam caleld with:", res )
        #print("\n\ni... IS  is ALREADY init ?????????:",  config.CONFIG["camera_on"],"\n\n\n")

        #if config.CONFIG["camera_on"]:
        #    print("i... init_cam is ALREADY ON:" )
        #    return cap


        vids = recommend_video( config.CONFIG["recommended"]  )
        if len(vids)>0:
            vidnum = vids[0]
            cap = cv2.VideoCapture(vidnum,  cv2.CAP_V4L2)

            # config.CONFIG["camera_on"] = True

            # - with C270 - it showed corrupt jpeg
            # - it allowed to use try: except: and not stuck@!!!
            #cap = cv2.VideoCapture(vidnum)
            #   70% stucks even with timeout
            pixelformat = "MJPG"
            w,h =  int(res.split("x")[0]), int(res.split("x")[1])
            fourcc = cv2.VideoWriter_fourcc(*pixelformat)
            cap.set(cv2.CAP_PROP_FOURCC, fourcc)
            cap.set(cv2
                    .CAP_PROP_FRAME_WIDTH,   w )
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT,  h )
            return cap
        return None


    @staticmethod
    def frames( ):
        """
        vidnum = number; res 640x480;
        recommended= ... uses the recommend_video to restart the same cam
        """
        # print("i... staticmethod frames @ real -  enterred; target_frame==", target_frame)
        senh = Stream_Enhancer()

        camera = Camera(  )
        cap = camera.init_cam(  )

        nfrm = 0
        if config.CONFIG["recommended"]:
            wname = "none "
        else:
            wname = config.CONFIG["recommended"]

        # -----------get parameters for DetMot, same for web as for all
        target_frame = config.CONFIG['target_frame']
        average      = config.CONFIG['average']
        threshold    = config.CONFIG['threshold']
        blur         = config.CONFIG['blur']
        timelaps     = config.CONFIG['timelaps']
        histogram    = config.CONFIG['histogram']

        frame_prev = None
        while True:

            timeoutok = False
            ret = False
            frame = None
            if (cap is None) or (not cap.isOpened()):
                print("X... camera None or not Opened(real)")
                ret = False
            else:
                try: #----this catches errors of libjpeg with cv2.CAP_V4L2
                    print(f"i... frame {nfrm:8d}   ", end="\r" )
                    ret, frame = cap.read()
                    BaseCamera.nframes+=1

                    #wname = f"res {frame.shape[1]}x{frame.shape[0]}"
                    nfrm+=1
                    #print(f"D... got frame (frames iter)   ret={ret}  {frame.shape}")
                except Exception as ex:
                    print("D... SOME OTHER EXCEPTION ON RECV...", ex)
                    config.CONFIG["camera_on"] = False


            if not ret:
                time.sleep(0.5)
                #vids = recommend_video(recommended) # try to re-init the same video
                #if len(vids)>0:
                #    vidnum = vids[0]
                config.CONFIG["camera_on"] = False

                cap = Camera.init_cam( )
                nfrm = 0

                # create gray + moving lines BUT prev_frame is bad sometimes
                try:
                    print("D... trying to gray frame")
                    frame = cv2.cvtColor(frame_prev, cv2.COLOR_BGR2GRAY)
                    height, width = frame.shape[0] , frame.shape[1]

                    skip = 10
                    startl = 2*(nfrm % skip) # moving lines
                    for il in range(startl,height,skip):
                        x1, y1 = 0, il
                        x2, y2 = width, il
                        #image = np.ones((height, width)) * 255
                        line_thickness = 1
                        cv2.line(frame, (x1, y1), (x2, y2), (111, 111, 111),
                                 thickness=line_thickness)
                except:
                    print("X... prev_frame was bad, no gray image")

            #print("D... ret==", ret)
            if ret:
                frame_prev = frame
                if senh.add_frame(frame):  # it is a proper image....

                    # EARLIER  timelaps = config.CONFIG['timelaps']

                    # ----------  I need to calculate histogram before labels...


                    if histogram: # just calculate a number on plain frame
                        hmean = senh.histo_mean( )

                    #--------------- now apply labels ------i cannot get rid in DETM---
                    #--------- all this will be on all rames histo,detect,direct,delta
                    senh.setbox(" ", senh.TIME)
                    if target_frame in ["detect","delta","histo"]:
                        senh.setbox(f"DISP {target_frame}",senh.DISP)
                    if average>0:
                        senh.setbox(f"acc {average}",  senh.avg)
                    if blur>0:
                        senh.setbox(f"blr  {blur}",  senh.blr)
                    if threshold>0:
                        senh.setbox(f"trh  {threshold}",  senh.trh)
                    if timelaps>0:
                        senh.setbox(f"laps {timelaps}",  senh.lap)
                    if histogram:
                        senh.setbox(f"his {hmean:.0f}",  senh.hist)


                    # ----  for detmo ---- work with detect motion--------------------
                    if (threshold>0) :
                        senh.setbox("MODE DM", senh.MODE) #---push UP to avoid DetMot
                        senh.detmo( average, blur)
                        senh.chk_threshold( threshold )
                        if senh.motion_detected:
                            # print("D... sav mot", senh.motion_detected)
                            senh.save_avi( seconds = -1, name = "dm" )
                    else:
                        senh.setaccum( average  )
                        senh.setblur( blur )
                        #senh.setbox("MODE  ", senh.MODE)

                    # ---draw histogram
                    if target_frame == "histo":
                        senh.histo( )

                    if timelaps>0:
                        senh.save_avi( seconds = timelaps )


                    #------------yield the resulting frame-----------------------------
                    if target_frame in ["detect","delta","histo"]:
                        frame = senh.get_frame(  typ = target_frame)
                    else:
                        frame = senh.get_frame(  )

            yield frame



    @staticmethod
    def set_video_source(source):

        print("D... set_video_source: source=", source)
        camera = cv2.VideoCapture( source,  cv2.CAP_V4L2)
        print("D... ",camera)
        print("D... setting MJPG writer....FMP4 works too")
        # camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('F','M','P','4'))
        print("D... first camera read ....")
        ok = False
        try:
            _, img = camera.read()
            print(img.size) # this can fail and reset to DEV 0
            ok = True
        except Exception as ex:
            print("X... CAMERA read ... FAILED",ex)

        if ok:
            return camera
        return None
