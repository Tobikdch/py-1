import cv2
import numpy as np
import Handtrackmod as htm
import time
# import autopy
import pyautogui

wCam, hCam = 1280, 720
frameR = 100
smooth = 2

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0
pTime = 0
plocX, plocY = 0,0
clocX, clocY = 0,0

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
detector = htm.HandDetector(maxHands=1)
wScr, hScr = pyautogui.size()
# wScr, hScr = autopy.screen.size()
print(wScr, hScr)

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    if len(lmList)!=0:
        x0, y0 = lmList[4][1:]
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        x3, y3 = lmList[16][1:]
        x4, y4 = lmList[20][1:]

        # print(x1,y1,x2,y2)
        fingers = detector.fingersUp()
        # print(fingers)
        if fingers[1]==1 and fingers[2]==0:
            cv2.rectangle(img,(frameR,frameR), (wCam-frameR,hCam-frameR),
                          (255,0,255), 2)
            x9 = np.interp(x1, (frameR, wCam-frameR), (0,wScr))
            y9 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))
            clocX = plocX + (x9 - plocX) / smooth
            clocY = plocY + (y9 - plocY) / smooth
            pyautogui.moveTo(wScr - clocX, clocY)
            # autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1,y1), 15, (255,0,255), cv2.FILLED)
            plocX, plocY = clocX, clocY
        if fingers[1]==1 and fingers[2]==1:
            cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                          (255, 0, 255), 2)
            x9 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y9 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            clocX = plocX + (x9 - plocX) / smooth
            clocY = plocY + (y9 - plocY) / smooth
            length, img, lineInfo = detector.findDistance(8,12,img)
            print(length)
            if length < 32 :
                cv2.circle(img, (lineInfo[4],lineInfo[5]), 15, (0,255,0), cv2.FILLED)
                pyautogui.mouseDown()
                pyautogui.moveTo(wScr - clocX, clocY)
                # autopy.mouse.click()
            else:
                pyautogui.mouseUp()
        # if fingers[0]==1 and fingers[1]==1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==1:
        #     cv2.circle(img, (x0, y0), 15, (255, 0, 255), cv2.FILLED)
        #     cv2.circle(img, (x1,y1), 15, (255,0,255), cv2.FILLED)
        #     cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        #     cv2.circle(img, (x3, y3), 15, (255, 0, 255), cv2.FILLED)
        #     cv2.circle(img, (x4, y4), 15, (255, 0, 255), cv2.FILLED)
        #     cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
        #                   (255, 0, 255), 2)
        #     x10 = np.interp(x3, (frameR, wCam - frameR), (0, wScr))
        #     y10 = np.interp(y3, (frameR, hCam - frameR), (0, hScr))
        #     clocX = plocX + (x10 - plocX) / smooth
        #     clocY = plocY + (y10 - plocY) / smooth
        #     pyautogui.moveTo(wScr - clocX, clocY)
        #     if fingers[1]==1 and fingers[2]==1:
        #         length, img, lineInfo = detector.findDistance(8,12,img)
        #         print(length)
        #         if length < 32 :
        #             cv2.circle(img, (lineInfo[4],lineInfo[5]), 15, (0,255,0), cv2.FILLED)
        #             pyautogui.mouseDown()
        #             # autopy.mouse.click()
        #         else:
        #             pyautogui.mouseUp()

    #FrameRate
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20,50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
    #Display
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break