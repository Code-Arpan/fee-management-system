# Fee Management System

### My Class 12 Informatics Practices Project | CBSE Board Exam 2023-24
**School:** O.P. Jindal School, Kharsia Road, Raigarh

---

## About This Project
This is a Fee Management System built in Python with MySQL as the database.
It helps schools manage student records and fee payments digitally,
replacing manual paper-based processes.

---

## Features
- Add new student records with full details
- Record fee payments with multiple payment methods (Cash, Card, Net Banking, Cheque)
- Auto-generate fee receipts and save them as image files
- Update existing student details anytime
- View all student records in a table format
- Visual graphs to analyze fee collection and student data

---

## Technologies Used
- **Language:** Python 3.8+
- **Database:** MySQL
- **Libraries:** mysql-connector-python, Pillow, pandas, matplotlib, python-dotenv

---

## How to Run This Project on Any Computer

### Step 1: Install Python
Download and install Python 3.8 or above from https://python.org  
Make sure to check **"Add Python to PATH"** during installation.

### Step 2: Install MySQL
Download and install MySQL Community Server from https://dev.mysql.com/downloads/  
During setup, note down the root username and password you set.

### Step 3: Clone or Download This Project
git clone https://github.com/Code-Arpan/fee-management-system.git
cd fee-management-system
Or download the ZIP from GitHub and extract it.

### Step 4: Install All Required Dependencies
Open terminal or command prompt inside the project folder and run:
pip install -r requirements.txt
This single command installs everything the project needs automatically.

### Step 5: Create the Database
Open MySQL Workbench or MySQL command line and run:
CREATE DATABASE fee_management;

### Step 6: Set Your Database Password
Create a file named `.env` in the project folder and add this line:
DB_PASSWORD=your_mysql_password_here
Replace `your_mysql_password_here` with your actual MySQL root password.

### Step 7: Run the Project
python main.py

---

## Project Structure
fee-management-system/

├── main.py             # Main application file
├── requirements.txt    # All dependencies (install with pip)
├── .env                # Your local DB password (never shared)
├── .gitignore          # Files excluded from GitHub
└── README.md           # This file

---

## How to Use

| Option | What it does |
|--------|-------------|
| 1. Add New Student | Enter student details to register them |
| 2. Pay Fees | Record a fee payment and generate receipt |
| 3. Print Receipt | View and save receipt as an image by admission number |
| 4. Update Details | Edit any stored detail of a student |
| 5. View All Students | See all registered students in a table |
| 6. Graph Menu | View bar graph, line graph, or histogram of data |
| 7. Exit | Close the program |

---

## Made By
**Name:** Arpan Paul 
**Class:** XII  
**Subject:** Informatics Practices  
**Board:** CBSE  
**Session:** 2023-24