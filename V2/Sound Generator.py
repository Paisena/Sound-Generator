# Jonathan Ng
# Sound generator
# Simple GUI with allows user to input frequency, duration, and amplitude and plays a simple sine wave

from tkinter.ttk import Checkbutton
import numpy as np
import sounddevice as sd
import tkinter as tk
import sys
import wave 

def getSoundValues():
    textFreq = entryFrequency.get()
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
    if ADSR_enabled.get() == 1:
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
    return mysound

def on_click():
    textFreq = entryFrequency.get()
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
    if ADSR_enabled.get() == 1:
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
    sd.play(mysound, samplerate=sampleRate)
    sd.wait()
    #print(sys.getsizeof(mysound))

#region Sound Generation Functions

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

#endregion
def checkIfNum(str):
    try:
        float(str)
        return True
    except ValueError:
        return False
#region GUI Helper func

def ADRSSwitch():
    if ADSR_enabled.get() == 1:
        attackLabel.config(state=tk.NORMAL)
        attackSlider.config(state=tk.NORMAL)
        entryAttack.config(state=tk.NORMAL) 
        decayLabel.config(state=tk.NORMAL)
        decaySlider.config(state=tk.NORMAL) 
        entryDecay.config(state=tk.NORMAL)
        sustainLabel.config(state=tk.NORMAL)
        sustainSlider.config(state=tk.NORMAL)
        entrySustain.config(state=tk.NORMAL) 
        releaseSlider.config(state=tk.NORMAL)
        releaseLabel.config(state=tk.NORMAL)
        entryRelease.config(state=tk.NORMAL)
        
    else:
        attackSlider.config(state=tk.DISABLED)
        attackLabel.config(state=tk.DISABLED)
        entryAttack.config(state=tk.DISABLED) 
        decaySlider.config(state=tk.DISABLED)
        decayLabel.config(state=tk.DISABLED)
        entryDecay.config(state=tk.DISABLED)
        sustainSlider.config(state=tk.DISABLED)
        sustainLabel.config(state=tk.DISABLED)
        entrySustain.config(state=tk.DISABLED)
        releaseSlider.config(state=tk.DISABLED)
        releaseLabel.config(state=tk.DISABLED)
        entryRelease.config(state=tk.DISABLED)
    updateLabels("")

def updateFrequency(var, index, mode):
    if checkIfNum(entryFrequency.get()):
        frequencySlider.set(float(entryFrequency.get()))

def updateDuration(var, index, mode):
    if checkIfNum(entryDuration.get()):
        durationSlider.set(float(entryDuration.get()))

def updateAmplitude(var, index, mode):
    if checkIfNum(entryAmplitude.get()):
        amplitudeSlider.set(float(entryAmplitude.get()))

def updateAttack(var, index, mode):
    if checkIfNum(entryAttack.get()):
        attackSlider.set(float(entryAttack.get()))

def updateDecay(var, index, mode):
    if checkIfNum(entryDecay.get()):
        decaySlider.set(float(entryDecay.get()))

def updateSustain(var, index, mode):
    if checkIfNum(entrySustain.get()):
        sustainSlider.set(float(entrySustain.get()))

def updateRelease(var, index, mode):
    if checkIfNum(entryRelease.get()):
        releaseSlider.set(float(entryRelease.get()))

def updateSliders(var, index, mode):
    updateFrequency("", "", "")
    updateDuration("", "", "")
    updateAmplitude("", "", "")
    updateAttack("", "", "")
    updateDecay("", "", "")
    updateSustain("", "", "")
    updateRelease("", "", "")
    

def updateLabels(var):
    entryFrequency.delete(0, tk.END)
    entryFrequency.insert(0, (str(frequencySlider.get())))

    entryDuration.delete(0, tk.END)
    entryDuration.insert(0, (str(durationSlider.get())))

    entryAmplitude.delete(0, tk.END)
    entryAmplitude.insert(0, (str(amplitudeSlider.get())))

    entryAttack.delete(0, tk.END)
    entryAttack.insert(0, (str(attackSlider.get())))

    entryDecay.delete(0, tk.END)
    entryDecay.insert(0, (str(decaySlider.get())))

    entrySustain.delete(0, tk.END)
    entrySustain.insert(0, (str(sustainSlider.get())))

    entryRelease.delete(0, tk.END)
    entryRelease.insert(0, (str(releaseSlider.get())))
    updateSliders("", "", "")

