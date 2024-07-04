import tkinter as tk
import mysql.connector

class NotificationPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Notifications")
        self.root.config(bg="#ADD8E6")  # Set background color to light blue
        self.root.iconbitmap(r"C:\Users\aksha\Downloads\mediconect.ico")


        self.display_notifications()

        self.back_button = tk.Button(self.root, text="Back", command=self.root.destroy)
        self.back_button.pack(side="top",padx=8, pady=(10,5))

    def remove_notification(self, frame):
        frame.destroy()

    def display_notifications(self):
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
            frame = tk.Frame(self.root, bd=2, relief="groove", bg="white")  # Set background color of boxes to white
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

        # Center the window on the screen
        window_width = 1000
        window_height = 1000
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = (screen_width - window_width) / 2
        y_coordinate = (screen_height - window_height) / 2
        self.root.geometry(f"{window_width}x{window_height}+{int(x_coordinate)}+{int(y_coordinate)}")

def main():
    root = tk.Tk()
    NotificationPage(root)
    root.mainloop() 

if __name__ == "__main__":
    main()