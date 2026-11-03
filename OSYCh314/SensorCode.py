from machine import Pin, PWM, I2C
import time
import dht

# --- Hardware Configuration ---
# Match the pins configured inside diagram.json
class screen:
  def __init__(self, num = 0, sda = 0, scl = 1, freq=400000):
    self.i2c = I2C(num, sda=Pin(sda), scl=Pin(scl), freq=freq)
    self.I2C_ADDR = self.i2c.scan()[0]  # Default address for the Wokwi I2C LCD component
  # --- LCD Bitmasks ---
    self.En = 0b00000100        # Enable bit (Clock trigger pin)
    self.Rs = 0b00000001        # Register Select bit (0 = Command, 1 = Data)
    self.Backlight = 0b00001000 # Pin mask to keep the panel illuminated
  
  def strobe(self,data):
      """Pulses the Enable pin to clock data into the HD44780."""
      # Write initial data state with backlight on
      self.i2c.writeto(self.I2C_ADDR, bytes([data | self.Backlight]))
      # Pull Enable HIGH
      self.i2c.writeto(self.I2C_ADDR, bytes([data | self.En | self.Backlight]))
      # Pull Enable LOW
      self.i2c.writeto(self.I2C_ADDR, bytes([(data & ~self.En) | self.Backlight]))
  
  def send_byte(self,bits, mode):
      """Splits an 8-bit byte into 4-bit nibbles for the hardware."""
      high_nibble = mode | (bits & 0xF0)
      low_nibble = mode | ((bits << 4) & 0xF0)
      
      self.strobe(high_nibble)
      self.strobe(low_nibble)
  
  def start(self):
      """Wakes the display up in 4-bit operational mode."""
      time.sleep_ms(50)
      self.strobe(0x03 << 4)
      time.sleep_ms(5)
      self.strobe(0x03 << 4)
      time.sleep_ms(5)
      self.strobe(0x03 << 4)
      time.sleep_ms(1)
      self.strobe(0x02 << 4) # Set to 4-bit mode
      
      # Configure display rules
      self.send_byte(0x28, 0) # Function Set: 4-bit, 2 lines, 5x8 font
      self.send_byte(0x0C, 0) # Display Control: Display ON, Cursor OFF
      self.send_byte(0x06, 0) # Entry Mode: Increment cursor right
      self.send_byte(0x01, 0) # Clear Display command
      time.sleep_ms(5)
  
  def display_line(self,string, line):
      """Maps the display target line to row DDRAM matrix addresses."""
      if line == 1:
          self.send_byte(0x80, 0) # Row 1 Start Address
      elif line == 2:
          self.send_byte(0xC0, 0) # Row 2 Start Address
          
      for char in string:
          self.send_byte(ord(char), self.Rs)
  
  def display(self,str):
    line1, line2 = str.split('\n')
    self.display_line(line1,1)
    self.display_line(line2,2)

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
    
    r_true = r*256
    self.r.duty_u16(r_true)

    g_true = g*256
    self.g.duty_u16(g_true)

    b_true = b*256
    self.b.duty_u16(b_true)

lcd = screen()
lcd.start()
lcd.display('Values\nSettings')

led1 = rgb_led(18,19,20)
buzzer = PWM(Pin(16))

page = 'Home'
scrolldown = 0
inverted = False
sensor = dht.DHT11(Pin(15))
temps = [20,30,40,50]
hums = [30,50,60,80]
Home = ['Values','Settings']
edit_settings = False
movement = 2

led = rgb_led(18,19,20)
led2 = rgb_led(18,19,20)

buttonf = Pin(12, Pin.IN, Pin.PULL_DOWN)
buttonb = Pin(11, Pin.IN, Pin.PULL_DOWN)
buttons = Pin(13, Pin.IN, Pin.PULL_DOWN)

