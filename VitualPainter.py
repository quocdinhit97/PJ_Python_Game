import os

import cv2
import numpy as np

import HandsTracking as handTrack

#########################################
folderImg = "img"
listImg = os.listdir(folderImg)
overlayList = []
color = (0, 0, 255)
brushThickness = 40
eraserThickness = 150
xp, yp = 0, 0
w, h = 1280, 720
##########################################

# Read image
for imgPath in listImg:
    image = cv2.imread(f'{folderImg}/{imgPath}')
    overlayList.append(image)


header = overlayList[0]
cap = cv2.VideoCapture(0)
cap.set(3, w)
cap.set(4, h)

detector = handTrack.handDetector(detectionCon=0.85)
canvas = np.zeros((720, 1280, 3), np.uint8)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Find hands
    img = detector.findHands(img, draw=False)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        fingers = detector.fingersUp()

        # Select menu
        if fingers[1] and fingers[2]:
            if y1 < 71:
                if 0 < x1 < 322:
                    header = overlayList[0]
                    color = (0, 0, 255)
                elif 325 < x1 < 640:
                    header = overlayList[1]
                    color = (0, 255, 0)
                elif 645 < x1 < 975:
                    header = overlayList[2]
                    color = (0, 255, 255)
                elif 980 < x1 < 1280:
                    header = overlayList[3]
                    color = (0, 0, 0)

        # Drawing
        if fingers[1] and fingers[2] == False:
            xp, yp = 0, 0
            cv2.circle(img, (x1, y1), 15, color, cv2.FILLED)
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if color == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), color, eraserThickness)
                cv2.line(canvas, (xp, yp), (x1, y1), color, eraserThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), color, brushThickness)
                cv2.line(canvas, (xp, yp), (x1, y1), color, brushThickness)

            xp, yp = x1, y1

    # Show draw
    imgGray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, imgInvert = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInvert = cv2.cvtColor(imgInvert, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInvert)
    img = cv2.bitwise_or(img, canvas)

    # Show header and video
    img[0:71, 0:1280] = header
    cv2.imshow("Paint", img)
    cv2.waitKey(1)