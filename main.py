import ttkbootstrap as ttk
from tkinter import filedialog
import pygame
import os

mixer_volume = 100
song_length_in_s = 0
track_list = []
current_track_index = 0

current_song_time = 0
is_timer_running = False

user_dragging_progress_slider = False
progress_update_job = None

pygame.mixer.init()

def format_time(seconds):
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02}:{secs:02}"

def load_music():
    global song_length_in_s, current_song_time, is_timer_running, progress_update_job, current_track_index
    file_paths = filedialog.askopenfilenames(
        filetypes=[("MP3 Files", "*.mp3"), ("WAV Files", "*.wav"), ("All Files", "*.*")])
    if file_paths:
        for file_path in file_paths:
            track_list.append(file_path)
            file_name = os.path.basename(file_path)
            track_table.insert('', 'end', values=('', len(track_list), file_name, '', ''))

    if len(track_list) > 0:
        current_track_index = 0
        play_track(current_track_index)

def play_track(index):
    global song_length_in_s, current_song_time, is_timer_running, progress_update_job, current_track_index
    current_track_index = index
    file_path = track_list[index]

    if progress_update_job is not None:
        app.after_cancel(progress_update_job)

    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    song_length_in_s = 300  # Example length, you can replace it with actual song length logic
    song_progress_slider.config(to=song_length_in_s)
    max_time_label.config(text=f"/ {format_time(song_length_in_s)}")
    current_song_time = 0
    is_timer_running = True
    update_progress_slider()

    file_name = os.path.basename(file_path)
    track_name_label.config(text=file_name)

    item_ids = track_table.get_children()

    for i, item_id in enumerate(item_ids):
        if i == index:
            track_table.item(item_id, values=('▶', i + 1,
                                        track_table.item(item_id, 'values')[2], track_table.item(item_id, 'values')[3], track_table.item(item_id, 'values')[4]))
        else:
            track_table.item(item_id, values=('', i + 1,
                                        track_table.item(item_id, 'values')[2], track_table.item(item_id, 'values')[3], track_table.item(item_id, 'values')[4]))



def pause_music():
    global is_timer_running
    if is_timer_running:
        pygame.mixer.music.pause()
        is_timer_running = False
        pause_button.config(text="▶")
    else:
        pygame.mixer.music.unpause()
        is_timer_running = True
        pause_button.config(text="⏸︎")

def stop_music():
    global current_song_time, is_timer_running, progress_update_job
    pygame.mixer.music.stop()
    current_time_label.config(text=format_time(0))
    current_song_time = 0
    is_timer_running = False
    if progress_update_job is not None:
        app.after_cancel(progress_update_job)

def set_volume(event):
    volume = volume_slider.get() / 100
    pygame.mixer.music.set_volume(volume)

def update_progress_slider():
    global current_song_time, progress_update_job
    if is_timer_running and not user_dragging_progress_slider:
        current_song_time += 1
        if current_song_time <= song_length_in_s:
            song_progress_slider.set(current_song_time)
            current_time_label.config(text=format_time(current_song_time))
    progress_update_job = app.after(1000, update_progress_slider)

def on_progress_slider_press(event):
    global user_dragging_progress_slider
    user_dragging_progress_slider = True

def on_progress_slider_release(event):
    global user_dragging_progress_slider, current_song_time
    user_dragging_progress_slider = False

    current_song_time = int(song_progress_slider.get())
    pygame.mixer.music.pause()
    pygame.mixer.music.set_pos(current_song_time)
    current_time_label.config(text=format_time(current_song_time))
    pygame.mixer.music.unpause()

def on_track_double_click(event):
    selected_item = track_table.selection()

    if selected_item:
        track_number = int(track_table.item(selected_item)['values'][1]) - 1
        play_track(track_number)


app = ttk.Window(themename="darkly")
app.title("Music Player")
app.geometry("550x600")

app.grid_columnconfigure(0, weight=1)

track_name_label = ttk.Label(app, text="Track Name", anchor="center")
track_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

main_frame = ttk.Frame(app)
main_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

song_progress_slider = ttk.Scale(main_frame, from_=0, to=100, length=400)
song_progress_slider.pack(side="left", fill="x", expand=True)
song_progress_slider.bind("<Button-1>", on_progress_slider_press)
song_progress_slider.bind("<ButtonRelease-1>", on_progress_slider_release)

controls_frame = ttk.Frame(app)
controls_frame.grid(row=2, column=0, pady=10, sticky="ew")

control_buttons_frame = ttk.Frame(controls_frame)
control_buttons_frame.pack(side="left", padx=10)

skip_back_button = ttk.Button(control_buttons_frame, text="⏮︎︎")
skip_back_button.pack(side="left", padx=5)

stop_button = ttk.Button(control_buttons_frame, text="⏹︎", command=stop_music)
stop_button.pack(side="left", padx=5)

pause_button = ttk.Button(control_buttons_frame, text="⏸︎", command=pause_music)
pause_button.pack(side="left", padx=5)

skip_forward_button = ttk.Button(control_buttons_frame, text="⏭︎")
skip_forward_button.pack(side="left", padx=5)

time_frame = ttk.Frame(controls_frame)
time_frame.pack(side="right", padx=10)

volume_frame = ttk.Frame(time_frame)
volume_frame.pack(side="left", padx=10, pady=10, fill="x")

volume_slider = ttk.Scale(volume_frame, from_=0, to=100, orient='horizontal', value=mixer_volume, command=set_volume)
volume_slider.pack()
set_volume(None)

current_time_label = ttk.Label(time_frame, text="00:00")
current_time_label.pack(side="left")

max_time_label = ttk.Label(time_frame, text="/ 00:00")
max_time_label.pack(side="left")

playlist_controls_frame = ttk.Frame(app)
playlist_controls_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

load_button = ttk.Button(playlist_controls_frame, text="Add to playlist", command=load_music)
load_button.pack(side="left", padx=5)

save_playlist_button = ttk.Button(playlist_controls_frame, text="Save playlist")
save_playlist_button.pack(side="left", padx=5)

load_playlist_button = ttk.Button(playlist_controls_frame, text="Load playlist")
load_playlist_button.pack(side="left", padx=5)

clear_playlist_button = ttk.Button(playlist_controls_frame, text="Clear playlist")
clear_playlist_button.pack(side="left", padx=5)

table_frame = ttk.Frame(app)
table_frame.grid(row=4, column=0, padx=10, pady=5, sticky="nsew")

app.grid_rowconfigure(4, weight=1)

track_table = ttk.Treeview(table_frame, columns=('Playing', 'Number', 'Title', 'Artist/Album', 'Duration'), show='headings', height=10)
track_table.heading('Playing', text='')
track_table.heading('Number', text='#')
track_table.heading('Title', text='Title')
track_table.heading('Artist/Album', text='Artist/Album')
track_table.heading('Duration', text='Duration')
track_table.column('Playing', width=30, stretch=False)
track_table.column('Number', width=30, stretch=False)
track_table.column('Title', width=200, stretch=True)
track_table.column('Artist/Album', width=150)
track_table.column('Duration', width=80, stretch=False)

track_table.pack(side="left", fill="both", expand=True)
track_table.bind("<Double-1>", on_track_double_click)

track_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=track_table.yview)
track_scrollbar.pack(side="right", fill="y")
track_table.configure(yscrollcommand=track_scrollbar.set)

app.mainloop()