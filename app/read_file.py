import librosa
from scipy.signal import lfilter

def read_file(file_name):
    "Loads and preprocesses a given file with the transfer function H(z) = 1 - 0.97 z^(-1)"

    x, sr = librosa.load(file_name)
    y = lfilter([1, -0.97], [1], x)
    return y, sr

