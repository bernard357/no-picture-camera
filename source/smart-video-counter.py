#
# uses OpenCV to analyse images captured by Raspberry Pi camera
# then pushes counters every 2 seconds to some Unix Domain Socket
#

from picamera.array import PiRGBArray
from picamera import PiCamera
from imutils.object_detection import non_max_suppression
import time
import datetime
import cv2
import numpy as np
import imutils
import logging
import config

# uncomment only one
#
logging.basicConfig(format='%(message)s', level=logging.INFO)
#logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

# load camera configuration
#
try:
    settings = config.camera

except:
    settings = {}

# send counters to Unix Domain Socket
#
import uds

# use Raspberry Pi Camera
#
camera = PiCamera()
camera.resolution = (320,240)
rawCapture = PiRGBArray(camera, size=(320,240))
time.sleep(0.1)

camera.capture(rawCapture, format="bgr")
image = rawCapture.array
prev = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
clone = np.zeros_like(prev)
rawCapture.truncate(0)

# initialise model for human faces
#
face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_alt.xml')

# initialise model for standing humans
#
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# compute counters every 2 seconds
#
flagone = datetime.datetime.now()
while True:

    flagtwo = datetime.datetime.now()
    elapsed = (flagtwo - flagone).total_seconds()

    if elapsed < 2:
        time.sleep(0.1)
        continue
    flagone = datetime.datetime.now()

    people_count = 0
    people_moves = 0
    people_faces = 0

    # capture an image
    #
    mask = np.zeros(image.shape[:2], dtype = "uint8")
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rawCapture.truncate(0)

    # detect human faces
    #
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    people_faces = len(faces)

    # detect human beings
    #
    (rects, weights) = hog.detectMultiScale(image,
                                            winStride=(4,4),
                                            padding=(8,8),
                                            scale=1.07)
    rects = np.array([[x, y, x+w, y+h] for (x,y,w,h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
    people_count = len(pick)

    # count moving people
    #
    nextim = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    nextim = cv2.bitwise_and(nextim, nextim, mask=mask)
    flow = cv2.calcOpticalFlowFarneback(prev, nextim, 0.5, 1, 15, 3, 5, 1.2, 0)
    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    mag = mag*0.8
    prev = nextim

    for(xA, yA,xB, yB) in pick:
        try:
            m = np.median(mag[yA:yB,xA:xB])
            if m > 1.6:
                people_moves += 1
        except RuntimeWarning:
            pass

    # push counters via Unix Domain Socket
    #
    message = "%s %d %d %d" % (settings.get('id', 'myCamera'),
                               people_count,
                               people_moves,
                               people_faces)
    uds.push(message)

    # provide feedback on screen (requires VNC access)
    #
#    for(xA, yA, xB, yB) in pick:
#        cv2.rectangle(mask, (xA,yA), (xB,yB), 255, -1)
#        cv2.rectangle(gray, (xA,yA), (xB,yB), 255, 2)
#    cv2.imshow("image", gray)
#    if cv2.waitKey(1) & 0xFF == ord('q'):
#        break
