import tkinter as tk
from tkinter import messagebox
import mysql.connector

class MedicineRequest:
    def _init_(self, name, hostel, room_no, phone_number, medicine):
        self.name = name
        self.hostel = hostel
        self.room_no = room_no
        self.phone_number = phone_number
        self.medicine = medicine

def student_login():
    username = student_username_entry.get()
    password = student_password_entry.get()

    cursor.execute('''SELECT * FROM registration WHERE username=%s AND password=%s''',
                   (username, password))
    if cursor.fetchone():
        messagebox.showinfo("Login Successful", "Student login successful!")
        open_medicine_options()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def doctor_login():
    username = doctor_username_entry.get()
    password = doctor_password_entry.get()

    cursor.execute('''SELECT * FROM doctor_details WHERE username=%s AND password=%s''',
                   (username, password))
    if cursor.fetchone():
        messagebox.showinfo("Login Successful", "Doctor login successful!")
        open_medicine_options()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def open_medicine_options():
    # Close the login window
    main_window.withdraw()
    

    # Create a new window for medicine options
    medicine_window = tk.Toplevel()
    medicine_window.title("Medicine Options")
    #main_window.iconbitmap(r"C:\Users\aksha\Downloads\mediconect.ico")
    medicine_window.geometry("800x600")  # Adjust dimensions as needed
    medicine_window.configure(bg='lightblue')

    # Create labels for options
    need_med_label = tk.Label(medicine_window, text="Need a Medicine",font=("times new roman", 12))
    give_med_label = tk.Label(medicine_window, text="Give a Medicine", font=("times new roman", 12))
    notifications_label  = tk.Label(medicine_window, text="Notifications", font=("times new roman", 12))

    # Place the labels
    need_med_label.pack(pady=20)
    give_med_label.pack(pady=20)
    notifications_label.pack(pady=20)

    # Binding labels to their respective functions
    need_med_label.bind("<Button-1>", lambda event: option_selected(1))
    give_med_label.bind("<Button-1>", lambda event: option_selected(2))
    notifications_label.bind("<Button-1>", lambda event: option_selected(3))

    # Run the medicine options GUI
    medicine_window.mainloop()

def option_selected(option):
    if option == 1:
        messagebox.showinfo("Option Selected", "You selected: Need a Medicine")
    elif option == 2:
        messagebox.showinfo("Option Selected", "You selected: Give a Medicine")
    elif option == 3:
        messagebox.showinfo("Option Selected", "You selected: Notifications")


def open_signup_window():
    signup_window = tk.Toplevel()
    signup_window.title("Sign Up")
    signup_window.geometry("400x300")
    signup_window.configure(bg='lightblue')

    # Add your sign-up fields and functionality here

    signup_window.mainloop()


# Establish connection to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Akshaya@2005",
    database="wise"
)
cursor = conn.cursor()

# Create main window for login
main_window = tk.Tk()
main_window.title("Login Portal")

# Set the icon for the window
main_window.iconbitmap(r"C:\Users\aksha\Downloads\mediconect.ico")

# Calculate screen width and height
screen_width = main_window.winfo_screenwidth()
screen_height = main_window.winfo_screenheight()

# Set window dimensions and position to center
window_width = 800  # Adjust width as needed
window_height = 600  # Adjust height as needed
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

main_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
main_window.configure(bg='lightblue')

# Create student frame for login
student_frame = tk.Frame(main_window, bg='steelblue', padx=20, pady=20)

# Create labels and entry widgets for student login
student_heading_label = tk.Label(student_frame, text="Student Login", font=("times new roman", 16, "bold"))
student_username_label = tk.Label(student_frame, text="Username:")
student_username_entry = tk.Entry(student_frame)

student_password_label = tk.Label(student_frame, text="Password:")
student_password_entry = tk.Entry(student_frame, show='*')

# Create student login button
student_login_button = tk.Button(student_frame, text="Login", command=student_login)

# Create sign up button
signup_button = tk.Button(student_frame, text="Sign Up", command=open_signup_window)

# Pack labels, entry widgets, and buttons for student login
student_heading_label.grid(row=0, column=0, columnspan=2, pady=10)
student_username_label.grid(row=1, column=0, padx=10, pady=5)
student_username_entry.grid(row=1, column=1, padx=10, pady=5)
student_password_label.grid(row=2, column=0, padx=10, pady=5)
student_password_entry.grid(row=2, column=1, padx=10, pady=5)
student_login_button.grid(row=3, column=0, pady=10)
signup_button.grid(row=3, column=1, pady=10)  # Add signup_button to grid

# Create doctor frame for login
doctor_frame = tk.Frame(main_window, bg='steelblue', padx=20, pady=20)

# Create labels and entry widgets for doctor login
doctor_heading_label = tk.Label(doctor_frame, text="Doctor Login", font=("times new roman", 16, "bold"))
doctor_username_label = tk.Label(doctor_frame, text="Username:")
doctor_username_entry = tk.Entry(doctor_frame)

doctor_password_label = tk.Label(doctor_frame, text="Password:")
doctor_password_entry = tk.Entry(doctor_frame, show='*')

# Create doctor login button
doctor_login_button = tk.Button(doctor_frame, text="Login", command=doctor_login)

# Pack labels, entry widgets, and button for doctor login
doctor_heading_label.grid(row=0, column=0, columnspan=2, pady=10)
doctor_username_label.grid(row=1, column=0, padx=10, pady=5)
doctor_username_entry.grid(row=1, column=1, padx=10, pady=5)
doctor_password_label.grid(row=2, column=0, padx=10, pady=5)
doctor_password_entry.grid(row=2, column=1, padx=10, pady=5)
doctor_login_button.grid(row=3, column=0, columnspan=2, pady=10)

# Calculate center coordinates for frames
student_frame.place(relx=0.25, rely=0.5, anchor=tk.CENTER)
doctor_frame.place(relx=0.75, rely=0.5, anchor=tk.CENTER)

# Run the login GUI
main_window.mainloop()

# Close database connection
conn.close()