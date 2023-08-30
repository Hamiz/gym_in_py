import tkinter as tk
from tkinter import messagebox
import mysql.connector

class GymManagementSystem:
    def __init__(self):
        self.db_connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="haier12345",
            database="gym_management"
        )
        self.members = {}
        self.attendance = {}

    def add_member(self, member_id, name):
        cursor = self.db_connection.cursor()
        query = "INSERT INTO members (member_id, name) VALUES (%s, %s)"
        data = (member_id, name)
        cursor.execute(query, data)
        self.db_connection.commit()
        cursor.close()

    def mark_attendance(self, member_id, date):
        cursor = self.db_connection.cursor()
        query = "INSERT INTO attendance (member_id, date) VALUES (%s, %s)"
        data = (member_id, date)
        cursor.execute(query, data)
        self.db_connection.commit()
        cursor.close()

    def view_members(self):
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM members"
        cursor.execute(query)
        members = cursor.fetchall()
        cursor.close()
        return members

    def view_attendance(self, member_id):
        cursor = self.db_connection.cursor()
        query = "SELECT date FROM attendance WHERE member_id = %s"
        data = (member_id,)
        cursor.execute(query, data)
        attendance = cursor.fetchall()
        cursor.close()
        return [date[0] for date in attendance]

    def __del__(self):
        if self.db_connection.is_connected():
            self.db_connection.close()

class GymManagementUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gym Management System")
        self.gym_system = GymManagementSystem()

        self.create_ui()

    def create_ui(self):
        label = tk.Label(self.root, text="Gym Management System")
        label.pack(pady=10)

        add_member_button = tk.Button(self.root, text="Add Member", command=self.add_member)
        add_member_button.pack()

        mark_attendance_button = tk.Button(self.root, text="Mark Attendance", command=self.mark_attendance)
        mark_attendance_button.pack()

        view_members_button = tk.Button(self.root, text="View Members", command=self.view_members)
        view_members_button.pack()

        view_attendance_button = tk.Button(self.root, text="View Attendance", command=self.view_attendance)
        view_attendance_button.pack()

    def add_member(self):
        self.add_member_window = tk.Toplevel(self.root)
        self.add_member_window.title("Add Member")

        member_id_label = tk.Label(self.add_member_window, text="Member ID:")
        member_id_label.pack()
        self.member_id_entry = tk.Entry(self.add_member_window)
        self.member_id_entry.pack()

        name_label = tk.Label(self.add_member_window, text="Name:")
        name_label.pack()
        self.name_entry = tk.Entry(self.add_member_window)
        self.name_entry.pack()

        confirm_button = tk.Button(self.add_member_window, text="Confirm", command=self.confirm_add_member)
        confirm_button.pack()

    def confirm_add_member(self):
        member_id = self.member_id_entry.get()
        name = self.name_entry.get()

        if member_id and name:
            self.gym_system.add_member(member_id, name)
            messagebox.showinfo("Success", "Member added successfully.")
            self.add_member_window.destroy()
        else:
            messagebox.showerror("Error", "Please enter valid information.")

    def mark_attendance(self):
        self.mark_attendance_window = tk.Toplevel(self.root)
        self.mark_attendance_window.title("Mark Attendance")

        member_id_label = tk.Label(self.mark_attendance_window, text="Member ID:")
        member_id_label.pack()
        self.member_id_entry = tk.Entry(self.mark_attendance_window)
        self.member_id_entry.pack()

        date_label = tk.Label(self.mark_attendance_window, text="Date (YYYY-MM-DD):")
        date_label.pack()
        self.date_entry = tk.Entry(self.mark_attendance_window)
        self.date_entry.pack()

        confirm_button = tk.Button(self.mark_attendance_window, text="Confirm", command=self.confirm_mark_attendance)
        confirm_button.pack()

    def confirm_mark_attendance(self):
        member_id = self.member_id_entry.get()
        date = self.date_entry.get()

        if member_id and date:
            self.gym_system.mark_attendance(member_id, date)
            messagebox.showinfo("Success", "Attendance marked successfully.")
            self.mark_attendance_window.destroy()
        else:
            messagebox.showerror("Error", "Please enter valid information.")

    def view_members(self):
        members = self.gym_system.view_members()
        if members:
            member_list = "\n".join([f"Name: {member[2]}, Member ID: {member[1]}" for member in members])
            messagebox.showinfo("Members", member_list)
        else:
            messagebox.showinfo("Members", "No members found.")

    def view_attendance(self):
        self.view_attendance_window = tk.Toplevel(self.root)
        self.view_attendance_window.title("View Attendance")

        member_id_label = tk.Label(self.view_attendance_window, text="Member ID:")
        member_id_label.pack()
        self.member_id_entry = tk.Entry(self.view_attendance_window)
        self.member_id_entry.pack()

        confirm_button = tk.Button(self.view_attendance_window, text="Confirm", command=self.confirm_view_attendance)
        confirm_button.pack()

    def confirm_view_attendance(self):
        member_id = self.member_id_entry.get()

        if member_id:
            attendance = self.gym_system.view_attendance(member_id)
            if attendance:
                attendance_list = "\n".join([f"Date: {date}" for date in attendance])
                messagebox.showinfo("Attendance", f"Attendance for {member_id}:\n{attendance_list}")
            else:
                messagebox.showinfo("Attendance", f"No attendance records found for {member_id}.")
        else:
            messagebox.showerror("Error", "Please enter valid information.")

def main():
    root = tk.Tk()
    app = GymManagementUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
