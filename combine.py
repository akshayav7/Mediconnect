import tkinter as tk
from tkinter import messagebox
import mysql.connector

class NotificationPage:
    def __init__(self, notifications_window):
        self.notifications_window = notifications_window
        self.notifications_window.title("Notifications")
        self.notifications_window.config(bg="#ADD8E6")  # Set background color to light blue
        self.notifications_window.iconbitmap(r"C:\Users\aksha\Downloads\mediconect.ico")

        self.display_notifications(notifications_window)
      
        #back_button = tk.Button(self.root, text="Back", command=lambda :go_back_to_options(notifications_window))
        #back_button.pack(side="top",padx=8, pady=(10,5))
    def remove_notification(self, frame):
        frame.destroy()

    def display_notifications(self,notifications_window):
        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Akshaya@2005",
            database="wise"
        )
        cursor = conn.cursor()

        # Fetch data from the medicine_requests table
        cursor.execute("SELECT provider_name, provider_hostel, provider_phone_number, medicine_requested, requester_name, requester_hostel, requester_room_no, requester_phone_number, place_to_meet FROM medicine_requests")
        notifications = cursor.fetchall()

        # Close the database connection
        conn.close()

        num_notifications = len(notifications)

        for notification in notifications:
            frame = tk.Frame(self.notifications_window, bd=2, relief="groove", bg="white")  # Set background color of boxes to white
            frame.pack(padx=10, pady=10)

            heading = f"{notification[0]} wants to give {notification[3]} to {notification[4]}"
            heading_label = tk.Label(frame, text=heading, font=("Helvetica", 12, "bold"), bg="white", fg="black")
            heading_label.pack(padx=5, pady=(5, 0))

            provider_frame = tk.Frame(frame, bg="#FFB6C1")  # Light salmon
            provider_frame.pack(padx=5, pady=5, fill="both", expand=True, side="left")

            requested_frame = tk.Frame(frame, bg="#87CEEB")  # Pale green
            requested_frame.pack(padx=5, pady=5, fill="both", expand=True, side="right")

            provider_details = f"Provider:\nName: {notification[0]}\nHostel: {notification[1]}\nPhone: {notification[2]}"
            provider_label = tk.Label(provider_frame, text=provider_details, bg="#FFB6C1", font=("Helvetica", 10), fg="black")
            provider_label.pack(padx=5, pady=5, anchor="w")

            requested_details = f"Requested by:\nName: {notification[4]}\nHostel: {notification[5]}\nRoom No: {notification[6]}\nPhone: {notification[7]}\nPlace to Meet: {notification[8]}"
            requested_label = tk.Label(requested_frame, text=requested_details, bg="#87CEEB", font=("Helvetica", 10), fg="black")
            requested_label.pack(padx=5, pady=5, anchor="w")

            cancel_button = tk.Button(frame, text="Cancel", command=lambda f=frame: self.remove_notification(f), width=15)
            cancel_button.pack(padx=5, pady=10)
            
            #back_button = tk.Button(frame, text="Back", command=lambda :go_back_to_options(notifications_window))
            #back_button.pack(side="top",padx=8, pady=(10,5))

        # Center the window on the screen
        window_width = 1000
        window_height = 1000
        screen_width = self.notifications_window.winfo_screenwidth()
        screen_height = self.notifications_window.winfo_screenheight()
        x_coordinate = (screen_width - window_width) / 2
        y_coordinate = (screen_height - window_height) / 2
        self.notifications_window.geometry(f"{window_width}x{window_height}+{int(x_coordinate)}+{int(y_coordinate)}")
        
def open_notifications_page(medicine_window):
    medicine_window.withdraw()
    notifications_window = tk.Toplevel()
    notifications_window.attributes('-fullscreen', True)
    back_button = tk.Button(notifications_window, text="Back", command=lambda: go_back_to_notioptions(notifications_window,medicine_window))
    back_button.pack(side="top",padx=8, pady=(10,5))
    NotificationPage(notifications_window)
    
def go_back_to_notioptions(window,medicine_window):
    window.destroy()
    medicine_window.deiconify()
    
