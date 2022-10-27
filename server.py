from books_authors_app import app
from books_authors_app.controllers import controller_authors,controller_books

if __name__ == "__main__":
    app.run(debug=True)