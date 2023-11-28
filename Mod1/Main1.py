#Hello World :D

#Importing Modules
import cv2
from keras.models import load_model
import numpy as np
from pygame import mixer
import time
import os
from PIL import ImageFont, ImageDraw, Image
import sys

def Module_1():

    #Initilizing Alarm
    mixer.init()
    sound = mixer.Sound("D:\Code Of Honour\Mod1\Alarm.wav")

    #Loading Cascade 
    face = cv2.CascadeClassifier('D:\Code Of Honour\Mod1\Haar Cascade Files\haarcascade_frontalface_alt.xml')
    leye = cv2.CascadeClassifier('D:\Code Of Honour\Mod1\Haar Cascade Files\haarcascade_lefteye_2splits.xml')
    reye = cv2.CascadeClassifier('D:\Code Of Honour\Mod1\Haar Cascade Files\haarcascade_righteye_2splits.xml')

    #Labels
    lbl=['Close','Open']

    #Loading Model
    model = load_model('D:\Code Of Honour\Mod1\Ml Model\Eye_Position.h5')

    #Assigning Path
    path = "D:\Code Of Honour\Mod1"

    #Open CV Capture
    cap = cv2.VideoCapture(0)

    #Font
    font_path = 'D:\\Code Of Honour\\Mod1\\CV_Font.ttc'  
    font_size = 30  
    custom_font = ImageFont.truetype(font_path, font_size)

    #Var 1
    count=0
    score=0
    thicc=2
    rpred=[99]
    lpred=[99]

    #Var 2
    closed_eye_count = 0
    open_eye_count = 0
    total_frame_count = 0

    while True:
        ret, frame = cap.read()
        height, width = frame.shape[:2]

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        faces = face.detectMultiScale(gray, minNeighbors=5, scaleFactor=1.1, minSize=(25, 25))
        left_eye = leye.detectMultiScale(gray)
        right_eye = reye.detectMultiScale(gray)

        cv2.rectangle(frame, (0, height-30), (width, height), (0, 0, 0), thickness=cv2.FILLED)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (100, 100, 100), 1)

        for (x, y, w, h) in right_eye:
            r_eye = frame[y:y+h, x:x+w]
            count += 1
            r_eye = cv2.cvtColor(r_eye, cv2.COLOR_BGR2GRAY)
            r_eye = cv2.resize(r_eye, (24, 24))
            r_eye = r_eye / 255
            r_eye = r_eye.reshape(24, 24, -1)
            r_eye = np.expand_dims(r_eye, axis=0)
            rpred = model.predict(r_eye)
            rpred = np.argmax(rpred)
            if rpred == 1:
                lbl = 'Open'
            if rpred == 0:
                lbl = 'Closed'
            break

        for (x, y, w, h) in left_eye:
            l_eye = frame[y:y+h, x:x+w]
            count += 1
            l_eye = cv2.cvtColor(l_eye, cv2.COLOR_BGR2GRAY)  
            l_eye = cv2.resize(l_eye, (24, 24))
            l_eye = l_eye / 255
            l_eye = l_eye.reshape(24, 24, -1)
            l_eye = np.expand_dims(l_eye, axis=0)
            lpred = model.predict(l_eye)
            lpred = np.argmax(lpred)

            if lpred == 1:
                lbl = 'Open'
            if lpred == 0:
                lbl = 'Closed'
            break

        if rpred == 0 and lpred == 0:
            score += 1
            closed_eye_count += 1
            total_frame_count += 1 
            frame_pil = Image.fromarray(frame)
            draw = ImageDraw.Draw(frame_pil)
            text = "Closed"
            text_size = custom_font.getbbox(text)
            text_width = text_size[2] - text_size[0]
            text_position = ((width - text_width) // 2, height - 30)
            text_color = (255, 255, 255)
            draw.text(text_position, text, fill=text_color, font=custom_font)
            frame = np.array(frame_pil)

        else:
            score -= 1
            open_eye_count += 1
            total_frame_count += 1
            frame_pil = Image.fromarray(frame)
            draw = ImageDraw.Draw(frame_pil)
            text = "Open"
            text_size = custom_font.getbbox(text)
            text_width = text_size[2] - text_size[0]
            text_position = ((width - text_width) // 2, height - 30)
            text_color = (255, 255, 255)
            draw.text(text_position, text, fill=text_color, font=custom_font)
            frame = np.array(frame_pil)

        if score < 0:
            score = 0
        frame_pil = Image.fromarray(frame)
        draw = ImageDraw.Draw(frame_pil)
        text = 'Score:' + str(score)
        text_position = (10, 10)
        text_color = (255, 255, 255)
        draw.text(text_position, text, fill=text_color, font=custom_font)
        frame = np.array(frame_pil)

        if score > 15:
            #cv2.imwrite(os.path.join(path, 'Check_Frame.jpg'), frame)
            try:
                sound.play()
            except:
                pass
            if thicc < 16:
                thicc = thicc + 2
            else:
                thicc = thicc - 2
                if thicc < 2:
                    thicc = 2
            cv2.rectangle(frame, (0, 0), (width, height), (0, 0, 255), thicc)

        cv2.imshow('Drowsiness Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    #Grading System
    awake_percentage = (open_eye_count / total_frame_count) * 100
    sleepy_percentage = (closed_eye_count / total_frame_count) * 100

    if sleepy_percentage >= 50:
        grade = 'F (Very Sleepy)'
    elif sleepy_percentage >= 30:
        grade = 'D (Sleepy)'
    elif sleepy_percentage >= 10:
        grade = 'C (Awake, but drowsy)'
    else:
        grade = 'A (Fully Awake)'

    for i in range(10):
        print("\n") 
    
    print("Drowsiness Detection Results\n")
    print(f"Closed Eye Count: {closed_eye_count}")
    print(f"Open Eye Count: {open_eye_count}")
    print(f"Total Frames: {total_frame_count}")
    print(f"Awake Percentage: {awake_percentage:.2f}%")
    print(f"Sleepy Percentage: {sleepy_percentage:.2f}%")
    print(f"Grade: {grade}")
    
    

#End Of Code


#Function Call If Main File
if  __name__ == "__main__":
    Module_1()