def list_books():
    print("Listing books...")

def borrow_book(book_name):
    print(f"Borrowing book: {book_name}")

def return_book(book_name):
    print(f"Returning book: {book_name}")

def main():
    list_books()
    borrow_book("Python Programming")
    return_book("Python Programming")

if __name__ == "__main__":
    main()