def button_pressed():
    global buttonf, buttonb, buttons, movement
    if buttons.value() == 1:
        movement = 0
    elif buttonf.value() == 1:
        movement = 1
    elif buttonb.value() == 1:
        movement = -1
    else:
        movement = 2
    
    return movement

click = False

buzzer.freq(1000)
buzzer.duty_u16(0)

while True:
    click = False
    if page == 'Values' and scrolldown != 2:
        sensor.measure()
    temp, hum = sensor.temperature(), sensor.humidity()
    #print(temp,hum,scrolldown)
    Values = ['Temp: %.2f'%temp+'°C','Humidity: %.2f'%hum+"%",'Back ->']
    Settings = ['Temperature','Humidity','Inverted: %s'%inverted,'Back ->']
    Temperature = ['Min: %.2f'%temps[0],'Ideal Min: %.2f'%temps[1],'Ideal Max: %.2f'%temps[2],'Max: %.2f'%temps[3],'Back ->']
    Humidity = ['Min: %.2f'%hums[0],'Ideal Min: %.2f'%hums[1],'Ideal Max: %.2f'%hums[2],'Max: %.2f'%hums[3],'Back ->']
    second_line = eval(page+'[%d]'%scrolldown)
    lcd.display(page+' '*(16-len(page))+'\n'+second_line+' '*(16-len(second_line)))

    movement = button_pressed()
    
    if movement == 1 and not edit_settings and not click:
        scrolldown += 1
        scrolldown %= eval('len('+page+')')
        click = True
    if movement ==1 and edit_settings and not click:
        if page == 'Temperature':
            exec('temps[%d]'%scrolldown + '+= 1')
        if page == 'Humidity':
            exec('hums[%d]'%scrolldown + '+= 1')
        click = True
    if movement == -1 and not edit_settings and not click:
        scrolldown -= 1
        scrolldown %= eval('len('+page+')')
        click = True
    if movement == -1 and edit_settings and not click and not click:
        if page == 'Temperature':
            exec('temps[%d]'%scrolldown + '-= 1')
        if page == 'Humidity':
            exec('hums[%d]'%scrolldown + '-= 1')
        click = True
    if movement == 0 and second_line != 'Back ->' and not ':' in second_line and not click:
        page = second_line
        scrolldown = 0
        click = True
    if movement == 0 and second_line == 'Back ->' and not click:
        if page == 'Values' or page == 'Settings':
            page = 'Home'
        if page == 'Temperature' or page == 'Humidity':
            page = 'Settings'
        scrolldown = 0
        click = True
    if movement == 0 and page != 'Values' and second_line[-1].isdigit() and not click:
        edit_settings += 1
        edit_settings %= 2
        edit_settings = bool(edit_settings)
        click = True
    if movement == 0 and page == 'Settings' and scrolldown == 2 and not click:
        inverted += 1
        inverted %= 2
        inverted = bool(inverted)
        click = True
    
    sound = 0
    
    if hum > hums[3] or hum < hums[0]:
        if inverted:
            led.show_colour((0, 128, 0))  # Green
        else:
            led.show_colour((128, 0, 0))  # Red
            sound += 1
    elif hum > hums[2] or hum < hums[1]:
        led.show_colour((128, 128, 0))  # Yellow
    else:
        if inverted:
            led.show_colour((128, 0, 0))  # Red
            sound +=1
        else:
            led.show_colour((0, 128, 0))  # Green
    
    if temp > temps[3] or temp < temps[0]:
            if inverted:
                led2.show_colour((0, 128, 0))  # Green
            else:
                led2.show_colour((128, 0, 0))  # Red
                sound += 1
    elif temp > temps[2] or temp < temps[1]:
        led2.show_colour((128, 128, 0))  # Yellow
    else:
        if inverted:
            led2.show_colour((128, 0, 0))  # Red
            sound +=1
        else:
            led2.show_colour((0, 128, 0))  # Green
    
    if sound:
        buzzer.duty_u16(32768)
    else:
        buzzer.duty_u16(0)
    time.sleep(0.1)