import os
from flask import Flask, render_template, request, flash, redirect, session, g, url_for, jsonify, Blueprint
from flask.globals import g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User, Favorite, ReadingList, ReadingListBook
from forms import LoginForm, RegisterForm, ReadingListForm, EditReadingListForm, NewBookForReadingListForm
from api import search_books, get_book_details
from func import process_description
  
# from flask_login import login_required


CURR_USER_KEY = "curr_user"

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///bookfinder'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)

# with app.app_context():
#     db.drop_all()
#     db.create_all()  

@app.before_request
def before_request():
    """If logged in, add curr user to Flask global"""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

def do_login(user):
    '''logs user in'''

    session[CURR_USER_KEY] = user.id


def do_logout():
    '''logs user out'''
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
        

@app.route("/")
def home():
    return render_template("home.html")

#route for about page
@app.route("/about")
def about():
    return render_template("about.html")



# API ROUTES

# Handles API search data
@app.route("/search")
def search():
    reading_lists = None
    if g.user:
        reading_lists = ReadingList.query.filter_by(user_id=g.user.id).all()

    # Use request.args.get() to retrieve query parameters for GET requests
    query = request.args.get('query', '')  # Default to empty string if 'query' parameter is not present

    if query:  # Proceed with search only if query parameter is provided
        results = search_books(query)
        return render_template("search_results.html", results=results, reading_lists=reading_lists)

    # If no query is provided, render the search page possibly with reading lists if the user is logged in
    return render_template("search.html", reading_lists=reading_lists)

#  Handles API book data
@app.route('/book/<book_id>')
def book_detail(book_id):
    book_data = get_book_details(book_id)
    if not book_data:
        return "Book details not found", 404
    if 'description' in book_data:
        book_description = process_description(book_data['description'])
    else:  
        book_description = "No description available."
    
    return render_template('book.html', book=book_data, description=book_description)

# USER ROUTES
    
