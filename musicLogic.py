import numpy as np
import pandas as pd
import plotly.express as px
import simpleaudio as aud

#finds f1 fundamental frequency for any musical note letter name
def noteToFreq(noteName):
    if (noteName == "A"):
        f1 = 220.0
    elif (noteName == "A#" or noteName == "Bb"):
        f1 = 233.08
    elif (noteName == "B"):
        f1 = 246.94
    elif (noteName == "C"):
        f1 = 261.63
    elif (noteName == "C#" or noteName == "Db"):
        f1 = 277.18
    elif (noteName == "D"):
        f1 = 293.66
    elif (noteName == "D#" or noteName == "Eb"):
        f1 = 311.13
    elif (noteName == "E"):
        f1 = 329.63
    elif (noteName == "F"):
        f1 = 349.23
    elif (noteName == "F#" or noteName == "Gb"):
        f1 = 369.99
    elif (noteName == "G"):
        f1 = 196.0
    elif (noteName == "G#" or noteName == "Ab"):
        f1 = 207.65
    else:
        print("Please input a valid note name")
    
    return f1

#calculates f2-8 based on f1 and chord quality
def chordBuilder8notes(noteName, Quality):
    f1 = noteToFreq(noteName)
    if (Quality == "Major7"):
        f2=f1*5/4
        f3=f1*3/2
        f4=f1*15/8
        f5=f1*5/2
        f6=f1*3
        f7=f1*15/4
        f8=f1*5
    elif (Quality == "Major"):
        f2=f1*5/4
        f3=f1*3/2
        f4=f1*2
        f5=f1*5/2
        f6=f1*3
        f7=f1*4
        f8=f1*5
    elif (Quality == "minor"):
        f2=f1*6/5
        f3=f1*3/2
        f4=f1*2
        f5=f1*12/5
        f6=f1*3
        f7=f1*4
        f8=f1*24/5
    elif (Quality == "minor7"):
        f2=f1*6/5
        f3=f1*3/2
        f4=f1*7/4
        f5=f1*12/5
        f6=f1*3
        f7=f1*7/2
        f8=f1*24/5
    elif (Quality == "7"):
        f2=f1*5/4
        f3=f1*3/2
        f4=f1*7/4
        f5=f1*5/2
        f6=f1*3
        f7=f1*7/2
        f8=f1*5
    else:
        print("Please input a valid chord quality(Major, Major7, minor, minor7, or 7)")
    
    return [f2, f3, f4, f5, f6, f7, f8]

#combine and hold chord for T based on 
# calls: noteToFreq, chodBuilder8notes
def ChordHold(noteName, Quality, fs, T, wt):
    #find fundamental frequency based on note name e.g. C or Eb
    f1 = noteToFreq(noteName)
    
    #build chord based on frequency ratios associated with chord quality e.g. Major7
    eightNoteChord = chordBuilder8notes(noteName, Quality)  #returns f2-8
    
    #start with sine wave of fundatmental
    notes = np.sin(f1 * wt)

    #add sine waves of the other 7 notes, weighted
    for i in eightNoteChord:
        notes = notes + (np.sin(i * wt)/(i*2/f1))  #weights lower notes louder based on ratio to fundamental

    return notes[0:int(T*fs)]

#generates ones and zeros to multiply for on-off eighth notes
def twoEighthNotesOnBeat(T, fs):
    ones = int(np.round(T*fs/4))
    envpt1 = np.ones(ones)
    zeros = np.zeros(int(np.round((T*fs/2)-ones)))

    envelope = np.hstack((envpt1, zeros))
    envelope = np.hstack((envelope, envelope))
    return envelope[0:int(T*fs)]
#generates zeros and ones to multiply for off-on eighth notes
def twoEightNotesOffBeat(T,fs):
    ones = int(np.round(T*fs/4))
    envpt1 = np.ones(ones)
    zeros = np.zeros(int(np.round((T*fs/2)-ones)))

    envelope = np.hstack((zeros, envpt1))
    envelope = np.hstack((envelope, envelope))
    return envelope[0:int(T*fs)]

#arpeggiates through all 8 notes in the given numbeer of beats
def ArpEightSteps(noteName, Quality, fs, T):
    f1 = noteToFreq(noteName)
    eightNoteChord = chordBuilder8notes(noteName, Quality)
    t=np.arange(0,T/8.0,1.0/fs)                             #samples in time based of period and sampling frequenccy
    wt = t * 2 * np.pi                                     #multiplier to get freq to w for sin functions  
    notes = np.sin(f1*wt)
    for i in eightNoteChord:
        notes = np.hstack((notes, np.sin(i * wt)))
    return notes[0:int(T*fs)]

