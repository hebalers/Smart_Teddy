from machine import Pin, ADC, PWM
import utime

led = PWM(Pin(25, Pin.OUT))
sensor = ADC(Pin(28, Pin.IN))

#Initialize variables
tresh = 1                     #Treshold for attention algorithm  
speed_t = 0                     #Tail speed min,max(0,100)[%] 
k_h = 0.3                    #Variable for determing tail speed above treshold
k_l = 0.009                     #Variable for determing tail speed below treshold
startTime = utime.ticks_ms()    #Start time 



def Attention(voltage, speed_t):
    if voltage >= tresh:
        diff = voltage - tresh
        speed_t += diff*k_h
        if speed_t > 100:
            speed_t = 100
    else:
        diff = tresh - voltage
        speed_t -= diff*k_l
        if speed_t < 0:
            speed_t = 0

    return speed_t

while(1):
    currentTime = utime.ticks_ms() - startTime
    # --------        Read sensor       ---------------- 
    
    value = sensor.read_u16()
    voltage = (value/2**16) * 3.3

   
    speed_t = Attention(voltage,speed_t)
    print("Spanning", round(voltage, 1), "Tijd in ms", currentTime)
    print("Tail speed", int(speed_t))

    # --------        Read sensor       ---------------- 

    # --------        Servo control     ---------------- 

    utime.sleep_ms(10)