@app.route('/profile')
def user_profile():
    '''shows a user's profile page'''
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")
    
    favorites = Favorite.query.filter_by(user_id=g.user.id).all()  # Assuming a Favorite model exists
    return render_template('user/user_profile.html', user=g.user, favorites=favorites)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle login"""
    
    form = LoginForm()

    if form.is_submitted() and form.validate():
        user = User.authenticate(form.username.data,
                                 form.password.data)
        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")
        
        flash("Invalid credentials.", 'danger')
    return render_template('user/login.html', form=form)

@app.route('/signup', methods = ["GET", "POST"])
def signup():
    

    
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = RegisterForm()

    if form.is_submitted() and form.validate():
        try:
            user = User.signup(
                email=form.email.data,
                username=form.username.data,
                password=form.password.data
                # image_url=form.image_url.data or User.image_url.default.arg,
            )
            # db.session.add(new_user)
            db.session.commit()

        except IntegrityError as e:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")
    else:
        return render_template('user/signup.html', form=form)


@app.route('/logout', methods=['POST'])
def logout():
    """Handle logout of user."""

    do_logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/login")



# Route to handle favorites
@app.route('/add_favorite', methods=["POST"])
def add_favorite():
    # Correctly parsing JSON data from the request
    data = request.get_json()

    # Ensuring all data fields are present
    book_id = data.get('book_id')
    title = data.get('title')
    author = data.get('author')
    cover_url = data.get('cover_url')

    if not all([book_id, title, author]):  # Checking for necessary data
        return jsonify({'status': 'error', 'message': 'Missing book information.'}), 400

    user_id = g.user.id

    # Proceed with checking and adding the favorite
    existing_favorite = Favorite.query.filter_by(user_id=user_id, book_id=book_id).first()
    if not existing_favorite:
        new_favorite = Favorite(user_id=user_id, book_id=book_id, title=title, author=author, cover_url=cover_url)
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Book added to favorites!'})
    else:
        return jsonify({'status': 'error', 'message': 'Book already in favorites.'})
    
@app.route('/delete_favorite/<int:favorite_id>', methods=['POST'])
def delete_favorite(favorite_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")
    
    favorite_to_delete = Favorite.query.get_or_404(favorite_id)
    if favorite_to_delete.user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/profile")

    db.session.delete(favorite_to_delete)
    db.session.commit()
    flash("Favorite removed successfully.", "success")
    return redirect(url_for('user_profile'))
    
#Reading Lists
    

# Route to create a new reading list   
@app.route('/reading-lists/new', methods=['GET', 'POST'])
# requires user to be logged in to access
def create_reading_list():
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    form = ReadingListForm()

    if form.is_submitted() and form.validate():
        new_list = ReadingList(name=form.name.data, description=form.description.data, user_id=g.user.id)
        db.session.add(new_list)
        db.session.commit()
        flash("Reading list created!", "success")
        return redirect(url_for('user_profile'))

    return render_template('reading_lists/new.html', form=form)

# Route to view  reading lists
@app.route('/reading-lists')
def view_reading_lists():
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")
    
    lists = ReadingList.query.filter_by(user_id=g.user.id).all()
    return render_template('reading_lists/index.html', lists=lists)

def populate_reading_list_form(form):
    form.reading_list_id.choices = [(list.id, list.name) for list in ReadingList.query.filter_by(user_id=g.user.id).all()]

@app.route('/reading-lists/<int:list_id>/add-book', methods=['GET', 'POST'])
def add_book_to_reading_list(list_id):
    reading_list = ReadingList.query.get_or_404(list_id)
    form = NewBookForReadingListForm()

    # Get the current book_ids on the reading list to exclude them from the choices
    curr_on_readlist = [book.book_id for book in reading_list.reading_list_books]

    # Populate form.book_id.choices with user favorites not already in the reading list
    user_favorites = Favorite.query.filter(Favorite.user_id == reading_list.user_id).all()
    form.book_id.choices = [(str(fav.id), fav.title) for fav in user_favorites if fav.book_id not in curr_on_readlist]

    if form.validate_on_submit():
        selected_favorite = Favorite.query.get(int(form.book_id.data))
        
        # Check if the book is already in the reading list
        if selected_favorite.book_id in curr_on_readlist:
            flash("This book is already in your reading list.", "warning")
            return render_template("reading_lists/add_book.html", reading_list=reading_list, form=form)
        
        # Create a new ReadingListBook entry
        new_book_to_list = ReadingListBook(reading_list_id=list_id, book_id=selected_favorite.book_id, author=selected_favorite.author, title=selected_favorite.title, cover_url=selected_favorite.cover_url)
        db.session.add(new_book_to_list)
        db.session.commit()

        flash("Book added to reading list successfully.", "success")
        return redirect(f"/reading-lists/view/{list_id}")

    return render_template("reading_lists/add_book.html", reading_list=reading_list, form=form)




# Edit a reading list
@app.route('/reading-lists/edit/<int:list_id>', methods=['GET', 'POST'])
def edit_reading_list(list_id):
    reading_list = ReadingList.query.get_or_404(list_id)
    if g.user.id != reading_list.user_id:
        flash("You do not have permission to edit this reading list.", "danger")
        return redirect(url_for('user_profile'))
    
    form = EditReadingListForm(obj=reading_list)
    
    if form.is_submitted() and form.validate():
        reading_list.name = form.name.data
        reading_list.description = form.description.data
        db.session.commit()
        flash('Reading list updated successfully.', 'success')
        return redirect(url_for('user_profile'))
    elif request.method == 'GET':
        form.name.data = reading_list.name
        form.description.data = reading_list.description

    return render_template('reading_lists/edit.html', form=form, list_id=list_id)

@app.route('/reading-lists/book/<int:reading_list_book_id>/delete', methods=['POST'])
def delete_book_from_reading_list(reading_list_book_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    reading_list_book = ReadingListBook.query.get_or_404(reading_list_book_id)

    # Optional: Check if the current user owns the reading list
    if reading_list_book.reading_list.user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/reading-lists")

    db.session.delete(reading_list_book)
    db.session.commit()

    flash("Book removed from the reading list.", "success")
    return redirect(url_for('view_reading_list', list_id=reading_list_book.reading_list_id))



# Delete a reading list
@app.route('/reading-lists/<int:list_id>/delete', methods=['POST'])
def delete_reading_list(list_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect(url_for('login'))

    reading_list = ReadingList.query.get_or_404(list_id)
    if reading_list.user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect(url_for('view_reading_lists'))

    db.session.delete(reading_list)
    db.session.commit()
    flash("Reading list deleted.", "success")
    return redirect(url_for('user_profile'))


# view details of a specific reading list
@app.route('/reading-lists/view/<int:list_id>')
def view_reading_list(list_id):
    reading_list = ReadingList.query.get_or_404(list_id)
    # Assuming ReadingListBook links books to reading lists
    books = ReadingListBook.query.filter_by(reading_list_id=list_id).all()
    return render_template('reading_lists/view.html', reading_list=reading_list, books=books)

