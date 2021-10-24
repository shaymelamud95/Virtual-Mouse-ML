import cv2
import numpy as np
import HandTrackingModule as htm
import time
# import autopy
import pyautogui

##########################
wCam, hCam = 640, 480
frameR = 100  # Frame Reduction

smoothening = 2
#########################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = pyautogui.size()
print(wScr, hScr)
flag = False
isMouseDown = False
def moveMouse(x1, y1, plocX, plocY):
    # 5. Convert Coordinates
    x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
    y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
    # print(x3, y3)
    # 6. Smoothen Values
    clocX = plocX + (x3 - plocX) / smoothening
    clocY = plocY + (y3 - plocY) / smoothening
    # print(clocX,clocY)

    # 7. Move Mouse
    pyautogui.moveTo(wScr - clocX, clocY, duration=0.0)
    # cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
    plocX, plocY = clocX, clocY
    return plocX, plocY, x3, y3
while True:
    # 1. Find hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    # 2. Get the tip of the index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:] # index finger
        x2, y2 = lmList[12][1:] # second finger
        x33, y33 = lmList[7][1:] #index rist
        x44, y44 = lmList[11][1:] # second rist
        # print(x1, y1,x33, y33 )
        # print("length, img, lI, x1, y1, x2, y2")
        length1, img1, lineInfo1 = detector.findDistance(12, 0, img, draw = False)
        if length1 < 60:
            continue
    # 3. Check which fingers are up
    fingers = detector.fingersUp()
    # print(fingers)
    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                  (255, 0, 255), 2)
    # 4. Only Index Finger : Moving Mode
    if fingers == [0,1,0,0,0]:
        plocX, plocY, x3, y3 = moveMouse(x1, y1, plocX, plocY)

    # 8. Both Index and middle fingers are up : Clicking Mode
    if fingers and fingers[1] == 1 and fingers[2] == 1:
        # 9. Find distance between fingers
        length, img, lineInfo = detector.findDistance(8, 12, img)
        # print(int(length1), int(length))

        #treatment for size of the hand, (distance of the hand from the camera)
        dis = int(length1)/10 + int(length1)/20 -1

        # 10. drug mouse if distance short
        if length < dis:
            cv2.circle(img, (lineInfo[4], lineInfo[5]),
                       2, (0, 255, 0), cv2.FILLED)
            if not isMouseDown:
                pyautogui.mouseDown()
            isMouseDown = True
            plocX, plocY, x3, y3 = moveMouse(x1, y1, plocX, plocY)
        elif not isMouseDown:
            pyautogui.mouseUp()
            isMouseDown = False
        # click mouse left/right if fingers are folded
        if y44 < y2:
            pyautogui.click(button='right')
        elif y33 < y1:
            pyautogui.click()
    # scrolling mode
    if fingers == [1,1,0,0,0]:
        if y33 > y1:
            pyautogui.scroll(10)
        else:
            pyautogui.scroll(-10)
    if fingers and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0 and fingers[0] == 0 and flag:
        pname = str(cTime) + ".png"
        image = pyautogui.screenshot(pname,region=(0,0,wScr, hScr))  # returns a Pillow/PIL Image object
        image.save("C://Users/sm251206/PycharmProjects/VM/auto-py-to-exe/screenshots" + pname)
        # flag = False
    if flag:
        startLogo = pyautogui.locateOnScreen('start.png')
        print(startLogo)
        #onScreen for safety reasons
        pyautogui.click(startLogo.left + startLogo.width / 2, startLogo.top + startLogo.height / 2)
        flag = False

    # pyautogui.rightClick(x=moveToX, y=moveToY)
    # pyautogui.middleClick(x=moveToX, y=moveToY)
    # pyautogui.doubleClick(x=moveToX, y=moveToY)
    # pyautogui.tripleClick(x=moveToX, y=moveToY)
    # pyautogui.scroll(amount_to_scroll, x=moveToX, y=moveToY)
    # pyautogui.hscroll(10)  # scroll right 10 "clicks"
    # pyautogui.mouseDown(x=moveToX, y=moveToY, button='left')
    # pyautogui.mouseUp(x=moveToX, y=moveToY, button='left')
    # pyautogui.typewrite("hello", interval=2)
    # pyautogui.hotkey('ctrl', 'c')  # ctrl-c to copy
    # pyautogui.keyDown(key_name)
    # pyautogui.keyUp(key_name)
    # pyautogui.alert('This displays some text with an OK button.')
    # pyautogui.confirm('This displays text and has an OK and Cancel button.')
    # pyautogui.prompt('This lets the user type in a string and press OK.')
    # x = pyautogui.screenshot('foo.png',region=(0,0, 300, 400))  # returns a Pillow/PIL Image object
    # pyautogui.locateOnScreen('looksLikeThis.png')  # returns (left, top, width, height) of first place it is found
    # onScreen
    # pyautogui.dragTo(100, 200,button='left')  # drag mouse to X of 100, Y of 200 while holding down left mouse button
    # pyautogui.press('enter')  # press the Enter key
    # pyautogui.press('f1')  # press the F1 key
    # pyautogui.press('left')  # press the left arrow key
    x1 = ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
     ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
     '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
     'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
     'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
     'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
     'browserback', 'browserfavorites', 'browserforward', 'browserhome',
     'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
     'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
     'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
     'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
     'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
     'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
     'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
     'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
     'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
     'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
     'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
     'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
     'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
     'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
     'command', 'option', 'optionleft', 'optionright']














    # 11. Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    # cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 0), 3)
    # 12. Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)