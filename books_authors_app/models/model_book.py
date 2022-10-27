from books_authors_app.config.mysqlconnection import connectToMySQL
from books_authors_app.models import model_author
class Book:
    def __init__(self,data):
        self.id=data['id']
        self.title=data['title']
        self.num_of_pages=data['num_of_pages']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.favorites = []

    @classmethod
    def get_books(cls):
        query='''
            SELECT * FROM books    
            '''
        response_query=connectToMySQL('book_schema_db').query_db(query)
        books = []
        for book in response_query:
            books.append(cls(book))
        return books
    @classmethod
    def create_book(cls,data):
        query='''
            INSERT INTO books (title,num_of_pages)
            VALUES (%(title)s,%(num_of_pages)s)  
            '''
        response_query=connectToMySQL('book_schema_db').query_db(query,data)
        return response_query
    @classmethod
    def get_favorites_book_authors(cls,data):
        query = '''
                SELECT * FROM books 
                LEFT JOIN favorites ON books.id = favorites.book_id
                LEFT JOIN authors ON favorites.author_id = authors.id
                WHERE books.id = %(id)s;
                '''
        response_query = connectToMySQL("book_schema_db").query_db(query,data)
        books_obj= cls(response_query[0])
        for author in response_query:
            data = {
            'id':author['authors.id'],
            'name':author['name'],
            'created_at':author['authors.created_at'],
            'updated_at':author['authors.updated_at']
            }
            books_obj.favorites.append(model_author.Author(data))
        return books_obj

    @classmethod
    def get_unfavorites_book_authors(cls,data):
        query = '''
                SELECT * FROM authors WHERE authors.id 
                NOT IN ( SELECT author_id FROM favorites WHERE book_id = %(id)s );
                '''
        response_query = connectToMySQL("book_schema_db").query_db(query,data)
        authors=[]
        for author in response_query:
            data = {
            'id':author['id'],
            'name':author['name'],
            'created_at':author['created_at'],
            'updated_at':author['updated_at']
            }
            authors.append(model_author.Author(data))

        return authors
    @classmethod
    def insert_favorite_book_author(cls,data):
        query = '''
                INSERT INTO favorites (author_id,book_id)
                VALUES (%(author_id)s,%(book_id)s);
                '''
        response_query = connectToMySQL("book_schema_db").query_db(query,data)
        
        return response_query