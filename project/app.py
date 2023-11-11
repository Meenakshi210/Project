from flask import Flask, render_template, send_from_directory
import os
import random

app = Flask(__name__, static_folder='static')

# Define the directory where your audio files are stored
audio_directory = "audio"
thumbnail_file = "image.jpg"

# Get a list of audio files and shuffle them
audio_files = os.listdir(audio_directory)
random.shuffle(audio_files)

# Initialize variables to keep track of the current song index and shuffle state
current_song_index = 0
is_shuffled = True

@app.route("/")
def index():
    return render_template("index.html", audio_files=audio_files, thumbnail_file=thumbnail_file, current_song_index=current_song_index)

@app.route("/audio/<path:filename>")
def serve_audio(filename):
    return send_from_directory(audio_directory, filename)

@app.route("/image/<path:filename>")
def serve_image(filename):
    return send_from_directory('static', filename)

@app.route("/play/<int:song_index>")
def play(song_index):
    global current_song_index
    current_song_index = song_index
    return render_template("play.html", audio_file=audio_files[song_index], thumbnail_file=thumbnail_file, current_song_index=current_song_index)

@app.route("/next")
def play_next():
    global current_song_index
    if is_shuffled:
        current_song_index = (current_song_index + 1) % len(audio_files)
    else:
        current_song_index = min(current_song_index + 1, len(audio_files) - 1)
    return render_template("play.html", audio_file=audio_files[current_song_index], thumbnail_file=thumbnail_file, current_song_index=current_song_index)

@app.route("/prev")
def play_previous():
    global current_song_index
    if is_shuffled:
        current_song_index = (current_song_index - 1) % len(audio_files)
    else:
        current_song_index = max(current_song_index - 1, 0)
    return render_template("play.html", audio_file=audio_files[current_song_index], thumbnail_file=thumbnail_file, current_song_index=current_song_index)

@app.route("/shuffle")
def toggle_shuffle():
    global is_shuffled
    is_shuffled = not is_shuffled
    return render_template("play.html", audio_file=audio_files[current_song_index], thumbnail_file=thumbnail_file, current_song_index=current_song_index)

if __name__ == "__main__":
    app.run(debug=True)

