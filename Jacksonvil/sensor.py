from machine import Pin
import dht
import time

# Initialize the DHT11 sensor
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

        return e

print(measure())