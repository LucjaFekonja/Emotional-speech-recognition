from tkinter import *
from tkinter import filedialog
import numpy as np
from audio_player import RealTimeAudioPlayer, AudioFilePlayer
from prediction import make_prediction, make_prediction_from_audio

root = Tk()
root.title("Emotion Recognition of Speech")
root.geometry("400x450")

# Global variables
player_original = None  # For original audio
player_modified = None  # For modified audio
file_name = None
modified_audio = None
sample_rate = None


def select_file():
    global player_original, player_modified, file_name
    if player_original:
        player_original.stop()
    if player_modified:
        player_modified.stop()

    # Ask to select a file
    file_name = filedialog.askopenfilename(initialdir="C:/School/RZP/vaje/Projekt",
                                           title="Select a file",
                                           filetypes=(("wav files", "*.wav"), ("all files", ".")))
    display_name = Label(root, text=file_name.split("/")[-1])
    display_name.grid(row=0, column=0)

    display_emotion = Label(root, text=make_prediction(file_name))
    display_emotion.grid(row=0, column=6)

    # Initialize the original player with the file path
    player_original = AudioFilePlayer(file_name)

    # Initialize the modified player (initially no modifications)
    player_modified = RealTimeAudioPlayer(file_name)

    # Add sliders and playback controls
    add_sliders_and_controls()


def add_sliders_and_controls():
    global player_original, player_modified

    # Play and Pause buttons for Original Audio
    play_button_original = Button(root, text="Play Original", padx=6, pady=4, bg="white", command=player_original.play)
    pause_button_original = Button(root, text="Pause Original", padx=6, pady=4, bg="white", command=player_original.pause)

    play_button_original.grid(row=1, column=0, padx=5, pady=10)
    pause_button_original.grid(row=1, column=1, padx=5, pady=10)

    # Link sliders to player
    def update_pitch(value):
        if player_modified:
            player_modified.update_pitch(float(value))

    def update_tempo(value):
        if player_modified:
            player_modified.update_tempo(float(value))

    def update_volume(value):
        if player_modified:
            player_modified.update_volume(float(value))
            

    # Pitch slider
    Label(root, text="Pitch Shift (semitones):").grid(row=3, column=0, padx=10, pady=10)
    pitch_slider = Scale(root, from_=-4, to=4, resolution=0.01, orient="horizontal", length=200, command=update_pitch)
    pitch_slider.grid(row=3, column=1, columnspan=2, padx=10, pady=10)

    # Tempo slider
    Label(root, text="Tempo Multiplier:").grid(row=4, column=0, padx=10, pady=10)
    tempo_slider = Scale(root, from_=0.5, to=3.0, resolution=0.01, orient="horizontal", length=200, command=update_tempo)
    tempo_slider.grid(row=4, column=1, columnspan=2, padx=10, pady=10)
    tempo_slider.set(1)

    # Volume slider
    Label(root, text="Volume:").grid(row=5, column=0, padx=10, pady=10)
    volume_slider = Scale(root, from_=0.0, to=2.0, resolution=0.01, orient="horizontal", length=200, command=update_volume)
    volume_slider.grid(row=5, column=1, columnspan=2, padx=10, pady=10)
    volume_slider.set(1)

    # Play and Pause buttons for Modified Audio
    play_button_modified = Button(root, text="Play Modified", padx=6, pady=4, bg="white", command=player_modified.play)
    pause_button_modified = Button(root, text="Pause Modified", padx=6, pady=4, bg="white", command=player_modified.pause)

    play_button_modified.grid(row=2, column=0, padx=5, pady=10)
    pause_button_modified.grid(row=2, column=1, padx=5, pady=10)

    # Save button for the modified audio
    save_button = Button(root, text="Save Modified", padx=6, pady=4, bg="white", command=lambda: save_modified_audio())
    save_button.grid(row=2, column=2, padx=5, pady=10)


def save_modified_audio():
    global player_modified

    # Get modified audio and sample rate from player
    if player_modified is None:
        Label(root, text="No modified audio to save!", fg="red").grid(row=6, column=0, padx=10, pady=10)
        return

    save_path = filedialog.asksaveasfilename(defaultextension=".wav",
                                             filetypes=[("WAV files", "*.wav"), ("All files", "*.*")],
                                             title="Save Modified Audio")
    if save_path:
        # Saving the modified audio using soundfile
        import soundfile as sf
        sf.write(save_path, player_modified.modified_audio.astype(np.int16), player_modified.sample_rate)
        Label(root, text="File saved successfully!", fg="green").grid(row=6, column=0, padx=10, pady=10)


def close():
    global player_original, player_modified
    if player_original:
        player_original.stop()
    if player_modified:
        player_modified.stop()
    root.destroy()


########################  START THE WINDOW  ########################

select_file_button = Button(root, text="Select file", padx=20, pady=5, bg="white", command=select_file)
select_file_button.grid(row=0, column=1)

# Stop recording if the window is closed
root.protocol('WM_DELETE_WINDOW', close)
root.mainloop()
