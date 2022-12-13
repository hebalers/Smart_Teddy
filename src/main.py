from machine import Pin, ADC, PWM
import utime


led = PWM(Pin(25, Pin.OUT))
sensor = ADC(Pin(28, Pin.IN))

print("Start")

while(1):
    value = sensor.read_u16()

    if value > 10000:
        led.duty_u16(int(value/2))
    else:
        led.duty_u16(0)
    print(value, "Hi")
    # print(servo.duty_u16())
    utime.sleep_ms(10)

