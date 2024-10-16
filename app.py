from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = "johntanner"
books = []


@app.before_request
def authenticate_token():
    token = request.headers.get("Authorization")
    if not token or token != f"Bearer {TOKEN}":
        return jsonify({"message": "Invalid token"}), 401

@app.route('/books',methods=["GET"])
def get_books():
    return jsonify(books)
@app.route('/books',methods=["POST"])
def create_book():
    name = request.json.get("name")
    isbn = request.json.get("isbn")
    author = request.json.get("author")
    book = {"id": len(books) + 1, "name": name, "isbn": isbn, "author": author}

    books.append(book)
    return jsonify(books)
@app.route('/books/<int:id>',methods=["GET"])
def find_book(id):
    book = next((book for book in books if book["id"] == id), None)
    if book is None:
        return jsonify({"message": "Book not found"}),404
    return jsonify(book)
@app.route('/books/<int:id>',methods=["PUT"])
def update_book(id):
    book = next(book for book in books if book["id"] == id)
    book["name"] = request.json.get("name")
    book["isbn"] = request.json.get("isbn")
    book["author"] = request.json.get("author")
    return jsonify(book)
@app.route('/books/<int:id>',methods=["DELETE"])
def delete_book(id):
    book = next(book for book in books if book["id"] == id)
    books.remove(book)
    return jsonify({"message": "Book deleted", "deleted_book": book})

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request"}), 400
@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({"error": "Resource not found"}), 404