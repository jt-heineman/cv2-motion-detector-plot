import pandas
import cv2
import time
from datetime import datetime

first_frame = None
status_list=[None, None]
times=[]
df=pandas.DataFrame(columns=["Start","End"])
video=cv2.VideoCapture(0) #argument can be number or video file path.Different cameras with different indexes.

while True:
    check, frame = video.read() #generates a boolean (that is running), and numpy array with all the frames
    status = 0
    #print(check)
    #print(frame)
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray, (21,21),0) #smooth noise and make more accurate calculations, pass image and tuple paramenters of gaussian blur. last parameter standard deviation

    if first_frame is None:
        first_frame=gray
        continue #will continue to the beggining of the while loop

    delta_frame=cv2.absdiff(first_frame, gray) #difference between frames

    #method to get noise - parameters: image, limit, what color assign, threshhold method
    #will apply to deltas more than 30, generate white as 255 
    #cv2.threshold returns a tuple with two value, need to access second item of the tuple 
    thresh_frame=cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1] 
    #method to smooth frame
    thresh_frame=cv2.dilate(thresh_frame, None, iterations=2)
    #find the contour of the thresh_frame. findcontours or drawcontours method
    #drawcontours draws contour in an image
    #in this case we want to find the contour, find the area that contour defines
    #findcontours find contours and store in a tuple
    (cnts,_)=cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #copy not to modify the frame. method to get external contour 
    #filter out only contours needed
    for contour in cnts:
        if cv2.contourArea(contour) < 1000: #area less than 1000 pixels
            continue
        
        status=1
        #iterating in the for loop
        (x,y,w,h) = cv2.boundingRect(contour) # get the parameters of the contour
        #draw on color frame
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)

    status_list.append(status)

    status_list=status_list[-2:] #to save memory and just store the last two items

    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())

    cv2.imshow("Normal Frame",frame)
    cv2.imshow("Gray GaussianBlur Frameq",gray)
    cv2.imshow("Delta Frame",delta_frame)
    cv2.imshow("Thresh Delta Frame",thresh_frame)

    key=cv2.waitKey(1)
    #print(gray)
    #print(delta_frame)
    #print(thresh_frame)

    
    if key==ord('q'):
        if status==1:
            times.append(datetime.now())
        break
    
print(status_list)
print(times)

#generating data output with pandas
for i in range(0,len(times),2):
    df=df.append({"Start":times[i],"End":times[i+1]},ignore_index=True)

print(df)
df.to_csv("Times.csv")

video.release()
cv2.destroyAllWindows()