from flask import Flask, jsonify, request
from firebase_admin import credentials, firestore, initialize_app
# create an instance of the Flask class with the name of the current module
app = Flask(__name__)
# Initialize Firestore DB
crud = credentials.Certificate('keys/key.json')
default_app = initialize_app(crud)
db = firestore.client()
todo_ref = db.collection('books')


# GET /books
# garante que a rota só aceite requisições do tipo GET
@app.route('/books', methods=['GET'])
def get_books():
    print(db.books)
    try:
        # Persistencia em memória
        # Check if ID was passed to URL query
        # todo_id = request.args.get('id')
        # print(todo_id)
        # if todo_id:
        #     todo = todo_ref.document(todo_id).get()
        #     return jsonify(todo.to_dict()), 200
        # else:
        docs = todo_ref.stream()
        all_books = []
        for doc in docs:
            # all_books.append(doc.id)
            all_books.append(doc.to_dict())
            print(f'{doc.id} => {doc.to_dict()}')

        sort = sorted(all_books, key=lambda k: k['tittle'])
        return jsonify(sort), 200
        # all_todos = [doc.to_dict() for doc in todo_ref.stream()]
        # return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

    # jsonify() converts the Python dictionary to a JSON object
    # return jsonify({'books': books})
    # {'books': books} is a dictionary with a key 'books' and a value books
    # return jsonify(books) is also valid


# GET /books/<string:id>
@app.route('/books/<string:id>', methods=['GET'])
def get_book_id(id):
    """ Usado para persistencia em memória
    book = [book for book in books if book.get('id') == id]
    if len(book) == 0:
        return jsonify({'message': 'Book not found!'}), 404
    return jsonify({'book': book[0]}) """
    try:
        book = todo_ref.document(str(id)).get()
        if not book.exists:
            return jsonify({'message': 'Book not found!'}), 404
        return jsonify(book.to_dict()), 200
        id = request.json['id']
        todo_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"
    # return jsonify(book) is also valid


# PUT /books/<int:id>
@app.route('/books/<string:id>', methods=['PUT'])
def edit_book(id):
    livro_alterado = request.get_json()
    # todo_ref.document(id).update(livro_alterado)
    book = todo_ref.document(id).get()
    if not book.exists:
        return jsonify({'message': 'Book not found!'}), 404

    todo_ref.document(id).update(livro_alterado)
    return jsonify({'message': 'Book updated!'}), 200

    """ Usado para persistencia em memória
    books = [doc.to_dict() for doc in todo_ref.stream()]
    for index, book in enumerate(books):
        if book.get('id') == id:
            books[index].update(livro_alterado)
            return jsonify({'message': 'Book updated!'})
    return jsonify({'message': 'Book not found!'}), 404 """


# POST /books
@app.route('/books', methods=['POST'])
def add_book():
    """ Usado para persistencia em memória
    book = request.get_json()
    books.append(book)
    return jsonify({'message': 'Book added!'}) """
    try:
        todo_ref.add(request.get_json())
        # todo_ref.document(id).set(request.json)
        return jsonify({'message': 'Book added'}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


# DELETE /books/<int:id>
@app.route('/books/<string:id>', methods=['DELETE'])
def delete_book(id):
    """ Usado para persistencia em memória
    for index, book in enumerate(books):
        if book.get('id') == id:
            del books[index]
            # books.pop(index)
            return jsonify({'message': 'Book deleted!'}, {'books': books})
    """
    book = todo_ref.document(id).get()
    if not book.exists:
        return jsonify({'message': 'Book not found!'}), 404

    todo_ref.document(id).delete()
    return jsonify({'message': 'Book deleted!'}), 200


app.run(host='localhost', port=5000, debug=True)
