import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import webbrowser
from backend2 import Database 

class BookManagerApp:
    def __init__(self, root):
        self.db = Database("books.db")
        self.root = root
        self.root.title("Book Management System")
        self.root.geometry("900x650")
                
        self.bg_image = Image.open("backgroundimage.jpeg")
        self.bg_image = self.bg_image.resize((900, 650), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f8ff")
        self.style.configure("TButton", background="#4CAF50", foreground="green", font=("Arial", 12), padding=10)
        self.style.configure("TLabel", background="#f0f8ff", font=("Arial", 12))

        self.login_frame = ttk.Frame(root, padding=20, style="TFrame")
        self.create_login_screen()

        self.main_frame = ttk.Frame(root, padding=20, style="TFrame", width=700, height=400)

    def create_login_screen(self):
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(self.login_frame, text="WELCOME", font=("Times New Roman", 24, "bold"), background="#e0e0d1").grid(row=0, column=0, columnspan=2, pady=20)
        ttk.Label(self.login_frame, text="Username:", font=("Times New Roman", 14), background="#e0e0d1").grid(row=1, column=0, sticky="e", pady=10)
        ttk.Label(self.login_frame, text="Password:", font=("Times New Roman", 14), background="#e0e0d1").grid(row=2, column=0, sticky="e", pady=10)

        self.username_entry = ttk.Entry(self.login_frame, font=("Times New Roman", 12), width=30)
        self.username_entry.grid(row=1, column=1, pady=10)
        self.password_entry = ttk.Entry(self.login_frame, show="*", font=("Times New Roman", 12), width=30)
        self.password_entry.grid(row=2, column=1, pady=10)

        ttk.Button(self.login_frame, text="Login", command=self.authenticate, style="TButton").grid(row=3, column=0, columnspan=2, pady=20)
        ttk.Button(self.login_frame, text="Register", command=self.open_registration_window, style="TButton").grid(row=4, column=0, columnspan=2, pady=10)

    def open_registration_window(self):
        self.registration_win = tk.Toplevel(self.root)
        self.registration_win.title("User  Registration")
        self.registration_win.geometry("400x300")
        self.registration_win.config(bg="#e6e6fa")

        ttk.Label(self.registration_win, text="Register", font=("Times New Roman", 16, "bold"), background="#e6e6fa").pack(pady=10)

        ttk.Label(self.registration_win, text="Username:", background="#e6e6fa").pack(pady=5)
        self.reg_username_entry = ttk.Entry(self.registration_win)
        self.reg_username_entry.pack(pady=5)

        ttk.Label(self.registration_win, text="Password:", background="#e6e6fa").pack(pady=5)
        self.reg_password_entry = ttk.Entry(self.registration_win, show="*")
        self.reg_password_entry.pack(pady=5)

        ttk.Button(self.registration_win, text="Register", command=self.register_user, style="TButton").pack(pady=20)

    def register_user(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        if self.db.register_user(username, password):  
            messagebox.showinfo("Success", "Registration successful!")
            self.registration_win.destroy()
        else:
            messagebox.showerror("Error", "Registration failed. Please try again.")

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        role, success = self.db.authenticate_user(username, password)
        if success:
            messagebox.showinfo("Success", "Login successful!")
            self.current_user = username
            self.user_role = role  
            self.login_frame.place_forget()
            self.create_main_screen()  
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def create_main_screen(self):
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(self.main_frame, text="Book Management System", font=("Times New Roman", 24, "bold"), background="#f25f3a").grid(row=0, column=0, columnspan=2, pady=20)

        ttk.Button(self.main_frame, text="View Books", command=self.view_books, style="TButton").grid(row=1, column=0, pady=10, padx=10, sticky="ew", columnspan=2)
        ttk.Button(self.main_frame, text="Search Books", command=self.search_books, style="TButton").grid(row=2, column=0, pady=10, padx=10, sticky="ew", columnspan=2)
        ttk.Button(self.main_frame, text="View Orders", command=self.view_orders, style="TButton").grid(row=3, column=0, pady=10, padx=10, sticky="ew", columnspan=2)
        ttk.Button(self.main_frame, text="Logout", command=self.logout, style="TButton").grid(row=4, column=0, pady=10, padx=10, sticky="ew", columnspan=2)

        if self.user_role == 'admin':
            ttk.Button(self.main_frame, text="Add Book", command=self.add_book, style="TButton").grid(row=5, column=0, pady=10, padx=10, sticky="ew", columnspan=2)
            ttk.Button(self.main_frame, text="Edit Book", command=self.edit_book, style="TButton").grid(row=6, column=0, pady=10, padx=10, sticky="ew", columnspan=2)
            ttk.Button(self.main_frame, text="Delete Book", command=self.delete_book, style="TButton").grid(row=7, column=0, pady=10, padx=10, sticky="ew", columnspan=2)

    def logout(self):
        self.main_frame.place_forget()  
        self.create_login_screen()  

    def add_book(self):
        self.book_window("Add", "#f0e68c")

    def edit_book(self):
        self.book_window("Edit", "#ffcccb")

    def delete_book(self):
        self.book_window("Delete", "#d3d3d3")

    def view_books(self):
        books = self.db.fetch_books()  # Fetch books from the database
        self.show_books(books, "View Books")  # Pass the books to show_books

    def search_books(self):
        self.search_win = tk.Toplevel(self.root)
        self.search_win.transient(self.root)  # Set parent window
        self.search_win.grab_set()  # Make window modal
        self.search_win.title("Search Books")
        self.search_win.geometry("400x250")
        self.center_window_within_root(self.search_win, 400, 250)
        self.search_win.config(bg="#e6e6fa")

        ttk.Label(self.search_win, text="Search Books", font=("Times New Roman", 16, "bold"), background="#e6e6fa").grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self.search_win, text="Title:", font=("Times New Roman", 12), background="#e6e6fa").grid(row=1, column=0, sticky="e", pady=5)
        self.title_search = ttk.Entry(self.search_win, font=("Times New Roman", 12), width=25)
        self.title_search.grid(row=1, column=1, pady=5)

        ttk.Label(self.search_win, text="Author:", font=("Times New Roman", 12), background="#e6e6fa").grid(row=2, column=0, sticky="e", pady=5)
        self.author_search = ttk.Entry(self.search_win, font=("Times New Roman", 12), width=25)
        self.author_search.grid(row=2, column=1, pady=5)

        ttk.Label(self.search_win, text="Year:", font=("Times New Roman", 12), background="#e6e6fa").grid(row=3, column=0, sticky="e", pady=5)
        self.year_search = ttk.Entry(self.search_win, font=("Times New Roman", 12), width=25)
        self.year_search.grid(row=3, column=1, pady=5)

        ttk.Button(self.search_win, text="Search", command=self.perform_search, style="TButton").grid(row=4, column=0, columnspan=2, pady=20)

    def perform_search(self):
        title = self.title_search.get()
        author = self.author_search.get()
        year = self.year_search.get()

        results = self.db.search_books(title, author, year)
        if results:
            self.show_books(results, "Search Results")
        else:
            messagebox.showinfo("No Results", "No books found matching your search.")

    def show_books(self, books, title):
        self.books_win = tk.Toplevel(self.root)
        self.books_win.transient(self.root)
        self.books_win.grab_set()
        self.books_win.title(title)
        self.books_win.geometry("700x500")
        self.center_window_within_root(self.books_win, 700, 500)
        self.books_win.config(bg="#b0e0e6")

        if books:
            cols = ("ID", "Title", "Author", "Year", "ISBN", "Purchase Link")
            tree = ttk.Treeview(self.books_win, columns=cols, show="headings", height=15)

            tree.heading("ID", text="ID")
            tree.heading("Title", text="Title")
            tree.heading("Author", text="Author")
            tree.heading("Year", text="Year")
            tree.heading("ISBN", text="ISBN")
            tree.heading("Purchase Link", text="Buy")

            tree.column("ID", width=50, anchor="center")
            tree.column("Title", width=250, anchor="w")
            tree.column("Author", width=150, anchor="w")
            tree.column("Year", width=100, anchor="center")
            tree.column("ISBN", width=150, anchor="center")
            tree.column("Purchase Link", width=200, anchor="center")

            for book in books:
                tree.insert("", "end", values=book)

            tree.pack(padx=10, pady=10)

            # Create buttons directly in the books_win window
            ttk.Button(self.books_win, text="Buy Book", 
                    command=lambda: self.open_link(tree), 
                    style="TButton").pack(pady=10)
            
            ttk.Button(self.books_win, text="Return Book", 
                    command=lambda: self.return_book(tree), 
                    style="TButton").pack(pady=10)
        else:
            messagebox.showinfo("No Books", "No books found.")

            
    def return_book(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Select Book", "Please select a book to return")
            return
            
        book = tree.item(selected)['values']
        book_title = book[1]
        user_id = self.get_user_id(self.current_user)
        
        if messagebox.askyesno("Confirm Return", f"Do you want to return '{book_title}'?"):
            orders = self.db.get_user_orders(user_id)
            active_order = next((order for order in orders if order['book_title'] == book_title), None)
            
            if active_order:
                if self.db.process_return(active_order['order_id']):
                    messagebox.showinfo("Success", "Book returned successfully!")
                else:
                    messagebox.showerror("Error", "Return failed")
            else:
                messagebox.showinfo("No Order", "You haven't purchased this book")

        

    def view_orders(self):
        orders = self.db.get_orders()  
        orders_window = tk.Toplevel(self.root)
        orders_window.transient(self.root)  # Set parent window
        orders_window.grab_set()  # Make window modal
        orders_window.title("View Orders")
        
        self.center_window(orders_window, 600, 400)  

        orders_window.configure(bg="#d1f533")

        title_label = tk.Label(orders_window, text="Orders List", bg="#f0f0f0", font=("Times New Roman", 16, "bold"))
        title_label.pack(pady=10)
        orders_listbox = tk.Listbox(orders_window, width=70, height=15, bg="#ffffff", fg="#333333", font=("Times New Roman", 12))
        orders_listbox.pack(pady=10)

        for order in orders:
            orders_listbox.insert(tk.END, f"Book: {order['book_title']}, User ID: {order['user_id']}, Date: {order['order_date']}")

        scrollbar = tk.Scrollbar(orders_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        orders_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=orders_listbox.yview)

        close_button = tk.Button(orders_window, text="Close", command=orders_window.destroy, bg="#007BFF", fg="#ffffff", font=("Times New Roman", 12), padx=12, pady=5)
        close_button.pack(pady=5)

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        window.geometry(f"{width}x{height}+{x}+{y}")
    def open_link(self, tree):
          selected_item = tree.selection()
          if selected_item:
              selected_book = tree.item(selected_item)["values"]
              if selected_book:
                  link = selected_book[-1]  
                  book_title = selected_book[1]
                  book_price = "49.99"  # You can add price to your books table and fetch it here
                  user_id = self.get_user_id(self.current_user)

                  # First show order received message
                  messagebox.showinfo("Order Received", f"Your order for '{book_title}' has been received!")
                
                  # Open payment window
                  if self.process_payment(book_title, book_price):
                      # If payment successful, store order and open purchase link
                      self.db.store_order(book_title, user_id)
                      messagebox.showinfo("Success", "Order confirmed and payment processed successfully!")
                      if link:
                          webbrowser.open(link)
                  else:
                      messagebox.showwarning("Payment Failed", "Order cancelled due to payment failure.")
              else:
                  messagebox.showwarning("No Data", "No book data available.")
          else:
              messagebox.showwarning("No Selection", "Please select a book to purchase.")
    def process_payment(self, book_title, price):
            self.payment_window = tk.Toplevel(self.root)
            self.payment_window.transient(self.root)
            self.payment_window.grab_set()
            self.payment_window.title("Payment Page")
            self.center_window_within_root(self.payment_window, 400, 500)
            self.payment_window.configure(bg="#e6e6fa")

            # Payment form header
            ttk.Label(self.payment_window, text=f"Payment for: {book_title}", 
                    font=("Times New Roman", 14, "bold")).pack(pady=10)
            ttk.Label(self.payment_window, text=f"Amount: ${price}", 
                    font=("Times New Roman", 12)).pack(pady=5)

            # Card number validation function
            def validate_card_number(P):
                if P == "": return True
                if not P.isdigit(): return False
                return len(P) <= 16

            vcmd = (self.payment_window.register(validate_card_number), '%P')

            # Payment input fields with validation
            ttk.Label(self.payment_window, text="Card Number (12 or 16 digits):", background="#e6e6fa").pack(pady=5)
            self.card_number = ttk.Entry(self.payment_window, width=30, validate='key', validatecommand=vcmd)
            self.card_number.pack(pady=5)

            ttk.Label(self.payment_window, text="Expiry Date (MM/YY):", background="#e6e6fa").pack(pady=5)
            self.expiry_date = ttk.Entry(self.payment_window, width=30)
            self.expiry_date.pack(pady=5)

            ttk.Label(self.payment_window, text="CVV:", background="#e6e6fa").pack(pady=5)
            self.cvv = ttk.Entry(self.payment_window, show="*", width=30)
            self.cvv.pack(pady=5)

            self.payment_status = tk.BooleanVar(value=False)

            ttk.Button(self.payment_window, 
                       text="Confirm Payment",
                       command=self.confirm_payment,
                       style="TButton").pack(pady=20)

            self.payment_window.wait_window()
            return self.payment_status.get()

    def confirm_payment(self):
            card_num = self.card_number.get()
            if len(card_num) not in [12, 16]:
                messagebox.showerror("Error", "Card number must be 12 or 16 digits")
                return
            
            if self.card_number.get() and self.expiry_date.get() and self.cvv.get():
                self.payment_status.set(True)
                messagebox.showinfo("Success", "Payment processed successfully!")
                self.payment_window.destroy()
            else:
                messagebox.showerror("Error", "Please fill in all payment details")

    def get_user_id(self, username):
        
        user = self.db.fetch_user_by_username(username) 
        return user[0] if user else None  

    def center_window_within_root(self, window, width, height):
        screen_width = self.root.winfo_width()
        screen_height = self.root.winfo_height()
        position_top = int(screen_height / 2 - height / 2)
        position_left = int(screen_width / 2 - width / 2)
        window.geometry(f'{width}x{height}+{position_left}+{position_top}')

    def book_window(self, mode, color):
        if self.user_role != 'admin':
            messagebox.showerror("Access Denied", "You are not authorized to access this feature.")
            return

        self.book_win = tk.Toplevel(self.root)
        self.book_win.title(f"{mode} Book")
        self.book_win.geometry("400x450")
        self.book_win.config(bg=color)

        ttk.Label(self.book_win, text=f"{mode} Book", font=("Times New Roman", 16, "bold"), background=color).pack(pady=10)

        ttk.Label(self.book_win, text="Title:", background=color).pack(pady=5)
        self.title_entry = ttk.Entry(self.book_win)
        self.title_entry.pack(pady=5)

        ttk.Label(self.book_win, text="Author:", background=color).pack(pady=5)
        self.author_entry = ttk.Entry(self.book_win)
        self.author_entry.pack(pady=5)

        ttk.Label(self.book_win, text="Year:", background=color).pack(pady=5)
        self.year_entry = ttk.Entry(self.book_win)
        self.year_entry.pack(pady=5)

        ttk.Label(self.book_win, text="ISBN:", background=color).pack(pady=5)
        self.isbn_entry = ttk.Entry(self.book_win)
        self.isbn_entry.pack(pady=5)

        ttk.Label(self.book_win, text="Purchase Link:", background=color).pack(pady=5)
        self.purchase_link_entry = ttk.Entry(self.book_win)
        self.purchase_link_entry.pack(pady=5)

        if mode == "Edit" or mode == "Delete":
            tk.Button(self.book_win, text="Load Book Details", command=self.load_book_details).pack(pady=10)

        if mode == "Add":
            tk.Button(self.book_win, text="Save Book", command=self.save_book).pack(pady=10)
        elif mode == "Edit":
            tk.Button(self.book_win, text="Update Book", command=self.update_book).pack(pady=10)
        elif mode == "Delete":
            tk.Button(self.book_win, text="Delete Book", command=self.confirm_delete).pack(pady=10)

    def save_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        year = self.year_entry.get()
        isbn = self.isbn_entry.get()
        purchase_link = self.purchase_link_entry.get()

        if title and author and year.isdigit() and isbn:  
            self.db.add_book(title, author, int(year), isbn, purchase_link)  
            messagebox.showinfo("Success", "Book added successfully!")
            self.book_win.destroy()
        else:
            messagebox.showerror("Error", "Please fill in all fields correctly.")

    def update_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        year = self.year_entry.get()
        isbn = self.isbn_entry.get()
        purchase_link = self.purchase_link_entry.get()

        if title and author and year.isdigit() and isbn:  
            book_id = self.db.fetch_book_by_title(title)[0]  # Get the book ID
            self.db.update_book(book_id, title, author, int(year), isbn, purchase_link)  
            messagebox.showinfo("Success", "Book updated successfully!")
            self.book_win.destroy()
        else:
            messagebox.showerror("Error", "Please fill in all fields correctly.")

    def confirm_delete(self):
        title = self.title_entry.get()
        if title:
            if self.db.delete_book(title):  
                messagebox.showinfo("Success", "Book deleted successfully!")
                self.book_win.destroy()
            else:
                messagebox.showerror("Error", "Book not found or could not be deleted.")
        else:
            messagebox.showerror("Error", "Please enter the book title to delete.")

    def load_book_details(self):
        title = self.title_entry.get()
        if not title:
            messagebox.showerror("Error", "Please enter a book title to load.")
            return

        book = self.db.fetch_book_by_title(title)
        if book:
            self.author_entry.delete(0, tk.END)
            self.year_entry.delete(0, tk.END)
            self.isbn_entry.delete( 0, tk.END)
            self.purchase_link_entry.delete(0, tk.END)

            self.author_entry.insert(0, book[2]) 
            self.year_entry.insert(0, str(book[3]))
            self.isbn_entry.insert(0, book[4])
            self.purchase_link_entry.insert(0, book[5])
            
            messagebox.showinfo("Success", f"Book '{title}' details loaded successfully.")
        else:
            messagebox.showerror("Error", f"No book found with title '{title}'")

if __name__ == "__main__":
    root = tk.Tk()
    app = BookManagerApp(root)
    root.mainloop()