from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from schemas import BookCreateSchema
import models

books_bp = Blueprint("books", __name__, url_prefix="/api/v1")


@books_bp.route("/books", methods=["GET"])
def get_books():
    return jsonify(models.get_all_books())


@books_bp.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = models.get_book_by_id(book_id)
    if book:
        return jsonify(book)
    return jsonify({"error": "Книгу не знайдено"}), 404


@books_bp.route("/books", methods=["POST"])
def add_book():
    try:
        book_schema = BookCreateSchema()
        book_data = book_schema.load(request.json)

        new_book = models.add_book(book_data)
        return jsonify(new_book), 201

    except ValidationError as err:
        return jsonify({"error": "Помилка валідації", "details": err.messages}), 400


@books_bp.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    deleted_book = models.delete_book(book_id)

    if deleted_book:
        return jsonify(
            {"message": f"Книгу '{deleted_book['title']}' успішно видалено"}
        ), 200

    return jsonify({"error": "Книгу не знайдено"}), 404
