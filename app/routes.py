from app import db
from app.models.book import Book
from flask import request, Blueprint, make_response, jsonify
from functools import wraps

books_bp = Blueprint("books", __name__, url_prefix="/books")

# create a function to use as a decorator, which will accept an incoming
# book_id, then look up an actual Book instance with it. The book instance
# will be passed to the wrapped function as the parameter named book.
# @wraps will use the metadata of the passed endpoint to update the "appearance"
# of the new function to look like the original endpoint.
# This approach lets us move the shared error handling from the various
# endpoints into the decorator, and only calling the endpoint logic if there is
# actually a book found.
# We do make assumptions about the parameter names, which we might avoid if we
# added customization to the decorator.
def require_book(endpoint):
    @wraps(endpoint)
    def fn(*args, book_id, **kwargs):
        book = Book.query.get(book_id)

        if not book:
            return jsonify(f"invalid book id {book_id}"), 404

        return endpoint(*args, book=book, **kwargs)

    return fn

@books_bp.route("", methods=["GET"])
def handle_books():
    title = request.args.get("title")
    limit = request.args.get("limit")

    query = Book.query
    # print(type(query))

    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))

    if limit:
        query = query.limit(limit)

    books = query.all()

    books_response = [book.to_dict() for book in books]
    return jsonify(books_response)

@books_bp.route("", methods=["POST"])
def create():
    request_body = request.get_json()
    new_book = Book.from_dict(request_body)

    db.session.add(new_book)
    db.session.commit()

    return jsonify(f"Book {new_book.title} successfully created"), 201


@books_bp.route("/<book_id>", methods=["GET"])
@require_book
def get(book):
    return book.to_dict()

@books_bp.route("/<book_id>", methods=["PUT"])
@require_book
def put(book):
    form_data = request.get_json()
    book.replace_with_dict(form_data)

    db.session.commit()

    return jsonify(f"Book #{book.id} successfully updated")

@books_bp.route("/<book_id>", methods=["PATCH"])
@require_book
def patch(book):
    form_data = request.get_json()
    book.update_from_dict(form_data)

    db.session.commit()

    return jsonify(f"Book #{book.id} successfully updated")

@books_bp.route("/<book_id>", methods=["DELETE"])
@require_book
def delete(book):
    db.session.delete(book)
    db.session.commit()
    return jsonify(f"Book #{book.id} successfully deleted")
