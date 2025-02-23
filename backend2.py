import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='books.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER NOT NULL,
            isbn TEXT UNIQUE NOT NULL,
            purchase_link TEXT
        )
        """)

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_title TEXT,
            user_id INTEGER,
            order_date DATETIME,
            status TEXT DEFAULT 'active'
        )
        ''')

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS returns (
            return_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            book_title TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            return_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            return_reason TEXT,
            FOREIGN KEY (order_id) REFERENCES orders (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """)

        self.cursor.execute("""
        INSERT OR IGNORE INTO users (username, password)
        VALUES (?, ?)
        """, ("admin", "123"))
        self.conn.commit()

        self.add_sample_books()

    def authenticate_user(self, username, password):
        self.cursor.execute("""
        SELECT username FROM users WHERE username = ? AND password = ?
        """, (username, password))
        user = self.cursor.fetchone()

        if user:
            is_admin = user[0] == 'admin'
            return ('admin' if is_admin else 'user', True)
        return (None, False)

    def register_user(self, username, password):
        try:
            self.cursor.execute("""
            INSERT INTO users (username, password)
            VALUES (?, ?)
            """, (username, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
   
    def add_sample_books(self):
        real_books = [
            ("The Great Gatsby", "F. Scott Fitzgerald", 1925, "9780743273565", "https://www.amazon.com/dp/0743273567"),
            ("1984", "George Orwell", 1949, "9780451524935", "https://www.amazon.com/dp/0451524934"),
            ("To Kill a Mockingbird", "Harper Lee", 1960, "9780061120084", "https://www.amazon.com/dp/0061120081"),
            ("Sapiens: A Brief History of Humankind", "Yuval Noah Harari", 2011, "9780062316097", "https://www.amazon.com/dp/0062316095"),
            ("Becoming", "Michelle Obama", 2018, "9781524763138", "https://www.amazon.com/dp/1524763136"),
            ("Educated", "Tara Westover", 2018, "9780399590504", "https://www.amazon.com/dp/0399590501"),
            ("The Silent Patient", "Alex Michaelides", 2019, "9781250301697", "https://www.amazon.com/dp/1250301696"),
            ("Where the Crawdads Sing", "Delia Owens", 2018, "9780735219090", "https://www.amazon.com/dp/073521909X"),
            ("Atomic Habits", "James Clear", 2018, "9780735211292", "https://www.amazon.com/dp/0735211299"),
            ("The Subtle Art of Not Giving a Fox", "Mark Manson", 2016, "9780062457714", "https://www.amazon.com/dp/0062457713")
        ]
        for book in real_books:
            self.add_book(*book)

    def add_book(self, title, author, year, isbn, purchase_link=None):
        try:
            self.cursor.execute("""
            INSERT OR IGNORE INTO books (title, author, year, isbn, purchase_link)
            VALUES (?, ?, ?, ?, ?)
            """, (title, author, year, isbn, purchase_link))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def update_book(self, book_id, title, author, year, isbn, purchase_link):
        self.cursor.execute("""
        UPDATE books
        SET title = ?, author = ?, year = ?, isbn = ?, purchase_link = ?
        WHERE id = ?
        """, (title, author, year, isbn, purchase_link, book_id))
        self.conn.commit()

    def delete_book(self, title):
        self.cursor.execute("""
        DELETE FROM books WHERE title = ?
        """, (title,))
        deleted = self.cursor.rowcount  
        self.conn.commit()
        return deleted > 0

    def fetch_books(self):
        self.cursor.execute("""
        SELECT id, title, author, year, isbn, purchase_link FROM books
        """)
        return self.cursor.fetchall()

    def search_books(self, title="", author="", year=""):
        query = "SELECT id, title, author, year, isbn, purchase_link FROM books WHERE 1=1"
        params = []

        if title:
            query += " AND title LIKE ?"
            params.append(f"%{title}%")
        if author:
            query += " AND author LIKE ?"
            params.append(f"%{author}%")
        if year:
            query += " AND year = ?"
            params.append(year)

        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetch_book_by_title(self, title):
        self.cursor.execute("""
        SELECT id, title, author, year, isbn, purchase_link FROM books WHERE title = ?
        """, (title,))
        return self.cursor.fetchone()

    def get_orders(self):
        self.cursor.execute("SELECT book_title, user_id, order_date, status FROM orders")
        return [{"book_title": row[0], "user_id": row[1], "order_date": row[2], "status": row[3]} 
                for row in self.cursor.fetchall()]

    def store_order(self, book_title, user_id):
        self.cursor.execute('''
            INSERT INTO orders (book_title, user_id, order_date, status)
            VALUES (?, ?, ?, ?)
        ''', (book_title, user_id, datetime.now(), 'active'))
        self.conn.commit()

    def fetch_user_by_username(self, username):
        self.cursor.execute('''
            SELECT id FROM users WHERE username = ?
        ''', (username,))
        return self.cursor.fetchone()
   
    def process_payment(self, book_title, user_id):
        payment_successful = True
        return payment_successful
   
    def get_user_orders(self, user_id):
        self.cursor.execute("""
            SELECT id, book_title, user_id, order_date 
            FROM orders 
            WHERE user_id=?
        """, (user_id,))
        orders = self.cursor.fetchall()
        return [{
            'order_id': order[0],
            'book_title': order[1],
            'user_id': order[2],
            'order_date': order[3],
            'status': 'active'  # Default status for existing orders
        } for order in orders]


    def process_return(self, order_id, return_reason=""):
        try:
            self.cursor.execute("SELECT book_title, user_id FROM orders WHERE id=?", (order_id,))
            order = self.cursor.fetchone()
            
            if order:
                self.cursor.execute("""
                    INSERT INTO returns (order_id, book_title, user_id, return_reason)
                    VALUES (?, ?, ?, ?)
                """, (order_id, order[0], order[1], return_reason))
                
                self.cursor.execute("UPDATE orders SET status='returned' WHERE id=?", (order_id,))
                
                self.conn.commit()
                return True
            return False
        except sqlite3.Error:
            return False

    def get_returns_history(self, user_id=None):
        if user_id:
            self.cursor.execute("""
                SELECT r.return_id, r.book_title, r.return_date, r.return_reason
                FROM returns r
                WHERE r.user_id=?
                ORDER BY r.return_date DESC
            """, (user_id,))
        else:
            self.cursor.execute("""
                SELECT r.return_id, r.book_title, u.username, r.return_date, r.return_reason
                FROM returns r
                JOIN users u ON r.user_id = u.id
                ORDER BY r.return_date DESC
            """)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
