import struct
import numpy as np
import pyaudio


CHUNK = 882  # Real time rate
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 176400  # Sample rate
audioIn = pyaudio.PyAudio()  # Use pyaudio
outputWave = 0


def output_wave(in_data):
    global outputWave
    out_data = abs(in_data) / 10  # Divided by 10 for reading
    outputWave = np.average(out_data)  # Get the average value of each set of waveforms
    return out_data


def audio_analysis(in_data, frame_count, time_info, status):
    global outputWave  # For output
    in_data_int = np.array(struct.unpack('<882h', in_data))
    out_data_int = output_wave(in_data_int)
    return out_data_int, pyaudio.paContinue  # Return the data which


def output():
    return outputWave  # Can be called externally and get data


def get_wave(start=True):
    stream_in = audioIn.open(format=FORMAT,
                             channels=CHANNELS,
                             rate=RATE,
                             input=True,
                             frames_per_buffer=CHUNK,
                             stream_callback=audio_analysis)  # Use callback functions in non-blocking situations

    # Start audio monitoring stream
    if start:
        stream_in.start_stream()
    else:
        stream_in.stop_stream()  # The recording stops when this sentence is run
        stream_in.close()
        audioIn.terminate()
