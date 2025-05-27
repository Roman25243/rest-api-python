from flask import Flask
from flask_restful import Api
from flasgger import Swagger
from models import db, init_sample_data, Book
import os
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)
    api = Api(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SWAGGER"] = {
        "title": "Library API",
        "uiversion": 3,
        "specs_route": "/docs/",
        "definitions": {
            "Book": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "readOnly": True},
                    "title": {"type": "string"},
                    "author": {"type": "string"},
                    "year": {"type": "integer"},
                    "isbn": {"type": "string"},
                },
                "required": ["title", "author", "year", "isbn"],
            }
        },
    }

    db.init_app(app)

    swagger = Swagger(app)

    from resources import BookResource, BookListResource

    api.add_resource(BookListResource, "/api/v1/books")
    api.add_resource(BookResource, "/api/v1/books/<int:book_id>")

    with app.app_context():
        db.create_all()
        if not db.session.query(Book).first():
            init_sample_data()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
