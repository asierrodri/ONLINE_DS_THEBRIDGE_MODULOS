from flask import Flask, request, jsonify, abort 
import sqlite3 
 
app = Flask(__name__) 
app.config["DEBUG"] = True 
 
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
 
@app.route('/api/v1/resources/books/all', methods=['GET']) 
def get_all(): 
    connection = sqlite3.connect('books.db')
    connection.row_factory = dict_factory 
    cursor = connection.cursor() 
 
    select_books = "SELECT * FROM books" 
 
    result = cursor.execute(select_books).fetchall() 
 
    connection.close() 
 
    return {'books': result}
 
@app.route('/api/v1/resources/book/<string:author>', methods=['GET']) 
def get_by_author(author): 
    connection = sqlite3.connect('books.db')
    connection.row_factory = dict_factory 
    cursor = connection.cursor() 
 
    select_books = "SELECT * FROM books WHERE author=?" 
 
    result = cursor.execute(select_books, (author,)).fetchall() 
 
    connection.close() 
 
    return {'books': result} 
 
@app.route('/api/v1/resources/book/filter', methods=['GET']) 
def filter_table(): 
    query_parameters = request.get_json() 
 
    id = query_parameters.get('id') 
    published = query_parameters.get('published') 
    author = query_parameters.get('author') 
 
    connection = sqlite3.connect('books.db')
    connection.row_factory = dict_factory 
    cursor = connection.cursor() 
 
    query = "SELECT * FROM books WHERE" 
    to_filter = [] 
 
    if id: 
        query += ' id=? AND' 
        to_filter.append(id) 
    if published: 
        query += ' published=? AND' 
        to_filter.append(published) 
    if author: 
        query += ' author=? AND' 
        to_filter.append(author) 
    if not (id or published or author): 
        return "page not found 404" 
 
    query = query[:-4] + ';' 
 
    result = cursor.execute(query, to_filter).fetchall() 
 
    connection.close() 
 
 
    return {'books': result} 

# 1) POST - añadir libro mediante parámetros (como tu ejemplo)
@app.route('/v1/add_book_params/', methods=['POST'])
def add_book_params():
    id = request.args.get('id')
    title = request.args.get('title')
    author = request.args.get('author')
    first_sentence = request.args.get('first_sentence')
    published = request.args.get('published')

    connection = sqlite3.connect('books.db')
    connection.row_factory = dict_factory
    cursor = connection.cursor()

    try:
        insert_book = """
            INSERT INTO books (id, title, author, first_sentence, published)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(insert_book, (id, title, author, first_sentence, published))
        connection.commit()

        # Devuelvo todos (igual que tu ejemplo devolvía la lista completa)
        result = cursor.execute("SELECT * FROM books").fetchall()
        return jsonify(result)

    except sqlite3.IntegrityError:
        return abort(409, "Ese id ya existe (conflicto).")
    finally:
        connection.close()


# 2) PUT - modificar un libro (ej: solo published, como tu ejemplo)
@app.route('/v1/modify_book/', methods=['PUT'])
def modify_book():
    id = request.args.get('id')
    published = request.args.get('published')

    if not (id and published):
        return abort(400, 'Debes pasar id y published.')

    connection = sqlite3.connect('books.db')
    connection.row_factory = dict_factory
    cursor = connection.cursor()

    try:
        # Comprobar si existe
        exists = cursor.execute("SELECT * FROM books WHERE id=?", (id,)).fetchone()
        if not exists:
            return abort(404, "Book not found.")

        cursor.execute("UPDATE books SET published=? WHERE id=?", (published, id))
        connection.commit()

        result = cursor.execute("SELECT * FROM books").fetchall()
        return jsonify(result)

    finally:
        connection.close()


# 3) DELETE - eliminar un libro (como tu ejemplo)
@app.route('/v1/delete_book/', methods=['DELETE'])
def delete_book():
    id = request.args.get('id')

    if not id:
        return abort(400, 'Debes pasar id.')

    connection = sqlite3.connect('books.db')
    connection.row_factory = dict_factory
    cursor = connection.cursor()

    try:
        exists = cursor.execute("SELECT * FROM books WHERE id=?", (id,)).fetchone()
        if not exists:
            return abort(404, "Book not found.")

        cursor.execute("DELETE FROM books WHERE id=?", (id,))
        connection.commit()

        result = cursor.execute("SELECT * FROM books").fetchall()
        return jsonify(result)

    finally:
        connection.close()


app.run()
