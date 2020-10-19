import cv2
import numpy as np

frameWidth = 980

frameHeight = 780
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

myColors = [[130,144, 0,  179,  232,255],
            [49,191,0, 96,  255,  245],
            [108,132, 84, 142,  255, 255]]

myColorValues = [[0, 0, 255],
                 [0, 215, 0],
                 [234, 0, 0]]

myPoints = [] #x, y, colorVal

def findColors(img, myColors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    count = 0

    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])

        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)

        if x != 0 and y != 0:
            newPoints.append([img.shape[1] - x, y, count])

        count += 1

    return newPoints


def getContours(img):
    x, y, w, h = 0, 0, 0, 0
    countours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in countours:
        area = cv2.contourArea(cnt)

        if area > 100:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)

    return x+w//2, y


def drawPoints(myPoints):
    for point in myPoints:
        print(point)
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)

while True:
    success, img = cap.read()
    imgResult = cv2.flip(img, 1)
    newPoints = findColors(img, myColors, myColorValues)

    if len(newPoints) != 0:
        for newPoint in newPoints:
            myPoints.append(newPoint)

    if len(myPoints) != 0:
        drawPoints(myPoints)

    # imgMask = cv2.cvtColor(imgMask, cv2.COLOR_GRAY2BGR)
    # imgHor = np.hstack((img, imgMask))
    cv2.imshow("Virtual Paint", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break