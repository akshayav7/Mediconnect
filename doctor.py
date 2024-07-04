import tkinter as tk
from tkinter import messagebox
import mysql.connector

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

def main():
    root = tk.Tk()

    # Setting the window icon
    root.iconbitmap(r"C:\Users\aksha\Downloads\mediconect.ico")  # Replace 'icon.ico' with the path to your icon file
    window_width = 1000
    window_height = 1000
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    root.title("Student Requests")

    # Heading for the message boxes
    heading_label = tk.Label(root, text="Messages", font=('Helvetica', 20, 'bold'))
    heading_label.pack(pady=10)

    pending_requests = fetch_pending_requests_from_database()

    for request in pending_requests:
        student_name, reg_number, medicine_needed = request
        student_frame = tk.Frame(root)
        student = Student(student_name, reg_number, medicine_needed, student_frame)
        student_frame.pack(pady=10, anchor="center")

        button = tk.Button(student_frame, text=f"NAME: {student.name}\nMEDICINE NEEDED: {student.medicine}",
                           command=lambda s=student, f=student_frame: show_message_box(s, f),
                           bg='lightblue', width=60, height=6, wraplength=400)
        button.pack()

        history_button = tk.Button(student_frame, text="History", command=lambda s=student: display_history(s), bg='lightyellow', width=10)
        history_button.pack()

    # Back button
    back_button = tk.Button(root, text="Logout", command=root.quit)
    back_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
