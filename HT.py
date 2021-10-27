import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode = False, maxHands = 3, detectionCon = 0.3, trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        
    def findHands(self,img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    #self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)


        return img

    def findPosition(self, img, handNo = 0, draw = True):

        lmlist = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)
                    #print(cx, ",", cy)
        return lmlist

def main():
    pTime = 0
    cTime = 0
    a = 0
    cap = cv2.VideoCapture(0)
    
    overlay = cv2.imread('dice.png')

    detector = handDetector()


    rows,cols,channels = overlay.shape

    while True:
        success, img = cap.read()        

       # img = cv2.flip(img,1)
        img = detector.findHands(img)
        a = a + 1
        #if a%13 == 0:
        	#print(img)
        	#time.sleep(0.5)
        
        lmlist = detector.findPosition(img)
#        if len(lmlist) != 0:
#           print(lmlist[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        handLandmarks = detector.findHandLandMarks(image=image, draw=True)

        if(len(handLandmarks) != 0):
            #for control we need 4th and 8th landmark
            
            x1, y1 = handLandmarks[4][1], handLandmarks[4][2]
            x2, y2 = handLandmarks[8][1], handLandmarks[8][2]
            length = math.hypot(x2-x1, y2-y1)
            print(length)

            #Hand range(length): 50-250
            #Volume Range: (-65.25, 0.0)

            volumeValue = np.interp(length, [50, 250], [-65.25, 0.0]) #coverting length to proportionate to volume range
            volume.SetMasterVolumeLevel(volumeValue, None)


            cv2.circle(image, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(image, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), 3)

            cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

       # cv2.addWeighted(img,0.4,overlay,0.1,0)
        
       # overlay = cv2.addWeighted(img[250:250+rows, 0:0+cols],0.5,overlay,0.5,0)

       # img[250:250+rows, 0:0+cols ] = overlay

        cv2.imshow("Image", img)
       # cv2.waitKey(1)

        k = cv2.waitKey(10)
        if k == 27:  # press ESC to exit
            break


if __name__ == "__main__":
    main()
