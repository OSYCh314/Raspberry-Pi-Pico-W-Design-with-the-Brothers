from machine import Pin
import dht
import time

# Initialize the DHT11 sensor
sensor = dht.DHT11(Pin(15))

def measure():
    try:
        # Trigger a sensor measurement
        sensor.measure()
        
        # Read the temperature and humidity values
        temp = sensor.temperature()    # Returns temperature in Celsius
        hum = sensor.humidity()        # Returns relative humidity percentage
        
        # Print the results to the Shell
        #print(f"Temperature: {temp}°C | Humidity: {hum}%")

        return 'Temp: '+str(temp)+'°C\nHum: '+str(hum)+'%%'
        
    except OSError as e:
        # Handle sensor reading failures (e.g., loose wires)
        print(f"Failed to read data from the DHT11 sensor. This is because of {e}.")

        return e

from machine import Pin, PWM, I2C
import time

# --- Hardware Configuration ---
# Match the pins configured inside diagram.json
import time
from machine import I2C, Pin

class Screen:
    def __init__(self, num=0, sda=0, scl=1, freq=400000):
        self.i2c = I2C(num, sda=Pin(sda), scl=Pin(scl), freq=freq)
        
        # Guard against empty scan list to prevent crashing if LCD isn't wired properly
        scan_results = self.i2c.scan()[0]
        if not scan_results:
            raise RuntimeError("No I2C devices found. Check your wiring!")
        self.I2C_ADDR = scan_results
        
        # --- LCD Bitmasks ---
        self.En = 0b00000100        # Enable bit (Clock trigger pin)
        self.Rs = 0b00000001        # Register Select bit (0 = Command, 1 = Data)
        self.Backlight = 0b00001000 # Pin mask to keep the panel illuminated

    def strobe(self, data):
        """Pulses the Enable pin to clock data into the HD44780."""
        # Write initial data state with backlight on
        self.i2c.writeto(self.I2C_ADDR, bytes([data | self.Backlight]))
        time.sleep_us(1) # Give the data lines a moment to settle
        
        # Pull Enable HIGH
        self.i2c.writeto(self.I2C_ADDR, bytes([data | self.En | self.Backlight]))
        time.sleep_us(1) # Pulse width MUST be at least 450ns. 1us is safe.
        
        # Pull Enable LOW
        self.i2c.writeto(self.I2C_ADDR, bytes([(data & ~self.En) | self.Backlight]))
        time.sleep_us(40) # Commands need execution time (minimum 37us)

    def send_byte(self, bits, mode):
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
        time.sleep_us(150) # Reduced from 5ms but still within spec
        self.strobe(0x03 << 4)
        time.sleep_ms(5)
        self.strobe(0x02 << 4) # Set to 4-bit mode
        
        # Configure display rules
        self.send_byte(0x28, 0) # Function Set: 4-bit, 2 lines, 5x8 font
        self.send_byte(0x0C, 0) # Display Control: Display ON, Cursor OFF
        self.send_byte(0x06, 0) # Entry Mode: Increment cursor right
        self.send_byte(0x01, 0) # Clear Display command
        time.sleep_ms(5)        # Clearing display needs a longer delay

    def display_line(self, string, line):
        """Maps the display target line to row DDRAM matrix addresses."""
        if line == 1:
            self.send_byte(0x80, 0) # Row 1 Start Address
        elif line == 2:
            self.send_byte(0xC0, 0) # Row 2 Start Address
            
        for char in string:
            self.send_byte(ord(char), self.Rs)

    def display(self, text):
        """Displays text, splitting by newline if present."""
        self.display_line(' '*16,1)
        self.display_line(' '*16,2)
        if '\n' in text:
            line1, line2 = text.split('\n', 1)
        else:
            line1, line2 = text, ""
            
        self.display_line(line1, 1)
        if line2:
            self.display_line(line2, 2)

lcd = Screen()

lcd.start()

while True:
    lcd.display(measure())
    time.sleep(1)