from books_authors_app.config.mysqlconnection import connectToMySQL
from books_authors_app.models import model_book

class Author:
    def __init__(self,data):
        self.id=data['id']
        self.name=data['name']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.favorites=[]

    @classmethod
    def create_author(cls,data):
        query = '''
                INSERT INTO authors(name)
                VALUES (%(name)s);
                '''
        response_query = connectToMySQL('book_schema_db').query_db(query,data)
        return response_query


    @classmethod
    def get_authors(cls):
        query = '''
                SELECT * FROM authors;
                '''
        response_data = connectToMySQL('book_schema_db').query_db(query)
        authors = []
        for author in response_data:
            authors.append(cls(author))
        return authors
    
    @classmethod
    def get_favorites_author_books(cls,data):
        query = '''
                SELECT * FROM authors 
                LEFT JOIN favorites ON authors.id = favorites.author_id
                LEFT JOIN books ON favorites.book_id = books.id
                WHERE authors.id = %(id)s
                '''
        response_query = connectToMySQL("book_schema_db").query_db(query,data)
        authors_obj= cls(response_query[0])
        for book in response_query:
            data = {
            'id':book['books.id'],
            'title':book['title'],
            'num_of_pages':book['num_of_pages'],
            'created_at':book['books.created_at'],
            'updated_at':book['books.updated_at']
            }
            authors_obj.favorites.append(data)
        authors_obj
        return authors_obj
    
    @classmethod
    def get_unfavorites_author_books(cls,data):
        query = '''
                SELECT * FROM books WHERE books.id 
                NOT IN ( SELECT book_id FROM favorites WHERE author_id = %(id)s );
                '''
        response_query = connectToMySQL("book_schema_db").query_db(query,data)
        books_obj= []
        for book in response_query:
            data = {
            'id':book['id'],
            'title':book['title'],
            'num_of_pages':book['num_of_pages'],
            'created_at':book['created_at'],
            'updated_at':book['updated_at']
            }
            books_obj.append(model_book.Book(data))
        
        return books_obj
    @classmethod
    def insert_favorite_author_book(cls,data):
        query = '''
                INSERT INTO favorites (author_id,book_id)
                VALUES (%(author_id)s,%(book_id)s);
                '''
        response_query = connectToMySQL("book_schema_db").query_db(query,data)
        
        return response_query