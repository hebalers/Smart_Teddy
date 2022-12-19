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

deltaServoTime = 50 # Period of everyloop 
servoSpeed = 100 # Topp speed is 90 degree a sec
servoPosition = 0
servoDirection = 0

sensor = ADC(Pin(FSR_PIN, Pin.IN))
servo1 = Servo(SERVO_PIN=SERVO_PIN, duty_0=SERVO_MIN, duty_180=SERVO_MAX)

startTime = utime.ticks_ms()
oldServoTime = 0
i = deltaServoTime

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
    if(currentTime > oldServoTime + deltaServoTime):
        # Control servo speed in degree per second
        # Max 180 degree min 0 degree
        # Set servoposition
        servo1.posDegree(servoPosition)
        # Calculate stepsize acording to the speed
        stepsize = servoSpeed*deltaServoTime*10**-3
        # Servo sweep from 0 to 180 degree
        if(servoDirection == 0):
            servoPosition = servoPosition + stepsize
            if(servoPosition >= 180):
                servoPosition = 180
                servoDirection = 1
        if(servoDirection == 1):
            servoPosition = servoPosition - stepsize
            if(servoPosition <= 0):
                servoPosition = 0
                servoDirection = 0

        oldServoTime = currentTime
        
        
        
        

    # --------        Servo control     ---------------- 
  
