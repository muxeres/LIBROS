from flask import redirect, render_template, request
from books_authors_app import app
from books_authors_app.models import model_book

@app.route("/books", methods=['GET','POST'])
def book():
    if request.method=='GET':
        return_data = model_book.Book.get_books()
        return render_template("book.html",books=return_data)
    if request.method=='POST':
        data={
            'title':request.form['title'],
            'num_of_pages':request.form['pages']
        }
        return_data = model_book.Book.create_book(data)
        print(return_data)
        return redirect("/books")

@app.route("/books/<int:number>",methods=['GET','POST'])
def book_detail(number):
    if request.method=='GET':
        data = {
            "id":number
        }
        response_model=model_book.Book.get_favorites_book_authors(data)
        response_model_unfavorites_authors=model_book.Book.get_unfavorites_book_authors(data)
        return render_template("book_detail.html",books=response_model,authors_unfav=response_model_unfavorites_authors)
    if request.method=='POST':
        data = {
            'author_id':request.form['author'],
            'book_id':number
        }
        response_model = model_book.Book.insert_favorite_book_author(data)
        print(request.form)
        return redirect(f"/books/{number}")