import numpy as np
import pandas as pd
import librosa
import scipy
from scipy.signal import correlate
from scipy.signal import lfilter, find_peaks
from scipy.signal.windows import hamming
from scipy.interpolate import interp1d
from scipy.fftpack import fft
from read_file import read_file 


hop_length = 128
frame_length = 256

def energy(x):
    energy = np.array([
        sum(abs(x[i:i+frame_length]**2))
        for i in range(0, len(x)-frame_length, hop_length)
    ])
    return energy

def zero_crossing_rate(x):
    return librosa.feature.zero_crossing_rate(x, frame_length=frame_length, hop_length=hop_length)[0][:-2]

def energy_times_zero_crossing_rate(x):
    e = energy(x)
    zcr = zero_crossing_rate(x)
    return [e[i] * zcr[i] for i in range(len(e))]


# Helper for pitch
def autocorrelation_pitch(frame, sr):
    frame = frame - np.mean(frame)
    corr = correlate(frame, frame, mode='full')
    corr = corr[len(corr)//2:]  

    d = np.diff(corr)
    if np.any(d > 0):
        start = np.where(d > 0)[0][0]  
    else:start = 0
    peak = np.argmax(corr[start:]) + start  
    
    if peak > 0:
        return sr / peak
    else:
        return 0
        
def pitch(x, sr):
    pitches = []
    for i in range(0, len(x)-frame_length, hop_length):
        frame = x[i:i+frame_length]
        pitch = autocorrelation_pitch(frame, sr)
        pitches.append(pitch)

    return pitches


# Helper for formant frequencies
def get_formants_from_lpc(frame, sr, order=12):
    frame = frame * hamming(len(frame))
    frame = frame - np.mean(frame)
    a = np.polyfit(np.arange(len(frame)), frame, order)
    
    roots = np.roots(a)
    roots = [r for r in roots if np.imag(r) >= 0]  
    
    angles = np.angle(roots)
    formant_freqs = sorted(angles * (sr / (2 * np.pi)))  
    
    return formant_freqs

def formants(x, sr):
    f1_list, f2_list, f3_list = [], [], []
    for i in range(0, len(x)-frame_length, hop_length):
        frame = x[i:i+frame_length]
        
        formants = get_formants_from_lpc(frame, sr)
        if len(formants) >= 3:
            f1_list.append(formants[0])
            f2_list.append(formants[1])
            f3_list.append(formants[2])
    
    return f1_list, f2_list, f3_list


def spectral_centroid(x):
    return librosa.feature.spectral_centroid(y=x, n_fft=frame_length, hop_length=hop_length)[0][:-2]


def cutoff_frequency(x, sr):
    
    cutoff_frequencies = []
    for i in range(0, len(x)-frame_length, hop_length):
        frame = x[i:i+frame_length]
        
        fft_result = np.fft.fft(frame, n=frame_length)
        magnitude_spectrum = np.abs(fft_result[:frame_length // 2]) 
        
        total_energy = np.sum(magnitude_spectrum)
        cumulative_energy = np.cumsum(magnitude_spectrum)
        cutoff_index = np.argmax(cumulative_energy / total_energy >= 0.85)

        cutoff_frequency = (cutoff_index * sr) / frame_length
        cutoff_frequencies.append(cutoff_frequency)
    
    return cutoff_frequencies


def apply_one_pole_filter(signal, alpha):
    """
    Apply a one-pole filter to a signal.
    Y_k(i) = alpha * Y_k(i-1) + X(i)
    """
    y = np.zeros_like(signal, dtype=np.float64)
    for i in range(1, len(signal)):
        y[i] = np.real(alpha) * y[i-1] + signal[i]
    return y

def compute_autocorrelation(Y_k, hanning, L):
    """
    Compute the frame-level autocorrelation for a filtered signal Y_k.
    """
    autocorr = 0.0
    for i in range(L - 1):  # Up to L-1 for (i+1) to stay within bounds
        autocorr += Y_k[i] * hanning[i] * Y_k[i + 1] * hanning[i + 1]
    return autocorr

def correlation_density(x, etas=[0.125, 0.25, 0.5, 0.75, 0.875], frame_length=frame_length, theta=0.05 * np.pi):
    """
    Calculate the correlation density C_d(t) for the given signal.
    """
    # Initialize
    hanning = np.hanning(frame_length)
    alphas = [eta * np.exp(1j * theta) for eta in etas]
    correlation_density = []

    # Process each frame
    for i in range(0, len(x)-frame_length, hop_length):
        frame = x[i:i+frame_length]
        L = len(frame)
        
        # Apply filters and compute autocorrelation
        autocorrelations = []
        for alpha in alphas:
            Y_k = apply_one_pole_filter(frame, alpha)
            rho_k = compute_autocorrelation(Y_k, hanning, L)
            autocorrelations.append(rho_k)
        
        # Calculate C_d(t) based on Eq. (8)
        autocorrelations = np.array(autocorrelations)
        rho_differences = autocorrelations[1:] - autocorrelations[:-1]
        cd_t = np.log(np.sum(rho_differences**-2))
        correlation_density.append(cd_t)

    return np.array(correlation_density)


def fractal_dimension(x, cellmax=1024):

    fractal_dimensions = []
    for i in range(0, len(x)-frame_length, hop_length):
        frame = x[i:i+frame_length]
    
        # Step 1: Shift Y to make the minimum value zero
        Y_min = np.min(frame)
        Y_shift = frame - Y_min

        # Step 2: Interpolate Y_shift to have a fixed length of `cellmax`
        L = len(Y_shift)
        x_original = np.arange(1, L + 1)
        x_interp = np.linspace(1, L, cellmax)
        interp_function = interp1d(x_original, Y_shift, kind='linear')
        Y_interp = interp_function(x_interp)

        # Step 3: Normalize the interpolated signal
        YY = (Y_interp * cellmax) / np.max(Y_interp)

        # Step 4: Cover YY with nets of sizes `s = 1, 2, 4, ..., cellmax`
        scales = np.array([2**i for i in range(int(np.log2(cellmax)) + 1) if 2**i <= cellmax])
        N_s = []

        for s in scales:
            # Create a grid of mesh size `s`
            grid_count = 0
            for i in range(0, cellmax, s):
                # Check if any part of the signal lies within this grid cell
                cell_min = i
                cell_max = i + s
                if np.any((YY >= cell_min) & (YY < cell_max)):
                    grid_count += 1
            N_s.append(grid_count)

        # Step 5: Fit log-log data to a line to calculate Db
        log_s = np.log2(scales)
        log_N_s = np.log2(N_s)

        # Perform linear regression to estimate Db
        coefficients = np.polyfit(log_s, log_N_s, 1)
        Db = coefficients[0]  # The slope is the box-counting dimension

        fractal_dimensions.append(Db)

    return fractal_dimensions


def hz_to_mel(hz):
    return 2595 * np.log10(1 + hz / 700)

def mel_to_hz(mel):
    return 700 * (10**(mel / 2595) - 1)

def mel_filter_bank(num_bands, num_fft_bins, sample_rate, freq_min=0, freq_max=None):
    """
    Create a Mel filter bank with specified number of bands.
    Parameters:
        num_bands (int): Number of Mel bands (e.g., 5).
        num_fft_bins (int): Number of FFT bins (e.g., N/2).
        sample_rate (int): Sampling rate of the signal.
        freq_min (float): Minimum frequency (default=0 Hz).
        freq_max (float): Maximum frequency (default=Nyquist frequency).
    Returns:
        np.ndarray: Filter bank of shape (num_bands, num_fft_bins).
    """
    if freq_max is None:
        freq_max = sample_rate / 2  # Nyquist frequency

    mel_min = hz_to_mel(freq_min)
    mel_max = hz_to_mel(freq_max)

    # Generate Mel points and convert to Hz
    mel_points = np.linspace(mel_min, mel_max, num_bands + 2)
    hz_points = mel_to_hz(mel_points)

    # Map Hz points to FFT bins
    bin_points = np.floor((num_fft_bins + 1) * hz_points / sample_rate).astype(int)

    # Create triangular filters
    filters = np.zeros((num_bands, num_fft_bins))
    for i in range(1, num_bands + 1):
        start, center, end = bin_points[i - 1], bin_points[i], bin_points[i + 1]
        for j in range(start, center):
            filters[i - 1, j] = (j - start) / (center - start)
        for j in range(center, end):
            filters[i - 1, j] = (end - j) / (end - center)

    return filters

def mel_band_energies(signal, sample_rate, frame_length=frame_length, hop_length=hop_length, num_mel_bands=5):
    """
    Calculate Mel-band energies for each frame of a signal.
    Parameters:
        signal (np.ndarray): Input signal.
        frame_length (int): Length of each frame in samples.
        hop_length (int): Hop size between frames in samples.
        sample_rate (int): Sampling rate of the signal.
        num_mel_bands (int): Number of Mel-frequency bands (default=5).
    Returns:
        np.ndarray: Energy values for each Mel band and frame (shape: [num_frames, num_mel_bands]).
    """
    # Pre-compute FFT parameters
    num_fft_bins = frame_length // 2
    mel_filters = mel_filter_bank(num_mel_bands, num_fft_bins, sample_rate)

    # Frame the signal
    frames = []
    for i in range(0, len(signal)-frame_length, hop_length):
        frame = signal[i:i+frame_length]
        frames.append(frame)
    frames = np.array(frames)

    # Compute the FFT and power spectrum for each frame
    fft_frames = np.abs(fft(frames, axis=1)[:, :num_fft_bins])**2

    # Compute Mel-band energies
    mel_energies = np.dot(fft_frames, mel_filters.T)

    mel1 = [m[0] for m in mel_energies]
    mel2 = [m[1] for m in mel_energies]
    mel3 = [m[2] for m in mel_energies]
    mel4 = [m[3] for m in mel_energies]
    mel5 = [m[4] for m in mel_energies]

    return mel1, mel2, mel3, mel4, mel5


def derivative(s):
    delta = np.diff(s)
    return delta



def calculate_feature_matrix(file_names):
    X = pd.DataFrame()
    # X_list = []

    for i, file_name in enumerate(file_names):
        x, sr = read_file(file_name)

        # Calculate features from the signal
        xenergy = energy(x)
        xzero_crossing_rate = zero_crossing_rate(x)
        xenergy_times_zero_crossing_rate = energy_times_zero_crossing_rate(x)
        xpitch = pitch(x, sr)
        xformant1, xformant2, xformant3 = formants(x, sr)
        xspectral_centroid = spectral_centroid(x)
        xcutoff_frequency = cutoff_frequency(x, sr)
        xcorrelation_density = correlation_density(x)
        xfractal_dimension = fractal_dimension(x)
        xmel1, xmel2, xmel3, xmel4, xmel5 = mel_band_energies(x, sr)

        # Save features in a dictionary
        basic_features = {"energy": xenergy,
                          "zero_crossing_rate": xzero_crossing_rate,
                          "energy_times_zero_crossing_rate": xenergy_times_zero_crossing_rate,
                          "pitch": xpitch,
                          "formant1": xformant1, "formant2": xformant2, "formant3": xformant3,
                          "spectral_centroid": xspectral_centroid,
                          "cutoff_frequency": xcutoff_frequency,
                          "correlation_density": xcorrelation_density,
                          "fractal_dimension": xfractal_dimension,
                          "mel1": xmel1, "mel2": xmel2, "mel3": xmel3, "mel4": xmel4, "mel5": xmel5}
        
        features = dict()

        for k, v in basic_features.items():
            # Calculate first and second derivative of each signal
            diff = derivative(v)
            diff_diff = derivative(diff)
            # features["first_diff_" + k] = diff
            # features["second_diff_" + k] = diff_diff
        
            # Calculate other statistics: max, min, mean, standard deviation, skewness, kurtosis 
            features["min_" + k] = float(np.min(v))
            features["max_" + k] = float(np.max(v))
            features["mean_" + k] = float(np.mean(v))
            features["std_" + k] = float(np.std(v))
            features["ske_" + k] = float(scipy.stats.skew(v, axis=0))
            features["kur_" + k] = float(scipy.stats.kurtosis(v, axis=0))
        
            # Calculate other statistics: max, min, mean, standard deviation, skewness, kurtosis; for first derivative
            features["min_1_diff_" + k] = float(np.min(diff))
            features["max_1_diff_" + k] = float(np.max(diff))
            features["mean_1_diff_" + k] = float(np.mean(diff))
            features["std_1_diff_" + k] = float(np.std(diff))
            features["ske_1_diff_" + k] = float(scipy.stats.skew(diff, axis=0))
            features["kur_1_diff_" + k] = float(scipy.stats.kurtosis(diff, axis=0))
        
            # Calculate other statistics: max, min, mean, standard deviation, skewness, kurtosis; for second derivative
            features["min_2_diff_" + k] = float(np.min(diff_diff))
            features["max_2_diff_" + k] = float(np.max(diff_diff))
            features["mean_2_diff_" + k] = float(np.mean(diff_diff))
            features["std_2_diff_" + k] = float(np.std(diff_diff))
            features["ske_2_diff_" + k] = float(scipy.stats.skew(diff_diff, axis=0))
            features["kur_2_diff_" + k] = float(scipy.stats.kurtosis(diff_diff, axis=0))

        # Save features in X
        new_df = pd.DataFrame(features, index=[i])
        X = pd.concat([X, new_df])

        # X_list += [features]
    return X

    
def calculate_selected_features_savee(file_name):
    
    x, sr = read_file(file_name)

    xenergy = energy(x)
    xzero_crossing_rate = zero_crossing_rate(x)
    xenergy_times_zero_crossing_rate = energy_times_zero_crossing_rate(x)
    xpitch = pitch(x, sr)

    basic_features = {"energy": xenergy,
                      "zero_crossing_rate": xzero_crossing_rate,
                      "energy_times_zero_crossing_rate": xenergy_times_zero_crossing_rate}
    
    features = dict()
    for k, v in basic_features.items():
        # Calculate first and second derivative of each signal
        diff = derivative(v)
        diff_diff = derivative(diff)

        # Calculate other statistics: max, min, mean, standard deviation, skewness, kurtosis 
        features["min_" + k] = [float(np.min(v))]
        features["max_" + k] = [float(np.max(v))]
        features["mean_" + k] = [float(np.mean(v))]
        features["std_" + k] = [float(np.std(v))]
        features["ske_" + k] = [float(scipy.stats.skew(v, axis=0))]
        features["kur_" + k] = [float(scipy.stats.kurtosis(v, axis=0))]
    
        # Calculate other statistics: max, min, mean, standard deviation, skewness, kurtosis; for first derivative
        features["min_1_diff_" + k] = [float(np.min(diff))]
        features["max_1_diff_" + k] = [float(np.max(diff))]
        features["mean_1_diff_" + k] = [float(np.mean(diff))]
        features["std_1_diff_" + k] = [float(np.std(diff))]
        features["ske_1_diff_" + k] = [float(scipy.stats.skew(diff, axis=0))]
        features["kur_1_diff_" + k] = [float(scipy.stats.kurtosis(diff, axis=0))]
    
        # Calculate other statistics: max, min, mean, standard deviation, skewness, kurtosis; for second derivative
        features["min_2_diff_" + k] = [float(np.min(diff_diff))]
        features["max_2_diff_" + k] = [float(np.max(diff_diff))]
        features["mean_2_diff_" + k] = [float(np.mean(diff_diff))]
        features["std_2_diff_" + k] = [float(np.std(diff_diff))]
        features["ske_2_diff_" + k] = [float(scipy.stats.skew(diff_diff, axis=0))]
        features["kur_2_diff_" + k] = [float(scipy.stats.kurtosis(diff_diff, axis=0))]

    features["min_pitch"] = [float(np.min(xpitch))]
    features["max_pitch"] = [float(np.max(xpitch))]
    features["mean_pitch"] = [float(np.mean(xpitch))]
    features["std_pitch"] = [float(np.std(xpitch))]

    return pd.DataFrame.from_dict(features)




def calculate_selected_features_tess(file_name):
    
    x, sr = read_file(file_name)
    features = dict()

    xfractal_dimension = fractal_dimension(x)
    x2_diff_fractal_dimension = derivative(derivative(xfractal_dimension))

    x2_diff_energy = derivative(derivative(energy(x)))
    x2_diff_correlation_density = derivative(derivative(correlation_density(x)))

    xmel1, xmel2, xmel3, xmel4, xmel5 = mel_band_energies(x, sr)
    x1_diff_mel1 = derivative(xmel1)
    x1_diff_mel2 = derivative(xmel2)
    x1_diff_mel3 = derivative(xmel3)
    x1_diff_mel5 = derivative(xmel5)
    x2_diff_mel1 = derivative(x1_diff_mel1)
    x2_diff_mel2 = derivative(x1_diff_mel2)
    x2_diff_mel3 = derivative(x1_diff_mel3)
    x2_diff_mel5 = derivative(x1_diff_mel5)

    xzero_crossing_rate = zero_crossing_rate(x)
    x1_diff_zero_crossing_rate = derivative(xzero_crossing_rate)
    x2_diff_zero_crossing_rate = derivative(x1_diff_zero_crossing_rate)
    

    features["max_fractal_dimension"] = [float(np.max(xfractal_dimension))]
    features["min_fractal_dimension"] = [float(np.min(xfractal_dimension))]

    features["kur_2_diff_correlation_density"] = [float(scipy.stats.kurtosis(x2_diff_correlation_density, axis=0))]
    features["ske_2_diff_correlation_density"] = [float(scipy.stats.skew(x2_diff_correlation_density, axis=0))]

    features["kur_2_diff_fractal_dimension"] = [float(scipy.stats.kurtosis(x2_diff_fractal_dimension, axis=0))]
    features["ske_2_diff_fractal_dimension"] = [float(scipy.stats.skew(x2_diff_fractal_dimension, axis=0))]
    features["std_2_diff_fractal_dimension"] = [float(np.std(x2_diff_fractal_dimension))]
    features["mean_2_diff_fractal_dimension"] = [float(np.mean(x2_diff_fractal_dimension))]

    features["max_2_diff_zero_crossing_rate"] = [float(np.max(x2_diff_zero_crossing_rate))]
    features["min_2_diff_zero_crossing_rate"] = [float(np.min(x2_diff_zero_crossing_rate))]

    features["kur_2_diff_energy"] = [float(scipy.stats.kurtosis(x2_diff_energy, axis=0))]
    features["ske_2_diff_energy"] = [float(scipy.stats.skew(x2_diff_energy, axis=0))]

    features["kur_mel5"] = [float(scipy.stats.kurtosis(xmel5, axis=0))]

    f = {
        "mel1" : xmel1,
        "1_diff_mel1" : x1_diff_mel1,
        "2_diff_mel1" : x2_diff_mel1,
        "mel2" : xmel2,
        "1_diff_mel2" : x1_diff_mel2,
        "2_diff_mel2" : x2_diff_mel2,
        "mel3" : xmel3,
        "1_diff_mel3" : x1_diff_mel3,
        "2_diff_mel3" : x2_diff_mel3,
        "mel4" : xmel4,
        "1_diff_mel5" : x1_diff_mel5,
        "2_diff_mel5" : x2_diff_mel5,
        "zero_crossing_rate" : xzero_crossing_rate,
        "1_diff_zero_crossing_rate" : x1_diff_zero_crossing_rate
    }

    for k, v in f.items():
        features["min_" + k] = [float(np.min(v))]
        features["max_" + k] = [float(np.max(v))]
        features["mean_" + k] = [float(np.mean(v))]
        features["std_" + k] = [float(np.std(v))]
        features["ske_" + k] = [float(scipy.stats.skew(v, axis=0))]
        features["kur_" + k] = [float(scipy.stats.kurtosis(v, axis=0))]

    return pd.DataFrame.from_dict(features)