import cv2
import base64
import time
import requests
from PIL import Image
from multiprocessing import Pool
from datetime import datetime as dt
from lxml import html
import re
import json
 
API_URI = "https://vision.googleapis.com/v1/images:annotate"
API_KEY = "AIzaSyAy-Twv2K3ukFiMfRHMWhjG9ZSP0h9RJ_A"

camera_port = 0
ramp_frames = 60
camera = ""

def initializeCamera():
    global camera
    camera = cv2.VideoCapture(camera_port)
    camera.set(15, -4);
    for i in range(ramp_frames):
        get_image()
    return

def shutdownCamera():
    global camera
    camera.release()

def encode_image(image):
    f = open(image, 'rb')
    image_content = f.read()
    f.close()
    return base64.b64encode(image_content).decode('utf-8')

def get_image():
        retval, im = camera.read()
        return im
 
def save_image(camera_capture):
     file = "test_image.png"
     cv2.imwrite(file, camera_capture)
     return
 
def runCamera():
    for i in range (5):
        camera_capture = get_image()
    save_image(camera_capture)
    return camera_capture

def readQuestion():
         encoded = encode_image("test_image.png")
         
         payload = {
              "requests": [
                {
                  "image": {
                    "content": encoded
                  },
                  "features": [
                    {
                      "type": "TEXT_DETECTION"
                    }
                  ]
                }
              ]
            }
        
         r = requests.post(API_URI, params={'key':API_KEY}, json=payload)
         data = r.json()['responses'][0]['textAnnotations'][0]['description']
         print(data)
         question = data[:data.index("?")].replace('\n',' ')
         answers = data.split("\n")[-4:-1]
         print("Question: ", question)
         print("Answers: ", answers)
         
         ## add question parsing
         return question, answers
     
def getResultStat(query):
        q = {"q":query}
        page = requests.get("https://www.google.ca/search", params=q)
        parsed = html.fromstring(page.content)
        resultText = parsed.xpath('//div[@id="resultStats"]/text()')
        resultStat = int(re.sub('[^0-9]', "", str(resultText)))
        return resultStat
        
def getAnswer(question, answers):
   # question = "Botany is the study of what"
   # answers = ["Plants", "Intersellar Life", "New York"]
    aKey = ["A","B","C"]
    queries = []
    
    for i in range(len(answers)):
        queries.append(question + ' "' + answers[i] + '"')
        #queries.append(answers[i])
    
    with Pool(len(queries)) as p:
        results = p.map(getResultStat, queries)
    
    answerIndex = results.index(max(results))
    answer = aKey[answerIndex] + ": " + answers[answerIndex]
    #answer = answers[answerIndex]
    return answer

def calibrate():
    for i in range(4):
        input("Calibrate...")
        frame = runCamera()
        
def app():
    initializeCamera()
    #try:
    calibrate()
    input("Ready?")

    for i in range(12):
         start = dt.now()
         print("Taking image...")
         runCamera()
         print("Running OCR...")
         question, answers = readQuestion()
         print(question, answers)
         print("Figuring out answer...")
         answer = getAnswer(question, answers)
         
         print("Answer is: ", answer)
         
         print("Total Time: ", dt.now()-start)
    #except:  
        #shutdownCamera()
        
    shutdownCamera()
    
if __name__ == '__main__':
    app()