import os
from datetime import datetime

from app.models import File
from app import app, db_session, desc
from flask import render_template, redirect, url_for

from config import DIR


@app.route('/')
@db_session
def index():
    files = File.select().order_by(desc(File.time))[:10]
    return render_template('index.html', files=files)


@app.route('/scan')
@db_session
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
