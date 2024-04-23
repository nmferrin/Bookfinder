from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__, template_folder='templates')


#main routes
@main_bp.route("/")
def home():
    return render_template("home.html")

@main_bp.route("/about")
def about():
    return render_template("about.html")






#book routes
@main_bp.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form.get("query")
        results = search_books(query)
        return render_template("books/search_results.html", results=results)
    return render_template("books/search.html")

@main_bp.route('/book/<book_id>')
def book_detail(book_id):
    book_data = get_book_details(book_id)
    if not book_data:
        flash("Book details not found.", "danger")
        return redirect(url_for("books.search"))
    
    book_description = process_description(book_data.get('description', "No description available."))
    return render_template('books/book_detail.html', book=book_data, description=book_description)