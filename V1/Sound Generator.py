# Jonathan Ng
# Sound generator
# Simple GUI with allows user to input frequency, duration, and amplitude and plays a simple sine wave

import numpy as np
import sounddevice as sd
import tkinter as tk

def on_click():
    textFreq = entry.get()
    if textFreq:
        try:
            frequency = float(textFreq)
        except ValueError:
            frequency = 440
    else:
        frequency = 440

    textDur = entryDuration.get()
    if textDur:
        try:
            duration = float(textDur)
        except ValueError:
            duration = 1.0
    else:
        duration = 1.0

    textamp = entryAmplitude.get()
    if textamp:
        try:
            amplitude = float(textamp)
        except ValueError:
            amplitude = 0.01
    else:
        amplitude = 0.01

    sines = [sine_tone(frequency = 200 * i, amplitude=0.3 /i) for i in range(1, 31, 2)]
    sinesBeating = [sine_tone(200, 2, 0.01), sine_tone(205, 2, 0.01)]

    sine1 = sine_tone(frequency, duration, amplitude/1000)
    sine2 = sine_tone(frequency*2, duration, amplitude/2000)
    sine3 = sine_tone(frequency*4, duration, amplitude/3000)

    mysound = sum([sine1, sine2, sine3])
    # mysound3 = sum(sines)
    # mysound4 = sum(sinesBeating)
    # mysound2 = sine_tone(400, 1, 0.01)
    sd.play(mysound)
    sd.wait()

def white_noise(
        duration: float =1.0,
        amplitude: float =0.01,
        sample_rate: int =44100
    ) -> np.ndarray:
    n_samples = int(duration * sample_rate)

    noise = np.random.uniform(-1, 1, n_samples)

    noise *= amplitude

    return noise

def sine_tone(
        frequency: float =222.0,
        duration: float =5.0,
        amplitude: float =0.01,
        sample_rate: int =44100
    ) -> np.ndarray:
    n_samples = int(duration * sample_rate)

    time_points = np.linspace(0, duration, n_samples, False)

    sine = np.sin(2 * np.pi * frequency * time_points)

    sine *= amplitude
    return sine

frequency = 440.0
duration = 1.0
amplitude = 1
root = tk.Tk()

root.title("Sound Generator")

frame = tk.Frame(root)
frame.grid(row=0, column=0)

frequencyLabel = tk.Label(frame, text="Frequency (Hz):")
frequencyLabel.grid(row=0, column=0)

entry = tk.Entry(frame)
entry.grid(row=1, column=0)

durationLabel = tk.Label(frame, text="Duration:")
durationLabel.grid(row=2, column=0)

entryDuration = tk.Entry(frame)
entryDuration.grid(row=3, column=0)

amplitudeLabel = tk.Label(frame, text="Amplitude:")
amplitudeLabel.grid(row=4, column=0)

entryAmplitude = tk.Entry(frame)
entryAmplitude.grid(row=5, column=0)

entry_btn = tk.Button(frame, text="Play", command=on_click)
entry_btn.grid(row=0, column=1)



root.mainloop()
