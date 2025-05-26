from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from schemas import BookCreateSchema
from models import Book

books_bp = Blueprint("books", __name__, url_prefix="/api/v1")


@books_bp.route("/books", methods=["GET"])
def get_books():
    limit = request.args.get("limit", default=10, type=int)
    offset = request.args.get("offset", default=0, type=int)
    return jsonify(Book.get_all(limit=limit, offset=offset))


@books_bp.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = Book.get_by_id(book_id)
    if book:
        return jsonify(book)
    return jsonify({"error": "Книгу не знайдено"}), 404


@books_bp.route("/books", methods=["POST"])
def add_book():
    try:
        book_schema = BookCreateSchema()
        book_data = book_schema.load(request.json)
        new_book = Book.create(book_data)
        return jsonify(new_book), 201
    except ValidationError as err:
        return jsonify({"error": "Помилка валідації", "details": err.messages}), 400


@books_bp.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    deleted_book = Book.delete(book_id)
    if deleted_book:
        return jsonify(
            {"message": f"Книгу '{deleted_book['title']}' успішно видалено"}
        ), 200
    return jsonify({"error": "Книгу не знайдено"}), 404
