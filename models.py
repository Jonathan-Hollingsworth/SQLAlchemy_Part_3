from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    "Initiates the connection to the database"
    db.app = app
    db.init_app(app)

class User(db.Model):
    "Information for each user"

    __tablename__ = "users"

    def __repr__(self):
        "Display information about the user"

        u = self
        return f"<User{u.id}: {u.get_full_name()} {u.image_url}>"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(30),
                           nullable=False)

    last_name = db.Column(db.String(30),
                          nullable=False)
    
    image_url = db.Column(db.String(50),
                          nullable=False,
                          default="https://tinyurl.com/default-pfp")

    def get_full_name(self):
        """Combines first name and last name into a single string and returns it"""

        first_name = self.first_name
        last_name = self.last_name

        return f'{first_name} {last_name}'
    
class Post(db.Model):
    "Information for each post"

    __tablename__ = "posts"

    def __repr__(self):
        "Display information about the post"

        p = self
        return f"<Post{p.id}: '{p.title}' by {p.user.get_full_name()}>"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.String,
                      nullable=False)
    
    content = db.Column(db.String,
                        nullable=False)
    
    created_at = db.Column(db.DateTime,
                           default=datetime.now())
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))
    
    user = (db.relationship('User', backref='posts'))

    tags = (db.relationship('Tag', secondary='posts_tags', backref='posts'))

class Tag(db.Model):
    "Information for each tag"

    __tablename__ = "tags"

    def __repr__(self):
        """Display information about the tag"""

        t = self
        return f"Tag{t.id}: {t.name}"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    name = db.Column(db.String,
                     nullable=False,
                     unique=True)
    
class PostTag(db.Model):
    "Conection for posts and tags"

    __tablename__ = "posts_tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)