#class that uses mediapipe to track hand and fingers


import cv2
import mediapipe as mp
import time
import math

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
    
            #initializing variables
            self.mode = mode
            self.maxHands = maxHands
            self.detectionCon = detectionCon
            self.trackCon = trackCon
    
            #initializing mediapipe
            self.mpHands = mp.solutions.hands
            self.hands = self.mpHands.Hands()
            self.mpDraw = mp.solutions.drawing_utils
    
    #function to find hands
    def findHands(self,img,draw=True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        #print(results.multi_hand_landmarks)
    
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS)
        return img
    
    #function to find position of hands
    def findPosition(self,img,handNo=0,draw=True):
    
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
    
            for id,lm in enumerate(myHand.landmark):
                #print(id,lm)
                h,w,c = img.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                #print(id,cx,cy)
                lmList.append([id,cx,cy])    
        return lmList
    
    #function to find distance between two points
    def findDistance(self,p1,p2,img,r=15,t=3):
        x1,y1 = p1[1],p1[2]
        x2,y2 = p2[1],p2[2]
        cx,cy = (x1+x2)//2,(y1+y2)//2
    
        
    
        length = math.hypot(x2-x1,y2-y1)
        return length,img,[x1,y1,x2,y2,cx,cy]
    

    #function to draw a ball on the cv2 window using pygame
    def drawBall(self,img,ballX,ballY):
        cv2.circle(img,(ballX,ballY),15,(255,0,255),cv2.FILLED)
        return img
   

    #main function starting with "
    
#game class that holds the game logic
class game():
    score = 0
    ballX = ballY = 0

    def __init__(self):
        pass
    def drawBall(self,img):
        cv2.circle(img,(self.ballX,self.ballY),15,(255,0,255),cv2.FILLED)
        return img
    def moveBall(self):
        self.ballX += 10
        self.ballY += 10
        if self.ballX > 640:
            self.ballX = 0
        if self.ballY > 480:
            self.ballY = 0
    def findDistance(self,f1,f2,p1,p2):
        x1,y1 = p1,p2
        x2,y2 = f1,f2

        length = math.hypot(x2-x1,y2-y1)
        return length
    #function to add to score everytime the ball touches any finger
    def addScore(self):
        self.score += 1
        return self.score
    #function to reset the score
    def resetScore(self):
        self.score = 0
        return self.score
    #function to check if the ball is touching any finger
    def checkTouch(self,fingerX,fingerY,ballX,ballY):
        if self.findDistance(fingerX,fingerY,ballX, ballY)<20:
            self.score+=1

if __name__ == "__main__":
    pTime = 0
    cTime = 0
    game = game()
    cap = cv2.VideoCapture("D:\documents\VScodeables\copilot\Andrew.mp4")
    detector = handDetector()
    while True:
        success,img = cap.read()
        if img is None:
            continue
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            for finger in lmList:
                game.checkTouch(finger[1],finger[2],game.ballX,game.ballY)
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        img = game.drawBall(img)
        game.moveBall()          
        #check if the ball is touching any finger
       
        #log ball coordinates        
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

        #show the score on the screen
        cv2.putText(img,str(game.score),(10,100),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
        cv2.imshow("Image",img)
        if cv2.waitKey(1)== 27:
            cap.release()
            cv2.destroyAllWindows()
            break
        