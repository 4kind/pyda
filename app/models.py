from . import db


class Password(db.Model):
    __tablename__ = 'passwords'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True, nullable=False, unique=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    website = db.Column(db.String(100))
    description = db.Column(db.String(200))

    def __repr__(self):
        return '<Password %r>' % self.title
