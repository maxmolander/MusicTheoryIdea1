import numpy as np
import pandas as pd
import plotly.express as px
import simpleaudio as aud
from typing import Dict, List, Optional

#maps f1 fundamental frequency for any musical note letter name
noteToFreq: Dict[str, float] = {
    "A": 220.0,
    "A#": 233.08,
    "Bb": 233.08,
    "B": 246.94,
    "C": 261.63,
    "C#": 277.18,
    "Db": 277.18,
    "D": 293.66,
    "D#": 311.13,
    "Eb": 311.13,
    "E": 329.63,
    "F": 349.23,
    "F#": 369.99,
    "Gb": 369.99,
    "G": 196.0,
    "G#": 207.65,
    "Ab": 207.65
}

def getFreqForNote(noteName) -> Optional[float]:
    if noteName not in noteToFreq:
        print ("Please input a valid note name")
        return None
    return noteToFreq[noteName]

#maps frequency ratios based on chord quality
qualToRatios: Dict[str, List[float]] = {
    "Major":    [1.0, 5/4, 3/2, 2, 5/2, 3, 4, 5],
    "Major7":  [1.0, 5/4, 3/2, 15/8, 5/2, 3, 15/4, 5],
    "7":        [1.0, 5/4, 3/2, 7/4, 5/2, 3, 7/2, 5],
    "minor":    [1.0, 6/5, 3/2, 2, 12/5, 3, 4, 24/5],
    "minor7":   [1.0, 6/5, 3/2, 7/4, 12/5, 3, 7/2, 24/5] 
}

def getRatiosForQuality(quality) -> Optional[List[float]]:
    if quality not in qualToRatios:
        print("Please input a valid chord quality(Major, Major7, minor, minor7, or 7)")
        return None
    return qualToRatios[quality]

def chordBuilder8notes(noteName, quality) -> Optional[List[float]]:
    f1 = getFreqForNote(noteName)
    if f1 is None:
        return None

    ratios = getRatiosForQuality(quality)
    if ratios is None:
        return None

    return [f1 * m for m in ratios]

#combine and hold chord for T based on 
# calls: noteToFreq, chodBuilder8notes
def ChordHold(noteName, quality, fs, T, wt):
    f1 = getFreqForNote(noteName)

    if f1 is None:
        return None
    
    #build chord based on frequency ratios 
    eightNoteChord = chordBuilder8notes(noteName, quality)  
    if eightNoteChord is None:
        return None
    
    notes = 0 * wt

    #add sine waves for each of 8 notes, weighted lower is louder
    for f in eightNoteChord:
        notes = notes + (np.sin(f * wt)/(f*2/f1))  

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

#arpeggiates up through all 8 notes in the given numbeer of beats
def ArpEightSteps(noteName, quality, fs, T):
    f1 = getFreqForNote(noteName)
    eightNoteChord = chordBuilder8notes(noteName, quality)
    t=np.arange(0,T/8.0,1.0/fs)   
    wt = t * 2 * np.pi    
    notes = [0]

    if eightNoteChord is None:
            return None
    
    for f in eightNoteChord:
        notes = np.hstack((notes, np.sin(f * wt)))

    return notes[0:int(T*fs)]

