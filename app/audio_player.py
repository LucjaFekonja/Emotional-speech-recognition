import pyaudio
import wave
import threading

class AudioPlayer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.chunk_size = 1024
        self.pause_flag = threading.Event()
        self.pause_flag.set()  # Initially, playback is allowed
        self.stop_flag = False

    def play(self):
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
        while data and not self.stop_flag:
            self.pause_flag.wait()  # Wait here if paused
            stream.write(data)
            data = wf.readframes(self.chunk_size)

        # Close the stream and PyAudio instance
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf.close()

    def pause(self):
        self.pause_flag.clear()  # Clear the flag to pause playback

    def unpause(self):
        self.pause_flag.set()  # Set the flag to resume playback

    def stop(self):
        self.stop_flag = True  # Stop the playback
        self.pause_flag.set()  # Resume if paused to exit the loop

