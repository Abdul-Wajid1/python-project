import json
import os

# Add Student
def add_student(students):
    name = input_nonempty_string("Enter student name: ")
    f_name = input_nonempty_string("Enter student's father's name: ")
    age = input_positive_int("Enter student age: ")
    rollNumber = input_nonempty_string("Enter student roll number: ")
    Class = input_nonempty_string("Enter student class: ")
    attendance = input_percentage("Enter student attendance in percentage: ")
    subjects = input_positive_int(input("How many subjects student learns: "))
    fee = input_fee("Enter student fee: ")
    paid_fee = input_fee("Enter paid fee: ")

    students.append({
        'name': name,
        'fatherName': f_name,
        'age': age,
        'rollNumber': rollNumber,
        'class': Class,
        'attendance': attendance,
        'subjects': subjects,
        'fee': fee,
        'paid_fee': paid_fee
    })
    print("\n✅ Student added successfully.\n")

# Enter Subjects and Marks
def enter_subjects(students):
    roll = input("Enter the roll number of the student: ")
    student = search_student(students, roll, show_info=True)

    if not student:
        print("⚠️ Student not found.\n")
        return

    # Determine previous subject count
    prev_subject_count = student.get('subjects', 0)
    if isinstance(prev_subject_count, dict):  # subjects already entered
        prev_subject_count = len(prev_subject_count)
    elif isinstance(prev_subject_count, int):  # number entered during add_student
        pass
    else:
        prev_subject_count = 0

    # Confirm or update subject count
    if prev_subject_count > 0:
        confirm = input(f"The student currently has {prev_subject_count} subjects. Is this correct? (yes/no): ").lower()
        if confirm != "yes":
            prev_subject_count = int(input("Enter the correct number of subjects: "))
    else:
        prev_subject_count = int(input("Enter number of subjects the student is learning: "))

    # Enter subject names and marks using helper
    subjects = {}
    for i in range(prev_subject_count):
        subject_name = input(f"Enter subject {i+1} name: ")
        marks = input_marks(subject_name)  # call helper
        subjects[subject_name] = marks

    # Update student data
    student['subjects'] = subjects
    total_marks = sum(subjects.values())
    student['total_marks'] = total_marks
    student['percentage'] = total_marks / prev_subject_count
    student['gpa'], student['grade'] = calculate_gpa_and_grade(student['percentage'])

    print(f"\n✅ Subjects and marks updated for {student['name']}.\n")

# Update Student Info
def update_student_info(students):
    roll = input("Enter roll number of the student to update: ")
    student = None
    for s in students:
        if s['rollNumber'] == roll:
            student = s
            break

    if not student:
        print("⚠️ Student not found.\n")
        return

    print("\nEnter new values or press Enter to keep current value.")

    # Input functions with validation inside this function
    def input_nonempty(prompt, current):
        while True:
            val = input(f"{prompt} [{current}]: ").strip()
            if val != "":
                return val
            elif current != "":
                return current
            print("❌ Input cannot be empty!")

    def input_positive_int(prompt, current):
        while True:
            val = input(f"{prompt} [{current}]: ").strip()
            if val == "":
                return current
            if val.isdigit() and int(val) > 0:
                return int(val)
            print("❌ Please enter a valid age!")

    def input_percentage(prompt, current):
        while True:
            val = input(f"{prompt} [{current}]: ").strip()
            if val == "":
                return current
            try:
                val_float = float(val)
                if 0 <= val_float <= 100:
                    return val_float
                else:
                    print("❌ Percentage must be between 0 and 100.")
            except ValueError:
                print("❌ Enter a valid number.")

    def input_fee(prompt, current):
        while True:
            val = input(f"{prompt} [{current}]: ").strip()
            if val == "":
                return current
            try:
                val_float = float(val)
                if val_float >= 0:
                    return val_float
                else:
                    print("❌ Fee cannot be negative.")
            except ValueError:
                print("❌ Enter a valid number.")

    # Update each field
    student['name'] = input_nonempty("Name", student['name'])
    student['fatherName'] = input_nonempty("Father's Name", student['fatherName'])
    student['class'] = input_nonempty("Class", student['class'])
    student['age'] = input_positive_int("Age", student['age'])
    student['attendance'] = input_percentage("Attendance (%)", student['attendance'])
    student['fee'] = input_fee("Fee", student['fee'])
    student['paid_fee'] = input_fee("Paid Fee", student['paid_fee'])

    print(f"\n✅ Student info updated successfully for {student['name']}.\n")

