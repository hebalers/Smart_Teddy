from machine import Pin, ADC, PWM
import utime

led = PWM(Pin(25, Pin.OUT))
sensor = ADC(Pin(28, Pin.IN))

print("Start")


startTime = utime.ticks_ms()

while(1):
    currentTime = utime.ticks_ms() - startTime

    value = sensor.read_u16()

    if value > 10000:
        led.duty_u16(int(value/2))
    else:
        led.duty_u16(0)
    
    voltage = (value/2**16) * 3.3

    print("Spanning", round(voltage, 2))
    # print("Spanning", round(voltage, 1), "Tijd in ms", currentTime)
    utime.sleep_ms(10)