import ttkbootstrap as ttk
from tkinter import filedialog
import pygame


mixer_volume = 100

pygame.mixer.init()

def load_music():
    file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3"), ("WAV Files", "*.wav"), ("All Files", "*.*")])
    if file_path:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

def pause_music():
    pygame.mixer.music.pause()

def unpause_music():
    pygame.mixer.music.unpause()

def stop_music():
    pygame.mixer.music.stop()

def set_volume(event):
    volume = volume_slider.get() / 100
    pygame.mixer.music.set_volume(volume)


app = ttk.Window(themename="darkly")
app.title("Music Player")
app.geometry("400x300")

song_slider = ttk.Scale(from_=0, to=100)
song_slider.pack(pady=10)

load_button = ttk.Button(app, text="Play from file", command=load_music)
load_button.pack(pady=10)

pause_button = ttk.Button(app, text="Pause", command=pause_music)
pause_button.pack(pady=10)

unpause_button = ttk.Button(app, text="Unpause", command=unpause_music)
unpause_button.pack(pady=10)

stop_button = ttk.Button(app, text="Stop", command=stop_music)
stop_button.pack(pady=10)

volume_slider = ttk.Scale(from_=100, to=0, orient='vertical', value=mixer_volume, command=set_volume)
volume_slider.pack(pady=10)
set_volume(None)

app.mainloop()