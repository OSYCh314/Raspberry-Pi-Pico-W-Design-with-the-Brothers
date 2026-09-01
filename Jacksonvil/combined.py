import time
import random
from machine import Pin, PWM
import dht

button = Pin(0, Pin.IN, Pin.PULL_UP)

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
led = rgb_led(12,13,14)
led2 = rgb_led(11, 10, 9)
#led1 = Pin(n/a, Pin.OUT)
buzzer_pin = Pin(15)
buzzer = PWM(buzzer_pin)
sensor = dht.DHT11(Pin(16))

def measure():
    try:
        # Trigger a sensor measurement
        sensor.measure()
        
        # Read the temperature and humidity values
        temp = sensor.temperature()    # Returns temperature in Celsius
        hum = sensor.humidity()        # Returns relative humidity percentage
        
        # Print the results to the Shell
        #print(f"Temperature: {temp}°C | Humidity: {hum}%")

        return temp, hum
        
    except OSError as e:
        # Handle sensor reading failures (e.g., loose wires)
        print(f"Failed to read data from the DHT11 sensor. This is because of {e}.")

        return 0, 0

def play_tone(frequency, duration_ms):
    if frequency == 0:
        # Frequency of 0 means silence/rest
        buzzer.duty_u16(0)
    else:
        buzzer.freq(frequency)     # Set the tone pitch
        buzzer.duty_u16(32768)    # Set volume / 50% duty cycle
        
    time.sleep_ms(duration_ms)
    buzzer.duty_u16(0)

NOTES = {
    'C4': 262,
    'D4': 294,
    'E4': 330,
    'F4': 349,
    'G4': 392,
    'A4': 440,
    'B4': 494,

    'C5': 523,
    'D5': 587,
    'E5': 659,
    'F5': 698,
    'G5': 784,
    'A5': 880,
    'B5': 988,

    'C6': 1047,
    'D6': 1175,
    'E6': 1319,
    'F6': 1397,
    'G6': 1568,
    'A6': 1760,
    'B6': 1976,
}

notes = [
    'C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4',
    'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5',
    'C6', 'D6', 'E6', 'F6', 'G6', 'A6', 'B6'
]

#for note in notes:
#    play_tone(NOTES[note], 300)
#    time.sleep_ms(50)

ledtoggle = True

while True:

    temp, hum = measure()

    if ledtoggle == False:
       led.show_colour((0,0,0))
       led2.show_colour((0, 0,0))

    if hum < 54:
       if ledtoggle:
        led.show_colour((0, 0, 0))
        led2.show_colour((50, 50, 50))
       play_tone(0, 0)
    elif hum >= 54 and hum <= 57:
       if ledtoggle:
        led.show_colour((200, 200, 0)) 
        led2.show_colour((0, 0, 0))  
       play_tone(784, 120)
    elif hum > 57:
       if ledtoggle:
        led.show_colour((200, 0, 0))
        led2.show_colour((0, 0, 0))
       play_tone(1047, 50)

    print(temp, hum)

    if button.value() == 0:  # Button is pressed (LOW)
        if ledtoggle == True:
            ledtoggle = False
            play_tone(784, 100)   # G5 — turning OFF
            print("False")
        elif ledtoggle == False:
            ledtoggle = True
            play_tone(880, 100)   # A5 — turning ON
            print("True")
    else:                    # Button is not pressed (HIGH)
        play_tone(0, 0)

'''
while True:
    if button.value() == 0:  # Button is pressed (LOW)
        led.show_colour((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255) )) 
        #led1.on()  
        play_tone(262, 150) 
    else:                    # Button is not pressed (HIGH)
        led.show_colour((0,0,0))
        #led1.off()
    time.sleep(0.1)
'''