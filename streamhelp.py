from flask import Flask, jsonify, send_file, Response, render_template,\
                current_app
import threading
from mpd import MPDClient
from pathlib import Path
import re
import json
import socket

MUSIC_FOLDER = '/home/codl/media/music'
app = Flask('streamhelp')

local = threading.local()

def get_mpd(reset=False):
    global local
    if not hasattr(local, 'mpd') or reset:
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


@app.route('/api/mpd/playing')
def mpd_playing():
    return jsonify(playing())


COVER_REGEX = (re.compile('^(?:.*front|.*cover|folder)\.(?:jpe?g|gif|png)$',
                          re.I), re.compile('\.(?:jpe?g|gif|png)$', re.I))


@app.route('/api/mpd/cover')
def mpd_cover_art():
    path = Path(MUSIC_FOLDER) / playing()['file']
    folder = path.parent
    cover_path = None
    for regex in COVER_REGEX:
        for child in folder.iterdir():
            if regex.search(str(child)):
                return send_file(str(child))
    return '', 404


@app.route('/api/mpd/stream')
def mpd_stream():
    def gen():
        mpd = get_mpd()
        while True:
            mpd.idletimeout = 1.8
            try:
                mpd.idle('player')
            except socket.timeout:
                mpd = get_mpd(True)

            yield ("""event: player
data: """ + json.dumps(playing()) + """
retry: 1

""")

    return Response(gen(), mimetype='text/event-stream')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/elements/<element>')
def show_element(element):
    if (Path(current_app.static_folder) / (element + '.js')).exists():
        return render_template('element.html', element=element)
    return 'no such element', 404
