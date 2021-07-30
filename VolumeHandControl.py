import math
import time
from ctypes import cast, POINTER

import cv2
import numpy as np
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import HandsTracking as htm

wCam, hCam = 640, 480

pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
cap.set(2, wCam)
cap.set(3, hCam)
detector = htm.handDetector(detectionCon=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None
)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
volume.SetMasterVolumeLevel(0, None)
minVol = volRange[0]
maxVol = volRange[1]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 7, (68, 255, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 7, (68, 255, 0), cv2.FILLED)
        cv2.circle(img, (cx, cy), 7, (68, 255, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (0, 213, 255), 3)

        # change volume
        length = math.hypot(x2 - x1, y2 - y1)
        vol = np.interp(length, [15, 150], [minVol, maxVol])
        volBar = np.interp(length, [15, 150], [400, 150])
        volPer = np.interp(length, [15, 150], [0, 100])
        volume.SetMasterVolumeLevel(vol, None)

        # show volume range
        cv2.rectangle(img, (50, 150), (85, 400), (0, 124, 25), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)

    # Display FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    # cv2.putText(img, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

    cv2.imshow("Control", img)
    cv2.waitKey(1)
