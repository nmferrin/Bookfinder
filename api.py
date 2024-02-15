import requests

def search_books(query):
    #use the Open library API to search for books based on a query string.
    base_url = "https://openlibrary.org/search.json"
    params = {"q": query}
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def get_book_details(book_id):
    """Fetch a book's details from Open Library using its ID."""
    response = requests.get(f"https://openlibrary.org/works/{book_id}.json")
    if response.ok:
        return response.json()
    return None

# def get_author_details(author_key):
#     """Fetch an author's details from Open Library using its key."""
#     response = requests.get(f"https://openlibrary.org/authors/{author_key}.json")
#     if response.ok:
#         return response.json()
#     return None
