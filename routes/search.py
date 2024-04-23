@app.route("/search", methods=["GET", "POST"])
def search():
    reading_lists = None  # Initialize variable to hold reading lists
    if g.user:
        # Fetch the current user's reading lists if logged in
        reading_lists = ReadingList.query.filter_by(user_id=g.user.id).all()

    if request.method == "POST":
        query = request.form["query"]
        results = search_books(query)
        # Pass the user's reading lists along with the search results to the template
        return render_template("search_results.html", results=results, reading_lists=reading_lists)
    else:
        # If it's a GET request, just show the search page without results
        # Make sure to pass the reading lists to the search template if it needs them
        return render_template("search.html", reading_lists=reading_lists)