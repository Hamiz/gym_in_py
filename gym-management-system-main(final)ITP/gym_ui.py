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

    def view_attendance(self, date):
        cursor = self.db_connection.cursor()
        query = "SELECT member_id FROM attendance WHERE date = %s"
        data = (date,)
        cursor.execute(query, data)
        attendance = cursor.fetchall()
        cursor.close()
        return [member_id[0] for member_id in attendance]

    def __del__(self):
        if self.db_connection.is_connected():
            self.db_connection.close()

class GymManagementUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gym Management System")
        self.gym_system = GymManagementSystem()

        self.root.configure(bg="#f0f0f0")  

        self.create_ui()

    def create_ui(self):
        label = tk.Label(self.root, text="welcomme To Our Gym", font=("Palatino", 26, "bold"), bg="#f0f0f0")
        label.pack(pady=10)
        label = tk.Label(self.root, text="Change your body not because you hate it, because you love it.", font=("Palatino", 26, "bold"), bg="#f0f0f0")
        label.pack(pady=10)
        label = tk.Label(self.root, text="Gym Management System", font=("Palatino", 32, "bold", "italic"), bg="#f0f0f0")
        label.pack(pady=10)

        buttons_frame = tk.Frame(self.root, bg="#f0f0f0")
        buttons_frame.pack()

        button_styles = {
            "bg": "#007ACC",
            "fg": "white",
            "font": ("Helvetica", 16, "bold"),
            "padx": 15,  
            "pady": 10,  
            "width": 20,
            "borderwidth": 2,  
            "relief": "raised",  
            "activebackground": "#005A9C",  
            "activeforeground": "white",  
        }


        add_member_button = tk.Button(buttons_frame, text="Add Member", command=self.add_member, **button_styles)
        add_member_button.pack(side="left", padx=20, pady=10)

        mark_attendance_button = tk.Button(buttons_frame, text="Mark Attendance", command=self.mark_attendance, **button_styles)
        mark_attendance_button.pack(side="left", padx=20, pady=10)

        view_members_button = tk.Button(buttons_frame, text="View Members", command=self.view_members, **button_styles)
        view_members_button.pack(side="left", padx=20, pady=10)

        view_attendance_button = tk.Button(buttons_frame, text="View Attendance", command=self.view_attendance, **button_styles)
        view_attendance_button.pack(side="left", padx=20, pady=10)

    def add_member(self):
        self.add_member_window = tk.Toplevel(self.root)
        self.add_member_window.title("Add Member")
        self.add_member_window.geometry("700x400") 

        form_frame = tk.Frame(self.add_member_window, bg="white")
        form_frame.pack(expand=True, fill="both")

        member_id_label = tk.Label(form_frame, text="Member ID:", font=("Helvetica", 14))
        member_id_label.pack(pady=10)

        self.member_id_entry = tk.Entry(form_frame, font=("Helvetica", 14))
        self.member_id_entry.pack()

        name_label = tk.Label(form_frame, text="Name:", font=("Helvetica", 14))
        name_label.pack(pady=10)

        self.name_entry = tk.Entry(form_frame, font=("Helvetica", 14))
        self.name_entry.pack()

        confirm_button = tk.Button(form_frame, text="Confirm", command=self.confirm_add_member, font=("Helvetica", 14), bg="#007ACC", fg="white")
        confirm_button.pack(pady=10)

        self.add_member_window.geometry(f"+{self.root.winfo_rootx() + 50}+{self.root.winfo_rooty() + 50}")

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
        self.mark_attendance_window.geometry("700x400")  

        form_frame = tk.Frame(self.mark_attendance_window, bg="white")
        form_frame.pack(expand=True, fill="both")

        member_id_label = tk.Label(form_frame, text="Member ID:", font=("Helvetica", 14))
        member_id_label.pack(pady=10)

        self.member_id_entry = tk.Entry(form_frame, font=("Helvetica", 14))
        self.member_id_entry.pack()

        date_label = tk.Label(form_frame, text="Date (YYYY-MM-DD):", font=("Helvetica", 14))
        date_label.pack(pady=10)

        self.date_entry = tk.Entry(form_frame, font=("Helvetica", 14))
        self.date_entry.pack()

        confirm_button = tk.Button(form_frame, text="Confirm", command=self.confirm_mark_attendance, font=("Helvetica", 14), bg="#007ACC", fg="white")
        confirm_button.pack(pady=20)

        self.mark_attendance_window.geometry(f"+{self.root.winfo_rootx() + 50}+{self.root.winfo_rooty() + 50}")

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

            members_window = tk.Toplevel(self.root)
            members_window.title("Members")
            members_window.geometry("900x700") 

            text_widget = tk.Text(members_window, font=("Helvetica", 14))
            text_widget.pack(padx=20, pady=20, expand=True, fill="both")

            text_widget.insert("1.0", member_list)

            text_widget.config(state="disabled")
        else:
            messagebox.showinfo("Members", "No members found.")


    def view_attendance(self):
        self.view_attendance_window = tk.Toplevel(self.root)
        self.view_attendance_window.title("View Attendance")
        self.view_attendance_window.geometry("700x400")  

        form_frame = tk.Frame(self.view_attendance_window, bg="white")
        form_frame.pack(expand=True, fill="both")

        member_id_label = tk.Label(form_frame, text="Enter Date:", font=("Helvetica", 14))
        member_id_label.pack(pady=10)

        self.member_id_entry = tk.Entry(form_frame, font=("Helvetica", 14))
        self.member_id_entry.pack()

        confirm_button = tk.Button(form_frame, text="Confirm", command=self.confirm_view_attendance, font=("Helvetica", 14), bg="#007ACC", fg="white")
        confirm_button.pack(pady=20)

        self.view_attendance_window.geometry(f"+{self.root.winfo_rootx() + 50}+{self.root.winfo_rooty() + 50}")


    def confirm_view_attendance(self):
        date = self.member_id_entry.get()
        if date:
            attendance = self.gym_system.view_attendance(date)
            if attendance:
                attendance_list = "\n".join([f"Member Id: {member_id}" for member_id in attendance])
                messagebox.showinfo("Attendance", f"Attendance for {date}:\n{attendance_list}")
            else:
                messagebox.showinfo("Attendance", f"No attendance records found for {date}.")
        else:
            messagebox.showerror("Error", "Please enter a valid date.")

def main():
    root = tk.Tk()
    app = GymManagementUI(root)
    root.geometry("1280x960")
    root.mainloop()

if __name__ == "__main__":
    main()