class MedicineRequest:
    def __init__(self, name, hostel, room_no, phone_number, medicine):
        self.name = name
        self.hostel = hostel
        self.room_no = room_no
        self.phone_number = phone_number
        self.medicine = medicine

def fetch_accepted_requests_from_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Akshaya@2005",
        database="wise"
    )
    cursor = conn.cursor()

    cursor.execute("SELECT name, hostel_name, hostel_number, phone_number, medicine_required FROM medicine_details WHERE status = 'accepted'")
    accepted_requests = cursor.fetchall()

    conn.close()
    return accepted_requests

def submit_givemedicine_details(name_entry, hostel_entry, phone_entry, place_to_meet_entry, request):
    provider_name = name_entry.get()
    provider_hostel = hostel_entry.get()
    provider_phone = phone_entry.get()
    place_to_meet = place_to_meet_entry.get()

    # Validate if all fields are filled
    if not (provider_name and provider_hostel and provider_phone and place_to_meet):
        messagebox.showerror("Error", "Please fill in all the details.")
    else:
        # Perform the action (e.g., submit details to the database)
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Akshaya@2005",
            database="wise"
        )
        cursor = conn.cursor()

        # Construct the SQL query to insert details of both requester and provider
        query = "INSERT INTO medicine_requests (requester_name, requester_hostel, requester_room_no, requester_phone_number, medicine_requested, provider_name, provider_hostel, provider_phone_number,place_to_meet, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
        values = (request.name, request.hostel, request.room_no, request.phone_number, request.medicine, provider_name, provider_hostel, provider_phone,place_to_meet, 'accepted')

        try:
            cursor.execute(query, values)
            
            # Update the status of the corresponding request to 'submitted'
            update_query = "UPDATE medicine_details SET status = 'submitted' WHERE name = %s AND hostel_name = %s AND phone_number = %s"
            cursor.execute(update_query, (request.name, request.hostel, request.phone_number))
            
            conn.commit()
            messagebox.showinfo("Submitted", "Your details have been submitted successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            conn.rollback()
            messagebox.showerror("Error", "Failed to submit details.")

        conn.close()

def show_accepted_request_details(request, frame,give_medicine_window):
    
    frame.pack_forget()  # Hide the main frame
    details_frame = tk.Frame(give_medicine_window, padx=20, pady=20)
    details_frame.pack()

    tk.Label(details_frame, text="Name:").grid(row=0, column=0, sticky="e")
    tk.Label(details_frame, text=request.name).grid(row=0, column=1, sticky="w")

    tk.Label(details_frame, text="Hostel:").grid(row=1, column=0, sticky="e")
    tk.Label(details_frame, text=request.hostel).grid(row=1, column=1, sticky="w")

    tk.Label(details_frame, text="Room No:").grid(row=2, column=0, sticky="e")
    tk.Label(details_frame, text=request.room_no).grid(row=2, column=1, sticky="w")

    tk.Label(details_frame, text="Phone Number:").grid(row=3, column=0, sticky="e")
    tk.Label(details_frame, text=request.phone_number).grid(row=3, column=1, sticky="w")

    tk.Label(details_frame, text="Medicine Requested:").grid(row=4, column=0, sticky="e")
    tk.Label(details_frame, text=request.medicine).grid(row=4, column=1, sticky="w")

    tk.Label(details_frame, text="Your Name:").grid(row=5, column=0, sticky="e")
    name_entry = tk.Entry(details_frame)
    name_entry.grid(row=5, column=1, sticky="w")

    tk.Label(details_frame, text="Hostel:").grid(row=6, column=0, sticky="e")
    hostel_entry = tk.Entry(details_frame)
    hostel_entry.grid(row=6, column=1, sticky="w")

    tk.Label(details_frame, text="Phone Number:").grid(row=7, column=0, sticky="e")
    phone_entry = tk.Entry(details_frame)
    phone_entry.grid(row=7, column=1, sticky="w")

    tk.Label(details_frame, text="Place to Meet:").grid(row=8, column=0, sticky="e")
    place_to_meet_entry = tk.Entry(details_frame)
    place_to_meet_entry.grid(row=8, column=1, sticky="w")

    submit_button = tk.Button(details_frame, text="Submit", command=lambda: submit_givemedicine_details(name_entry, hostel_entry, phone_entry, place_to_meet_entry, request))
    submit_button.grid(row=9, columnspan=2, pady=10)

    back_button = tk.Button(details_frame, text="Back", command=lambda: [details_frame.pack_forget(), frame.pack()])
    back_button.grid(row=10, columnspan=2, pady=10, sticky="s")

def open_give_medicine_window(medicine_window):
    
    medicine_window.withdraw()
    give_medicine_window = tk.Toplevel()
    give_medicine_window.attributes('-fullscreen', True)
    give_medicine_window.title("Give Medicine")
    give_medicine_window.geometry("1000x1000")
    give_medicine_window.iconbitmap(r"C:\Users\aksha\Downloads\mediconect.ico")


    requests_frame = tk.Frame(give_medicine_window)
    requests_frame.pack(pady=20)

    accepted_requests = fetch_accepted_requests_from_database()

    for request in accepted_requests:
        student_name, hostel, room_no, phone_number, medicine_needed = request
        student = MedicineRequest(student_name, hostel, room_no, phone_number, medicine_needed)
        student.frame = requests_frame

        request_button = tk.Button(requests_frame, text=f"Request: {student.name} - {student.medicine}",
                                   command=lambda r=student: show_accepted_request_details(r, requests_frame,give_medicine_window),
                                   bg="lightblue", width=60, height=4)
        request_button.pack(pady=5)

    #back_button = tk.Button(requests_frame, text="Back", command=go_back_to_giveoptions(give_medicine_window,medicine_window))
    back_button = tk.Button(requests_frame, text="Back", command=lambda: go_back_to_giveoptions(give_medicine_window, medicine_window))

    back_button.pack(pady=10, anchor="s")

    give_medicine_window.mainloop()
    
def go_back_to_giveoptions(window,medicine_window):
    window.destroy()
    medicine_window.deiconify()
    
    
class MessageHistory:
    def __init__(self):
        self.accepted_messages = []
        self.rejected_messages = []

    def add_accepted_message(self, message):
        self.accepted_messages.append(message)

    def add_rejected_message(self, message):
        self.rejected_messages.append(message)

    def get_accepted_messages(self):
        return self.accepted_messages

    def get_rejected_messages(self):
        return self.rejected_messages

class Student:
    def __init__(self, name, reg_number, medicine, frame):
        self.name = name
        self.reg_number = reg_number
        self.medicine = medicine
        self.message_history = MessageHistory()
        self.frame = frame

def fetch_pending_requests_from_database():
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Akshaya@2005",
        database="wise"
    )
    cursor = conn.cursor()

    # Fetch only pending medicine requests from the database that have not been accepted or rejected
    cursor.execute("SELECT name, reg_number, medicine_required FROM medicine_details WHERE status = 'pending'")
    pending_requests = cursor.fetchall()

    conn.close()
    return pending_requests 

