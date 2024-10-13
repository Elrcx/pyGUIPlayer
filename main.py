import ttkbootstrap as ttk


app = ttk.Window(themename="darkly")
app.title("Music Player")
app.geometry("400x300")

load_button = ttk.Button(app, text="Play from file")
load_button.pack(pady=10)

pause_button = ttk.Button(app, text="Pause")
pause_button.pack(pady=10)

unpause_button = ttk.Button(app, text="Unpause")
unpause_button.pack(pady=10)

stop_button = ttk.Button(app, text="Stop")
stop_button.pack(pady=10)

app.mainloop()