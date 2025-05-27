from app import db
from typing import List, Dict, Optional, Tuple


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

    @classmethod
    def get_all(cls, cursor: int = None, limit: int = 10) -> Tuple[List[Dict], int]:
        query = cls.query.order_by(cls.id)

        if cursor:
            query = query.filter(cls.id > cursor)

        books = query.limit(limit).all()
        next_cursor = books[-1].id if books else None
        return [book.to_dict() for book in books], next_cursor

    @classmethod
    def get_by_id(cls, book_id: int) -> Optional[Dict]:
        book = cls.query.get(book_id)
        return book.to_dict() if book else None

    @classmethod
    def create(cls, book_data: Dict) -> Dict:
        book = cls(**book_data)
        db.session.add(book)
        db.session.commit()
        return book.to_dict()

    @classmethod
    def delete(cls, book_id: int) -> Optional[Dict]:
        book = cls.query.get(book_id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return book.to_dict()
        return None
