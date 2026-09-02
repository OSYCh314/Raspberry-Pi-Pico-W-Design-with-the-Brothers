from machine import Pin, PWM
import dht
from I2C_LCD import screen
from RGB_LED import rgb_led

def get_colour(bounds,value,inverted = False): #Colour function to read the bounds
  if value < bounds[0] or value > bounds[-1]:
      return (128,0,128)
  if inverted:
    if value < bounds[1] or value > bounds[-2]:
      return (0,255,0)
    elif value < bounds[2] or value > bounds[-3]:
      return (255,255,0)
    else:
      return (255,0,0)
  else:
    if value < bounds[1] or value > bounds[-2]:
      return (255,0,0)
    elif value < bounds[2] or value > bounds[-3]:
      return (255,255,0)
    else:
      return (0,255,0)

#Set up the display
lcd = screen()
lcd.start()

#Set up the sensor
dht_sensor = dht.DHT11(Pin(16,Pin.OUT,Pin.PULL_UP))

#Set up the RGB LEDs
temp_led = rgb_led(3,4,5)
hum_led = rgb_led(6,7,8)

#Set up the bounds - temporary and can be changed
temp_bounds = [0,20,30,50,60,100]
hum_bounds = [0,20,30,50,60,100]
