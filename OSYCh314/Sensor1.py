import dht
from machine import Pin, PWM
import time

sensor = dht.DHT11(Pin(16,Pin.OUT,Pin.PULL_UP))
button = Pin(0, Pin.IN, Pin.PULL_UP)
buzzer = PWM(Pin(15))

buzzer.freq(523)
buzzer.duty_u16(0)

class rgb_led:
  def __init__(self,pin_r=0,pin_g=1,pin_b=2,freq = 1000):
    self.r = PWM(Pin(pin_r))
    self.g = PWM(Pin(pin_g))
    self.b = PWM(Pin(pin_b))

    self.r.freq(freq)
    self.g.freq(freq)
    self.b.freq(freq)

  def show_colour(self,rgb_tuple):
    #Converts from 0-255 to 65535-0
    r,g,b = rgb_tuple
    
    r_true = r*256 + 255
    self.r.duty_u16(r_true)

    g_true = g*256 + 255
    self.g.duty_u16(g_true)

    b_true = b*256 +255
    self.b.duty_u16(b_true)

led = rgb_led(12,13,14)

try:
    while True:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        if button.value() == 0:
            print("Temperature: {}°C, Humidity: {}%".format(temp, hum))
        
        if hum > 50:
            buzzer.duty_u16(32768)
            buzzer.freq(523)
            led.show_colour((128, 0, 0))  # Red
        elif hum > 47:
            buzzer.duty_u16(32768)
            buzzer.freq(440)
            led.show_colour((128, 128, 0))  # Yellow
        else:
            buzzer.duty_u16(0)
            led.show_colour((0, 128, 0))  # Green
except KeyboardInterrupt:
    buzzer.duty_u16(0)
    print("Program stopped by user.")
    led.show_colour((0, 0, 0))  # Turn off LED