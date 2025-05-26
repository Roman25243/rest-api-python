from typing import List, Dict, Optional

books = [
    {
        "id": 1,
        "title": "Кобзар",
        "author": "Тарас Шевченко",
        "year": 1840,
        "isbn": "978-966-01-0585-5",
    },
    {
        "id": 2,
        "title": "Енеїда",
        "author": "Іван Котляревський",
        "year": 1798,
        "isbn": "978-966-10-4104-0",
    },
]


def get_all_books() -> List[Dict]:
    return books


def get_book_by_id(book_id: int) -> Optional[Dict]:
    return next((book for book in books if book["id"] == book_id), None)


def add_book(book_data: Dict) -> Dict:
    new_id = max(book["id"] for book in books) + 1 if books else 1
    new_book = {"id": new_id, **book_data}
    books.append(new_book)
    return new_book


def delete_book(book_id: int) -> Optional[Dict]:
    book_index = next(
        (index for index, book in enumerate(books) if book["id"] == book_id), None
    )
    if book_index is not None:
        return books.pop(book_index)
    return None
