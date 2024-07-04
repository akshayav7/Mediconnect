import tkinter as tk
from tkinter import messagebox
import mysql.connector

def submit_details():
    medicine_required = medicine_entry.get()
    name = name_entry.get()
    reg_number = reg_entry.get()
    hostel_name = hostel_name_entry.get()
    hostel_number = hostel_number_entry.get()
    phone_number = phone_entry.get()

    # Check if any of the fields is empty
    if not medicine_required or not name or not reg_number or not hostel_name or not hostel_number or not phone_number:
        messagebox.showerror("Error", "Please fill in all fields.")
    # Check if the phone number has at least 10 digits
    elif len(phone_number) < 10:
        messagebox.showwarning("Warning", "Please provide a valid phone number (at least 10 digits).")
    else:
        # Connect to MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Akshaya@2005",
            database="wise"
        )
        cursor = conn.cursor()

        # Insert data into the table
        sql = "INSERT INTO medicine_details (medicine_required, name, reg_number, hostel_name, hostel_number, phone_number) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (medicine_required, name, reg_number, hostel_name, hostel_number, phone_number)
        cursor.execute(sql, val)

        conn.commit()
        conn.close()

        output_text = f"Medicine Required: {medicine_required}\nName: {name}\nRegistration Number: {reg_number}\nHostel Name: {hostel_name}\nHostel Number: {hostel_number}\nPhone Number: {phone_number}"
        messagebox.showinfo("Details Submitted", output_text)

def go_back(window):
    window.destroy()

# Create the main window
root = tk.Tk()
root.title("Medicine Details")

# Set background color to blue
root.configure(bg="lightblue")
root.iconbitmap(r"C:\Users\aksha\Downloads\mediconect.ico")
# Entry fields for the user to fill in
medicine_label = tk.Label(root, text="Medicine Required:")
medicine_label.pack(pady=5)
medicine_entry = tk.Entry(root)
medicine_entry.pack(pady=5)

name_label = tk.Label(root, text="Name:")
name_label.pack(pady=5)
name_entry = tk.Entry(root)
name_entry.pack(pady=5)

reg_label = tk.Label(root, text="Registration Number:")
reg_label.pack(pady=5)
reg_entry = tk.Entry(root)
reg_entry.pack(pady=5)

hostel_name_label = tk.Label(root, text="Hostel Name:")
hostel_name_label.pack(pady=5)
hostel_name_entry = tk.Entry(root)
hostel_name_entry.pack(pady=5)

hostel_number_label = tk.Label(root, text="Room Number:")
hostel_number_label.pack(pady=5)
hostel_number_entry = tk.Entry(root)
hostel_number_entry.pack(pady=5)

phone_label = tk.Label(root, text="Phone Number:")
phone_label.pack(pady=5)
phone_entry = tk.Entry(root)
phone_entry.pack(pady=5)

# Submit button
submit_button = tk.Button(root, text="Submit", command=submit_details)
submit_button.pack(pady=10)

# Back button
back_button = tk.Button(root, text="Back", command=lambda: go_back(root))
back_button.pack(pady=10)

# Center the window on the screen
root_width = 1000  # set the width as needed
root_height = 1000  # set the height as needed
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (root_width // 2)
y = (screen_height // 2) - (root_height // 2)
root.geometry(f"{root_width}x{root_height}+{x}+{y}")

# Start the Tkinter event loop
root.mainloop()
