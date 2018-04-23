from flask import Flask, jsonify, send_file, Response, render_template
#from redis import StrictRedis as Redis
import threading
from mpd import MPDClient
from pathlib import Path
import re
import json

MUSIC_FOLDER = '/home/codl/media/music'
app = Flask('thing')


def get_mpd():
    local = threading.local()
    if not hasattr(local, 'mpd'):
        local.mpd = MPDClient()
        local.mpd.connect('127.0.0.1', 6600)
    return local.mpd


def playing():
    try:
        mpd = get_mpd()
        status = mpd.status()
        song = mpd.playlistid(status['songid'])[0]
        status.update(song)
        return status
    except Exception:
        return None


@app.route('/playing')
def show_playing():
    return jsonify(playing())


COVER_REGEX = (
    re.compile(
        '^(?:.*front|.*cover|folder)\.(?:jpe?g|gif|png)$',
        re.I),
    re.compile(
        '\.(?:jpe?g|gif|png)$',
        re.I)
)

@app.route('/cover')
def show_cover_art():
    path = Path(MUSIC_FOLDER) / playing()['file']
    folder = path.parent
    cover_path = None
    for regex in COVER_REGEX:
        for child in folder.iterdir():
            if regex.search(str(child)):
                return send_file(str(child))
    return '', 404


@app.route('/stream')
def stream():
    mpd = get_mpd()

    def gen():
        while True:
            mpd.idle('player')
            yield (
"""event: player
data: """+json.dumps(playing())+"""
retry: 1

""")
    return Response(gen(), mimetype='text/event-stream')


@app.route('/')
def index():
    return render_template('index.html')