# Delete Student
def delete_student(students):
    roll = input("Enter roll number of the student to delete: ")
    for i, student in enumerate(students):
        if student['rollNumber'] == roll:
            confirm = input(f"Are you sure you want to delete {student['name']}? (yes/no): ").lower()
            if confirm == 'yes':
                students.pop(i)
                print(f"\n✅ Student {student['name']} has been deleted.\n")
            else:
                print("Deletion cancelled.\n")
            return
    print("⚠️ Student not found.\n")

# Search Student
def search_student(students, rollNumber, show_info=True):
    for student in students:
        if student['rollNumber'] == rollNumber:
            if show_info:
                print(f"\n--- Student Found ---")
                print(f"Name: {student['name']}")
                print(f"Father's Name: {student['fatherName']}")
                print(f"Roll Number: {student['rollNumber']}")
                print(f"Age: {student['age']}")
                print(f"Class: {student['class']}")
                print(f"Attendance: {student['attendance']}%")
            return student
    return None

# Fee Management
def fee_management(students, rollNumber):
    student = search_student(students, roll, show_info=True)
    if student:
        remaining = float(student['fee']) - float(student['paid_fee'])
        print(f"\n💰 Fee Management for {student['name']}:")
        print(f"Total Fee: {student['fee']}")
        print(f"Paid Fee: {student['paid_fee']}")
        print(f"Remaining Fee: {remaining}\n")
    else:
        print("⚠️ Student not found.\n")

# Attendance Management
def attendance_management(students, rollNumber):
    student = search_student(students, roll, show_info=True)

    if student:
        print(f"\n📋 Attendance for {student['name']}: {student['attendance']}%\n")
    else:
        print("⚠️ Student not found.\n")

# Generate Result Card
def result_card(students, rollNumber):
    student = search_student(students, roll, show_info=False)
    if not student:
        print("⚠️ Student not found.\n")
        return

    print("\n================= RESULT CARD =================")
    print(f"Name          : {student['name']}")
    print(f"Father's Name : {student['fatherName']}")
    print(f"Roll Number   : {student['rollNumber']}")
    print(f"Class         : {student['class']}")
    print(f"Attendance    : {student['attendance']}%")
    print("-----------------------------------------------------")

    # Subjects table
    if isinstance(student.get('subjects'), dict) and student['subjects']:
        print(f"{'Subject':<20} {'Marks':>6}")
        print("-" * 27)
        for subject, marks in student['subjects'].items():
            print(f"{subject:<20} {marks:>6}/100")
    else:
        print("No subjects entered yet.")

    print("------------------------------------------------")
    total_marks = student.get('total_marks', 'N/A')
    percentage = student.get('percentage', 'N/A')
    gpa = student.get('gpa', 'N/A')
    grade = student.get('grade', 'N/A')

    print(f"Total Marks : {total_marks}")
    print(f"Percentage  : {percentage}%")
    print(f"GPA         : {gpa}")
    print(f"Grade       : {grade}")
    print("==============================================\n")

