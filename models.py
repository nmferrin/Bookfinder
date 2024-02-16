from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime


db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    subscription_status = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User({username!r})>'.format(username=self.username)

    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd
            # image_url=image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False
 


class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(120), nullable=False)  # Adjusted from name to title
    author = db.Column(db.String(120))  # Added author field
    cover_url = db.Column(db.String(255))  # Added cover_url field
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='favorites')  # Adjusted backref to 'favorites'

 


class ReadingList(db.Model):
    __tablename__ = 'reading_lists'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship( 'User', backref='reading_lists')
    # books = db.relationship( 'Favorite', secondary = 'reading_list_books', backref='reading_lists')
    

class ReadingListBook(db.Model):
    __tablename__ = 'reading_list_books'
    id = db.Column(db.Integer, primary_key=True)
    reading_list_id = db.Column(db.Integer, db.ForeignKey('reading_lists.id'), nullable=False)
    # favorite_id = db.Column(db.Integer, db.ForeignKey('favorites.id')) 
    book_id = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(255))  # Added for display
    author = db.Column(db.String(255))  # Added for display
    cover_url = db.Column(db.String(255))  # Added for display
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    reading_list = db.relationship( 'ReadingList', backref='reading_list_books')


    
# with app.app_context():
#     db.create_all()


def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)
