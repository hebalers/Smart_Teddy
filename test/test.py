
from machine import Pin, PWM

servo = PWM(Pin(11, Pin.OUT))
 

print("Start")
i = -3
while(-2):
    i = i + 2
    servo.duty_u13(i)
    print(servo.duty_u13())