def exportSound():

    with wave.open('output.wav', 'w') as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(sampleRate/2)
        sound = getSoundValues()

        sound = np.int16(sound * 32767)

        f.writeframes(sound.tobytes())
        print(sampleRate)
#endregion

#region main

frequency = 440.0
duration = 1.0
amplitude = 5
attack = 1
decay = 0.1
sustain = 0.5
release = 0.2
sampleRate = 44100
root = tk.Tk()
ADSR_enabled = tk.IntVar()
chord_enabled = tk.IntVar()
EightBit_enabled = tk.IntVar()


root.title("Sound Generator")

frame = tk.Frame(root)
frame.grid(row=0, column=0)

# Frequncy
frequencyLabel = tk.Label(frame, text="Frequency (Hz):")
frequencyLabel.grid(row=0, column=0)
frequencySlider = tk.Scale(frame, variable=frequency,from_=100, to=1000, orient=tk.HORIZONTAL, command=updateLabels)
frequencySlider.set(frequency)
frequencySlider.grid(row=1, column=0)

svF = tk.StringVar()
svF.trace_add('write', updateFrequency)

entryFrequency = tk.Entry(frame, textvariable=svF)
entryFrequency.grid(row=2, column=0)
entryFrequency.insert(0, (str(frequencySlider.get())))

# Duration
durationLabel = tk.Label(frame, text="Duration:")
durationLabel.grid(row=3, column=0)
durationSlider = tk.Scale(frame, variable=duration, from_=0.1, to=10, orient=tk.HORIZONTAL, command=updateLabels, resolution=0.1)
durationSlider.set(duration)
durationSlider.grid(row=4, column=0)

svD = tk.StringVar()
svD.trace_add('write', updateDuration)

entryDuration = tk.Entry(frame, textvariable=svD)
entryDuration.grid(row=5, column=0)
entryDuration.insert(0, (str(durationSlider.get())))

# Amplitude
amplitudeLabel = tk.Label(frame, text="Amplitude:")
amplitudeLabel.grid(row=6, column=0)
amplitudeSlider = tk.Scale(frame, variable=amplitude, from_=1, to=100, orient=tk.HORIZONTAL, command=updateLabels)
amplitudeSlider.set(amplitude)
amplitudeSlider.grid(row=7, column=0)

svAmp = tk.StringVar()
svAmp.trace_add('write', updateAmplitude)
entryAmplitude = tk.Entry(frame, textvariable=svAmp)
entryAmplitude.grid(row=8, column=0)
entryAmplitude.insert(0, (str(amplitudeSlider.get())))

# Attack
attackLabel = tk.Label(frame, text="Attack:", state=tk.DISABLED)
attackLabel.grid(row=9, column=0)
attackSlider = tk.Scale(frame, variable=attack, from_=0.1, to=5, orient=tk.HORIZONTAL, command=updateLabels, resolution=0.1, state=tk.DISABLED)
attackSlider.set(attack)
attackSlider.grid(row=10, column=0)

svA = tk.StringVar()
svA.trace_add('write', updateAttack)
entryAttack = tk.Entry(frame, state=tk.DISABLED, textvariable=svA)
entryAttack.grid(row=11, column=0)
entryAttack.insert(0, (str(attackSlider.get())))

# Decay
decayLabel = tk.Label(frame, text="Decay:", state=tk.DISABLED)
decayLabel.grid(row=12, column=0)
decaySlider = tk.Scale(frame, variable=decay, from_=0.1, to=5, orient=tk.HORIZONTAL, command=updateLabels, resolution=0.1, state=tk.DISABLED)
decaySlider.set(decay)
decaySlider.grid(row=13, column=0)

svDecay = tk.StringVar()
svDecay.trace_add('write', updateDecay)
entryDecay = tk.Entry(frame, state=tk.DISABLED, textvariable=svDecay)
entryDecay.grid(row=14, column=0)
entryDecay.insert(0, (str(decaySlider.get())))

