from tkinter import *
from tkinter import filedialog
import numpy as np
from audio_player import RealTimeAudioPlayer, AudioFilePlayer
from prediction import make_prediction
import change_emotion

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

    emotion = make_prediction(file_name)
    display_emotion = Label(root, text=emotion)
    display_emotion.grid(row=0, column=6)

    # Initialize the original player with the file path
    player_original = AudioFilePlayer(file_name)

    # Initialize the modified player (initially no modifications)
    player_modified = RealTimeAudioPlayer(file_name)

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

    # Buttons to change emotion from neutral
    if emotion == "neutral":
        happy_button = Button(root, text="Happy", padx=6, pady=4, bg="white", command=lambda: change_emotion.neutral_to_happy(player_modified))
        happy_button.grid(row=6, column=0, columnspan=1, padx=5, pady=10)

        sad_button = Button(root, text="Sad", padx=6, pady=4, bg="white", command=lambda: change_emotion.neutral_to_sad(player_modified))
        sad_button.grid(row=6, column=1, columnspan=1, padx=5, pady=10)
        
        angry_button = Button(root, text="Angry", padx=6, pady=4, bg="white", command=lambda: change_emotion.neutral_to_angry(player_modified))
        angry_button.grid(row=6, column=2, columnspan=1, padx=5, pady=10)
        
        fearful_button = Button(root, text="Fearful", padx=6, pady=4, bg="white", command=lambda: change_emotion.neutral_to_fearful(player_modified))
        fearful_button.grid(row=6, column=3, columnspan=1, padx=5, pady=10)
        
        disgusted_button = Button(root, text="Disgusted", padx=6, pady=4, bg="white", command=lambda: change_emotion.neutral_to_disgusted(player_modified))
        disgusted_button.grid(row=6, column=4, columnspan=1, padx=5, pady=10)

        surprised_button = Button(root, text="Surprised", padx=6, pady=4, bg="white", command=lambda: change_emotion.neutral_to_surprised(player_modified))
        surprised_button.grid(row=6, column=5, columnspan=1, padx=5, pady=10)

    # Buttons to change emotion from happy
    elif emotion == "happy":
        neutral_button = Button(root, text="Neutral", padx=6, pady=4, bg="white", command=lambda: change_emotion.happy_to_neutral(player_modified))
        neutral_button.grid(row=6, column=0, columnspan=1, padx=5, pady=10)

        sad_button = Button(root, text="Sad", padx=6, pady=4, bg="white", command=lambda: change_emotion.happy_to_sad(player_modified))
        sad_button.grid(row=6, column=1, columnspan=1, padx=5, pady=10)
        
        angry_button = Button(root, text="Angry", padx=6, pady=4, bg="white", command=lambda: change_emotion.happy_to_angry(player_modified))
        angry_button.grid(row=6, column=2, columnspan=1, padx=5, pady=10)
        
        fearful_button = Button(root, text="Fearful", padx=6, pady=4, bg="white", command=lambda: change_emotion.happy_to_fearful(player_modified))
        fearful_button.grid(row=6, column=3, columnspan=1, padx=5, pady=10)
        
        disgusted_button = Button(root, text="Disgusted", padx=6, pady=4, bg="white", command=lambda: change_emotion.happy_to_disgusted(player_modified))
        disgusted_button.grid(row=6, column=4, columnspan=1, padx=5, pady=10)

        surprised_button = Button(root, text="Surprised", padx=6, pady=4, bg="white", command=lambda: change_emotion.happy_to_surprised(player_modified))
        surprised_button.grid(row=6, column=5, columnspan=1, padx=5, pady=10)

    # Buttons to change emotion from sad
    elif emotion == "sadness":
        neutral_button = Button(root, text="Neutral", padx=6, pady=4, bg="white", command=lambda: change_emotion.sad_to_neutral(player_modified))
        neutral_button.grid(row=6, column=0, columnspan=1, padx=5, pady=10)

        happy_button = Button(root, text="Happy", padx=6, pady=4, bg="white", command=lambda: change_emotion.sad_to_happy(player_modified))
        happy_button.grid(row=6, column=1, columnspan=1, padx=5, pady=10)
        
        angry_button = Button(root, text="Angry", padx=6, pady=4, bg="white", command=lambda: change_emotion.sad_to_angry(player_modified))
        angry_button.grid(row=6, column=2, columnspan=1, padx=5, pady=10)
        
        fearful_button = Button(root, text="Fearful", padx=6, pady=4, bg="white", command=lambda: change_emotion.sad_to_fearful(player_modified))
        fearful_button.grid(row=6, column=3, columnspan=1, padx=5, pady=10)
        
        disgusted_button = Button(root, text="Disgusted", padx=6, pady=4, bg="white", command=lambda: change_emotion.sad_to_disgusted(player_modified))
        disgusted_button.grid(row=6, column=4, columnspan=1, padx=5, pady=10)

        surprised_button = Button(root, text="Surprised", padx=6, pady=4, bg="white", command=lambda: change_emotion.sad_to_surprised(player_modified))
        surprised_button.grid(row=6, column=5, columnspan=1, padx=5, pady=10)

    # Buttons to change emotion from angry
    elif emotion == "angry":
        neutral_button = Button(root, text="Neutral", padx=6, pady=4, bg="white", command=lambda: change_emotion.angry_to_neutral(player_modified))
        neutral_button.grid(row=6, column=0, columnspan=1, padx=5, pady=10)

        happy_button = Button(root, text="Happy", padx=6, pady=4, bg="white", command=lambda: change_emotion.angry_to_happy(player_modified))
        happy_button.grid(row=6, column=1, columnspan=1, padx=5, pady=10)
        
        sad_button = Button(root, text="Sad", padx=6, pady=4, bg="white", command=lambda: change_emotion.angry_to_sad(player_modified))
        sad_button.grid(row=6, column=2, columnspan=1, padx=5, pady=10)
        
        fearful_button = Button(root, text="Fearful", padx=6, pady=4, bg="white", command=lambda: change_emotion.angry_to_fearful(player_modified))
        fearful_button.grid(row=6, column=3, columnspan=1, padx=5, pady=10)
        
        disgusted_button = Button(root, text="Disgusted", padx=6, pady=4, bg="white", command=lambda: change_emotion.angry_to_disgusted(player_modified))
        disgusted_button.grid(row=6, column=4, columnspan=1, padx=5, pady=10)

        surprised_button = Button(root, text="Surprised", padx=6, pady=4, bg="white", command=lambda: change_emotion.angry_to_surprised(player_modified))
        surprised_button.grid(row=6, column=5, columnspan=1, padx=5, pady=10)

    # Buttons to change emotion from fearful
    elif emotion == "fearful":
        neutral_button = Button(root, text="Neutral", padx=6, pady=4, bg="white", command=lambda: change_emotion.fearful_to_neutral(player_modified))
        neutral_button.grid(row=6, column=0, columnspan=1, padx=5, pady=10)

        happy_button = Button(root, text="Happy", padx=6, pady=4, bg="white", command=lambda: change_emotion.fearful_to_happy(player_modified))
        happy_button.grid(row=6, column=1, columnspan=1, padx=5, pady=10)
        
        sad_button = Button(root, text="Sad", padx=6, pady=4, bg="white", command=lambda: change_emotion.fearful_to_sad(player_modified))
        sad_button.grid(row=6, column=2, columnspan=1, padx=5, pady=10)
        
        angry_button = Button(root, text="Angry", padx=6, pady=4, bg="white", command=lambda: change_emotion.fearful_to_angry(player_modified))
        angry_button.grid(row=6, column=3, columnspan=1, padx=5, pady=10)
        
        disgusted_button = Button(root, text="Disgusted", padx=6, pady=4, bg="white", command=lambda: change_emotion.fearful_to_disgusted(player_modified))
        disgusted_button.grid(row=6, column=4, columnspan=1, padx=5, pady=10)

        surprised_button = Button(root, text="Surprised", padx=6, pady=4, bg="white", command=lambda: change_emotion.fearful_to_surprised(player_modified))
        surprised_button.grid(row=6, column=5, columnspan=1, padx=5, pady=10)

    # Buttons to change emotion from disgusted
    elif emotion == "disgusted":
        neutral_button = Button(root, text="Neutral", padx=6, pady=4, bg="white", command=lambda: change_emotion.disgusted_to_neutral(player_modified))
        neutral_button.grid(row=6, column=0, columnspan=1, padx=5, pady=10)

        happy_button = Button(root, text="Happy", padx=6, pady=4, bg="white", command=lambda: change_emotion.disgusted_to_happy(player_modified))
        happy_button.grid(row=6, column=1, columnspan=1, padx=5, pady=10)
        
        sad_button = Button(root, text="Sad", padx=6, pady=4, bg="white", command=lambda: change_emotion.disgusted_to_sad(player_modified))
        sad_button.grid(row=6, column=2, columnspan=1, padx=5, pady=10)
        
        angry_button = Button(root, text="Angry", padx=6, pady=4, bg="white", command=lambda: change_emotion.disgusted_to_angry(player_modified))
        angry_button.grid(row=6, column=3, columnspan=1, padx=5, pady=10)
        
        fearful_button = Button(root, text="Fearful", padx=6, pady=4, bg="white", command=lambda: change_emotion.disgusted_to_fearful(player_modified))
        fearful_button.grid(row=6, column=4, columnspan=1, padx=5, pady=10)

        surprised_button = Button(root, text="Surprised", padx=6, pady=4, bg="white", command=lambda: change_emotion.disgusted_to_surprised(player_modified))
        surprised_button.grid(row=6, column=5, columnspan=1, padx=5, pady=10)

    # Buttons to change emotion from surprised
    elif emotion == "surprised":
        neutral_button = Button(root, text="Neutral", padx=6, pady=4, bg="white", command=lambda: change_emotion.surprised_to_neutral(player_modified))
        neutral_button.grid(row=6, column=0, columnspan=1, padx=5, pady=10)

        happy_button = Button(root, text="Happy", padx=6, pady=4, bg="white", command=lambda: change_emotion.surprised_to_happy(player_modified))
        happy_button.grid(row=6, column=1, columnspan=1, padx=5, pady=10)
        
        sad_button = Button(root, text="Sad", padx=6, pady=4, bg="white", command=lambda: change_emotion.surprised_to_sad(player_modified))
        sad_button.grid(row=6, column=2, columnspan=1, padx=5, pady=10)
        
        angry_button = Button(root, text="Angry", padx=6, pady=4, bg="white", command=lambda: change_emotion.surprised_to_angry(player_modified))
        angry_button.grid(row=6, column=3, columnspan=1, padx=5, pady=10)
        
        fearful_button = Button(root, text="Fearful", padx=6, pady=4, bg="white", command=lambda: change_emotion.surprised_to_fearful(player_modified))
        fearful_button.grid(row=6, column=4, columnspan=1, padx=5, pady=10)

        disgusted_button = Button(root, text="Disgusted", padx=6, pady=4, bg="white", command=lambda: change_emotion.surprised_to_disgusted(player_modified))
        disgusted_button.grid(row=6, column=5, columnspan=1, padx=5, pady=10)


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
