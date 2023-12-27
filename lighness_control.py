import mediapipe as mp
import cv2, time, math,wmi

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
    imgRGB = cv2.flip(imgRGB, 1)
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

                    
                    def set_screen_brightness(brightness_level):
                        c = wmi.WMI(namespace='wmi')
                        methods = c.WmiMonitorBrightnessMethods()[0]
                        methods.WmiSetBrightness(brightness_level, 0)

                    # Set the brightness level (0 to 100)
                    level = 0
                    if 20<res<50:
                        level = 0
                    elif 50<= res < 100:
                        level = 20
                    elif 100<= res < 150:
                        level = 40
                    elif 150<= res < 200:
                        level = 60
                    elif 200 <= res < 250:
                        level = 80
                    elif 250< res:
                        level = 100
                    brightness_level = level
                    set_screen_brightness(brightness_level)

            # mp_draw.draw_landmarks(img, handLM, mp_hands.HAND_CONNECTIONS)


    cv2.imshow("frame", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
