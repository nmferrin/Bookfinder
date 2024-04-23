from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from ..models import db, Favorite
from ..api.api import search_books, get_book_details
from ..utils.helpers import process_description

books_bp = Blueprint('books', __name__, template_folder='templates/books')

@books_bp.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form.get("query")
        results = search_books(query)
        return render_template("books/search_results.html", results=results)
    return render_template("books/search.html")

@books_bp.route('/book/<book_id>')
def book_detail(book_id):
    book_data = get_book_details(book_id)
    if not book_data:
        flash("Book details not found.", "danger")
        return redirect(url_for("books.search"))
    
    book_description = process_description(book_data.get('description', "No description available."))
    return render_template('books/book_detail.html', book=book_data, description=book_description)
