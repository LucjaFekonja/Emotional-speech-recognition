from tkinter import *
from tkinter import filedialog
from app.read_file import read_file, play_audio
from app.audio_player import AudioPlayer
import threading


root = Tk()
root.title("Emotion recognition of speech")
root.geometry("380x400")

# Get filename
player = None
thread = None
file_name = None

def select_file():
    root.filename = filedialog.askopenfilename(initialdir="C:/School/RZP/vaje/Projekt", 
                                               title="Select a file", 
                                               filetypes=(("wav files", "*.wav"), ("mp3 files", "*.mp3"), ("all files", ".")))
    display_name = Label(root, text=root.filename.split("/")[-1])
    display_name.grid(row=0, column = 0)

    global file_name
    file_name = root.filename

    start_button = Button(root, text="Play", padx=6, pady=4, bg="white", command=start)
    start_button.grid(row=0, column=2)


def start():
    global player
    player = AudioPlayer(root.filename)

    global thread
    thread = threading.Thread(target=player.play)
    thread.start()

    play_button = Button(root, text="Play", padx=6, pady=4, bg="white", command=lambda: player.unpause())
    pause_button = Button(root, text="Pause", padx=6, pady=4, bg="white", command=lambda: player.pause())

    play_button.grid(row=0, column=2)
    pause_button.grid(row=0, column=3)


def close():
    global player 
    player.stop()

    global thread
    thread.join()
    
    root.destroy()


# Create widgets

emotion = Label(root, text="<emotion>")
select_file_button = Button(root, text="Select file", padx=20, pady=5, bg="white", command=select_file)


# Show on root

select_file_button.grid(row=0, column=1)
emotion.grid(row=1, column=0)



root.protocol('WM_DELETE_WINDOW', close)
root.mainloop()