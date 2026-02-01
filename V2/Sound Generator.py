# Jonathan Ng
# Sound generator
# Simple GUI with allows user to input frequency, duration, and amplitude and plays a simple sine wave

from tkinter.ttk import Checkbutton
import numpy as np
import sounddevice as sd
import tkinter as tk
import sys


def on_click():
    textFreq = entry.get()
    if checkIfNum(textFreq):
        frequency = float(textFreq)
    else:
        frequency = 440

    textDur = entryDuration.get()
    if checkIfNum(textDur):
        duration = float(textDur)
    else:
        duration = 1.0

    textamp = entryAmplitude.get()
    if checkIfNum(textamp):
        amplitude = float(textamp)
    else:
        amplitude = 0.01
    textAttack = entryAttack.get()
    if checkIfNum(textAttack):
        attack = float(textAttack)
    else:
        attack = 1
    textDecay = entryDecay.get()
    if checkIfNum(textDecay):
        decay = float(textDecay)
    else:
        decay = 0.1
    textSustain = entrySustain.get()
    if checkIfNum(textSustain):
        sustain = float(textSustain)
    else:
        sustain = 0.5
    textRelease = entryRelease.get()
    if checkIfNum(textRelease):
        release = float(textRelease)
    else:
        release = 0.2
    if checkIfNum(entrySampleRate.get()):
        sampleRate = int(entrySampleRate.get())
    else:
        sampleRate = 44100
    if duration < (attack + decay + release):
        duration = attack + decay + release + 0.1
        
    sines = [sine_tone(frequency = 200 * i, amplitude=0.3 /i) for i in range(1, 31, 2)]
    sinesBeating = [sine_tone(200, 2, 0.01), sine_tone(205, 2, 0.01)]

    sine1 = sine_tone(frequency, duration, amplitude/1000, sample_rate=sampleRate)
    sine2 = sine_tone(frequency*2, duration, amplitude/2000, sample_rate=sampleRate)
    sine3 = sine_tone(frequency*4, duration, amplitude/3000, sample_rate=sampleRate)

    mysound = sine1 if chord_enabled.get() == 0 else sum([sine1, sine2, sine3])
    if(ADSR_enabled.get()==1):
        mysound = apply_envelope(mysound, [attack, decay, sustain, release], smaple_rate=sampleRate)
    # mysound3 = sum(sines)
    # mysound4 = sum(sinesBeating)
    # mysound2 = sine_tone(400, 1, 0.01)
    sd.play(mysound)
    sd.wait()
    print(sys.getsizeof(mysound))

def white_noise(
        duration: float =1.0,
        amplitude: float =0.01,
        sample_rate: int =11000
    ) -> np.ndarray:
    n_samples = int(duration * sample_rate)

    noise = np.random.uniform(-1, 1, n_samples)

    noise *= amplitude

    return noise

def sine_tone(
        frequency: float =222.0,
        duration: float =5.0,
        amplitude: float =0.01,
        sample_rate: int =8000
    ) -> np.ndarray:
    n_samples = int(duration * sample_rate)

    time_points = np.linspace(0, duration, n_samples, False)

    sine = np.sin(2 * np.pi * frequency * time_points)

    sine *= amplitude

    if(EightBit_enabled.get()==1):
        for i in range(0, len(sine), 16):
            sine[i:i+16] = sine[i]
    return sine

def apply_envelope(sound: np.array,
                    adsr:list,
                    smaple_rate: int=8000) ->np.array:
    sound = sound.copy()

    attack_samples = int(adsr[0] * smaple_rate)
    decay_samples = int(adsr[1] * smaple_rate)
    release_samples = int(adsr[3] * smaple_rate)
    sustain_samples = len(sound) - (attack_samples + decay_samples + release_samples)

    sound[:attack_samples] *= np.linspace(0, 1, attack_samples)

    sound[attack_samples:attack_samples + decay_samples] *= np.linspace(1, adsr[2], decay_samples)

    sound[attack_samples + decay_samples:attack_samples + decay_samples + sustain_samples] *= adsr[2]

    sound[attack_samples + decay_samples + sustain_samples:] *= np.linspace(adsr[2], 0, release_samples)
    return sound

def checkIfNum(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

frequency = 440.0
duration = 1.0
amplitude = 1
attack = 1
decay = 0.1
sustain = 0.5
release = 0.2
sampleRate = 8000
root = tk.Tk()
ADSR_enabled = tk.IntVar()
chord_enabled = tk.IntVar()
EightBit_enabled = tk.IntVar()

root.title("Sound Generator")

frame = tk.Frame(root)
frame.grid(row=0, column=0)

frequencyLabel = tk.Label(frame, text="Frequency (Hz):")
frequencyLabel.grid(row=0, column=0)

entry = tk.Entry(frame)
entry.grid(row=1, column=0)
entry.insert(0, (str(frequency)))

durationLabel = tk.Label(frame, text="Duration:")
durationLabel.grid(row=2, column=0)

entryDuration = tk.Entry(frame)
entryDuration.grid(row=3, column=0)
entryDuration.insert(0, (str(duration)))

amplitudeLabel = tk.Label(frame, text="Amplitude:")
amplitudeLabel.grid(row=4, column=0)

entryAmplitude = tk.Entry(frame)
entryAmplitude.grid(row=5, column=0)
entryAmplitude.insert(0, (str(amplitude)))

AttackLabel = tk.Label(frame, text="Attack:")
AttackLabel.grid(row=6, column=0)

entryAttack = tk.Entry(frame)
entryAttack.grid(row=7, column=0)
entryAttack.insert(0, (str(attack)))

DecayLabel = tk.Label(frame, text="Decay:")
DecayLabel.grid(row=8, column=0)

entryDecay = tk.Entry(frame)
entryDecay.grid(row=9, column=0)
entryDecay.insert(0, (str(decay)))

SustainLabel = tk.Label(frame, text="Sustain:")
SustainLabel.grid(row=10, column=0)

entrySustain = tk.Entry(frame)
entrySustain.grid(row=11, column=0)
entrySustain.insert(0, (str(sustain)))

ReleaseLabel = tk.Label(frame, text="Release:")
ReleaseLabel.grid(row=12, column=0)

entryRelease = tk.Entry(frame)
entryRelease.grid(row=13, column=0)
entryRelease.insert(0, (str(release)))

SampleRateLabel = tk.Label(frame, text="Sample Rate:")
SampleRateLabel.grid(row=14, column=0)

entrySampleRate = tk.Entry(frame)
entrySampleRate.grid(row=15, column=0)
entrySampleRate.insert(0, (str(sampleRate)))

ASDRbutton = Checkbutton(frame, text="Enable ASDR",variable = ADSR_enabled, 
                    onvalue = 1, 
                    offvalue = 0)
ASDRbutton.grid(row=16, column=0)
chordButton = Checkbutton(frame, text="Enable chord",variable = chord_enabled, 
                    onvalue = 1, 
                    offvalue = 0)
chordButton.grid(row=17, column=0)
EightBitbutton = Checkbutton(frame, text="Enable 8-bit",variable = EightBit_enabled, 
                    onvalue = 1, 
                    offvalue = 0)
EightBitbutton.grid(row=18, column=0)

entry_btn = tk.Button(frame, text="Play", command=on_click)
entry_btn.grid(row=0, column=1)

root.mainloop()
