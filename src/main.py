from machine import Pin, ADC, PWM
import utime

led = PWM(Pin(25, Pin.OUT))
sensor = ADC(Pin(28, Pin.IN))

print("Start")

#Initialize variables
tresh = 1.4                     #Treshold for attention algorithm  
speed_t = 0                     #Tail speed min,max(0,100)[%] 
k = 0.005                       #Variable for determing tail speed
startTime = utime.ticks_ms()    #Start time 


def Attention(voltage, speed_t):
    if voltage >= tresh:
        diff = voltage - tresh
        speed_t += diff*k
        if speed_t < 100:
            speed_t = 100
    else:
        diff = tresh - voltage
        speed_t -= diff*k
        if speed_t < 0:
            speed_t = 0

    return speed_t

while(1):
    currentTime = utime.ticks_ms() - startTime
    value = sensor.read_u16()
    voltage = (value/2**16) * 3.3

    print("Spanning", round(voltage, 2))

    utime.sleep_ms(10)