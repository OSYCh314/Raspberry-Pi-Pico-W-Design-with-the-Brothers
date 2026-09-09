from machine import Pin,PWM
from time import sleep

buzzer = PWM(Pin(16))
buzzer.freq(1000)
buzzer.duty_u16(32768)

def play_notes(buzzer,notes,dur):
    for ii in range(len(notes)):
        buzzer.freq(notes[ii])
        sleep(dur[ii])
        buzzer.duty_u16(0)
        buzzer.duty_u16(32768)
    
    buzzer.duty_u16(0)

notes = [349,392,261,392,440,523,466,440,392,349,392,261,261,261,261,294,294,329,329]
dur = [0.75,0.75,0.5,0.75,0.75,0.125,0.125,0.125,0.125,0.75,0.75,0.25,1.25,0.125,0.125,0.125,0.125,0.125,0.125]

new_notes = []
new_dur = []

for x in notes:
    new_notes.append(x*2)

for y in notes:
    new_dur.append(y*1.25)

play_notes(buzzer,new_notes,dur)
