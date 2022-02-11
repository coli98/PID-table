import cv2
import numpy as np
import RPi.GPIO as GPIO
import time
import pigpio
from simple_pid import PID
import csv
from guizero import App, Slider, Text
import datetime
#controller settings
P=0.22
I=0.12
D=0.25

P_y=0.13
I_y=0.08
D_y=0.15
target=0
upper_limit=450
lower_limit=-450
#X:
pid = PID(-P, -I, -D, setpoint=target)
pid.output_limits = (lower_limit, upper_limit)
#Y:
pid_y = PID(P_y, I_y, D_y, setpoint=target)
pid_y.output_limits = (lower_limit, upper_limit)

pid.sample_time = 0.001
cap = cv2.VideoCapture(0)
position = 1500#deg
servo_pin_x = 12
servo_pin_y = 13
center_x = 1440
pwm = pigpio.pi() 
pwm.set_mode(servo_pin_x, pigpio.OUTPUT)
pwm.set_PWM_frequency( servo_pin_x, 50 )

pwm1 = pigpio.pi() 
pwm1.set_mode(servo_pin_y, pigpio.OUTPUT)
pwm1.set_PWM_frequency( servo_pin_y, 50 )

pwm.set_servo_pulsewidth( servo_pin_x, 1440) 
pwm1.set_servo_pulsewidth( servo_pin_y, 1560)
time.sleep(0.16)

cap.set(3, 640)
cap.set(4, 480)
_, frame = cap.read()
rows, cols, _ = frame.shape
x_medium = int(cols/2)
center_x = int(cols/2)
y_medium = int(rows/2)
center_y = int(rows/2)

prev_frame_time = 0
new_frame_time = 0

#file name
now=datetime.datetime.now()
t=now.strftime('%H_%M_%S')
name_file='P='+ str(P_y) + 'I='+ str(I_y) + 'D=' + str(D_y) + t +'.csv'

with open(name_file, 'w', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['czas[s]', 'pozycja_y[pixel]', 'wyjscie_y', 'bład errox_y', 'P=' + str(P_y), 'I= ' + str(I_y), 'D= ' + str(D_y)])
    start_time = time.time()

    while True:
        #cureent time     
        current_time = time.time()
        _, frame = cap.read()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        #ping pong
        low_red = np.array([17,137,101])
        high_red = np.array([20, 245, 172])

        font = cv2.FONT_HERSHEY_SIMPLEX
        new_frame_time = time.time()
        
        fps = 1/(new_frame_time-prev_frame_time)
        prev_frame_time = new_frame_time
        
        fps = int(fps)
        fps = str(fps)
        #hortex nut
        #low_red = np.array([98,61,36])
        #high_red = np.array([139, 176, 94])
        
        red_mask = cv2.inRange(hsv_frame, low_red, high_red)
        contours,hierachy=cv2.findContours(red_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
        
        for cnt in contours:
            (x,y,w,h) = cv2.boundingRect(cnt)
            
            #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            x_medium = int((x + x + w) / 2)
            y_medium = int((y + y + h) / 2)
            break
        
        cv2.line(frame, (x_medium,0), (x_medium, 480), (0, 255,0),2)
        cv2.line(frame, (0,y_medium), (640, y_medium), (0, 255,0),2)
        cv2.line(frame, (center_x, 0), (center_x, 480), (255, 0, 0),2)
        cv2.line(frame, (0,center_y), (640, center_y), (255, 0,0),2)
        cv2.putText(frame, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)
        error_x = x_medium - center_x
        error_y = y_medium - center_y
        
        print('x= ', x_medium, 'y= ', y_medium, 'uchyb x= ', error_x, 'uchyb y = ', error_y)
        
        cv2.imshow("Frame", frame)
        #cv2.imshow("", red_mask)
        key = cv2.waitKey(1)
        
        
        output = pid(error_x)
        output_y = pid_y(error_y)
        
        print('out put_x = ', round(output))
        print('out put_y = ', round(output_y))

        #pwm.set_servo_pulsewidth( servo_pin_x, 1440 + round(output))
        pwm1.set_servo_pulsewidth( servo_pin_y, 1560 + round(output_y))
        
        elapsed_time = current_time - start_time
        print('czas petli to= ', round(elapsed_time,2) )
        csvwriter = csv.writer(csvfile)
        #csvwriter.writerow([round(elapsed_time,2), x_medium, round(output), error_x, error_y, round(output_y)]) #, output])
        csvwriter.writerow([round(elapsed_time,2), y_medium, round(output_y), error_y]) #, output])


        if key ==27:
        
            break

pwm.set_PWM_dutycycle(servo_pin_y, 0)
pwm.set_PWM_frequency( servo_pin_y, 0 )
 
pwm1.set_PWM_dutycycle(servo_pin_x, 0)
pwm1.set_PWM_frequency( servo_pin_x, 0 )    
    

cv2.destroyAllWindows()



