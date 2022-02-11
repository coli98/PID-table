# Raspberry Pi + MG90S Servo PWM Control Python Code
#
#
import RPi.GPIO as GPIO
import time
import pigpio
import csv
import time
import cv2
# setup the GPIO pin for the servo
servo_pin = 12
servo_pin1 = 13
delay = 0.18

pwm = pigpio.pi() 
pwm.set_mode(servo_pin, pigpio.OUTPUT)
pwm.set_PWM_frequency( servo_pin, 50 )

pwm1 = pigpio.pi() 
pwm1.set_mode(servo_pin1, pigpio.OUTPUT)
pwm1.set_PWM_frequency( servo_pin1, 50 )
# setup PWM process
name_file= 'pomiar_predkosci.csv'

with open(name_file, 'w', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['czas[s]','wyjscie regulatora_x','wyjscie regulatora y',])
    start_time = time.time()

    while(1):
        current_time = time.time()
        print( "0 deg" )
        pwm.set_servo_pulsewidth( servo_pin, 1440) 
        pwm1.set_servo_pulsewidth( servo_pin1, 1560) 
        time.sleep(delay)
        elapsed_time = current_time - start_time
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([round(elapsed_time,2),1440, 1560])

        print( "-45 deg" )
        pwm.set_servo_pulsewidth( servo_pin, 1000) 
        pwm1.set_servo_pulsewidth( servo_pin1, 1000)
        elapsed_time = current_time - start_time
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([round(elapsed_time,2),1000, 1000])
        time.sleep(delay)
        print( "45 deg" )
        pwm.set_servo_pulsewidth( servo_pin, 2000) 
        pwm1.set_servo_pulsewidth( servo_pin1, 1000)
        elapsed_time = current_time - start_time
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([round(elapsed_time,2),2000, 1000])
        time.sleep(delay)
        print( "0 deg" )
        pwm.set_servo_pulsewidth( servo_pin, 2000) 
        pwm1.set_servo_pulsewidth( servo_pin1, 2000)
        elapsed_time = current_time - start_time
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([round(elapsed_time,2),2000, 2000])
        time.sleep(delay)
        print( "0 deg" )
        pwm.set_servo_pulsewidth( servo_pin, 1000) 
        pwm1.set_servo_pulsewidth( servo_pin1, 2000)
        elapsed_time = current_time - start_time
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([round(elapsed_time,2),1000, 2000])
        time.sleep(delay)
        key = cv2.waitKey(1)
        if key ==27:
        
            break
        

pwm.set_PWM_dutycycle(servo_pin, 0)
pwm.set_PWM_frequency( servo_pin, 0 )

pwm1.set_PWM_dutycycle(servo_pin1, 0)
pwm1.set_PWM_frequency( servo_pin1, 0)
