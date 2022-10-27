from flask import redirect, render_template, request
from books_authors_app import app
from books_authors_app.models import model_author,model_book

@app.route("/")
def index():
    return redirect("/authors")

@app.route("/authors",methods=['GET','POST'])
def authors():
    if request.method == 'GET':
        authors_obj = model_author.Author.get_authors()
        return render_template("index.html",authors=authors_obj)
    if request.method == 'POST':
        author = {
            'name':request.form['name']
        }
        response = model_author.Author.create_author(author)
        return redirect("/authors")

@app.route("/authors/<int:number>",methods=['GET','POST'])
def author_detail(number):
    if request.method == 'GET':
        data = {
            "id":number
        }
        respuesta_author_books = model_author.Author.get_favorites_author_books(data)
        respueta_books_unfavorite = model_author.Author.get_unfavorites_author_books(data)
        return render_template("author_detail.html",response=respuesta_author_books,books_unfav=respueta_books_unfavorite)
    if request.method == 'POST':
        author = {
            'author_id':number,
            'book_id':request.form['book']
        }
        request_model = model_author.Author.insert_favorite_author_book(author)
        print(request_model)
        return redirect(f"/authors/{number}")