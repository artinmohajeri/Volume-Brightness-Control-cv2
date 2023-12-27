import pycaw.pycaw as pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import mediapipe as mp
import cv2, math

# Get the volume control interface
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

# Control the volume
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.SetMasterVolumeLevel(-40.0, None)  # Set the volume level (-20.0 dB in this example)




per = 10
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands()




def calculate_distance(x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgRGB = cv2.flip(imgRGB,1)
    results = hands.process(imgRGB)
    img = cv2.flip(img, 1)

    if results.multi_hand_landmarks:
        for handLM in results.multi_hand_landmarks:
            thumb_fingure = None
            index_fingure = None
            for id,lm in enumerate(handLM.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                if id == 8:
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    cv2.circle(center=(cx,cy), img=img, color=(0,255,0), radius=20, thickness=-1)
                    index_fingure = (cx, cy)
                if id == 4:
                    cv2.circle(center=(cx,cy), img=img, color=(0,255,0), radius=20, thickness=-1)
                    thumb_fingure = (cx,cy)
                if index_fingure and thumb_fingure:
                    cv2.line(pt1=index_fingure,pt2=thumb_fingure, img=img, color=(0,255,0), thickness=2)
                    res = calculate_distance(index_fingure[0],index_fingure[1],thumb_fingure[0],thumb_fingure[1])

                    level = -60
                    if 20<res<30:
                        per = 200
                        level = -60
                    elif 30<= res < 50:
                        per=190
                        level = -50
                    elif 50<= res < 100:
                        per = 175
                        level = -40
                    elif 100<= res < 130:
                        per = 150
                        level = -30
                    elif 130 <= res < 150:
                        per=125
                        level = -20
                    elif 150< res<=180:
                        per=100
                        level = -10
                    elif 180< res<=200:
                        per=75
                        level = -7
                    elif 200< res<=230:
                        per = 50
                        level = -4
                    elif 230< res<=250:
                        per=25
                        level = -2
                    elif 250< res:
                        per = 10
                        level = 0
                    volume.SetMasterVolumeLevel(level, None)


            mp_draw.draw_landmarks(img, handLM, mp_hands.HAND_CONNECTIONS)
            
    cv2.rectangle(pt1=(10,per),pt2=(50,200), img=img, color=(0,0,255), thickness=-1)
    cv2.rectangle(pt1=(10,10),pt2=(50,200), img=img, color=(0,0,0), thickness=2)

    cv2.imshow("frame", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break