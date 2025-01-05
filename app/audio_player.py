import psutil
import os
import pyaudio
import wave
import threading
import numpy as np
import librosa
import librosa.effects

process = psutil.Process(os.getpid())

class AudioFilePlayer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.chunk_size = 1024
        self.pause_flag = threading.Event()
        self.pause_flag.set()  # Initially, playback is allowed
        self.stop_flag = True  # Indicates playback is stopped
        self.thread = None

    def _play_audio(self):
        # Open the WAV file
        wf = wave.open(self.file_path, 'rb')

        # Create a PyAudio instance
        p = pyaudio.PyAudio()

        # Open a stream
        stream = p.open(
            format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True
        )

        # print(f"Memory before playing the original: {process.memory_info().rss / 1024 ** 2:.2f} MB")

        # Read and play audio in chunks
        data = wf.readframes(self.chunk_size)
        while data:
            if self.stop_flag:  # Stop playback
                break
            self.pause_flag.wait()  # Wait here if paused
            stream.write(data)
            data = wf.readframes(self.chunk_size)

        # Set stop_flag to True when audio is done
        if not data:
            self.stop_flag = True

        # Close the stream and PyAudio instance
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf.close()

        # print(f"Memory after playing the original: {process.memory_info().rss / 1024 ** 2:.2f} MB")


    def play(self):
        if self.stop_flag:
            # Reset flags and start playback
            self.stop_flag = False
            self.pause_flag.set()  # Ensure playback isn't paused
            self.thread = threading.Thread(target=self._play_audio)
            self.thread.start()
        else:
            # Resume playback
            self.pause_flag.set()

    def pause(self):
        self.pause_flag.clear()  # Pause playback

    def stop(self):
        self.stop_flag = True
        self.pause_flag.set()  # Resume if paused to exit playback loop
        if self.thread:
            self.thread.join()


class RealTimeAudioPlayer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.chunk_size = 1024
        self.current_position = 0
        self.pause_flag = threading.Event()
        self.pause_flag.set()  # Initially, playback is allowed
        self.stop_flag = True  # Indicates playback is stopped
        self.thread = None
        self.audio = None  # To store the audio data
        self.sample_rate = None  # To store the sample rate
        self.original_audio = None  # To store the original unmodified audio
        self.modified_audio = None
        self.current_pitch_shift = 0.0  # Default pitch shift (no change)
        self.current_tempo_multiplier = 1.0  # Default tempo (normal speed)
        self.volume_multiplier = 1.0  # Default volume (100%)
        self.lock = threading.Lock()  # Initialize the lock for thread safety

        self.load_audio()

    def load_audio(self):
        # Read the audio file and load data
        wf = wave.open(self.file_path, 'rb')
        self.sample_rate = wf.getframerate()
        audio_data = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)
        self.audio = audio_data  # Convert to float32 for librosa
        self.original_audio = np.copy(self.audio)  # Store the original audio for modifications
        self.modified_audio = self.original_audio.copy()
        wf.close()


    def _play_audio(self):
        # Open a PyAudio stream
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            output=True
        )

        # print(f"Memory before playing the modified: {process.memory_info().rss / 1024 ** 2:.2f} MB")

        chunk_size = self.chunk_size
        while not self.stop_flag:
            self.pause_flag.wait()  # Wait here if paused

            # Apply pitch and tempo changes dynamically for the current chunk
            with self.lock:  # Ensure thread safety
                chunk_start = self.current_position
                chunk_end = min(chunk_start + chunk_size, len(self.original_audio))
                chunk_audio = self.original_audio[chunk_start:chunk_end].astype(np.float32)

                if len(chunk_audio) == 0:  # End of audio
                    break

                modified_chunk = librosa.effects.pitch_shift(chunk_audio, sr=self.sample_rate, n_steps=self.current_pitch_shift)
                modified_chunk = librosa.effects.time_stretch(modified_chunk, rate=self.current_tempo_multiplier)
                modified_chunk *= self.volume_multiplier 

                # Ensure the audio chunk is within the valid range
                modified_chunk = np.clip(modified_chunk, -32768, 32767).astype(np.int16)

            # Play the chunk
            stream.write(modified_chunk.tobytes())
            self.current_position = chunk_end

            # Reset to the beginning if the audio has finished
            if self.current_position >= len(self.original_audio):
                self.stop_flag = True
                self.current_position = 0

        # Close the stream and PyAudio instance
        stream.stop_stream()
        stream.close()
        p.terminate()

        # print(f"Memory after playing the modified: {process.memory_info().rss / 1024 ** 2:.2f} MB")


    def play(self):
        if self.stop_flag:
            # Reset flags and start playback
            self.stop_flag = False
            self.pause_flag.set()  # Ensure playback isn't paused
            self.thread = threading.Thread(target=self._play_audio)
            self.thread.start()
        else:
            # Resume playback
            self.pause_flag.set()

    def pause(self):
        self.pause_flag.clear()  # Pause playback

    def stop(self):
        self.stop_flag = True
        self.pause_flag.set()  # Resume if paused to exit playback loop
        if self.thread:
            self.thread.join()

    def update_pitch(self, pitch_shift):
        # print(f"Memory before updating pitch: {process.memory_info().rss / 1024 ** 2:.2f} MB")
        with self.lock:
            self.current_pitch_shift = pitch_shift  # Update pitch shift dynamically
        # print(f"Memory after updating pitch: {process.memory_info().rss / 1024 ** 2:.2f} MB")
        

    def update_tempo(self, tempo_multiplier):
        # print(f"Memory before updating tempo: {process.memory_info().rss / 1024 ** 2:.2f} MB")
        with self.lock:
            self.current_tempo_multiplier = tempo_multiplier  # Update tempo multiplier dynamically
        # print(f"Memory after updating tempo: {process.memory_info().rss / 1024 ** 2:.2f} MB")
        

    def update_volume(self, volume):
        # print(f"Memory before updating volume: {process.memory_info().rss / 1024 ** 2:.2f} MB")
        with self.lock:
            self.volume_multiplier = volume
        # print(f"Memory before updating volume: {process.memory_info().rss / 1024 ** 2:.2f} MB")
