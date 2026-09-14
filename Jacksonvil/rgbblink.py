import time
import random
from machine import Pin, PWM

class rgb_led:
  def __init__(self,pin_r,pin_g,pin_b,freq = 1000):
    self.r = PWM(Pin(pin_r))
    self.g = PWM(Pin(pin_g))
    self.b = PWM(Pin(pin_b))

    self.r.freq(freq)
    self.g.freq(freq)
    self.b.freq(freq)

  def show_colour(self,rgb_tuple):
    #Converts from 0-255 to 65535-0
    r,g,b = rgb_tuple
    
    r_true = r*256
    self.r.duty_u16(r_true)

    g_true = g*256
    self.g.duty_u16(g_true)

    b_true = b*256
    self.b.duty_u16(b_true)

#Initialisation
led = rgb_led(18,19,20)
led1 = Pin(13, Pin.OUT)
led2 = Pin(11, Pin.OUT)

#Main loop
for i in range(100):
    led.show_colour((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255) ))
    led1.toggle()
    led2.toggle()
    time.sleep(0.05)

#Disable
led.show_colour((0,0,0))