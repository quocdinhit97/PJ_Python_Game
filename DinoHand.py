import time

import cv2
from pynput.keyboard import Key, Controller

import HandsTracking as handTrack

wCam, hCam = 640, 480

pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
detector = handTrack.handDetector(detectionCon=0.7)
tipIds = [4, 8, 12, 16, 20]
keyboard = Controller()

# Use right hand to play game
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    fingers = []
    if len(lmList) != 0:
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        total = fingers.count(1)
        print(total)
        if total == 0:
            keyboard.press(Key.down)
            keyboard.release(Key.down)
            time.sleep(0.05)
        elif total == 5:
            keyboard.press(Key.up)
            keyboard.release(Key.up)
            time.sleep(0.05)

    # Display FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

    cv2.imshow("Dino", img)
    cv2.waitKey(1)