def fetch_history_from_database(reg_number):
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Akshaya@2005",
        database="wise"
    )
    cursor = conn.cursor()

    # Fetch history of medicine requests for the student based on registration number
    cursor.execute("SELECT medicine_required, status, timestamp FROM medicine_details WHERE reg_number = %s", (reg_number,))
    history = cursor.fetchall()

    conn.close()
    return history

def show_message_box(student, frame):
    top = tk.Toplevel()
    top.title("Message Box")

    label = tk.Label(top, text=f"NAME: {student.name}\nMEDICINE NEEDED: {student.medicine}", font=('Helvetica', 16))
    label.pack(padx=10, pady=10)

    frame_content = tk.Frame(top)
    frame_content.pack(pady=5)

    accept_button = tk.Button(frame_content, text="Accept", command=lambda: on_accept(student, top, frame), bg='lightgreen', width=10)
    accept_button.pack(side='left', padx=(5, 2), pady=10)

    reject_button = tk.Button(frame_content, text="Reject", command=lambda: on_reject(student, top, frame), bg='lightcoral', width=10)
    reject_button.pack(side='left', padx=(2, 5), pady=10)

def on_accept(student, top, frame):
    # Update the status of the request in the database to 'accepted'
    update_request_status(student.reg_number, 'accepted', student.medicine)

    message = f"Accepted: {student.name}'s medicine - {student.medicine}"
    student.message_history.add_accepted_message(message)
    top.destroy()
    frame.destroy()  # Destroy the frame after clicking accept

