from machine import Pin, ADC, PWM
import utime

class Servo():
    def __init__(self, SERVO_PIN, duty_0=int(2**16/20), duty_180=int(2*(2**16)/20)):
        self.pwm = PWM(Pin(SERVO_PIN))
        self.pwm.freq(50)

        self.duty_0  = duty_0
        self.duty_180 = duty_180
        self.servoPosition = 0
        self.servoDirection = 0

    def posDegree(self, theta):
        # Servo moves between a dutycycle of 1ms to 2ms with a period of 20ms (0 -> 180 degree)
        theta_max = int(180)
        dutyRange = self.duty_180 - self.duty_0
        # dutyRange = (2**16/20)
        dutycycle = int(theta/theta_max * dutyRange + self.duty_0)
        self.pwm.duty_u16(dutycycle)
        return self.pwm.duty_u16()
    
    def sweep(self, speed, dt):
        # Control servo speed in degree per second
        # Max 180 degree min 0 degree
        # Set servoposition
        servo.posDegree(self.servoPosition)
        # Calculate stepsize acording to the speed
        stepsize = speed*dt
        # Servo sweep from 0 to 180 degree
        if(self.servoDirection == 0):
            self.servoPosition += stepsize
            if(self.servoPosition >= 180):
                self.servoPosition = 180
                self.servoDirection = 1
                
        if(self.servoDirection == 1):
            self.servoPosition -= stepsize
            if(self.servoPosition <= 0):
                self.servoPosition = 0
                self.servoDirection = 0

FSR_PIN = 28
SERVO_PIN = 15
SERVO_MIN = 1800 
SERVO_MAX = 8000

deltaServoTime = 50 # Period of everyloop 
servoSpeed = 100 # Topp speed is 90 degree a sec


sensor = ADC(Pin(FSR_PIN, Pin.IN))
servo = Servo(SERVO_PIN=SERVO_PIN, duty_0=SERVO_MIN, duty_180=SERVO_MAX)
oldServoTime = 0

#Initialize variables
tresh = 1                     #Treshold for attention algorithm  
speed_t = 0                     #Tail speed min,max(0,100)[%] 
k_h = 0.3                    #Variable for determing tail speed above treshold
k_l = 0.05                    #Variable for determing tail speed below treshold

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


startTime = utime.ticks_ms()

while(1):
    currentTime = utime.ticks_ms() - startTime
    # --------        Read sensor       ---------------- 
    
    value = sensor.read_u16()
    voltage = (value/2**16) * 3.3
    speed_t = Attention(voltage,speed_t)
    print("Spanning", round(voltage, 1), "Tijd in ms", currentTime)
    print("Tail speed", int(speed_t))
    led.duty_u16(int(speed_t*100))

    # --------        Read sensor       ---------------- 

    # --------        Get servo speed       ---------------- 
    # 0 -> 100 %
    
    # Max speed = 180 degree a sec
    # servoSpeed = 180 * x
    # --------        Get servo speed       ---------------- 


    # --------        Servo control     ----------------     
    if(currentTime > oldServoTime + deltaServoTime):
        servo.sweep(servoSpeed, deltaServoTime*10**-3)
        oldServoTime = currentTime
    # --------        Servo control     ---------------- 
  
