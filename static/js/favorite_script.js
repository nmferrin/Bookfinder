// Javascript to handle favorite button clicks

document.addEventListener('DOMContentLoaded', function() {
    const favoriteButtons = document.querySelectorAll('.favorite-btn');
    favoriteButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Assuming each button has data attributes for bookId, title, author, and coverUrl
            const bookId = this.getAttribute('data-book-id');
            const title = this.getAttribute('data-title');
            const author = this.getAttribute('data-author');
            const coverUrl = this.getAttribute('data-cover-url');
            
            const data = {
                book_id: bookId,
                title: title,
                author: author,
                cover_url: coverUrl
            };

            fetch('/add_favorite', {
                method: 'POST',
                body: JSON.stringify(data),
                headers: {
                    'Content-Type': 'application/json'
                },
            })
            .then(response => response.json())
            .then(data => {
                if(data.status === 'success') {
                    // Optionally, change the star to a filled star to indicate it's a favorite
                    this.innerHTML = '<i class="fas fa-star"></i>'; // Switch to a filled star icon
                    alert(data.message); // Or update the UI to reflect the favorite status
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error adding favorite:', error);
                alert('An error occurred while adding the book to favorites.');
            });
        });
    });
});
