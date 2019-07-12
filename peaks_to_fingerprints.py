import dict_data
import audio_to_spec


def recording_peaks_to_fingerprints(peaks):
    """
    Compiles a list of fingerprints from a list of peaks for any type of audio data.

    :param peaks: a list of tuples that contain peaks in the form (freq, time)
    :return: a list of tuples that contain fingerprints in the form (f_n, f_n+i, t_n+i - t_n)
    """

    fan_out = 15
    fingerprints = []

    for idx, peak in enumerate(peaks):
        if len(peaks) - idx <= fan_out:
            break
        for i in range(1, fan_out+1):
            fingerprints.append((peak[0], peaks[idx+i][0], peaks[idx+i][1]-peak[1],peak[1]))

    return fingerprints



def create_database():
    database = {}
    data = dict_data.import_dictionaries('int_to_pathstring')
    for song_ID in range(2):
        sample = audio_to_spec.mp3_to_sample(
            '/Users/MeganFrisella/GitHub/audio-capstone/Audio/' + data[song_ID] + '.mp3')
        S, f, t = audio_to_spec.sample_to_spectrogram(sample)
        peaks = SpectogramToFingerprints.SpecToPeaks((S, f, t))
        fingerprints = peaks_to_fingerprints.recording_peaks_to_fingerprints(peaks)

        for fp in fingerprints:
            if fp[0:3] not in database:
                database[fp[0:3]] = [(song_ID,fp[3])]
            else:
                database[fp[0:3]].append((song_ID, fp[3]))
    return database 
