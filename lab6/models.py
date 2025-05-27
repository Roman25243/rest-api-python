from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.String(20), nullable=False, unique=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "isbn": self.isbn,
        }


def init_sample_data():
    if not Book.query.first():
        sample_books = [
            Book(
                title="Кобзар",
                author="Тарас Шевченко",
                year=1840,
                isbn="978-966-01-0585-5",
            ),
            Book(
                title="Енеїда",
                author="Іван Котляревський",
                year=1798,
                isbn="978-966-10-4104-0",
            ),
        ]
        db.session.bulk_save_objects(sample_books)
        db.session.commit()
