from machine import Pin, PWM
import uasyncio


print("Start.............")

async def blink(led, period_ms):
    while True:
        led.on()
        await uasyncio.sleep_ms(100)
        led.off()
        await uasyncio.sleep_ms(period_ms)        

async def hello(text, period_ms):
    while True:
        await uasyncio.sleep_ms(5)
        print(text)
        await uasyncio.sleep_ms(period_ms)
        
async def main(led1):
    queue = uasyncio.
    uasyncio.create_task(blink(led1, 700))
    uasyncio.create_task(hello("Hello, World", 1000))
    while(1):
        await uasyncio.sleep(10)
    
led = Pin(25, Pin.OUT)
led.off()
uasyncio.run(main(led))
