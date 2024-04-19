import sqlite3

# Connect to the database (creates a new database if it doesn't exist)
conn = sqlite3.connect('customervisit.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the table for customers with id, name, and age columns
cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER
    )
''')

# Commit the changes 
conn.commit()

# Populate the customers table with id, name, and age data
customers_data = [
    (1, 'John Doe', 30),
    (2, 'Jane Smith', 25),
    (3, 'Mike Johnson', 35),
    # Add more customer records here
]

cursor.executemany('INSERT INTO customers VALUES (?, ?, ?)', customers_data)

# Commit the changes and close the connection
conn.commit()
conn.close()
