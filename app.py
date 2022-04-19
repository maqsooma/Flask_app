from email import contentmanager, message
import os
from turtle import title
from flask import Flask,flash, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import sqlalchemy
from sqlalchemy import create_engine,true
from sqlalchemy.orm import sessionmaker,scoped_session
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24).hex()
engine = create_engine('mysql://root:@localhost/flask')
con = engine.connect()


    
@app.route('/')
def index():
    messages = con.execute('SELECT * from messsages')
    return render_template('index.html', messages=messages)


@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['content']

        if not title:
            flash('Title is required!')
        elif not message:
            flash('Content is required!')
        else:
            con.execute('INSERT INTO messsages(title,message) values(%s,%s)',(title,message))
            return redirect(url_for('index'))

    return render_template('create.html')
@app.route('/<int:message_id>/edit/', methods=('GET', 'POST'))

def edit(message_id):
    message_id= message_id

    if request.method == 'POST':
        title = request.form['title']
        message = request.form['content']

        if not title:
            flash('Title is required!')
        elif not message:
            flash('Content is required!')
        else:
            con.execute("UPDATE messsages SET title = '{}', message = '{}' WHERE id = '{}'" .format(title,message,message_id)) 
            return redirect(url_for('index'))

    return render_template('edit.html')

@app.post('/<int:message_id>/delete/')
def delete(message_id):
    message_id= message_id
    con.execute('DELETE from messsages where id = "{}"'.format(message_id))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)




