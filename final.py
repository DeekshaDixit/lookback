import numpy as np
import cv2
import time
import requests
import ftplib
import requests
import pymysql
conn=pymysql.connect(host="localhost", user="root", passwd="", db="people")
mycursor=conn.cursor()



# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

cap = cv2.VideoCapture(0)
#cap.set(cv2.cv.CV_CAP_PROP_FPS, 2)
currentframe = 0
ftp = ftplib.FTP()
host = "ftp.byethost4.com"
port = 21
test=0

# put your keys in the header
headers = {
    "app_id": "697adc6d",
    "app_key": "260f2011b6914b5a41da283d93bd7e55"
}

while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

##    for (x,y,w,h) in faces:
##        #cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
##        roi_gray = gray[y:y+h, x:x+w]
##        roi_color = img[y:y+h, x:x+w]
##        
##        eyes = eye_cascade.detectMultiScale(roi_gray)
##        #for (ex,ey,ew,eh) in eyes:
##            #cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    #print faces
    currentframe = currentframe + 1
    if np.asarray(faces).any():
        name = "image" + '.jpg'
        cv2.imwrite(name, img)
        if(test==0):
            ftp.connect(host, port)
            print (ftp.getwelcome())
            test=test+1
            try:
                print ("Logging in...")
                ftp.login("b4_21800984", "WELcome15")
            except:
                "failed to login"
        file = open('C:\Users\Deeksha\Desktop\Hackathon\image.jpg','rb')# file to send
        myfolder = '/htdocs/'
        ftp.cwd(myfolder)
        cv2.imshow('img',img)
        ftp.storbinary('STOR image.jpg', file)
        time.sleep(2)
        payload = '{"image":"http://lookback.byethost4.com/image.jpg"}'
        url = "http://api.kairos.com/detect"
        # make request
        r = requests.post(url, data=payload, headers=headers)
        #print r.content
        p = r.content
        start = 0
        age_index = p.find('"age"',start, len(p))
        male_index = p.find('"maleConfidence"', start, len(p))
        female_index = p.find('"femaleConfidence"', start, len(p))
        while (age_index>0):
            print (p[age_index+6 : age_index+8])
            age = p[age_index+6 : age_index+8]
            #print (p[male_index+17 : male_index+21])
            #print (p[female_index+19 : female_index+23])
            start= age_index + 6
            startm = male_index + 17
            startf = female_index + 17
            age_index = p.find('"age"',start, len(p))
            male_index = p.find('"maleConfidence"', start, len(p))
            female_index = p.find('"femaleConfidence"', start, len(p))
            male = p[male_index+17 : male_index+21]
            female = p[female_index+19 : female_index+23]
            sex = "none"
            if (float(male) > 0.5):
                sex = "male"
            else:
                sex = "female"
            mycursor.execute("INSERT INTO info(age,gender) VALUES(%s,%s)",
                               (age,sex))

            print(">Data inserted")
            conn.commit()
##        time.sleep(4)
    #cv2.imwrite("sa.jpg", img)
    k = cv2.waitKey(15) & 0xff
    if k == 27:
        break
ftp.quit()
cap.release()
cv2.destroyAllWindows()
