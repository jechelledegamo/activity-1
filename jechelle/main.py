
from database import (
    initialize_database,
    add_student,
    get_students,
    delete_student,
)


def main():
    initialize_database()

    while True:
        print("\n===== JECHELLE STUDENT DATABASE =====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Delete Student")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            first_name = input("First name: ").strip()
            last_name = input("Last name: ").strip()
            email = input("Email: ").strip()
            course = input("Course: ").strip()

            if not all([first_name, last_name, email, course]):
                print("Error: All fields are required.")
                continue

            try:
                student_id = add_student(
                    first_name, last_name, email, course
                )
                print(f"Student added! ID: {student_id}")
            except Exception as error:
                print(f"Could not add student: {error}")

        elif choice == "2":
            students = get_students()

            if not students:
                print("No students found.")
            else:
                for student in students:
                    print(
                        f"ID: {student['id']} | "
                        f"Name: {student['first_name']} "
                        f"{student['last_name']} | "
                        f"Email: {student['email']} | "
                        f"Course: {student['course']}"
                    )

        elif choice == "3":
            try:
                student_id = int(input("Enter student ID: "))
                if delete_student(student_id):
                    print("Student deleted successfully.")
                else:
                    print("Student ID not found.")
            except ValueError:
                print("Please enter a valid numeric ID.")

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
