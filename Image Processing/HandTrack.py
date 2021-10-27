import cv2
import mediapipe as mp
import time
import math
from gest_det import Gest_det
import requests

url = "http://192.168.29.203/asasasasa"

class handDetector():
    def __init__(self, mode = False, maxHands = 1, detectionCon = 0.6, trackCon = 0.3):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.gest=Gest_det()
        
    def findHands(self,img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        

        #if self.results.multi_hand_landmarks:
            #for handLms in self.results.multi_hand_landmarks:
                #if draw:
                    #self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo = 0, draw = True):

        lmlist = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            #print(myHand.landmark[0].x)
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 3, (204, 74, 88), 2)
                    #print(cx, ",", cy)
        return lmlist
    def get_vals(self,w,h):
        if self.results.multi_hand_landmarks:
            self.gest.wrist=(self.results.multi_hand_landmarks[0].landmark[0].x*w,self.results.multi_hand_landmarks[0].landmark[0].y*h)
            self.gest.thumb=(self.results.multi_hand_landmarks[0].landmark[4].x*w,self.results.multi_hand_landmarks[0].landmark[4].y*h)
            self.gest.mid=(self.results.multi_hand_landmarks[0].landmark[12].x*w,self.results.multi_hand_landmarks[0].landmark[12].y*h)
            self.gest.index=(self.results.multi_hand_landmarks[0].landmark[8].x*w,self.results.multi_hand_landmarks[0].landmark[8].y*h)
            self.gest.indexMCP=(self.results.multi_hand_landmarks[0].landmark[5].x*w,self.results.multi_hand_landmarks[0].landmark[5].y*h)
            self.gest.thumbCMC=(self.results.multi_hand_landmarks[0].landmark[1].x*w,self.results.multi_hand_landmarks[0].landmark[1].y*h)
            self.gest.angle=self.gest.getang(self.gest.wrist[0],self.gest.wrist[1],self.gest.mid[0],self.gest.mid[1])
            self.gest.im_ang=self.gest.finang(self.gest.index,self.gest.mid,self.gest.indexMCP)
            self.gest.ti_ang=self.gest.finang(self.gest.thumb,self.gest.indexMCP,self.gest.thumbCMC)
            self.gest.cur_mid=self.gest.distance(self.gest.wrist[0],self.gest.wrist[1],self.gest.mid[0],self.gest.mid[1])
            

    def calibration(self):
        #self.gest.ini_thumb=self.gest.cur_thumb
        self.gest.ini_mid=self.gest.cur_mid
        self.gest.calibrated=True
                
                
    # def Gest(self):
    #     #print(self.gest.wrist,self.gest.thumb,self.gest.mid,self.gest.angle)
    #     if(self.gest.wrist!=None and self.gest.calibrated):
    #          print(self.gest.angle,self.gest.ti_ang)
    #          print("left:",self.gest.isLeft(),"Right:",self.gest.isRight(),"Straight:",self.gest.isStrt(),"Fist:",self.gest.isFist(),"Thumb:",self.gest.isThumb(),"isopen:",self.gest.isOpen())
            


def main():
    pTime = 0
    cTime = 0
    a = 0
    cap = cv2.VideoCapture(0)

    detector = handDetector()

    print("Press ESC on frame to exit")

    L = False
    F = False
    S = False
    B = False
    R = False
    O = False
    



   # rows,cols,channels = overlay.shape

    while True:
        success, img = cap.read()
        
        img = cv2.flip(img,1)
        img = detector.findHands(img)
        c=detector.gest.main()

        detector.get_vals(img.shape[0],img.shape[1])
        k = cv2.waitKey(10)
        if k == 32: #SPACEBAR to start detection
            detector.calibration()
            print(detector.gest.thumb,detector.gest.mid)
        
        if(c!=None):
            #print(c)
            if c == "left":
                if L == False:
                    print(c)
                    response = requests.request("GET", url + "/left")
                    L = True
                    F = False
                    S = False
                    B = False
                    R = False
                    O = False
                    #print(response)

            elif c == "right":
                if R == False:
                    print(c)
                    response = requests.request("GET", url + "/right")
                    L = False
                    F = False
                    S = False
                    B = False
                    R = True
                    O = False
                
            elif c == "forward":
                if F == False:
                    print(c)
                    response = requests.request("GET", url + "/forward")
                    L = False
                    F = True
                    S = False
                    B = False
                    R = False
                    O = False
                
            elif c == "stop":
                if S == False:
                    print(c)
                    response = requests.request("GET", url + "/stop")
                    L = False
                    F = False
                    S = True
                    B = False
                    R = False
                    O = False
                
            elif c == "reverse":
                if B == False:
                    print(c)
                    response = requests.request("GET", url + "/backward")
                    L = False
                    F = False
                    S = False
                    B = True
                    R = False
                    O = False 

            elif c == "servo":
                if O == False:
                    print(c)
                    response = requests.request("GET", url + "/open")
                    L = False
                    F = False
                    S = False
                    B = False
                    R = False
                    O = True           
        
        lmlist = detector.findPosition(img)
        
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        #cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.putText(img, "Fist - Stop  |  Straight - Forward  |  TiltRight - Right  |  TiltLeft - Left", (10, 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)
        cv2.putText(img, "ThumbOut - Servo  |  IndexOut - Reverse", (146, 60), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)

        cv2.imshow("Gesture Remote", img)

        if k == 27:  # press ESC to exit
            break


if __name__ == "__main__":
    main()