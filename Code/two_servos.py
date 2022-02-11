from gpiozero import AngularServo
from guizero import App, Slider, Text
from time import sleep

app=App(title="Servo_GUI", layout="grid")
s = AngularServo(12, min_angle=-90, max_angle=90)
s1 = AngularServo(13, min_angle=-90, max_angle=90)


def update_text():
    s.angle = int(slider.value)
    print("motor1: ", s.angle)
    s1.angle = int(slider1.value)
    print("motor2: ",s1.angle, "\n------------------------------------------------")
    

slider =Slider(app, start=-90, end=90, command=update_text, grid=[1,2])
slider1 =Slider(app, start=-90, end=90, command=update_text, grid=[2,2])


Text(app, "M1",grid=[1,1])
Text(app, "M2",grid=[2,1])

app.display()