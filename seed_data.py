"""
Database seeding script for O Level Exam Portal
Populates the database with 100 Computer Science MCQ questions and default admin
"""

from models import db_manager, Question, Admin
from config import Config

# 100 O Level Computer Science MCQ Questions
questions_data = [
    # Computer Fundamentals (20 questions)
    {"question": "What does CPU stand for?", "options": ["Central Processing Unit", "Central Program Unit", "Computer Personal Unit", "Central Processor Utility"], "correct": "A"},
    {"question": "Which of the following is an input device?", "options": ["Monitor", "Printer", "Keyboard", "Speaker"], "correct": "C"},
    {"question": "What is the smallest unit of data in a computer?", "options": ["Byte", "Bit", "Nibble", "Word"], "correct": "B"},
    {"question": "How many bits are in a byte?", "options": ["4", "8", "16", "32"], "correct": "B"},
    {"question": "Which of the following is volatile memory?", "options": ["ROM", "Hard Disk", "RAM", "SSD"], "correct": "C"},
    {"question": "What does RAM stand for?", "options": ["Random Access Memory", "Read Access Memory", "Rapid Access Memory", "Real Access Memory"], "correct": "A"},
    {"question": "Which is an example of system software?", "options": ["MS Word", "Windows OS", "Chrome Browser", "Photoshop"], "correct": "B"},
    {"question": "What is the main circuit board of a computer called?", "options": ["CPU", "Motherboard", "RAM", "Hard Drive"], "correct": "B"},
    {"question": "Which storage device has the fastest access time?", "options": ["Hard Disk", "SSD", "CD-ROM", "Floppy Disk"], "correct": "B"},
    {"question": "What does GUI stand for?", "options": ["Graphical User Interface", "General User Interface", "Graphical Utility Interface", "General Utility Interface"], "correct": "A"},
    {"question": "Which of the following is an output device?", "options": ["Mouse", "Scanner", "Monitor", "Microphone"], "correct": "C"},
    {"question": "What is the brain of the computer?", "options": ["RAM", "Hard Disk", "CPU", "Monitor"], "correct": "C"},
    {"question": "1 KB equals how many bytes?", "options": ["1000", "1024", "512", "2048"], "correct": "B"},
    {"question": "Which type of software is used to create documents?", "options": ["System Software", "Application Software", "Utility Software", "Firmware"], "correct": "B"},
    {"question": "What does ROM stand for?", "options": ["Read Only Memory", "Random Only Memory", "Real Only Memory", "Rapid Only Memory"], "correct": "A"},
    {"question": "Which key is used to delete characters to the left of cursor?", "options": ["Delete", "Backspace", "Shift", "Ctrl"], "correct": "B"},
    {"question": "What is the extension of an executable file in Windows?", "options": [".txt", ".doc", ".exe", ".pdf"], "correct": "C"},
    {"question": "Which device is used to connect to the internet?", "options": ["Printer", "Modem", "Speaker", "Scanner"], "correct": "B"},
    {"question": "What does USB stand for?", "options": ["Universal Serial Bus", "Universal System Bus", "Uniform Serial Bus", "Uniform System Bus"], "correct": "A"},
    {"question": "Which is the fastest type of computer?", "options": ["Mainframe", "Supercomputer", "Microcomputer", "Minicomputer"], "correct": "B"},
    
    # Programming Concepts (20 questions)
    {"question": "Which of the following is a programming language?", "options": ["HTML", "CSS", "Python", "XML"], "correct": "C"},
    {"question": "What is a variable in programming?", "options": ["A constant value", "A storage location", "A function", "A loop"], "correct": "B"},
    {"question": "Which symbol is used for comments in Python?", "options": ["//", "#", "/*", "<!--"], "correct": "B"},
    {"question": "What is a loop in programming?", "options": ["A decision structure", "A repeated execution", "A function call", "A variable declaration"], "correct": "B"},
    {"question": "Which data type stores whole numbers?", "options": ["Float", "String", "Integer", "Boolean"], "correct": "C"},
    {"question": "What does 'if-else' represent in programming?", "options": ["Loop", "Conditional statement", "Function", "Array"], "correct": "B"},
    {"question": "Which operator is used for addition?", "options": ["-", "*", "+", "/"], "correct": "C"},
    {"question": "What is an array?", "options": ["A single variable", "A collection of elements", "A function", "A loop"], "correct": "B"},
    {"question": "Which keyword is used to define a function in Python?", "options": ["func", "define", "def", "function"], "correct": "C"},
    {"question": "What is the output of 5 % 2?", "options": ["2", "1", "0", "2.5"], "correct": "B"},
    {"question": "Which loop executes at least once?", "options": ["for loop", "while loop", "do-while loop", "nested loop"], "correct": "C"},
    {"question": "What is a string?", "options": ["A number", "A sequence of characters", "A boolean value", "An integer"], "correct": "B"},
    {"question": "Which operator checks equality?", "options": ["=", "==", "===", "!="], "correct": "B"},
    {"question": "What is a function?", "options": ["A variable", "A reusable block of code", "A loop", "A data type"], "correct": "B"},
    {"question": "Which is a logical operator?", "options": ["+", "-", "AND", "*"], "correct": "C"},
    {"question": "What does 'return' do in a function?", "options": ["Exits the program", "Sends back a value", "Starts a loop", "Declares a variable"], "correct": "B"},
    {"question": "Which is a comparison operator?", "options": ["+", ">", "=", "AND"], "correct": "B"},
    {"question": "What is debugging?", "options": ["Writing code", "Finding and fixing errors", "Running code", "Compiling code"], "correct": "B"},
    {"question": "Which keyword is used for inheritance in Python?", "options": ["extends", "inherits", "class", "super"], "correct": "C"},
    {"question": "What is an algorithm?", "options": ["A program", "A step-by-step procedure", "A variable", "A function"], "correct": "B"},
    
    # Database Concepts (15 questions)
    {"question": "What does SQL stand for?", "options": ["Structured Query Language", "Simple Query Language", "Standard Query Language", "System Query Language"], "correct": "A"},
    {"question": "Which SQL command is used to retrieve data?", "options": ["INSERT", "UPDATE", "SELECT", "DELETE"], "correct": "C"},
    {"question": "What is a primary key?", "options": ["A duplicate field", "A unique identifier", "A foreign key", "An index"], "correct": "B"},
    {"question": "Which command adds new data to a table?", "options": ["ADD", "INSERT", "UPDATE", "CREATE"], "correct": "B"},
    {"question": "What is a table in a database?", "options": ["A row", "A column", "A collection of records", "A query"], "correct": "C"},
    {"question": "Which SQL command deletes data?", "options": ["REMOVE", "DELETE", "DROP", "CLEAR"], "correct": "B"},
    {"question": "What is a foreign key?", "options": ["A primary key", "A link to another table", "An index", "A constraint"], "correct": "B"},
    {"question": "Which command modifies existing data?", "options": ["MODIFY", "CHANGE", "UPDATE", "ALTER"], "correct": "C"},
    {"question": "What does DBMS stand for?", "options": ["Database Management System", "Data Base Management Software", "Digital Base Management System", "Database Monitoring System"], "correct": "A"},
    {"question": "Which is a type of database?", "options": ["Relational", "Functional", "Procedural", "Sequential"], "correct": "A"},
    {"question": "What is a query?", "options": ["A table", "A request for data", "A record", "A field"], "correct": "B"},
    {"question": "Which SQL clause filters results?", "options": ["FILTER", "WHERE", "HAVING", "LIMIT"], "correct": "B"},
    {"question": "What is normalization?", "options": ["Adding data", "Organizing data efficiently", "Deleting data", "Backing up data"], "correct": "B"},
    {"question": "Which command creates a new table?", "options": ["NEW TABLE", "CREATE TABLE", "ADD TABLE", "MAKE TABLE"], "correct": "B"},
    {"question": "What is a record in a database?", "options": ["A column", "A row", "A table", "A field"], "correct": "B"},
    
    # Networking (15 questions)
    {"question": "What does IP stand for?", "options": ["Internet Protocol", "Internal Protocol", "Internet Process", "Internal Process"], "correct": "A"},
    {"question": "Which device connects multiple networks?", "options": ["Hub", "Switch", "Router", "Modem"], "correct": "C"},
    {"question": "What is the full form of LAN?", "options": ["Local Area Network", "Large Area Network", "Long Area Network", "Limited Area Network"], "correct": "A"},
    {"question": "Which protocol is used for email?", "options": ["HTTP", "FTP", "SMTP", "TCP"], "correct": "C"},
    {"question": "What does URL stand for?", "options": ["Uniform Resource Locator", "Universal Resource Locator", "Uniform Resource Link", "Universal Resource Link"], "correct": "A"},
    {"question": "Which is a web browser?", "options": ["Windows", "Chrome", "Linux", "Python"], "correct": "B"},
    {"question": "What is the purpose of DNS?", "options": ["Send emails", "Translate domain names to IP", "Transfer files", "Secure connections"], "correct": "B"},
    {"question": "Which topology connects all devices to a central hub?", "options": ["Bus", "Ring", "Star", "Mesh"], "correct": "C"},
    {"question": "What does HTTP stand for?", "options": ["HyperText Transfer Protocol", "HyperText Transmission Protocol", "High Transfer Text Protocol", "High Transmission Text Protocol"], "correct": "A"},
    {"question": "Which port does HTTP use?", "options": ["21", "25", "80", "443"], "correct": "C"},
    {"question": "What is a firewall?", "options": ["Antivirus software", "Network security system", "Web browser", "Email client"], "correct": "B"},
    {"question": "Which protocol is secure?", "options": ["HTTP", "FTP", "HTTPS", "SMTP"], "correct": "C"},
    {"question": "What does WAN stand for?", "options": ["Wide Area Network", "World Area Network", "Wireless Area Network", "Web Area Network"], "correct": "A"},
    {"question": "Which device amplifies network signals?", "options": ["Router", "Repeater", "Switch", "Hub"], "correct": "B"},
    {"question": "What is bandwidth?", "options": ["Network speed", "Data transfer capacity", "Cable length", "Signal strength"], "correct": "B"},
    
    # Operating Systems (10 questions)
    {"question": "Which is an operating system?", "options": ["MS Word", "Windows", "Chrome", "Excel"], "correct": "B"},
    {"question": "What is the main function of an OS?", "options": ["Browse internet", "Manage hardware and software", "Create documents", "Send emails"], "correct": "B"},
    {"question": "Which is a Linux distribution?", "options": ["Windows 10", "Ubuntu", "macOS", "Android"], "correct": "B"},
    {"question": "What is multitasking?", "options": ["Running one program", "Running multiple programs simultaneously", "Shutting down", "Restarting"], "correct": "B"},
    {"question": "Which file system is used by Windows?", "options": ["ext4", "NTFS", "HFS+", "FAT32"], "correct": "B"},
    {"question": "What is virtual memory?", "options": ["RAM", "Hard disk space used as RAM", "Cache", "ROM"], "correct": "B"},
    {"question": "Which command shows directory contents in Linux?", "options": ["dir", "ls", "show", "list"], "correct": "B"},
    {"question": "What is a process?", "options": ["A file", "A running program", "A folder", "A device"], "correct": "B"},
    {"question": "Which OS is open source?", "options": ["Windows", "macOS", "Linux", "iOS"], "correct": "C"},
    {"question": "What is booting?", "options": ["Shutting down", "Starting the OS", "Installing software", "Deleting files"], "correct": "B"},
    
    # Web Technologies (10 questions)
    {"question": "What does HTML stand for?", "options": ["HyperText Markup Language", "High Text Markup Language", "HyperText Machine Language", "High Text Machine Language"], "correct": "A"},
    {"question": "Which tag is used for headings in HTML?", "options": ["<head>", "<h1>", "<title>", "<header>"], "correct": "B"},
    {"question": "What does CSS stand for?", "options": ["Cascading Style Sheets", "Computer Style Sheets", "Creative Style Sheets", "Colorful Style Sheets"], "correct": "A"},
    {"question": "Which language adds interactivity to web pages?", "options": ["HTML", "CSS", "JavaScript", "XML"], "correct": "C"},
    {"question": "What is a hyperlink?", "options": ["A text", "A clickable link", "An image", "A video"], "correct": "B"},
    {"question": "Which tag creates a paragraph in HTML?", "options": ["<para>", "<p>", "<paragraph>", "<text>"], "correct": "B"},
    {"question": "What is the purpose of CSS?", "options": ["Structure content", "Style web pages", "Add functionality", "Store data"], "correct": "B"},
    {"question": "Which attribute specifies an image source?", "options": ["href", "src", "link", "url"], "correct": "B"},
    {"question": "What is a div tag used for?", "options": ["Division/container", "Image", "Link", "List"], "correct": "A"},
    {"question": "Which is a JavaScript framework?", "options": ["Bootstrap", "React", "Sass", "jQuery"], "correct": "B"},
    
    # Security & Ethics (10 questions)
    {"question": "What is a virus?", "options": ["Hardware", "Malicious software", "Operating system", "Web browser"], "correct": "B"},
    {"question": "What does antivirus software do?", "options": ["Create viruses", "Detect and remove malware", "Speed up computer", "Browse internet"], "correct": "B"},
    {"question": "What is phishing?", "options": ["Fishing online", "Fraudulent attempt to obtain information", "Gaming", "Shopping"], "correct": "B"},
    {"question": "What is encryption?", "options": ["Deleting data", "Converting data to secure format", "Copying data", "Backing up data"], "correct": "B"},
    {"question": "What is a strong password?", "options": ["123456", "password", "Mix of letters, numbers, symbols", "Your name"], "correct": "C"},
    {"question": "What is malware?", "options": ["Good software", "Malicious software", "System software", "Application software"], "correct": "B"},
    {"question": "What is two-factor authentication?", "options": ["One password", "Two security layers", "Two users", "Two computers"], "correct": "B"},
    {"question": "What is a backup?", "options": ["Deleting files", "Copy of data for recovery", "Installing software", "Updating system"], "correct": "B"},
    {"question": "What is copyright?", "options": ["Free to use", "Legal protection for creators", "Copying files", "Printing documents"], "correct": "B"},
    {"question": "What is plagiarism?", "options": ["Original work", "Using others' work without credit", "Citing sources", "Research"], "correct": "B"},
]