def on_reject(student, top, frame):
    # Update the status of the request in the database to 'rejected'
    update_request_status(student.reg_number, 'rejected', student.medicine)

    message = f"Rejected: {student.name}'s medicine - {student.medicine}"
    student.message_history.add_rejected_message(message)
    top.destroy()
    frame.destroy()  # Destroy the frame after clicking reject

def update_request_status(reg_number, status, medicine):
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Akshaya@2005",
        database="wise"
    )
    cursor = conn.cursor()

    # Update the status of the specific medicine request for the student in the database
    cursor.execute("UPDATE medicine_details SET status = %s WHERE reg_number = %s AND medicine_required = %s", (status, reg_number, medicine))

    conn.commit()
    conn.close()

def display_history(student):
    history = fetch_history_from_database(student.reg_number)
    history_text = ""
    for medicine, status, timestamp in history:
        history_text += f"Medicine Requested: {medicine}, Status: {status}, Timestamp: {timestamp}\n"
        
    messagebox.showinfo(f"{student.name}'s Medicine Request History", history_text)
    
    
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
    elif len(phone_number) < 10 or len(phone_number) > 10 :
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

# Function for going back to the previous window


# Function for opening the "Need Medicine" window
def open_need_medicine_window(medicine_window):
    medicine_window.withdraw()

    need_medicine_window = tk.Toplevel()
    need_medicine_window.attributes('-fullscreen', True)
    need_medicine_window.title("Need Medicine")
    need_medicine_window.geometry("1000x1000")
    need_medicine_window.configure(bg='lightblue')
    need_medicine_window.iconbitmap(r"C:\Users\aksha\Downloads\mediconect.ico")

    # Entry fields for medicine details
    medicine_label = tk.Label(need_medicine_window, text="Medicine Required:")
    medicine_label.pack(pady=5)
    global medicine_entry
    medicine_entry = tk.Entry(need_medicine_window)
    medicine_entry.pack(pady=5)

    name_label = tk.Label(need_medicine_window, text="Name:")
    name_label.pack(pady=5)
    global name_entry
    name_entry = tk.Entry(need_medicine_window)
    name_entry.pack(pady=5)

    reg_label = tk.Label(need_medicine_window, text="Registration Number:")
    reg_label.pack(pady=5)
    global reg_entry
    reg_entry = tk.Entry(need_medicine_window)
    reg_entry.pack(pady=5)

    hostel_name_label = tk.Label(need_medicine_window, text="Hostel Name:")
    hostel_name_label.pack(pady=5)
    global hostel_name_entry
    hostel_name_entry = tk.Entry(need_medicine_window)
    hostel_name_entry.pack(pady=5)

    hostel_number_label = tk.Label(need_medicine_window, text="Room Number:")
    hostel_number_label.pack(pady=5)
    global hostel_number_entry
    hostel_number_entry = tk.Entry(need_medicine_window)
    hostel_number_entry.pack(pady=5)

    phone_label = tk.Label(need_medicine_window, text="Phone Number:")
    phone_label.pack(pady=5)
    global phone_entry
    phone_entry = tk.Entry(need_medicine_window)
    phone_entry.pack(pady=5)

    # Submit button
    submit_button = tk.Button(need_medicine_window, text="Submit", command=submit_details)
    submit_button.pack(pady=10)

    # Back button
    back_button = tk.Button(need_medicine_window, text="Back", command=lambda: go_back_to_options(need_medicine_window,medicine_window))
    back_button.pack(pady=10)

    need_medicine_window.mainloop()

# Function for going back to the Medicine Options page from the Need Medicine page
def go_back_to_options(window,medicine_window):
    window.destroy()
    medicine_window.deiconify()
