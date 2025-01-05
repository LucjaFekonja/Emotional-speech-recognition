import psutil
import os
import time
from tkinter import *
from tkinter import filedialog
import numpy as np
from audio_player import RealTimeAudioPlayer, AudioFilePlayer
from prediction import make_prediction_savee, make_prediction_tess
import change_emotion
import argparse

# Track memory
process = psutil.Process(os.getpid())
# print(f"Memory usage at start: {process.memory_info().rss / 1024 ** 2:.2f} MB")

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Run Emotion Recognition of Speech")
parser.add_argument("dataset", choices=["savee", "tess"], help="Specify the dataset to use (savee or tess)")
args = parser.parse_args()
selected_dataset = args.dataset

root = Tk()
root.title("Emotion Recognition of Speech")
root.geometry("800x600")

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

frame = Frame(root)
frame.grid(row=0, column=0)

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

    select_file_button.place_forget()
    waiting_label = Label(root, text="Recognizing emotion")
    waiting_label.place(relx=0.5, rely=0.5, anchor="center")

    # print(f"Memory before selecting a file: {process.memory_info().rss / 1024 ** 2:.2f} MB")

    # Ask to select a file
    file_name = filedialog.askopenfilename(initialdir="C:/",
                                           title="Select a file",
                                           filetypes=(("wav files", "*.wav"), ("all files", ".")))
    display_name = Label(frame, text=file_name.split("/")[-1])
    display_name.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    start_time = time.time()  
    if selected_dataset == "savee":
        emotion = make_prediction_savee(file_name)
    elif selected_dataset == "tess":
        emotion = make_prediction_tess(file_name)
    end_time = time.time()

    elapsed_time = end_time - start_time  # Calculate the elapsed time
    print(f"Execution time: {elapsed_time} seconds")


    waiting_label.place_forget()

    select_button = Button(frame, text="Select file", padx=20, pady=5, bg="white", command=select_file)
    select_button.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    display_emotion = Label(frame, text=emotion)
    display_emotion.grid(row=1, column=1, columnspan=2, pady=20)

    # print(f"Memory after displaying emotion: {process.memory_info().rss / 1024 ** 2:.2f} MB")

    # Initialize the original player with the file path
    player_original = AudioFilePlayer(file_name)

    # Initialize the modified player (initially no modifications)
    player_modified = RealTimeAudioPlayer(file_name)

    # Play and Pause buttons for Original Audio
    play_button_original = Button(frame, text="Play Original", padx=6, pady=4, bg="white", command=player_original.play)
    pause_button_original = Button(frame, text="Pause Original", padx=6, pady=4, bg="white", command=player_original.pause)

    play_button_original.grid(row=0, column=2, padx=10, pady=10, sticky="e")
    pause_button_original.grid(row=0, column=3, padx=10, pady=10, sticky="e")

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
    Label(frame, text="Pitch Shift (semitones):").grid(row=2, column=0, padx=10, pady=10)
    pitch_slider = Scale(frame, from_=-4, to=4, resolution=0.01, orient="horizontal", length=200, command=update_pitch)
    pitch_slider.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

    # Tempo slider
    Label(frame, text="Tempo Multiplier:").grid(row=3, column=0, padx=10, pady=10)
    tempo_slider = Scale(frame, from_=0.5, to=3.0, resolution=0.01, orient="horizontal", length=200, command=update_tempo)
    tempo_slider.grid(row=3, column=1, columnspan=2, padx=10, pady=10)
    tempo_slider.set(1)

    # Volume slider
    Label(frame, text="Volume:").grid(row=4, column=0, padx=10, pady=10)
    volume_slider = Scale(frame, from_=0.0, to=2.0, resolution=0.01, orient="horizontal", length=200, command=update_volume)
    volume_slider.grid(row=4, column=1, columnspan=2, padx=10, pady=10)
    volume_slider.set(1)

    # Play and Pause buttons for Modified Audio
    play_button_modified = Button(frame, text="Play Modified", padx=6, pady=4, bg="white", command=player_modified.play)
    pause_button_modified = Button(frame, text="Pause Modified", padx=6, pady=4, bg="white", command=player_modified.pause)

    play_button_modified.grid(row=6, column=1, padx=10, pady=10)
    pause_button_modified.grid(row=6, column=2, padx=10, pady=10)

    # Save button for the modified audio
    save_button = Button(frame, text="Save Modified", padx=6, pady=4, bg="white", command=lambda: save_modified_audio())
    save_button.grid(row=6, column=3, padx=10, pady=10)

    # Buttons to change emotion from neutral
    if emotion == "neutral":
        happy_button = Button(frame, text="Happy", padx=6, pady=4, bg="white", command=lambda: change_emotion.neutral_to_happy(player_modified, pitch_slider, tempo_slider, volume_slider))
        happy_button.grid(row=5, column=0, padx=10, pady=10)

        sad_button = Button(frame, text="Sad", padx=6, pady=4, bg="white", command=lambda: change_emotion.neutral_to_sad(player_modified, pitch_slider, tempo_slider, volume_slider))
        sad_button.grid(row=5, column=1, padx=10, pady=10)
        
        angry_button = Button(frame, text="Angry", padx=6, pady=4, bg="white", command=lambda: change_emotion.neutral_to_angry(player_modified, pitch_slider, tempo_slider, volume_slider))
        angry_button.grid(row=5, column=2, padx=10, pady=10)
        
        fearful_button = Button(frame, text="Fearful", padx=6, pady=4, bg="white", command=lambda: change_emotion.neutral_to_fearful(player_modified, pitch_slider, tempo_slider, volume_slider))
        fearful_button.grid(row=5, column=3, padx=10, pady=10)
        
        disgusted_button = Button(frame, text="Disgusted", padx=6, pady=4, bg="white", command=lambda: change_emotion.neutral_to_disgusted(player_modified, pitch_slider, tempo_slider, volume_slider))
        disgusted_button.grid(row=5, column=4, padx=10, pady=10)

        surprised_button = Button(frame, text="Surprised", padx=6, pady=4, bg="white", command=lambda: change_emotion.neutral_to_surprised(player_modified, pitch_slider, tempo_slider, volume_slider))
        surprised_button.grid(row=5, column=5, padx=10, pady=10)

    # Buttons to change emotion from happy
    elif emotion == "happy":
        neutral_button = Button(frame, text="Neutral", padx=6, pady=4, bg="white", command=lambda: change_emotion.happy_to_neutral(player_modified, pitch_slider, tempo_slider, volume_slider))
        neutral_button.grid(row=5, column=0, padx=10, pady=10)

        sad_button = Button(frame, text="Sad", padx=6, pady=4, bg="white", command=lambda: change_emotion.happy_to_sad(player_modified, pitch_slider, tempo_slider, volume_slider))
        sad_button.grid(row=5, column=1, padx=10, pady=10)
        
        angry_button = Button(frame, text="Angry", padx=6, pady=4, bg="white", command=lambda: change_emotion.happy_to_angry(player_modified, pitch_slider, tempo_slider, volume_slider))
        angry_button.grid(row=5, column=2, padx=10, pady=10)
        
        fearful_button = Button(frame, text="Fearful", padx=6, pady=4, bg="white", command=lambda: change_emotion.happy_to_fearful(player_modified, pitch_slider, tempo_slider, volume_slider))
        fearful_button.grid(row=5, column=3, padx=10, pady=10)
        
        disgusted_button = Button(frame, text="Disgusted", padx=6, pady=4, bg="white", command=lambda: change_emotion.happy_to_disgusted(player_modified, pitch_slider, tempo_slider, volume_slider))
        disgusted_button.grid(row=5, column=4, padx=10, pady=10)

        surprised_button = Button(frame, text="Surprised", padx=6, pady=4, bg="white", command=lambda: change_emotion.happy_to_surprised(player_modified, pitch_slider, tempo_slider, volume_slider))
        surprised_button.grid(row=5, column=5, padx=10, pady=10)

    # Buttons to change emotion from sad
    elif emotion == "sadness":
        neutral_button = Button(frame, text="Neutral", padx=6, pady=4, bg="white", command=lambda: change_emotion.sad_to_neutral(player_modified, pitch_slider, tempo_slider, volume_slider))
        neutral_button.grid(row=5, column=0, padx=10, pady=10)

        happy_button = Button(frame, text="Happy", padx=6, pady=4, bg="white", command=lambda: change_emotion.sad_to_happy(player_modified, pitch_slider, tempo_slider, volume_slider))
        happy_button.grid(row=5, column=1, padx=10, pady=10)
        
        angry_button = Button(frame, text="Angry", padx=6, pady=4, bg="white", command=lambda: change_emotion.sad_to_angry(player_modified, pitch_slider, tempo_slider, volume_slider))
        angry_button.grid(row=5, column=2, padx=10, pady=10)
        
        fearful_button = Button(frame, text="Fearful", padx=6, pady=4, bg="white", command=lambda: change_emotion.sad_to_fearful(player_modified, pitch_slider, tempo_slider, volume_slider))
        fearful_button.grid(row=5, column=3, padx=10, pady=10)
        
        disgusted_button = Button(frame, text="Disgusted", padx=6, pady=4, bg="white", command=lambda: change_emotion.sad_to_disgusted(player_modified, pitch_slider, tempo_slider, volume_slider))
        disgusted_button.grid(row=5, column=4, padx=10, pady=10)

        surprised_button = Button(frame, text="Surprised", padx=6, pady=4, bg="white", command=lambda: change_emotion.sad_to_surprised(player_modified, pitch_slider, tempo_slider, volume_slider))
        surprised_button.grid(row=5, column=5, padx=10, pady=10)

    # Buttons to change emotion from angry
    elif emotion == "angry":
        neutral_button = Button(frame, text="Neutral", padx=6, pady=4, bg="white", command=lambda: change_emotion.angry_to_neutral(player_modified, pitch_slider, tempo_slider, volume_slider))
        neutral_button.grid(row=5, column=0, padx=10, pady=10)

        happy_button = Button(frame, text="Happy", padx=6, pady=4, bg="white", command=lambda: change_emotion.angry_to_happy(player_modified, pitch_slider, tempo_slider, volume_slider))
        happy_button.grid(row=5, column=1, padx=10, pady=10)
        
        sad_button = Button(frame, text="Sad", padx=6, pady=4, bg="white", command=lambda: change_emotion.angry_to_sad(player_modified, pitch_slider, tempo_slider, volume_slider))
        sad_button.grid(row=5, column=2, padx=10, pady=10)
        
        fearful_button = Button(frame, text="Fearful", padx=6, pady=4, bg="white", command=lambda: change_emotion.angry_to_fearful(player_modified, pitch_slider, tempo_slider, volume_slider))
        fearful_button.grid(row=5, column=3, padx=10, pady=10)
        
        disgusted_button = Button(frame, text="Disgusted", padx=6, pady=4, bg="white", command=lambda: change_emotion.angry_to_disgusted(player_modified, pitch_slider, tempo_slider, volume_slider))
        disgusted_button.grid(row=5, column=4, padx=10, pady=10)

        surprised_button = Button(frame, text="Surprised", padx=6, pady=4, bg="white", command=lambda: change_emotion.angry_to_surprised(player_modified, pitch_slider, tempo_slider, volume_slider))
        surprised_button.grid(row=5, column=5, padx=10, pady=10)

    # Buttons to change emotion from fearful
    elif emotion == "fearful":
        neutral_button = Button(frame, text="Neutral", padx=6, pady=4, bg="white", command=lambda: change_emotion.fearful_to_neutral(player_modified, pitch_slider, tempo_slider, volume_slider))
        neutral_button.grid(row=5, column=0, padx=10, pady=10)

        happy_button = Button(frame, text="Happy", padx=6, pady=4, bg="white", command=lambda: change_emotion.fearful_to_happy(player_modified, pitch_slider, tempo_slider, volume_slider))
        happy_button.grid(row=5, column=1, padx=10, pady=10)
        
        sad_button = Button(frame, text="Sad", padx=6, pady=4, bg="white", command=lambda: change_emotion.fearful_to_sad(player_modified, pitch_slider, tempo_slider, volume_slider))
        sad_button.grid(row=5, column=2, padx=10, pady=10)
        
        angry_button = Button(frame, text="Angry", padx=6, pady=4, bg="white", command=lambda: change_emotion.fearful_to_angry(player_modified, pitch_slider, tempo_slider, volume_slider))
        angry_button.grid(row=5, column=3, padx=10, pady=10)
        
        disgusted_button = Button(frame, text="Disgusted", padx=6, pady=4, bg="white", command=lambda: change_emotion.fearful_to_disgusted(player_modified, pitch_slider, tempo_slider, volume_slider))
        disgusted_button.grid(row=5, column=4, padx=10, pady=10)

        surprised_button = Button(frame, text="Surprised", padx=6, pady=4, bg="white", command=lambda: change_emotion.fearful_to_surprised(player_modified, pitch_slider, tempo_slider, volume_slider))
        surprised_button.grid(row=5, column=5, padx=10, pady=10)

    # Buttons to change emotion from disgusted
    elif emotion == "disgusted":
        neutral_button = Button(frame, text="Neutral", padx=6, pady=4, bg="white", command=lambda: change_emotion.disgusted_to_neutral(player_modified, pitch_slider, tempo_slider, volume_slider))
        neutral_button.grid(row=5, column=0, padx=10, pady=10)

        happy_button = Button(frame, text="Happy", padx=6, pady=4, bg="white", command=lambda: change_emotion.disgusted_to_happy(player_modified, pitch_slider, tempo_slider, volume_slider))
        happy_button.grid(row=5, column=1, padx=10, pady=10)
        
        sad_button = Button(frame, text="Sad", padx=6, pady=4, bg="white", command=lambda: change_emotion.disgusted_to_sad(player_modified, pitch_slider, tempo_slider, volume_slider))
        sad_button.grid(row=5, column=2, padx=10, pady=10)
        
        angry_button = Button(frame, text="Angry", padx=6, pady=4, bg="white", command=lambda: change_emotion.disgusted_to_angry(player_modified, pitch_slider, tempo_slider, volume_slider))
        angry_button.grid(row=5, column=3, padx=10, pady=10)
        
        fearful_button = Button(frame, text="Fearful", padx=6, pady=4, bg="white", command=lambda: change_emotion.disgusted_to_fearful(player_modified, pitch_slider, tempo_slider, volume_slider))
        fearful_button.grid(row=5, column=4, padx=10, pady=10)

        surprised_button = Button(frame, text="Surprised", padx=6, pady=4, bg="white", command=lambda: change_emotion.disgusted_to_surprised(player_modified, pitch_slider, tempo_slider, volume_slider))
        surprised_button.grid(row=5, column=5, padx=10, pady=10)

    # Buttons to change emotion from surprised
    elif emotion == "surprised":
        neutral_button = Button(frame, text="Neutral", padx=6, pady=4, bg="white", command=lambda: change_emotion.surprised_to_neutral(player_modified, pitch_slider, tempo_slider, volume_slider))
        neutral_button.grid(row=5, column=0, padx=10, pady=10)

        happy_button = Button(frame, text="Happy", padx=6, pady=4, bg="white", command=lambda: change_emotion.surprised_to_happy(player_modified, pitch_slider, tempo_slider, volume_slider))
        happy_button.grid(row=5, column=1, padx=10, pady=10)
        
        sad_button = Button(frame, text="Sad", padx=6, pady=4, bg="white", command=lambda: change_emotion.surprised_to_sad(player_modified, pitch_slider, tempo_slider, volume_slider))
        sad_button.grid(row=5, column=2, padx=10, pady=10)
        
        angry_button = Button(frame, text="Angry", padx=6, pady=4, bg="white", command=lambda: change_emotion.surprised_to_angry(player_modified, pitch_slider, tempo_slider, volume_slider))
        angry_button.grid(row=5, column=3, padx=10, pady=10)
        
        fearful_button = Button(frame, text="Fearful", padx=6, pady=4, bg="white", command=lambda: change_emotion.surprised_to_fearful(player_modified, pitch_slider, tempo_slider, volume_slider))
        fearful_button.grid(row=5, column=4, padx=10, pady=10)

        disgusted_button = Button(frame, text="Disgusted", padx=6, pady=4, bg="white", command=lambda: change_emotion.surprised_to_disgusted(player_modified, pitch_slider, tempo_slider, volume_slider))
        disgusted_button.grid(row=5, column=5, padx=10, pady=10)


def save_modified_audio():
    global player_modified

    # Get modified audio and sample rate from player
    if player_modified is None:
        Label(frame, text="No modified audio to save!", fg="red").grid(row=6, column=4, padx=10, pady=10)
        return

    save_path = filedialog.asksaveasfilename(defaultextension=".wav",
                                             filetypes=[("WAV files", "*.wav"), ("All files", "*.*")],
                                             title="Save Modified Audio")
    if save_path:
        # Saving the modified audio using soundfile
        import soundfile as sf
        sf.write(save_path, player_modified.modified_audio.astype(np.int16), player_modified.sample_rate)
        Label(frame, text="File saved successfully!", fg="green").grid(row=6, column=4, padx=10, pady=10)


def close():
    global player_original, player_modified
    if player_original:
        player_original.stop()
    if player_modified:
        player_modified.stop()
    root.destroy()


########################  START THE WINDOW  ########################

select_file_button = Button(root, text="Select file", padx=20, pady=5, bg="white", command=select_file)
select_file_button.place(relx=0.5, rely=0.5, anchor="center")

# Stop recording if the window is closed
root.protocol('WM_DELETE_WINDOW', close)
root.mainloop()
