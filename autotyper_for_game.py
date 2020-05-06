import mss
import cv2
import numpy as np
import pytesseract
from screeninfo import get_monitors
import time
import pyautogui


for m in get_monitors():
    print(str(m))
TYPETIME = 0.0001
CONFIG = (
    '-c tessedit_char_whitelist="C_ ,.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\\\"\'-?!:;" --psm 4')
with mss.mss() as sct:
    run = False
    monitor = {"top": 0, "left": 0, "width":m.width, "height": m.height}

   
    topTextBox = 640
    leftTextBox = 250
    widthTextBox = 1100
    heightTextBox = 200
    start = False
    while not start:
        img = np.array(sct.grab(monitor))
        greyImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        d = pytesseract.image_to_data(greyImg, output_type=pytesseract.Output.DICT)
        print("--------------")
        if "Start" in d['text']:
            start = True
    print("Ready to start")
    
    textBox = {"top": topTextBox, "left": leftTextBox, "width":widthTextBox, "height": heightTextBox}
    textImg = np.array(sct.grab(textBox))
    #cv2.imshow("OpenCV/Numpy normal", textImg)
    #cv2.waitKey(0)
    


    iterations = 0
    go = False
    while not go:
        iterations+=1
        img = np.array(sct.grab(monitor))
        greyImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        d = pytesseract.image_to_data(greyImg, output_type=pytesseract.Output.DICT)
        n_boxes = len(d['text'])
        for i in range(n_boxes):
            if int(d['conf'][i]) > 60:
                if d['text'][i]=="GO" or d['text'][i]=="GO!":
                    go = True
                    break
    print("Go!")
    text = pytesseract.image_to_string(textImg, config=CONFIG)
    text = text.replace('_', ' ')
    text = text.replace('  ', ' ')
    text = text.replace('   ', ' ')
    text = text.replace('\n', ' ')
    pyautogui.write(text, interval=TYPETIME)
