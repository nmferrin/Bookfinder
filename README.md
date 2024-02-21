# BookFinder Application
This is my first capstone project with the Springboard bootcamp using
the Open Library API to retrieve the book information to be saved onto the application's database and make reading lists.
The application uses Flask along with Python, a bit of Javascript, and Tailwind for styling.

## Stretch Goals
- AI-driven book recommendations
- Stripe-based paywall

## Setup Instructions

To get this application running, make sure you follow these steps in the Terminal:

1. Create a virtual environment:
python3 -m venv myenv

2. Activate the virtual environment:
source myenv/bin/activate

3. Install required dependencies:
pip install -r requirements.txt

4. Create the database:
createdb bookfinder

5. Run the Flask application:
flask run
