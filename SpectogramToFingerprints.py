from numba import njit
import numpy as np
import matplotlib.mlab as mlab
import librosa
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import Audio
from pathlib import Path
from microphone import record_audio
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure, binary_erosion
from scipy.ndimage.morphology import iterate_structure
#Marker of start code from Ryan
@njit()
def _peaks(spec, rows, cols, amp_min):
    peaks = []
    # We want to iterate over the array in column-major
    # order so that we order the peaks by time. That is,
    # we look for nearest neighbors of increasing frequencies
    # at the same times, and then move to the next time bin.
    # This is why we use the reversed-shape
    for c, r in np.ndindex(*spec.shape[::-1]):
        if spec[r, c] < amp_min:
            continue

        for dr, dc in zip(rows, cols):
            # don't compare element (r, c) with itself
            if dr == 0 and dc == 0:
                continue

            # mirror over array boundary
            if not (0 <= r + dr < spec.shape[0]):
                dr *= -1

            # mirror over array boundary
            if not (0 <= c + dc < spec.shape[1]):
                dc *= -1

            if spec[r, c] < spec[r + dr, c + dc]:
                break
        else:
            peaks.append((c, r))
    return peaks


def local_peaks(log_spectrogram, amp_min, p_nn):
    """
    Defines a local neighborhood and finds the local peaks
    in the spectrogram, which must be larger than the
    specified `amp_min`.

    Parameters
    ----------
    log_spectrogram : numpy.ndarray, shape=(n_freq, n_time)
        Log-scaled spectrogram. Columns are the periodograms of
        successive segments of a frequency-time spectrum.

    amp_min : float
        Amplitude threshold applied to local maxima

    p_nn : int
        Number of cells around an amplitude peak in the spectrogram in order

    Returns
    -------
    List[Tuple[int, int]]
        Time and frequency index-values of the local peaks in spectrogram.
        Sorted by ascending frequency and then time.

    Notes
    -----
    The local peaks are returned in column-major order for the spectrogram.
    That is, the peaks are ordered by time. That is, we look for nearest
    neighbors of increasing frequencies at the same times, and then move to
    the next time bin.
    """
    struct = generate_binary_structure(2, 1)
    neighborhood = iterate_structure(struct, p_nn)
    rows, cols = np.where(neighborhood)
    assert neighborhood.shape[0] % 2 == 1
    assert neighborhood.shape[1] % 2 == 1

    # center neighborhood indices around center of neighborhood
    rows -= neighborhood.shape[0] // 2
    cols -= neighborhood.shape[1] // 2

    detected_peaks = _peaks(log_spectrogram, rows, cols, amp_min=amp_min)

    # Extract peaks; encoded in terms of time and freq bin indices.
    # dt and df are always the same size for the spectrogram that is produced,
    # so the bin indices consistently map to the same physical units:
    # t_n = n*dt, f_m = m*df (m and n are integer indices)
    # Thus we can codify our peaks with integer bin indices instead of their
    # physical (t, f) coordinates. This makes storage and compression of peak
    # locations much simpler.

    return detected_peaks
# Marker of end code from Ryan

def SpecToPeaks(S):
    """
    :param S: np.array[int, int]
        floating point matrix (spectogram -- dimensions: frequency X time)
    :return: List[Tuple[int, int]]
        Time and frequency index-values of the local peaks in spectrogram.
        Sorted by ascending frequency and then time.
    """

    data = S.ravel()
    #should already be logged
    N = data.size
    hist, bin_edges = np.histogram(data, bins=int(N/2), density=True)
    bin_size = bin_edges[1]-bin_edges[0]

    #Ryan's suggested value: 0.77
    cutoff_percent = 0.77;
    #Ryan's suggested value: 15
    fan_out = 15;
    cumulative_distr = np.cumsum(hist)*bin_size
    index = np.searchsorted(cumulative_distr, cutoff_percent)
    amp_bin = times[index]
    amp_min = np.exp(amp_bin)

    return local_peaks(hist, amp_min, fan_out)

#def PeaksToFingerPrints():