from app import db
from app.models.book import Book
from flask import request, Blueprint, make_response, jsonify

books_bp = Blueprint("books", __name__, url_prefix="/books")


@books_bp.route("", methods=["GET", "POST"])
def handle_books():
    if request.method == "GET":
        books = Book.query.all()
        books_response = [book.to_dict() for book in books]
        return jsonify(books_response)
    elif request.method == "POST":
        request_body = request.get_json()
        new_book = Book.from_dict(request_body)

        db.session.add(new_book)
        db.session.commit()

        return jsonify(f"Book {new_book.title} successfully created"), 201


@books_bp.route("/<book_id>", methods=["GET", "PUT", "PATCH", "DELETE"])
def handle_book(book_id):
    book = Book.query.get(book_id)

    if request.method == "GET":
        return book.to_dict()

    elif request.method == "PUT":
        form_data = request.get_json()
        book.replace_with_dict(form_data)

        db.session.commit()

        return jsonify(f"Book #{book.id} successfully updated")

    elif request.method == "PATCH":
        form_data = request.get_json()
        book.update_from_dict(form_data)

        db.session.commit()

        return jsonify(f"Book #{book.id} successfully updated")
        
    elif request.method == "DELETE":
        db.session.delete(book)
        db.session.commit()
        return jsonify(f"Book #{book.id} successfully deleted")
