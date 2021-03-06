import os
from datetime import datetime

from app.models import File
from app import app, db_session, desc
from flask import render_template, redirect, url_for, request, session
from config import DIR, PAGESIZE


@app.route('/')
@app.route('/<int:page>')
@db_session
def index(page=1):
    p = request.args.get('page')
    if p:
        page = int(p)
    if 'q' in session:
        req = request.args.get('search')
        if req:
            q = req
            page = 1
            session['q'] = req
        elif req == '':
            q = ''
        else:
            q = session['q']
    else:
        q = request.args.get('search')
        if q:
            page = 1
            session['q'] = q
    if q:
        files = File.select(lambda p: q in p.name).order_by(desc(File.time)).page(page, pagesize=PAGESIZE)
        col = File.select(lambda p: q in p.name).count()
        if col % PAGESIZE == 0:
            pages = [i + 1 for i in range(col // PAGESIZE)][:20]
            total = col // PAGESIZE
        else:
            pages =  [i + 1 for i in range(col // PAGESIZE + 1)][:20]
            total = col // PAGESIZE + 1
    else:
        files = File.select().order_by(desc(File.time)).page(page, pagesize=PAGESIZE)
        col = File.select().count()
        if col % PAGESIZE == 0:
            pages = [i + 1 for i in range(col // PAGESIZE)][:20]
            total = col // PAGESIZE
        else:
            pages =  [i + 1 for i in range(col // PAGESIZE + 1)][:20]
            total = col // PAGESIZE + 1
    return render_template('index.html', files=files, pages=pages, total=total)

@app.route('/clear')
def clear_session():
    session.pop('q', None)
    return redirect(url_for('index'))

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


@app.route('/delete/<int:del_num>')
@db_session
def delete_file(del_num):
    file = File[del_num]
    try:
        os.remove(os.path.join(DIR, file.url[1:]))
        file.delete()
        return redirect(url_for('index'))
    except:
        return "<h1>Some trouble with deleting file</h1>"
