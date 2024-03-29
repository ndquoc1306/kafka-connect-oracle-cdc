import cx_Oracle

# Define the connection string
connection_string = 'C##BLOGWEBSITE/123456@localhost:1521/ORCLCDB'

# Establish a connection to the Oracle database
connection = cx_Oracle.connect(connection_string)

# Create a cursor object
cursor = connection.cursor()

# Example: Execute a SELECT query
try:
    cursor.execute(f"""SELECT s.EMAIL
FROM "C##BLOGWEBSITE"."SUBSCRIBERS" s
JOIN "C##BLOGWEBSITE".USER_SUBSCRIBER us ON s.SUBSCRIBER_ID = us.SUBSCRIBER_ID 
JOIN "C##BLOGWEBSITE"."USER" u ON us.USER_ID = u.ID 
JOIN "C##BLOGWEBSITE".BLOG b ON u.ID = b.AUTHOR_ID 
WHERE b.AUTHOR_ID = 22""")
    # Fetch and print the results
    for row in cursor.fetchall():
        print(row)
except cx_Oracle.DatabaseError as e:
    error, = e.args
    print("Database error:", error.message)

# Close the cursor and the connection
cursor.close()
connection.close()
