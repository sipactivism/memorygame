import cv2
import numpy as np
import mediapipe as mp
import random
import pymsgbox
from time import time, sleep
from PIL import ImageFont, ImageDraw, Image

from mediapipe.tasks import python
from mediapipe.tasks.python import vision, BaseOptions
from mediapipe.tasks.python.vision import GestureRecognizer, GestureRecognizerOptions, HandLandmarker, HandLandmarkerOptions

# get gesture_recognizer.task from https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/latest/gesture_recognizer.task
GESTURE_RECOGNITION_OPTIONS = BaseOptions(model_asset_path="gesture_recognizer.task")
GESTURES = {"Thumb_Up": "👍","Thumb_Down": "👎","Open_Palm": "🖐","Closed_Fist": "✊","Victory": "✌","None":"❌"}
TIME_TO_GUESS = 10

recognizer = GestureRecognizer.create_from_options(GestureRecognizerOptions(base_options=GESTURE_RECOGNITION_OPTIONS))

"""
gestures:
thumbs up: Thumb_Up
thumbs down: Thumb_Down
open hand: Open_Palm
closed hand: Closed_Fist
"""

def draw_emoji(frame,text: str,loc: tuple):
    pil_img = Image.fromarray(frame)
    draw = ImageDraw.Draw(pil_img)
    draw.text(loc,text,fill=(0,0,0),font=ImageFont.truetype("Noto_Emoji\\static\\NotoEmoji-Regular.ttf",100))
    return np.array(pil_img)

def game_loop(cap: cv2.VideoCapture):
    past_gestures = []
    correct_gestures = 0
    gesture_list = list(GESTURES.keys())
    gesture_list.remove("None")
    running = True
    # choose random gesture
    while running:
        past_gestures.append(random.choice(gesture_list))
        for i,gesture in enumerate(past_gestures):
            text = "❓"
            found = False
            hide_gesture = True
            start_time = time()
            end_time = start_time + TIME_TO_GUESS
            # decide whether or not to show the gesture based on position in list
            if i == (len(past_gestures) - 1):
                text = GESTURES[gesture]
                hide_gesture = False
            # timer
            while time() < end_time:
                _, frame = cap.read()
                width, height, _ = frame.shape
                # convert to mediapipe's image format
                mp_img = mp.Image(image_format=mp.ImageFormat.SRGB,data=frame)
                # feed into recognizer
                result = recognizer.recognize(mp_img)
                # check if gesture is found
                if len(result.gestures) > 0:
                    print(result.gestures[0])
                    located_gesture = result.gestures[0][0]
                    # is it the gesture
                    if located_gesture.category_name == gesture:
                        print("Found!")
                        text = "✅"
                        found = True
                        print(hide_gesture)
                # just clean up the presentation a bit
                remaining_time = round(end_time - time(),2)
                # just a nice bar for the top
                if remaining_time < 0:
                    text = GESTURES[gesture]
                    remaining_time = 0
                    # because the remaining time tends to differ when near 0, stop showing a little before the end
                elif remaining_time >= 0.025:
                    cv2.putText(frame,str(remaining_time),(50,200),1,2,(255,0,0),2)
		    # also add some basic informational stuff
                    cv2.putText(frame,f"Gesture {str(i+1)}/{str(len(past_gestures))}",(300,50),1,2,(255,0,0),2)
                    if hide_gesture:
                        cv2.putText(frame,"Show the correct gesture (from memory) to the camera",(10,450),1,1,(255,0,0),2)
                    else:
                        cv2.putText(frame,"Show the gesture on screen to the camera",(10,450),1,1,(255,0,0),2)  
                # add text
                frame = draw_emoji(frame,text,(50,50))

                cv2.imshow("frame",frame)
                cv2.waitKey(1)
				
                if found: break
            if not found:
                print("Looks like you lost...")
                running = False
                break
            print("Well done!")
            correct_gestures += 1
            sleep(1)
    again = pymsgbox.confirm(f"You remembered {correct_gestures} gesture(s)! Would you like to try again?","Try again?",buttons=["Yes","No"])
    if again == "Yes":
        # run entire function again
        game_loop(cap)
def setup():
    cap = cv2.VideoCapture(0)

    game_loop(cap)
    
    cap.release()
    cv2.destroyAllWindows()

setup()
