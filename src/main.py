from machine import Pin, ADC, PWM
import utime

class Servo():
    def __init__(self, SERVO_PIN, duty_0=int(2**16/20), duty_180=int(2*(2**16)/20)):
        self.pwm = PWM(Pin(SERVO_PIN))
        self.pwm.freq(50)

        self.duty_0  = duty_0
        self.duty_180 = duty_180

    def posDegree(self, theta):
        # Servo moves between a dutycycle of 1ms to 2ms with a period of 20ms (0 -> 180 degree)
        theta_max = int(180)
        dutyRange = self.duty_180 - self.duty_0
        # dutyRange = (2**16/20)

        dutycycle = int(theta/theta_max * dutyRange + self.duty_0)
        self.pwm.duty_u16(dutycycle)
        return self.pwm.duty_u16()


FSR_PIN = 28

SERVO_PIN = 15

SERVO_MIN = 1800 
SERVO_MAX = 8000

deltaTime = 10 # Period of everyloop 

sensor = ADC(Pin(FSR_PIN, Pin.IN))
servo1 = Servo(SERVO_PIN=SERVO_PIN, duty_0=SERVO_MIN, duty_180=SERVO_MAX)

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
    for i in range(180):
        servo1.posDegree(i)
        print(i)
        utime.sleep_ms(10)
    for i in range(180):
        x = 180 - i
        servo1.posDegree(x)
        print(x)
        utime.sleep_ms(10)

        
        
        

    # --------        Servo control     ---------------- 
    
    utime.sleep_ms(deltaTime)
