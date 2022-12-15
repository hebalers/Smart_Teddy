from machine import Pin, PWM

class Servo():
    def __init__(self, SERVO_PIN, duty_0=(2**16)/20, duty_180=2*(2**16)/20):
        self.pwm = PWM(Pin(SERVO_PIN))
        self.pwm.freq(50)

        self.duty_0  = duty_0
        self.duty_180 = duty_180

    def posDegree(self, theta):
        # Servo moves between a dutycycle of 1ms to 2ms with a period of 20ms (0 -> 180 degree)
        theta_max = 180
        dutyRange = self.duty_180 - self.duty_0
        dutycycle = (theta/theta_max) * dutyRange + self.duty_0
        self.pwm.duty_u16(dutycycle)