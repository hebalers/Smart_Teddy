from machine import Pin, ADC, PWM
from servo import Servo
import utime

# Declare objects
LED_PIN = 25
ADC_PIN = 28

servo = Servo(25)
led = PWM(Pin(LED_PIN, Pin.OUT))
sensor = ADC(Pin(ADC_PIN, Pin.IN))

startTime = utime.ticks_ms()

while(1):
    currentTime = utime.ticks_ms() - startTime
    value = sensor.read_u16()

    if value > 10000:
        led.duty_u16(int(value/2))
    else:
        led.duty_u16(0)
    
    voltage = (value/2**16) * 3.3
    print("Spanning", round(voltage, 1), "Tijd in ms", currentTime)
    utime.sleep_ms(10)

