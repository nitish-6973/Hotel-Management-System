import tkinter as tk
from tkinter import messagebox
import mysql.connector
from tabulate import tabulate

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Nitish6973@',
    'database': 'hotel_management'
}

def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

def add_room_gui():
    def submit():
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO rooms (room_number, room_type, room_rent, bed_type, status)
                VALUES (%s, %s, %s, %s, %s)
            """, (e1.get(), e2.get(), float(e3.get()), e4.get(), e5.get()))
            conn.commit()
            messagebox.showinfo("Success", "Room added successfully!")
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    top = tk.Toplevel(root)
    top.title("Add Room")

    tk.Label(top, text="Room Number").grid(row=0)
    tk.Label(top, text="Room Type").grid(row=1)
    tk.Label(top, text="Room Rent").grid(row=2)
    tk.Label(top, text="Bed Type").grid(row=3)
    tk.Label(top, text="Status").grid(row=4)

    e1 = tk.Entry(top)
    e2 = tk.Entry(top)
    e3 = tk.Entry(top)
    e4 = tk.Entry(top)
    e5 = tk.Entry(top)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)
    e4.grid(row=3, column=1)
    e5.grid(row=4, column=1)

    tk.Button(top, text="Submit", command=submit).grid(row=5, column=1)

def view_rooms_gui():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rooms")
        rows = cursor.fetchall()
        display_result(rows, [i[0] for i in cursor.description], "Room Details")
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def view_customers_gui():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers")
        rows = cursor.fetchall()
        display_result(rows, [i[0] for i in cursor.description], "Customer Details")
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def add_customer_gui():
    def submit():
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO customers (name, address, phone, email, id_proof, id_number, males, females, children)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (e1.get(), e2.get(), e3.get(), e4.get(), e5.get(), e6.get(), int(e7.get()), int(e8.get()), int(e9.get())))
            conn.commit()
            messagebox.showinfo("Success", "Customer added successfully!")
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    top = tk.Toplevel(root)
    top.title("Add Customer")

    labels = [
        "Name", "Address", "Phone", "Email", "ID Proof",
        "ID Number", "Males", "Females", "Children"
    ]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(top, text=label).grid(row=i, column=0)
        entry = tk.Entry(top)
        entry.grid(row=i, column=1)
        entries.append(entry)

    e1, e2, e3, e4, e5, e6, e7, e8, e9 = entries
    tk.Button(top, text="Submit", command=submit).grid(row=len(labels), column=1)

def book_room_gui():
    def submit():
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT status FROM rooms WHERE room_id = %s", (int(e2.get()),))
            result = cursor.fetchone()
            if result and result[0] == 'free':
                cursor.execute("""
                    INSERT INTO bookings (customer_id, room_id, check_in_date, check_out_date)
                    VALUES (%s, %s, %s, %s)
                """, (int(e1.get()), int(e2.get()), e3.get(), e4.get()))
                cursor.execute("UPDATE rooms SET status = 'occupied' WHERE room_id = %s", (int(e2.get()),))
                conn.commit()
                messagebox.showinfo("Success", "Room booked successfully!")
            else:
                messagebox.showwarning("Unavailable", "Room is not available.")
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    top = tk.Toplevel(root)
    top.title("Book Room")

    tk.Label(top, text="Customer ID").grid(row=0)
    tk.Label(top, text="Room ID").grid(row=1)
    tk.Label(top, text="Check-in Date (YYYY-MM-DD)").grid(row=2)
    tk.Label(top, text="Check-out Date (YYYY-MM-DD)").grid(row=3)

    e1 = tk.Entry(top)
    e2 = tk.Entry(top)
    e3 = tk.Entry(top)
    e4 = tk.Entry(top)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)
    e4.grid(row=3, column=1)

    tk.Button(top, text="Submit", command=submit).grid(row=4, column=1)

def view_bookings_gui():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b.booking_id, c.name, r.room_number, b.check_in_date, b.check_out_date
            FROM bookings b
            JOIN customers c ON b.customer_id = c.customer_id
            JOIN rooms r ON b.room_id = r.room_id
        """)
        rows = cursor.fetchall()
        headers = [i[0] for i in cursor.description]
        display_result(rows, headers, "Booking Details")
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def display_result(data, headers, title):
    top = tk.Toplevel(root)
    top.title(title)
    text = tk.Text(top)
    table = tabulate(data, headers, tablefmt="grid")
    text.insert(tk.END, table)
    text.pack()
def delete_room_gui():
    def submit():
        try:
            room_id = int(e1.get())
            conn = connect_db()
            cursor = conn.cursor()

            # Check if room exists
            cursor.execute("SELECT * FROM rooms WHERE room_id = %s", (room_id,))
            result = cursor.fetchone()

            if result:
                # Optional: Confirm before deleting
                if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Room ID {room_id}?"):
                    cursor.execute("DELETE FROM rooms WHERE room_id = %s", (room_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Room deleted successfully!")
            else:
                messagebox.showwarning("Not Found", "Room ID not found.")

            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    top = tk.Toplevel(root)
    top.title("Delete Room")
    tk.Label(top, text="Enter Room ID to Delete").grid(row=0)
    e1 = tk.Entry(top)
    e1.grid(row=0, column=1)
    tk.Button(top, text="Delete", command=submit).grid(row=1, column=1)


# GUI Window
root = tk.Tk()
root.title("Hotel Management System GUI")
root.geometry("800x600")  # Make window size bigger to show background better



buttons = [
    ("View Rooms", view_rooms_gui),
    ("Add Room", add_room_gui),
    ("Delete Room", delete_room_gui),  # <-- Add this line
    ("View Customers", view_customers_gui),
    ("Add Customer", add_customer_gui),
    ("Book Room", book_room_gui),
    ("View Bookings", view_bookings_gui),
    ("Exit", root.quit)
]


for (text, command) in buttons:
    tk.Button(root, text=text, width=30, command=command).pack(pady=5)

root.mainloop()
