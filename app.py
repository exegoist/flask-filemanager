import os
from datetime import datetime

from models import File
from pony import orm
from flask import Flask, render_template, redirect, url_for


app = Flask(__name__)
DIR = '/home/me/Downloads'


@app.route('/')
@orm.db_session
def index():
    files = File.select().order_by(orm.desc(File.time))[:10]
    return render_template('index.html', files=files)


@app.route('/scan')
@orm.db_session
def scan_folder():
    for root, dirs, files in os.walk(DIR, topdown=True):
        for f in files:
            if not File.select(lambda file: file.name == f):
                time = os.stat(os.path.join(root, f)).st_mtime
                size = str(os.stat(os.path.join(root, f)).st_size)
                timestamp_str = datetime.fromtimestamp(time)
                url = os.path.join(root.replace(DIR, ''), f)
                File(name=f, time=timestamp_str, size=size, url=url)
    return redirect(url_for('index'))
