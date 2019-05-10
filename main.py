from app import app,db
from models import Blog
from flask import render_template, request, redirect, flash, url_for, session
from datetime import datetime,timedelta



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
    
    blog_id = request.args.get('id')
    try:
        the_post = Blog.query.filter_by(id=int(blog_id)).first()
        if the_post:
            return render_template('index.html',posts=[the_post])
        else:
            flash('The requested blog does not exist.')
            return redirect('/')
    except TypeError:
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
            return render_template('index.html',posts=[new_post])
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
        return render_template('index.html',posts=get_inactive_posts())

if __name__ == '__main__':
    app.run()