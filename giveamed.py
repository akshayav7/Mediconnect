import tkinter as tk
import mysql.connector
from tkinter import messagebox

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

def submit_details(name_entry, hostel_entry, phone_entry, place_to_meet_entry, request):
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

def show_accepted_request_details(request, frame):
    frame.pack_forget()  # Hide the main frame
    details_frame = tk.Frame(root, padx=20, pady=20)
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

    submit_button = tk.Button(details_frame, text="Submit", command=lambda: submit_details(name_entry, hostel_entry, phone_entry, place_to_meet_entry, request))
    submit_button.grid(row=9, columnspan=2, pady=10)

    back_button = tk.Button(details_frame, text="Back", command=lambda: [details_frame.pack_forget(), frame.pack()])
    back_button.grid(row=10, columnspan=2, pady=10, sticky="s")

def main():
    global root
    root = tk.Tk()
    root.title("Give Medicine")

    requests_frame = tk.Frame(root)
    requests_frame.pack(pady=20)

    accepted_requests = fetch_accepted_requests_from_database()

    for request in accepted_requests:
        student_name, hostel, room_no, phone_number, medicine_needed = request
        student = MedicineRequest(student_name, hostel, room_no, phone_number, medicine_needed)
        student.frame = requests_frame

        request_button = tk.Button(requests_frame, text=f"Request: {student.name} - {student.medicine}",
                                   command=lambda r=student: show_accepted_request_details(r, requests_frame),
                                   bg="lightblue", width=60, height=4)
        request_button.pack(pady=5)

    back_button = tk.Button(requests_frame, text="Back", command=root.quit)
    back_button.pack(pady=10, anchor="s")

    root.mainloop()

if __name__ == "__main__":
    main()