# Sustain
sustainLabel = tk.Label(frame, text="Sustain:", state=tk.DISABLED)
sustainLabel.grid(row=15, column=0)
sustainSlider = tk.Scale(frame, variable=sustain, from_=0.1, to=1, orient=tk.HORIZONTAL, command=updateLabels, resolution=0.1, state=tk.DISABLED)
sustainSlider.set(sustain)
sustainSlider.grid(row=16, column=0)

svSustain = tk.StringVar()
svSustain.trace_add('write', updateSustain)
entrySustain = tk.Entry(frame, state=tk.DISABLED, textvariable=svSustain)
entrySustain.grid(row=17, column=0)
entrySustain.insert(0, (str(sustainSlider.get())))

# Release
releaseLabel = tk.Label(frame, text="Release:", state=tk.DISABLED)
releaseLabel.grid(row=18, column=0)
releaseSlider = tk.Scale(frame, variable=release, from_=0.1, to=5, orient=tk.HORIZONTAL, command=updateLabels, resolution=0.1, state=tk.DISABLED)
releaseSlider.set(release)
releaseSlider.grid(row=19, column=0)

svRelease = tk.StringVar()
svRelease.trace_add('write', updateRelease)
entryRelease = tk.Entry(frame, state=tk.DISABLED, textvariable=svRelease)
entryRelease.grid(row=20, column=0)
entryRelease.insert(0, (str(releaseSlider.get())))

ASDRbutton = Checkbutton(frame, text="Enable ASDR",variable = ADSR_enabled, 
                    onvalue = 1, 
                    offvalue = 0,
                    command=ADRSSwitch)
ASDRbutton.grid(row=21, column=0)
chordButton = Checkbutton(frame, text="Enable chord",variable = chord_enabled, 
                    onvalue = 1, 
                    offvalue = 0)
chordButton.grid(row=22, column=0)
EightBitbutton = Checkbutton(frame, text="Enable 8-bit",variable = EightBit_enabled, 
                    onvalue = 1, 
                    offvalue = 0)
EightBitbutton.grid(row=23, column=0)


entry_btn = tk.Button(frame, text="Play", command=on_click)
entry_btn.grid(row=0, column=1)

ExplanationsLabel = tk.Label(frame, text="Explanations:")
ExplanationsLabel.grid(row=1, column=1)

frequencyExplantionLabel = tk.Label(frame, text="Frequency is the pitch of the sound. Higher frequencies sound higher.")
frequencyExplantionLabel.grid(row=2, column=1)

durationExplantionLabel = tk.Label(frame, text="Duration is how long the sound plays for.")
durationExplantionLabel.grid(row=3, column=1)

amplitudeExplantionLabel = tk.Label(frame, text="Amplitude is the volume of the sound. Higher amplitude is louder.")
amplitudeExplantionLabel.grid(row=4, column=1)

AttackExplantionLabel = tk.Label(frame, text="Attack is how long it takes for the sound to reach full volume. Enable ASDR to use this feature.")
AttackExplantionLabel.grid(row=5, column=1)

decayExplantionLabel = tk.Label(frame, text="Decay is how long it takes for the sound to fall from full volume to sustain volume. Enable ASDR to use this feature.")
decayExplantionLabel.grid(row=6, column=1)

sustainExplantionLabel = tk.Label(frame, text="Sustain is the volume level that the sound maintains while playing. Enable ASDR to use this feature.")
sustainExplantionLabel.grid(row=7, column=1)

releaseExplantionLabel = tk.Label(frame, text="Release is how long it takes for the sound to fade out after releasing a key. Enable ASDR to use this feature.")
releaseExplantionLabel.grid(row=8, column=1)

ADRSExplanationLabel = tk.Label(frame, text="ADSR stands for Attack, Decay, Sustain, Release.")
ADRSExplanationLabel.grid(row=9, column=1)

chordExplanationLabel = tk.Label(frame, text="Enabling chord will play the several notes at the same time.")
chordExplanationLabel.grid(row=10, column=1)

eightBitExplanationLabel = tk.Label(frame, text="Enabling 8-bit will make the sound more 8-bit by lowering the rate data changes.")
eightBitExplanationLabel.grid(row=11, column=1)

exportbtn = tk.Button(frame, text="Export", command=exportSound)
exportbtn.grid(row=12, column=1)

updateSliders("", "", "")
updateLabels("")

root.mainloop()
#endregion