# Calculate GPA and Grade
def calculate_gpa_and_grade(percentage):
    if percentage >= 90:
        return 4.0, "A+"
    elif percentage >= 80:
        return 4.0, "A"
    elif percentage >= 75:
        return 3.5, "B+"
    elif percentage >= 70:
        return 3.0, "B"
    elif percentage >= 65:
        return 2.5, "C+"
    elif percentage >= 60:
        return 2.0, "C"
    elif percentage >= 55:
        return 1.5, "D+"
    elif percentage >= 50:
        return 1.0, "D"
    else:
        return 0.0, "F"  # Fail

# Save data to file
def save_data(students, filename="students_data.json"):
    with open(filename, "w") as f:
        json.dump(students, f, indent=4)
    print("\n💾 Data saved successfully.\n")

# Load data from file
def load_data(filename="students_data.json"):
    try:
        with open(filename, "r") as f:
            students = json.load(f)
        print("📂 Data loaded successfully.\n")
        return students
    except FileNotFoundError:
        print("No previous data found. Starting fresh.\n")
        return []

# Utility function to clear console
def clear_console():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Mac/Linux
    else:
        os.system('clear')

# Input validation functions
def input_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            else:
                print("⚠️ Please enter a positive integer.")
        except ValueError:
            print("⚠️ Invalid input. Enter a valid integer.")

def input_percentage(prompt):
    while True:
        try:
            value = float(input(prompt))
            if 0 <= value <= 100:
                return value
            else:
                print("⚠️ Please enter a value between 0 and 100.")
        except ValueError:
            print("⚠️ Invalid input. Enter a number between 0 and 100.")

def input_nonempty_string(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        else:
            print("⚠️ Input cannot be empty. Please enter a valid value.")

def input_fee(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value >= 0:
                return value
            else:
                print("⚠️ Please enter a non-negative number.")
        except ValueError:
            print("⚠️ Invalid input. Enter a valid number.")

def input_marks(subject_name):
    while True:
        try:
            marks = float(input(f"Enter marks for {subject_name} (0-100): "))
            if 0 <= marks <= 100:
                return marks
            else:
                print("⚠️ Marks must be between 0 and 100. Try again.")
        except ValueError:
            print("⚠️ Invalid input. Enter a number.")

students = []
students = load_data()
choice = ""

while choice != "9":
    print("===== Student Management System =====")
    print("1. Add Student")
    print("2. View Student Info")
    print("3. Update Student Info")
    print("4. Delete Student")
    print("5. Enter Subjects and Marks")
    print("6. Fee Management")
    print("7. Attendance Management")
    print("8. Result Card")
    print("9. Exit")

    choice = input("Enter your choice (1-9): ")

    if choice == "1": # Add Student
        clear_console()  # Clears the console every loop
        add_student(students)
        save_data(students)
    elif choice == "2": # View Student Info
        clear_console()  # Clears the console every loop
        roll = input("Enter roll number to search: ")
        student = search_student(students, roll)
        if student:
            print(f"\n✅ Student Found: {student['name']} (Roll No: {student['rollNumber']})\n")
        else:
            print("\n⚠️ Student not found.\n")
    elif choice == "3": # Update Student Info
        clear_console()  # Clears the console every loop
        update_student_info(students)
        save_data(students)
    elif choice == "4": # Delete Student
        clear_console()  # Clears the console every loop
        delete_student(students)
        save_data(students)
    elif choice == "5": 
        clear_console()  # Clears the console every loop
        enter_subjects(students)
        save_data(students)
    elif choice == "6":
        clear_console()  # Clears the console every loop
        roll = input("Enter roll number for fee management: ")
        fee_management(students, roll)
    elif choice == "7":
        clear_console()  # Clears the console every loop
        roll = input("Enter roll number for attendance: ")
        attendance_management(students, roll)
    elif choice == "8":
        clear_console()  # Clears the console every loop
        roll = input("Enter roll number for result card: ")
        result_card(students, roll)
    elif choice == "9":
        clear_console()  # Clears the console every loop
        print("\n👋 Exiting the system. Goodbye!\n")
    else:
        print("\n❌ Invalid choice. Please try again.\n")