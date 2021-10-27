import math
class Gest_det():
    def __init__(self,tres_ang=60,dist_c=.60,fing=20):
        #self.thumb_c=.75
        self.fing_ang=fing
        self.tres_ang=tres_ang
        self.dist_c=1-dist_c
        self.angle=None
        self.im_ang=None
        self.ti_ang=None
        self.ini_thumb=None
        self.ini_mid=None
        self.ini_in=None
        self.cur_mid=None
        self.thumb=None
        self.mid=None
        self.wrist=None
        self.index=None
        self.indexMCP=None
        self.thumbCMC=None
        self.calibrated=False

    def distance(self,x1,y1,x2,y2):
        return(round(abs(((x2-x1)**2+(y2-y1)**2)**0.5),2))
    def finang(self,t1,t2,p):
        return(abs(math.degrees(math.atan(self.distance(t1[0],t1[1],t2[0],t2[1])/self.distance(t2[0],t2[1],p[0],p[1])))))
        
    def getang(self,x1,y1,x2,y2):
        return(round(math.degrees(math.atan((y2-y1)/(x2-x1))),2))
    def isRight(self):
        if(-self.tres_ang<self.angle<0 ):
            return(True)
        return(False)
    def isLeft(self):
        if(0<self.angle<self.tres_ang):
            return(True)
        return(False)
    def isStrt(self):
        if(90>abs(self.angle)>75):
            return(True)
        return(False)
    def isFist(self):
        #print(self.cur_thumb,self.cur_mid)
        if(self.cur_mid<round(self.dist_c*self.ini_mid,2)):
            return(True)
        return(False)
    def isThumb(self):
        if(self.ti_ang>self.fing_ang+10):
            return(True)
        return(False)
    def isOpen(self):
        if(self.im_ang>self.fing_ang):
            return(True)
        return(False)
    def main(self):
        if(self.wrist!=None and self.calibrated):
            if(self.isOpen() and not self.isFist() and self.isStrt()):
                return("servo")
            if(not self.isThumb() and self.isFist()):#stop
                return("stop")
            elif(self.isThumb() and self.isStrt()):#reverse
                return("reverse")
            elif(self.isStrt()):#forward
                return("forward")
            elif(self.isLeft()):#left
                return("left")
            elif(self.isRight()):#right
                return("right")
            
        
        
    





