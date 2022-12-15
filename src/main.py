from machine import Pin, ADC, PWM
from servo import Servo
import utime

led = PWM(Pin(25, Pin.OUT))
sensor = ADC(Pin(28, Pin.IN))

startTime = utime.ticks_ms()

while(1):
    currentTime = utime.ticks_ms() - startTime
    # --------        Read sensor       ---------------- 
    """""
    value = sensor.read_u16()
    voltage = (value/2**16) * 3.3
    print("Spanning", round(voltage, 1), "Tijd in ms", currentTime)
    utime.sleep_ms(10)
    """""
    # --------        Read sensor       ---------------- 

    # --------        Servo control     ---------------- 

    # --------        Servo control     ---------------- 
    
    utime.sleep_ms(10)
