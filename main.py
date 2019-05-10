from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'This_is_a_very_secret_key'

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    post_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    body = db.Column(db.Text())
    active = db.Column(db.Boolean)

    def __init__(self,title):
        self.title = title
        self.date = datetime.now()
        self.body = 'No content yet'
        self.active = True

    def __repr__(self):
        return '< Title:"{}" ,date posted: {}>'.format(self.title,str(self.date)[:16])

def get_active_posts():
    return Blog.query.filter_by(active=True).order_by(-Blog.id).all()

def get_inactive_posts():
    return Blog.query.filter_by(active=False).order_by(-Blog.id).all()

@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        post_id = request.form['post-id']
        the_post = Blog.query.filter_by(id=post_id).first()
        the_post.active = False
        db.session.add(the_post)
        db.session.commit()
        flash('The post is archived.')
        return redirect('/')

    return render_template('index.html',posts=get_active_posts())

@app.route('/newpost', methods=['GET','POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if title and body:
            new_post = Blog(title)
            new_post.body = body
            db.session.add(new_post)
            db.session.commit()
            print(new_post)
            flash('Your new blog is published.')
            return render_template('index.html',posts=get_active_posts())
        else:
            flash('Your blog needs both "title" and some "text"')
            return render_template('newpost.html', title=title, body=body)
    else:
        return render_template('newpost.html')

@app.route('/archive',methods=['POST','GET'])
def archive():
    if request.method == 'POST':
        post_id = request.form['post-id']
        the_post = Blog.query.filter_by(id=post_id).first()
        the_post.active = True
        db.session.add(the_post)
        db.session.commit()
        flash('The post is unarchived.')
        return redirect('/')

    else:
        return render_template('archive.html',posts=get_inactive_posts())

if __name__ == '__main__':
    app.run()