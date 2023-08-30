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

        print("Members:")
        for member in members:
            print(f"Name: {member[2]}, Member ID: {member[1]}")

    def view_attendance(self, member_id):
        cursor = self.db_connection.cursor()
        query = "SELECT date FROM attendance WHERE member_id = %s"
        data = (member_id,)
        cursor.execute(query, data)
        attendance = cursor.fetchall()
        cursor.close()

        if attendance:
            member_name = self.members.get(member_id, "Member")
            print(f"Attendance for {member_name}:")
            for date in attendance:
                print(date[0])
        else:
            print("Member not found.")


    def __del__(self):
        if self.db_connection.is_connected():
            self.db_connection.close()

def main():
    gym_system = GymManagementSystem()

    while True:
        print("\nGym Management System")
        print("1. Add Member")
        print("2. Mark Attendance")
        print("3. View Members")
        print("4. View Attendance")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            member_id = input("Enter member ID: ")
            name = input("Enter member name: ")
            gym_system.add_member(member_id, name)
            print("Member added successfully.")

        elif choice == "2":
            member_id = input("Enter member ID: ")
            date = input("Enter date (YYYY-MM-DD): ")
            gym_system.mark_attendance(member_id, date)
            print("Attendance marked successfully.")

        elif choice == "3":
            gym_system.view_members()

        elif choice == "4":
            member_id = input("Enter member ID: ")
            gym_system.view_attendance(member_id)

        elif choice == "5":
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
 