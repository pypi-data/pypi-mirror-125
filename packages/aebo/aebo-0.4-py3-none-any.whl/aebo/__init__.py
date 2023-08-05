import nltk
import numpy as np
import random
import string
import cv2
import os

cascPath=os.path.dirname(cv2.__file__)+"/data/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)



from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

lemmer = nltk.stem.WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# Generating response
def response(user_input, filename = "info.txt"):
    f = open(filename, 'r', errors='ignore')
    raw = f.read()
    raw = raw.lower()
    sent_tokens = nltk.sent_tokenize(raw)
    sent_tokens.append(user_input)
    
    robo_response=''
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize)
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        #robo_response=robo_response+"I am sorry! I don't understand you"
        #robo_response = robo_response + "Please train me on this"
        print("I am sorry! I don't understand you.Please train me on this")
        train_input = input("enter the information : ")
        f = open(filename, "a")
        f.write("\n")
        f.write(train_input+".")
        f.close()
        robo_response = robo_response+"Thanks for training me..I am ready now"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response

def guiresponse(user_input, filename = "info.txt"):
    f = open(filename, 'r', errors='ignore')
    raw = f.read()
    raw = raw.lower()
    sent_tokens = nltk.sent_tokenize(raw)
    sent_tokens.append(user_input)
    
    robo_response=''
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize)
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        robo_response = robo_response + "Please train me on this"
        #print("I am sorry! I don't understand you.Please train me on this")
        #train_input = input("enter the information : ")
        flag=1
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response

def convert2Gray(frame):
    outFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return outFrame


def detectface(frame):

    faces = faceCascade.detectMultiScale(
        frame,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    return faces

def drawBox(frame,faces):

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    if x=None:
        x=0
        y=0
        w=0
        h=0
    
    return frame,x,y

def writeText(frame,text,x,y,R,G,B):

    cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (R, G, B), 2)
    return frame
    

def startCamera(num):
    vid = cv2.VideoCapture(num)
    return vid

def stopCamera(vid):
    vid.release()

def displayImage(name,frame):
    cv2.imshow(name,frame)


def saveImage(fileloc,frame):
    cv2.imwrite(fileloc,frame)
    

def closewindow():
    cv2.destrotAllWindows()


    
