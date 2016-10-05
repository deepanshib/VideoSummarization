#Brute-Force Matching with ORB Descriptions

import cv2
import glob
import operator
import itertools
import sys
import numpy as np
import timeit

dataSet = "/home/lp2/dataset/PTZ_Camera/PTZ/PTZ/intermittentPan/input/*.jpg"
#dataSet = "/home/lp2/workspace/BackgroundSubtraction/input/*.jpg"
orb = cv2.ORB()


def imagePreprocessing(frame):
    img1 = cv2.imread(frame); #104
    if  img1 is None:
       print "No image data"
       return None
    else:
       img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
       return img1

    
def getValuesAccordingToThreshold(dictVal, threshold = 300):
    maxVal = max(dictVal.iteritems(), key=operator.itemgetter(1))[1]
    thresholdVal = maxVal*0.60 #threshold value is 300 before
    print maxVal, thresholdVal

    subDictVal = {}
    for key, value in dictVal.items():
        if value >= 300:
           subDictVal[key] = value	
    return subDictVal
        

def findMatchingFrames(selectedFrame) :
    dictVal = {} 
    for filename in glob.glob(dataSet):
        img2 = imagePreprocessing(filename)
        if img2 is not None:
           kp1, des1 = orb.detectAndCompute(selectedFrame,None)
           kp2, des2 = orb.detectAndCompute(img2,None)
           bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
           matches = bf.match(des1, des2)
           good = []
           for m in matches:
               if m.distance < 70:
                  good.append(m)
           dictVal[filename] = len(good)
    return dictVal       
           
def showResultingImages(dictVal):
    sorted_d = sorted(dictVal.items(), key=operator.itemgetter(0),reverse=False)
    for key, value in sorted_d:
        img = cv2.imread(key)
        #cv2.rectangle(img, (img.height-10, img.width -10), (img.height-20, img.height-5), (255, 0, 0), 2)		
        cv2.imshow("result", img)#TODO FIX IT
        cv2.waitKey(10)        

        #print key, value

           

def printResultingValuesInOrder(dictVal):
    sorted_d = sorted(dictVal.items(), key=operator.itemgetter(0),reverse=True)    
    for key, value in sorted_d:
        print key, value
    print len(sorted_d)
    
def putRectangle(switch, img):
    h,w,c = img.shape
    x1 = (w*85)/100
    x2 = (h*83)/100
    x3 = (w*92)/100
    x4 = (h*94)/100	
    if switch == True:
        cv2.rectangle(img, (x1, x2), (x3, x4), (0, 255, 0), -2)#green
    else:
        cv2.rectangle(img, (x1, x2), (x3, x4), (0, 0, 255), -2)#red			        
    return img

def showAllFramesWithRectangle(dictVal):
    for filename in sorted(glob.glob(dataSet)):
         if filename in dictVal:
            print "inside " + filename		
            img = cv2.imread(filename);
            img = putRectangle(True, img)
         else:
            print "outside " + filename
            img = cv2.imread(filename);
            img = putRectangle(False, img)			            		
         cv2.imshow("result", img)
         cv2.waitKey(2000) 

#def createSummarizedVideo(dictVal):TODO


def readImageWithResize(frame) : 
    img1 = cv2.imread(frame); #104    


start = timeit.default_timer()         
if len(sys.argv) > 1 : 
   
   selectedFrame =  sys.argv[1]
   selectedImg = imagePreprocessing(selectedFrame)
   if selectedImg is not None:
      dictVal = findMatchingFrames(selectedImg)
      dictVal = getValuesAccordingToThreshold(dictVal)
      #printResultingValuesInOrder(dictVal)
      #showResultingImages(dictVal)
      stop = timeit.default_timer()
      seconds =  stop - start
      
      m, s = divmod(seconds, 60) 
      print "Total time = %02d:%02d" % (m, s)
      #showResultingImages(dictVal)
      printResultingValuesInOrder(dictVal)
      #showAllFramesWithRectangle(dictVal)
         
else:
   print "need to give a frame"
   
