from app import db
from datetime import datetime,timedelta

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    post_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    body = db.Column(db.Text())
    active = db.Column(db.Boolean)

    def __init__(self,title,body):
        self.title = title
        self.body = body
        self.active = True

    def __repr__(self):
        return '< Title:"{}" ,date posted: {}>'.format(self.title,str(self.date)[:16])
