# 2. Create and connect to a SQLite Database 
# Step 1: Import the sqlite3 module 
import sqlite3 
# Step 2: Connect to (or create) a local database file named 'students.db' 
conn = sqlite3.connect("students.db") 
# Step 3: Create a cursor object to execute SQL commands 
cursor = conn.cursor() 
# Step 4: Display confirmation message 
print("Connected to students.db")


# 3. Create a Table 
# Step 1: Write the SQL command to create a table 
create_table_query = """ 
CREATE TABLE IF NOT EXISTS students ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    full_name TEXT NOT NULL, 
    course TEXT NOT NULL, 
    year_level INTEGER NOT NULL 
) 
""" 
# Step 2: Execute the SQL command using the cursor 
cursor.execute(create_table_query) 
# Step 3: Commit the transaction to save changes 
conn.commit() 
# Step 4: Display success message 
print("Table 'students' created successfully.") 


# 4. Insert Sample Data into the Table
# Step 1: Define a list of sample student records (tuples) 
students = [ 
("Anna Reyes", "BS ECE", 3), 
("Carlos Dela Cruz", "BS EE", 2), 
("Mika Santos", "BS CE", 1) 
] 
# Step 2: Write a parameterized SQL INSERT query 
insert_query = """ 
INSERT INTO students (full_name, course, year_level) 
VALUES (?, ?, ?) 
""" 
# Step 3: Use executemany() to insert all records at once 
cursor.executemany(insert_query, students) 
# Step 4: Commit the transaction 
conn.commit() 
# Step 5: Display confirmation message 
print("Sample data inserted into 'students' table.")


# 5. Query the Data 
# Step 1: Retrieve all records from the students table 
cursor.execute("SELECT * FROM students") 
print("All Students:") 
for row in cursor.fetchall(): 
    print(row) 
# Step 2: Filter results - show only BS ECE students 
cursor.execute("SELECT * FROM students WHERE course = 'BS ECE'") 
print("\nBS ECE Students:") 
print(cursor.fetchall()) 
# Step 3: Sort records by year_level in descending order 
cursor.execute("SELECT * FROM students ORDER BY year_level DESC") 
print("\nSorted by Year Level:") 
print(cursor.fetchall()) 
# Step 4: Limit the results to the top 2 records 
cursor.execute("SELECT * FROM students LIMIT 2") 
print("\nTop 2 Students:") 
print(cursor.fetchall())


# 6. Update and Delete Records 
# Step 1: Update year level of a student 
cursor.execute(""" 
UPDATE students 
SET year_level = 4 
WHERE full_name = 'Anna Reyes' 
""") 
conn.commit() 
print("Updated Anna Reyes to 4th year.") 
# Step 2: Delete a student record 
cursor.execute(""" 
DELETE FROM students 
WHERE full_name = 'Carlos Dela Cruz' 
""") 
conn.commit() 
print("Deleted Carlos Dela Cruz from the database.")


# 7. Use Aggregate Functions
# Step 1: Count total number of students 
cursor.execute("SELECT COUNT(*) FROM students") 
print("Total Students:", cursor.fetchone()[0]) 
# Step 2: Calculate the average year level 
cursor.execute("SELECT AVG(year_level) FROM students") 
print("Average Year Level:", cursor.fetchone()[0]) 
# Step 3: Group records by course 
cursor.execute("SELECT course, COUNT(*) FROM students GROUP BY course") 
print("Students per Course:", cursor.fetchall())


# 8. Close the Database Connection 
# Step 1: Close the cursor 
cursor.close() 
# Step 2: Close the connection 
conn.close() 
# Step 3: Display closing message 
print("Database connection closed.")


# 9. Insert Data via User Input
import sqlite3

conn = sqlite3.connect("students.db")

full_name = input("Enter full name: ")
course = input("Enter course (e.g., BS ECE): ")
year_level = int(input("Enter year level: "))

cursor = conn.cursor()

cursor.execute("""
INSERT INTO students (full_name, course, year_level)
VALUES (?, ?, ?)
""", (full_name, course, year_level))

conn.commit()
print("Student record successfully added.")

conn.close()


#!0
import sqlite3

# Re-establish the connection and cursor
conn = sqlite3.connect('students.db') 
cursor = conn.cursor()

# Now run your reset logic
cursor.execute("DELETE FROM students")
conn.commit()

# Reset the auto-increment counter
cursor.execute("DELETE FROM sqlite_sequence WHERE name='students'")
conn.commit()

print("All records deleted. ID counter reset.")



# 11. Export Query Results to CSV File
import csv 
# Step 1: Retrieve all records 
cursor.execute("SELECT * FROM students") 
rows = cursor.fetchall() 
# Step 2: Write to CSV 
with open("students_export.csv", "w", newline='') as file: 
    writer = csv.writer(file) 
    writer.writerow(["ID", "Full Name", "Course", "Year Level"]) 
    writer.writerows(rows) 
print("Data exported to 'students_export.csv'.")


# 12. Create and Join Tables
# Step 1: Create the courses table
cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    course_code TEXT PRIMARY KEY,
    description TEXT NOT NULL
)
""")
conn.commit()

# Step 2: Insert data into the courses table
course_data = [
    ("BS ECE", "Electronics and Communications Engineering"),
    ("BS EE", "Electrical Engineering"),
    ("BS COE", "Computer Engineering"),
    ("BS CE", "Civil Engineering")
]

cursor.executemany("""
INSERT OR IGNORE INTO courses (course_code, description)
VALUES (?, ?)
""", course_data)
conn.commit()

# Step 3: Write a JOIN query to combine student names with their course descriptions
cursor.execute("""
SELECT s.full_name, s.course, c.description
FROM students s
JOIN courses c ON s.course = c.course_code
""")

# Step 4: Display results
for row in cursor.fetchall():
    print(row)


# 13. Create and Join Tables 
# Step 1: Write a JOIN query with filtering and sorting 
cursor.execute(""" 
SELECT s.full_name, s.course, c.description 
FROM students s 
JOIN courses c ON s.course = c.course_code 
WHERE s.course = 'BS CE' 
ORDER BY s.full_name ASC 
""")
# Step 2: Display the filtered and sorted results 
for row in cursor.fetchall(): 
    print(row) 


# 14. Search for Records Using Pattern Matching 
# Part A – Static query (for demonstration only) 
cursor.execute(""" 
SELECT * FROM students 
WHERE full_name LIKE '%Reyes%' 
""") 
print("Static search result:") 
for row in cursor.fetchall(): 
    print(row) 

# Part B – Parameterized query with user input 
keyword = input("Enter a name keyword to search: ") 
cursor.execute(""" 
SELECT * FROM students 
WHERE full_name LIKE ? 
""", ('%' + keyword + '%',)) 
print("Search results:") 
for row in cursor.fetchall(): 
    print(row) 


