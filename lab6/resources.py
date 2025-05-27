from urllib import request
from flask_restful import Resource, reqparse
from marshmallow import ValidationError
from models import Book
from app import db
from schemas import BookSchema

book_schema = BookSchema()


class BookListResource(Resource):
    def get(self):
        """
        Отримати список книг з курсорною пагінацією
        ---
        tags:
          - Books
        parameters:
          - name: cursor
            in: query
            type: integer
            required: false
            description: ID останньої отриманої книги
          - name: limit
            in: query
            type: integer
            required: false
            default: 10
            description: Кількість книг для повернення
        responses:
          200:
            description: Список книг
            schema:
              type: object
              properties:
                data:
                  type: array
                  items:
                    $ref: '#/definitions/Book'
                pagination:
                  type: object
                  properties:
                    next_cursor:
                      type: integer
                    has_more:
                      type: boolean
        """
        parser = reqparse.RequestParser()
        parser.add_argument("cursor", type=int, location="args")
        parser.add_argument("limit", type=int, location="args", default=10)
        args = parser.parse_args()

        query = Book.query.order_by(Book.id)
        if args["cursor"]:
            query = query.filter(Book.id > args["cursor"])

        books = query.limit(min(args["limit"], 100)).all()
        next_cursor = books[-1].id if books else None

        return {
            "data": [book.to_dict() for book in books],
            "pagination": {
                "next_cursor": next_cursor,
                "has_more": next_cursor is not None,
            },
        }

    def post(self):
        """
        Додати нову книгу
        ---
        tags:
          - Books
        parameters:
          - name: body
            in: body
            required: true
            schema:
              $ref: '#/definitions/Book'
        responses:
          201:
            description: Книга успішно додана
            schema:
              $ref: '#/definitions/Book'
          400:
            description: Помилка валідації
        """
        try:
            data = book_schema.load(request.get_json())
            book = Book(**data)
            db.session.add(book)
            db.session.commit()
            return book_schema.dump(book), 201
        except ValidationError as err:
            return {"error": "Помилка валідації", "details": err.messages}, 400


class BookResource(Resource):
    def get(self, book_id):
        """
        Отримати книгу за ID
        ---
        tags:
          - Books
        parameters:
          - name: book_id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Інформація про книгу
            schema:
              $ref: '#/definitions/Book'
          404:
            description: Книга не знайдена
        """
        book = Book.query.get_or_404(book_id)
        return book_schema.dump(book)

    def delete(self, book_id):
        """
        Видалити книгу
        ---
        tags:
          - Books
        parameters:
          - name: book_id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Книга успішно видалена
          404:
            description: Книга не знайдена
        """
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return {"message": f"Книга '{book.title}' успішно видалена"}, 200
