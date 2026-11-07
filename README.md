# Raspberry-Pi-Pico-W-Design-with-the-Brothers
This is some code for a Raspberry Pi Pico W with:
- an [I2C LCD 2x16 Display](https://www.jaycar.com.au/alphanumeric-dot-matrix-liquid-crystal-display-module-backlit/p/QP5516) with the corresponding [backpack](https://www.jaycar.com.au/arduino-compatible-lcd-i2c-port-expander-module/p/XC3706?srsltid=AfmBOoqkmIiEVycjD4T-cx-O_hNnfLRz8mOrgLI4cOCULVOfV21zELwt)
- Temperature and Humidity Sensor (DHT11)
- At least 1 RGB LED
- Optionally single coloured LEDs
- 3 buttons or a buzzer

Please note that the port numbers should be changed to be compatible.
Modules for the LCD display and the RGB LEDs are attached.

## Perquisites
- Micropython version >3.0
- 5V power required to power LCD screen (this can be supplied using USB)

## Notices
> [!important]
> This code is licensed under an AS-IS basis. Nothing here is guaranteed to work. Remember to double check your circuit wiring, port numbers and products (e.g., you cannot be using Arduino code for an ESP32). Also, this project is a school project only.

> [!caution]
> Risk of electrical shock! Always unplug before testing and wiring.

> [!warning]
> Risk of electrical fire! 5V and 3.3V are mixed. Please check if you have correct resistors and if the destination device supports the voltage.

Licensed under Apache 2.0.
