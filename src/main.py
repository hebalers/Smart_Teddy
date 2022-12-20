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
        print(servo.servoPosition)

class Attention():
    def __init__(self,sensor,tresh,k_h,k_l,speed_t):
        self.tresh = tresh
        self.k_h = k_h
        self.k_l = k_l
        self.speed_t = speed_t

    def getServoSpeed(self,sensorValue):
        #Convert sensorValue to voltage data 
        self.voltage = (sensorValue/2**16) * 3.3

        # SensorValue is a above treshold
        if self.voltage >= self.tresh:
            diff = self.voltage - self.tresh
            self.speed_t += diff*self.k_h
            if self.speed_t > 100:
                self.speed_t = 100
        # SensorValue is a below treshold
        else:
            diff = self.tresh - self.voltage
            self.speed_t -= diff*self.k_l
            if self.speed_t < 0:
                self.speed_t = 0
        return self.speed_t

    

# --------        Global variables Servo       ----------------
FSR_PIN = 28
SERVO_PIN = 15
SERVO_MIN = 1800 
SERVO_MAX = 8000

deltaServoTime = 50             # Period of everyloop 
servoSpeed = 100                # Topp speed is 90 degree a sec
max_speed = 180                 # degree a sec

oldServoTime = 0


# --------        Global variables Attention       ----------------
TRESH = 1                       #Treshold for attention algorithm 
K_H = 0.3                       #Variable for determing tail speed above treshold
K_L = 0.05                      #Variable for determing tail speed below treshold 
SPEED_T = 0                     #Tail speed min,max(0,100)[%] 

deltaAttentionTime = 50         # Period of everyloop
oldAttentionTime = 0

# --------        Create objects       ----------------
sensor = ADC(Pin(FSR_PIN, Pin.IN))
servo = Servo(SERVO_PIN=SERVO_PIN, duty_0=SERVO_MIN, duty_180=SERVO_MAX)
attention = Attention(sensor,tresh=TRESH,k_h=K_H,k_l=K_L,speed_t=SPEED_T)


startTime = utime.ticks_ms()

while(1):
    currentTime = utime.ticks_ms() - startTime

    # --------        Get servo speed       ---------------- 
    if(currentTime > oldAttentionTime + deltaAttentionTime):
        #Read Sensor
        sensorValue = sensor.read_u16()
        #getServoCoefficient
        servoCoefficient = attention.getServoSpeed(sensorValue) #Value between (0,100) [%]
        servoSpeed = max_speed // 100 * servoCoefficient
        # print("Servo speed", servoSpeed)
        oldAttentionTime = currentTime

    # --------        Servo control     ----------------     
    if(currentTime > oldServoTime + deltaServoTime):
        servo.sweep(servoSpeed, deltaServoTime*10**-3)
        oldServoTime = currentTime
    
  
