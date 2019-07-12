import numpy as np
import matplotlib.mlab as mlab
import librosa
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import Audio
from pathlib import Path
from microphone import record_audio
import pickle

import dict_data

import audio_to_spec
import peaks_to_fingerprints
import find_match
import SpectogramToFingerprints
database = dict_data.import_database()

def run(length):
    """Runs everything, as long as length is over 3 seconds
    
    parameters:
    -----------
    length: [int]
        [length of time for mic recording in seconds]
    
    returns:
    [string]
        [song title and artist]
    """
    
    if length < 3:
        return "Sorry, your sample length is too low! Please enter a value greater than 3, thanks!"

    sample = audio_to_spec.mic_to_sample(length)
    
    
    S, f, t = audio_to_spec.sample_to_spectrogram(sample)
    peaks = SpectogramToFingerprints.SpecToPeaks((S,f,t))
    fingerprints = peaks_to_fingerprints.recording_peaks_to_fingerprints(peaks)
    
    return find_match.match(fingerprints,database)