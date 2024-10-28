import ttkbootstrap as ttk
from player import (
    pause_music,
    stop_music,
    change_track,
    set_volume,
    on_progress_slider_press,
    on_progress_slider_release,
)
from playlist import load_music, save_playlist, load_playlist, clear_playlist, delete_selected_track, on_track_double_click
import state


def setup_ui():
    # Track name label
    state.track_name_label = ttk.Label(state.app, text="Track Name", anchor="center")
    state.track_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    # Main frame with progress slider
    main_frame = ttk.Frame(state.app)
    main_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    state.song_progress_slider = ttk.Scale(main_frame, from_=0, to=100, length=400)
    state.song_progress_slider.pack(side="left", fill="x", expand=True)
    state.song_progress_slider.bind("<Button-1>", on_progress_slider_press)
    state.song_progress_slider.bind("<ButtonRelease-1>", on_progress_slider_release)

    # Control buttons
    controls_frame = ttk.Frame(state.app)
    controls_frame.grid(row=2, column=0, pady=10, sticky="ew")

    control_buttons_frame = ttk.Frame(controls_frame)
    control_buttons_frame.pack(side="left", padx=10)

    stop_button = ttk.Button(control_buttons_frame, text=" ■  \u23F5", width=3, command=stop_music)
    stop_button.pack(side="left", padx=5)

    state.pause_button = ttk.Button(control_buttons_frame, text="▶", width=3, command=pause_music)
    state.pause_button.pack(side="left", padx=5)

    skip_back_button = ttk.Button(control_buttons_frame, text="⏮", width=3, command=lambda: change_track(-1))
    skip_back_button.pack(side="left", padx=5)

    skip_forward_button = ttk.Button(control_buttons_frame, text="⏭", width=3, command=lambda: change_track(1))
    skip_forward_button.pack(side="left", padx=5)

    # Volume control
    time_frame = ttk.Frame(controls_frame)
    time_frame.pack(side="right", padx=10)

    volume_frame = ttk.Frame(time_frame)
    volume_frame.pack(side="left", padx=10, pady=10, fill="x")

    state.volume_slider = ttk.Scale(volume_frame, from_=0, to=100, orient='horizontal', value=100, command=set_volume)
    state.volume_slider.pack()
    set_volume(None)

    # Time labels
    state.current_time_label = ttk.Label(time_frame, text="00:00")
    state.current_time_label.pack(side="left")

    state.max_time_label = ttk.Label(time_frame, text="/ 00:00")
    state.max_time_label.pack(side="left")

    # Playlist controls
    playlist_controls_frame = ttk.Frame(state.app)
    playlist_controls_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    load_button = ttk.Button(playlist_controls_frame, text="Add to playlist", command=load_music)
    load_button.pack(side="left", padx=5)

    save_playlist_button = ttk.Button(playlist_controls_frame, text="Save playlist", command=save_playlist)
    save_playlist_button.pack(side="left", padx=5)

    load_playlist_button = ttk.Button(playlist_controls_frame, text="Load playlist", command=load_playlist)
    load_playlist_button.pack(side="left", padx=5)

    clear_playlist_button = ttk.Button(playlist_controls_frame, text="Clear playlist", command=clear_playlist)
    clear_playlist_button.pack(side="left", padx=5)

    # Track table
    table_frame = ttk.Frame(state.app)
    table_frame.grid(row=4, column=0, padx=10, pady=5, sticky="nsew")

    state.app.grid_rowconfigure(4, weight=1)

    state.track_table = ttk.Treeview(
        table_frame, columns=('Playing', 'Number', 'Title', 'Artist/Album', 'Duration'), show='headings', height=10
    )
    state.track_table.heading('Playing', text='')
    state.track_table.heading('Number', text='#')
    state.track_table.heading('Title', text='Title')
    state.track_table.heading('Artist/Album', text='Artist/Album')
    state.track_table.heading('Duration', text='Duration')
    state.track_table.column('Playing', width=30, stretch=False)
    state.track_table.column('Number', width=30, stretch=False)
    state.track_table.column('Title', width=200, stretch=True)
    state.track_table.column('Artist/Album', width=150)
    state.track_table.column('Duration', width=80, stretch=False)

    state.track_table.pack(side="left", fill="both", expand=True)
    state.track_table.bind("<Double-1>", lambda event: on_track_double_click(event))
    state.track_table.bind("<Delete>", delete_selected_track)

    track_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=state.track_table.yview)
    track_scrollbar.pack(side="right", fill="y")
    state.track_table.configure(yscrollcommand=track_scrollbar.set)
