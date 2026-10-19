
import mysql.connector
from mysql.connector import Error

# XAMPP MySQL settings
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""  # Default XAMPP password is usually empty
DB_NAME = "jechelle_db"


def connect_server():
    """Connect to MySQL without selecting a database."""
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )


def connect_db():
    """Connect directly to the Jechelle database."""
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


def initialize_database():
    """Create database and tables automatically."""
    connection = None
    cursor = None

    try:
        connection = connect_server()
        cursor = connection.cursor()

        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`"
            " CHARACTER SET utf8mb4"
            " COLLATE utf8mb4_unicode_ci"
        )

        print(f"Database '{DB_NAME}' is ready.")

        cursor.execute(f"USE `{DB_NAME}`")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                email VARCHAR(150) NOT NULL UNIQUE,
                course VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subjects (
                id INT AUTO_INCREMENT PRIMARY KEY,
                subject_code VARCHAR(30) NOT NULL UNIQUE,
                subject_name VARCHAR(150) NOT NULL,
                units INT NOT NULL DEFAULT 3
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enrollments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                subject_id INT NOT NULL,
                enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE KEY unique_enrollment (student_id, subject_id),
                FOREIGN KEY (student_id)
                    REFERENCES students(id) ON DELETE CASCADE,
                FOREIGN KEY (subject_id)
                    REFERENCES subjects(id) ON DELETE CASCADE
            )
        """)

        connection.commit()
        print("Tables created successfully!")

    except Error as error:
        print("Database error:", error)

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def add_student(first_name, last_name, email, course):
    """Insert a student and return the new ID."""
    connection = None
    cursor = None

    try:
        connection = connect_db()
        cursor = connection.cursor()

        sql = """
            INSERT INTO students
                (first_name, last_name, email, course)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            sql, (first_name, last_name, email, course)
        )
        connection.commit()

        print("Student added successfully!")
        return cursor.lastrowid

    except Error as error:
        if connection and connection.is_connected():
            connection.rollback()
        print("Could not add student:", error)
        return None

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def get_students():
    """Retrieve all students."""
    connection = None
    cursor = None

    try:
        connection = connect_db()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM students ORDER BY id DESC")
        return cursor.fetchall()

    except Error as error:
        print("Could not retrieve students:", error)
        return []

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def delete_student(student_id):
    """Delete a student by ID."""
    connection = None
    cursor = None

    try:
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM students WHERE id = %s",
            (student_id,)
        )
        connection.commit()

        return cursor.rowcount > 0

    except Error as error:
        if connection and connection.is_connected():
            connection.rollback()
        print("Could not delete student:", error)
        return False

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    initialize_database()