def main():
    #def logout():
        #main_window.destroy()
        #main_window.deiconify()

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
            open_doctor_page()  # Open doctor's page
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def open_medicine_options():
        main_window.withdraw()

        medicine_window = tk.Toplevel()
        medicine_window.attributes('-fullscreen', True)
        medicine_window.title("Medicine Options")
        medicine_window.geometry("1000x1000")
        medicine_window.configure(bg='lightblue')
        medicine_window.iconbitmap(r"C:\Users\aksha\Downloads\mediconect.ico")
        need_med_button = tk.Button(medicine_window, text="Need a Medicine", font=("times new roman", 12),
                                    command=lambda :open_need_medicine_window(medicine_window))
        give_med_button = tk.Button(medicine_window, text="Give a Medicine", font=("times new roman", 12),
                                    command=lambda: open_give_medicine_window(medicine_window))
        notifications_button = tk.Button(medicine_window, text="Notifications", font=("times new roman", 12),
                                         command=lambda: open_notifications_page(medicine_window))
        back_button = tk.Button(medicine_window, text="Logout", font=("times new roman", 12),
                                command=lambda: go_back(medicine_window))
        back_button.place(relx=0.1, rely=0.9, anchor="center")

        need_med_button.pack(pady=20)
        give_med_button.pack(pady=20)
        notifications_button.pack(pady=20)
        # back_button.pack(pady=20)

        medicine_window.mainloop()

    def open_signup_window():
        main_window.withdraw()

        signup_window = tk.Toplevel()
        signup_window.attributes('-fullscreen', True)
        signup_window.title("Sign Up")
        signup_window.geometry("1000x1000")

        signup_window.configure(bg='lightblue')
        signup_window.iconbitmap(r"C:\Users\aksha\Downloads\mediconect.ico")

        label_padding_y = (2, 5)
        label_width = 18
        labels = [
            ("Name:", 0), ("Registration Number:", 1), ("Branch:", 2), ("Hostel Name:", 3),
            ("Hostel Room No:", 4), ("Username:", 5), ("New Password:", 6), ("Confirm Password:", 7)
        ]
        for label_text, row in labels:
            label = tk.Label(signup_window, text=label_text)
            label.place(relx=0.3, rely=0.1 + row * 0.075, anchor="center")
            label.config(width=label_width, anchor="e")

        entry_padding_y = (2, 5)
        entry_width = 20
        entry_fields = [
            ("name_entry", 0), ("reg_number_entry", 1), ("branch_entry", 2), ("hostel_name_entry", 3),
            ("room_number_entry", 4), ("username_entry", 5), ("password_entry", 6), ("confirm_password_entry", 7)
        ]
        for entry_field, row in entry_fields:
            entry = tk.Entry(signup_window)
            entry.place(relx=0.7, rely=0.1 + row * 0.075, anchor="center")
            entry.config(width=entry_width)
            globals()[entry_field] = entry

        register_button = tk.Button(signup_window, text="Register", command=register)
        register_button.place(relx=0.5, rely=0.9, anchor="center")

        back_button = tk.Button(signup_window, text="Back", command=lambda: go_back(signup_window))
        back_button.place(relx=0.1, rely=0.9, anchor="center")

        signup_window.mainloop()

    def register():
        name = name_entry.get()
        reg_number = reg_number_entry.get()
        branch = branch_entry.get()
        hostel_name = hostel_name_entry.get()
        room_number = room_number_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        if not all([name, reg_number, branch, hostel_name, room_number, username, password, confirm_password]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='wise',
                                                 user='root',
                                                 password='Akshaya@2005')
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO registration (name, registration_number, branch, hostel_name, room_number, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (name, reg_number, branch, hostel_name, room_number, username, password))
                connection.commit()
                messagebox.showinfo("Success", "Registration successful!")
                cursor.close()
        except mysql.connector.Error as e:
            print("Error while connecting to MySQL", e)
            messagebox.showerror("Error", "Failed to connect to database")
        finally:
            if 'connection' in locals() and connection.is_connected():
                connection.close()
                print("MySQL connection is closed")

    def go_back(window):
        window.destroy()
        main_window.deiconify()

    def open_doctor_page():
        main_window.withdraw()

        # Code for opening doctor's page goes here
        doctor_window = tk.Toplevel()
        doctor_window.attributes('-fullscreen', True)
        doctor_window.title("Doctor Page")
        doctor_window.geometry("1000x1000")
        doctor_window.iconbitmap(r"C:\Users\aksha\Downloads\mediconect.ico")

        # Heading for the message boxes
        heading_label = tk.Label(doctor_window, text="Student Requests", font=('Helvetica', 20, 'bold'))
        heading_label.pack(pady=10)

        pending_requests = fetch_pending_requests_from_database()

        for request in pending_requests:
            student_name, reg_number, medicine_needed = request
            student_frame = tk.Frame(doctor_window)
            student = Student(student_name, reg_number, medicine_needed, student_frame)
            student_frame.pack(pady=10, anchor="center")

            button = tk.Button(student_frame, text=f"NAME: {student.name}\nMEDICINE NEEDED: {student.medicine}",
                           command=lambda s=student, f=student_frame: show_message_box(s, f),
                           bg='lightblue', width=60, height=6, wraplength=400)
            button.pack()

            history_button = tk.Button(student_frame, text="History", command=lambda s=student: display_history(s), bg='lightyellow', width=10)
            history_button.pack()

        back_button = tk.Button(doctor_window, text="Logout", font=("times new roman", 12),
                                command=lambda: go_back(doctor_window))
        back_button.pack(pady=20)

        doctor_window.mainloop()

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Akshaya@2005",
        database="wise"
    )
    cursor = conn.cursor()

    main_window = tk.Tk()
    main_window.title("Login Portal")
    main_window.attributes('-fullscreen', True)
    main_window.iconbitmap(r"C:\Users\aksha\Downloads\mediconect.ico")

    screen_width = main_window.winfo_screenwidth()
    screen_height = main_window.winfo_screenheight()
    window_width = 1000
    window_height = 1000
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    main_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    main_window.configure(bg='lightblue')

    student_frame = tk.Frame(main_window, bg='steelblue', padx=20, pady=20)
    student_heading_label = tk.Label(student_frame, text="Student Login", font=("times new roman", 16, "bold"))
    student_username_label = tk.Label(student_frame, text="Username:")
    student_username_entry = tk.Entry(student_frame)
    student_password_label = tk.Label(student_frame, text="Password:")
    student_password_entry = tk.Entry(student_frame, show='*')
    student_login_button = tk.Button(student_frame, text="Login", bg='lightblue', command=student_login)  # Changed color
    signup_button = tk.Button(student_frame, text="Sign Up", bg='lightblue', command=open_signup_window)  # Changed color

    student_heading_label.grid(row=0, column=0, columnspan=2, pady=10)
    student_username_label.grid(row=1, column=0, padx=10, pady=5)
    student_username_entry.grid(row=1, column=1, padx=10, pady=5)
    student_password_label.grid(row=2, column=0, padx=10, pady=5)
    student_password_entry.grid(row=2, column=1, padx=10, pady=5)
    student_login_button.grid(row=3, column=0, pady=10)
    signup_button.grid(row=3, column=1, pady=10)

    doctor_frame = tk.Frame(main_window, bg='steelblue', padx=20, pady=20)
    doctor_heading_label = tk.Label(doctor_frame, text="Doctor Login", font=("times new roman", 16, "bold"))
    doctor_username_label = tk.Label(doctor_frame, text="Username:")
    doctor_username_entry = tk.Entry(doctor_frame)
    doctor_password_label = tk.Label(doctor_frame, text="Password:")
    doctor_password_entry = tk.Entry(doctor_frame, show='*')
    doctor_login_button = tk.Button(doctor_frame, text="Login", bg='lightblue', command=doctor_login)  # Changed color

    doctor_heading_label.grid(row=0, column=0, columnspan=2, pady=10)
    doctor_username_label.grid(row=1, column=0, padx=10, pady=5)
    doctor_username_entry.grid(row=1, column=1, padx=10, pady=5)
    doctor_password_label.grid(row=2, column=0, padx=10, pady=5)
    doctor_password_entry.grid(row=2, column=1, padx=10, pady=5)
    doctor_login_button.grid(row=3, column=0, columnspan=2, pady=10)

    student_frame.place(relx=0.25, rely=0.5, anchor=tk.CENTER)
    doctor_frame.place(relx=0.75, rely=0.5, anchor=tk.CENTER)

    main_window.mainloop()

    conn.close()

if __name__ == "__main__":
    main()
