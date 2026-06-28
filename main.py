import mysql.connector
import sys
from io import StringIO
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Establishing a connection to MySQL database
def connect_to_database():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password=os.environ.get('DB_PASSWORD'),
        database="fee_management"
    )

# Function to create tables if they don't exist
def create_tables(cursor):
    students_table_query = """
    CREATE TABLE IF NOT EXISTS students (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        date_of_birth DATE,
        gender ENUM('Male', 'Female', 'Other'),
        roll_number VARCHAR(20) NOT NULL,
        class VARCHAR(20),
        address VARCHAR(255),
        phone_number VARCHAR(15),
        email VARCHAR(50),
        admission_date DATE,
        guardian_name VARCHAR(100),
        admission_number VARCHAR(50) UNIQUE
    )
    """
    payments_table_query = """
    CREATE TABLE IF NOT EXISTS payments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        admission_number VARCHAR(50),
        amount DECIMAL(10, 2) NOT NULL,
        payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        payment_method ENUM('Cash', 'Credit Card', 'Debit Card', 'Net Banking', 'Cheque'),
        FOREIGN KEY (admission_number) REFERENCES students(admission_number)
    )
    """
    cursor.execute(students_table_query)
    cursor.execute(payments_table_query)

# Function to add a new student
def add_new_student(cursor, first_name, last_name, date_of_birth, gender,
                    roll_number, class_name, address, phone_number, email,
                    admission_date, guardian_name, admission_number):
    query = """
    INSERT INTO students 
    (first_name, last_name, date_of_birth, gender, roll_number, class, 
    address, phone_number, email, admission_date, guardian_name, admission_number)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (first_name, last_name, date_of_birth, gender, roll_number,
              class_name, address, phone_number, email, admission_date,
              guardian_name, admission_number)
    cursor.execute(query, values)
    print("New student added successfully!")

# Function to edit student details
def edit_student_details(cursor, admission_number):
    query = "SELECT * FROM students WHERE admission_number = %s"
    cursor.execute(query, (admission_number,))
    student_data = cursor.fetchone()

    if student_data:
        print("Current Student Details:")
        print("1. First Name:", student_data[1])
        print("2. Last Name:", student_data[2])
        print("3. Date of Birth:", student_data[3])
        print("4. Gender:", student_data[4])
        print("5. Roll Number:", student_data[5])
        print("6. Class:", student_data[6])
        print("7. Address:", student_data[7])
        print("8. Phone Number:", student_data[8])
        print("9. Email:", student_data[9])
        print("10. Admission Date:", student_data[10])
        print("11. Guardian Name:", student_data[11])

        choice = input("Enter the number of the detail you want to edit (or '0' to cancel): ")

        field_map = {
            '1': ('first_name', "Enter new first name: "),
            '2': ('last_name', "Enter new last name: "),
            '3': ('date_of_birth', "Enter new date of birth (YYYY-MM-DD): "),
            '4': ('gender', "Enter new gender (Male/Female/Other): "),
            '5': ('roll_number', "Enter new roll number: "),
            '6': ('class', "Enter new class: "),
            '7': ('address', "Enter new address: "),
            '8': ('phone_number', "Enter new phone number: "),
            '9': ('email', "Enter new email: "),
            '10': ('admission_date', "Enter new admission date (YYYY-MM-DD): "),
            '11': ('guardian_name', "Enter new guardian name: "),
        }

        if choice in field_map:
            field, prompt = field_map[choice]
            new_value = input(prompt)
            update_query = f"UPDATE students SET {field} = %s WHERE admission_number = %s"
            cursor.execute(update_query, (new_value, admission_number))
            print(f"{field.replace('_', ' ').title()} updated successfully!")
        else:
            print("No changes made.")
    else:
        print("No student found for the given admission number.")

# Function to pay fees and generate receipt
def pay_fees(cursor, admission_number, amount):
    print("Payment Methods:")
    print("1. Cash")
    print("2. Credit Card")
    print("3. Debit Card")
    print("4. Net Banking")
    print("5. Cheque")

    payment_methods = {
        '1': 'Cash',
        '2': 'Credit Card',
        '3': 'Debit Card',
        '4': 'Net Banking',
        '5': 'Cheque'
    }

    while True:
        choice = input("Enter the number of the payment method: ")
        if choice in payment_methods:
            payment_method = payment_methods[choice]
            break
        else:
            print("Invalid choice. Please try again.")

    query = "INSERT INTO payments (admission_number, amount, payment_method) VALUES (%s, %s, %s)"
    cursor.execute(query, (admission_number, amount, payment_method))
    print("Fees paid successfully!")
    generate_receipt(cursor, admission_number, amount)

# Function to generate a receipt
def generate_receipt(cursor, admission_number, amount):
    query = "SELECT * FROM students WHERE admission_number = %s"
    cursor.execute(query, (admission_number,))
    student_data = cursor.fetchone()

    print("=" * 50)
    print("O.P. Jindal School")
    print("Kharsia Road, Raigarh")
    print("=" * 50)
    print("Receipt:")
    print(" ")
    print("Student Name:", student_data[1] + " " + student_data[2])
    print("Date of Birth:", student_data[3])
    print("Gender:", student_data[4])
    print("Roll Number:", student_data[5])
    print("Class:", student_data[6])
    print("Address:", student_data[7])
    print("Phone Number:", student_data[8])
    print("Email:", student_data[9])
    print("Admission Date:", student_data[10])
    print("Guardian Name:", student_data[11])
    print("Admission Number:", admission_number)
    print("Amount Paid:", amount)
    print("Payment Date:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("=" * 50)

# Function to print receipt by admission number and save as image
def print_receipt_by_admission(cursor, admission_number):
    query = "SELECT * FROM students WHERE admission_number = %s"
    cursor.execute(query, (admission_number,))
    student_data = cursor.fetchone()

    if student_data:
        output_buffer = StringIO()
        original_stdout = sys.stdout
        sys.stdout = output_buffer

        print("=" * 50)
        print("O.P. Jindal School")
        print("Kharsia Road, Raigarh")
        print("=" * 50)
        print("Receipt:")
        print(" ")
        print("Student Name:", student_data[1] + " " + student_data[2])
        print("Date of Birth:", student_data[3])
        print("Gender:", student_data[4])
        print("Roll Number:", student_data[5])
        print("Class:", student_data[6])
        print("Address:", student_data[7])
        print("Phone Number:", student_data[8])
        print("Email:", student_data[9])
        print("Admission Date:", student_data[10])
        print("Guardian Name:", student_data[11])
        print("Admission Number:", admission_number)

        payment_query = "SELECT amount, payment_date, payment_method FROM payments WHERE admission_number = %s"
        cursor.execute(payment_query, (admission_number,))
        payment_data = cursor.fetchall()

        if payment_data:
            print("\nPayments:")
            for index, payment in enumerate(payment_data, start=1):
                print(f"Installment {index}:")
                print("Amount Paid:", payment[0])
                print("Payment Date:", payment[1])
                print("Payment Method:", payment[2])
                print()
        else:
            print("\nNo payments found for the given admission number.")

        print("=" * 50)

        sys.stdout = original_stdout

        # Save receipt as image
        image = Image.new('RGB', (400, 1000), color='white')
        d = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        y = 10
        for line in output_buffer.getvalue().split('\n'):
            d.text((10, y), line, fill=(0, 0, 0), font=font)
            y += 15
        image.save(f'{admission_number}.png')
        print(f"Receipt saved as '{admission_number}.png'")
    else:
        print("No student found for the given admission number.")

# Function to view details of all students
def view_all_students_details(cursor):
    query = "SELECT * FROM students"
    cursor.execute(query)
    student_data = cursor.fetchall()

    if student_data:
        columns = ["ID", "First Name", "Last Name", "Date of Birth", "Gender",
                   "Roll Number", "Class", "Address", "Phone Number", "Email",
                   "Admission Date", "Guardian Name", "Admission Number"]
        df = pd.DataFrame(student_data, columns=columns)
        print(df)
    else:
        print("No students found.")

# Graph functions
def display_graph_menu():
    print("Graph Menu:")
    print("1. Bar Graph")
    print("2. Line Graph")
    print("3. Histogram")
    print("4. Back to Main Menu")

def generate_bar_graph(cursor):
    cursor.execute("""
        SELECT admission_number, SUM(amount) AS total_amount
        FROM payments
        GROUP BY admission_number
    """)
    rows = cursor.fetchall()
    if not rows:
        print("No payment data available.")
        return
    admission_numbers, total_amounts = zip(*rows)
    plt.bar(admission_numbers, total_amounts)
    plt.xlabel('Admission Number')
    plt.ylabel('Total Amount')
    plt.title('Total Fees Paid by Each Student')
    plt.tight_layout()
    plt.show()

def generate_line_graph(cursor):
    cursor.execute("""
        SELECT class, COUNT(*) AS student_count
        FROM students
        GROUP BY class
    """)
    rows = cursor.fetchall()
    if not rows:
        print("No student data available.")
        return
    classes, student_counts = zip(*rows)
    plt.plot(classes, student_counts, marker='o')
    plt.xlabel('Class')
    plt.ylabel('Number of Students')
    plt.title('Distribution of Students by Class')
    plt.tight_layout()
    plt.show()

def generate_histogram(cursor):
    cursor.execute("SELECT amount FROM payments")
    rows = cursor.fetchall()
    if not rows:
        print("No payment data available.")
        return
    amounts = [row[0] for row in rows]
    plt.hist(amounts, bins=10, edgecolor='black')
    plt.xlabel('Amount')
    plt.ylabel('Frequency')
    plt.title('Distribution of Fees Paid by Students')
    plt.tight_layout()
    plt.show()

# Main function
def main():
    db_connection = connect_to_database()
    cursor = db_connection.cursor()
    create_tables(cursor)

    while True:
        print("\n" + "=" * 30)
        print("   Fee Management System")
        print("=" * 30)
        print("1. Add New Student")
        print("2. Pay Fees and Generate Receipt")
        print("3. Print Receipt by Adm. No.")
        print("4. Update Student Details")
        print("5. View Details of All Students")
        print("6. Display Graph Menu")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            first_name = input("Enter student's first name: ")
            last_name = input("Enter student's last name: ")
            date_of_birth = input("Enter student's date of birth (YYYY-MM-DD): ")
            gender = input("Enter student's gender (Male/Female/Other): ")
            roll_number = input("Enter student's roll number: ")
            class_name = input("Enter student's class: ")
            address = input("Enter student's address: ")
            phone_number = input("Enter student's phone number: ")
            email = input("Enter student's email: ")
            admission_date = input("Enter student's admission date (YYYY-MM-DD): ")
            guardian_name = input("Enter student's guardian name: ")
            admission_number = input("Enter student's admission number: ")
            add_new_student(cursor, first_name, last_name, date_of_birth, gender,
                            roll_number, class_name, address, phone_number, email,
                            admission_date, guardian_name, admission_number)
            db_connection.commit()

        elif choice == '2':
            admission_number = input("Enter student's admission number: ")
            amount = float(input("Enter amount to pay: "))
            pay_fees(cursor, admission_number, amount)
            db_connection.commit()

        elif choice == '3':
            admission_number = input("Enter student's admission number: ")
            print_receipt_by_admission(cursor, admission_number)

        elif choice == '4':
            admission_number = input("Enter student's admission number: ")
            edit_student_details(cursor, admission_number)
            db_connection.commit()

        elif choice == '5':
            view_all_students_details(cursor)

        elif choice == '6':
            while True:
                display_graph_menu()
                graph_choice = input("Enter your choice: ")
                if graph_choice == '1':
                    generate_bar_graph(cursor)
                elif graph_choice == '2':
                    generate_line_graph(cursor)
                elif graph_choice == '3':
                    generate_histogram(cursor)
                elif graph_choice == '4':
                    break
                else:
                    print("Invalid choice. Please try again.")

        elif choice == '7':
            print("Exiting. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

    cursor.close()
    db_connection.close()

if __name__ == "__main__":
    main()