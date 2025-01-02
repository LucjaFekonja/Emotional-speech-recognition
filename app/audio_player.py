import pyaudio
import wave
import threading
import numpy as np
import pyaudio
import numpy as np
import threading
import librosa
import librosa.effects


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

    def _apply_changes(self):
        self.modified_audio = self.original_audio.copy().astype(np.float32)
        self.modified_audio = librosa.effects.pitch_shift(self.modified_audio, sr=self.sample_rate, n_steps=self.current_pitch_shift)
        self.modified_audio = librosa.effects.time_stretch(self.modified_audio, rate=self.current_tempo_multiplier)
        
        # Ensure the modified audio is within the proper range for audio playback (int16)
        self.modified_audio = np.clip(self.modified_audio, -32768, 32767)  # Ensure audio is within 16-bit range
        self.modified_audio = self.modified_audio.astype(np.int16)  # Convert back to int16 for playback
        return self.modified_audio

    def _play_audio(self):
        # Open a PyAudio stream
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            output=True
        )

        while not self.stop_flag:
            # Get the modified audio based on current pitch/tempo
            self.modified_audio = self._apply_changes()

            # Read and play audio in chunks
            for i in range(0, len(self.modified_audio), self.chunk_size):
                if self.stop_flag:  # Stop playback
                    break
                self.pause_flag.wait()  # Wait here if paused
                chunk = self.modified_audio[i:i + self.chunk_size]
                stream.write(chunk.tobytes())

            # Set stop_flag to True when the audio finishes
            self.stop_flag = True

        # Close the stream and PyAudio instance
        stream.stop_stream()
        stream.close()
        p.terminate()

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
        self.current_pitch_shift = pitch_shift  # Update pitch shift

    def update_tempo(self, tempo_multiplier):
        self.current_tempo_multiplier = tempo_multiplier  # Update tempo multiplier
