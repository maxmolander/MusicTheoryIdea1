import numpy as np
import pandas as pd
import plotly.express as px
import simpleaudio as aud
from typing import Dict, List, Optional
import musicLogic as mus  #my library of music theory logic funtions

bpm = 100.0   #beats per minute
beats = 2.0   #number of beats per chord (default to 2)
T = 60.0*beats/bpm   #Period 
fs=44100     #sampling frequency             
pi=np.pi     
t=np.arange(0,T,1.0/fs)  #time samples
wt = t * 2 * pi   #multiplier to get freq to w for sin functions


#Generate on-off and off-on eighth note rhythms with 0s and 1s
eighths = mus.twoEighthNotesOnBeat(T,fs)   
eighthsRev = mus.twoEightNotesOffBeat(T,fs)   

#hold chord, multiply by rhythm, add with arpeggiator on opposite rhythm
chord1 = mus.ChordHold("F#", "minor", fs, T, wt)  
chord1 = chord1 * eighths   
chord1arp = mus.ArpEightSteps("F#", "minor", fs, T) 
chord1arp = chord1arp * eighthsRev  
chord1 = chord1/2 + chord1arp/2 

chord2arp = mus.ArpEightSteps("B","minor7",fs,T) 
chord2 = mus.ChordHold("B", "minor", fs, T, wt) 
chord2 = chord2 * eighthsRev
chord2 = chord2/2 + chord2arp

chord3 = mus.ChordHold("E", "7", fs, T, wt)
chord3 = chord3 * eighths
chord3 = chord3/2 + mus.ArpEightSteps("G", "7", fs, T)/2

chord4arp = mus.ArpEightSteps("A", "Major7", fs, T)
chord4 = mus.ChordHold("A", "Major7", fs, T, wt)
chord4 = chord4arp/2 + chord4/2

#concatenate chords together, normalize, 16-bit audio, play until done
audio=np.hstack((chord1, chord2, chord3, chord4))   
audio = audio * (2**15 - 1) / np.max(np.abs(audio)) 
audio = audio.astype(np.int16)                      
play_obj = aud.play_buffer(audio,1,2,fs)           
play_obj.wait_done()

#plot waveform
#fig = px.line(audio)                               
#fig.show()


