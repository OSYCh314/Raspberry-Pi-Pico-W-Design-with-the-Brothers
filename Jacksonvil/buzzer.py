import time
from machine import Pin, PWM

def play_tone(frequency, duration_ms):
    if frequency == 0:
        # Frequency of 0 means silence/rest
        buzzer.duty_u16(0)
    else:
        buzzer.freq(frequency)     # Set the tone pitch
        buzzer.duty_u16(32768)    # Set volume / 50% duty cycle
        
    time.sleep_ms(duration_ms)
    buzzer.duty_u16(0)

buzzer_pin = Pin(16)
buzzer = PWM(buzzer_pin)

NOTES = {
    'C5': 523,
    'E5': 659,
    'G5': 784
}

# Play a simple arpeggio melody
play_tone(NOTES['C5'], 300)
time.sleep_ms(50) # Tiny pause between notes

play_tone(NOTES['E5'], 300)
time.sleep_ms(50)

play_tone(NOTES['G5'], 500)

# Properly release the PWM hardware resource when finished
buzzer.deinit()