def seed_database():
    """Seed the database with questions and admin"""
    print("Connecting to database...")
    db = db_manager.connect()
    
    # Clear existing data (optional - comment out if you want to keep existing data)
    print("Clearing existing questions...")
    db.questions.delete_many({})
    
    # Insert questions
    print(f"Inserting {len(questions_data)} questions...")
    for q_data in questions_data:
        Question.create(
            question_text=q_data['question'],
            options=q_data['options'],
            correct_answer=q_data['correct'],
            subject='Computer Science'
        )
    
    # Ensure default admin exists
    print("Creating default admin...")
    Admin.ensure_default_admin()
    
    # Print statistics
    total_questions = Question.count()
    total_students = db.students.count_documents({})
    total_admins = db.admins.count_documents({})
    
    print("\n" + "="*50)
    print("Database seeding completed successfully!")
    print("="*50)
    print(f"Total Questions: {total_questions}")
    print(f"Total Students: {total_students}")
    print(f"Total Admins: {total_admins}")
    print(f"\nDefault Admin Credentials:")
    print(f"Username: {Config.DEFAULT_ADMIN_USERNAME}")
    print(f"Password: {Config.DEFAULT_ADMIN_PASSWORD}")
    print("="*50)
    print("\nIMPORTANT: Change the admin password after first login!")
    print("="*50)

if __name__ == '__main__':
    seed_database()
