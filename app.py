from kafka import KafkaConsumer
import json

import re
import base64

import cx_Oracle

from email.message import EmailMessage
import smtplib
import ssl

# Account smtp email
email_sender = 'ndquoc0602@gmail.com'
email_password = 'izehfgzgantnqyir'

# Kafka broker configurations
bootstrap_servers = 'localhost:9092'
topic = 'json'

# Create a Kafka consumer
consumer = KafkaConsumer(
    topic,
    bootstrap_servers=bootstrap_servers,
    auto_offset_reset='earliest',
    enable_auto_commit=True)


def extract_json_from_byte_string(byte_string):
    """
    Extracts the entire JSON object enclosed within curly braces from a byte string using regular expressions.

    Parameters:
        byte_string (bytes): The byte string containing JSON text.

    Returns:
        str: The extracted JSON object as a string, or an empty string if not found.
    """
    # Define a regular expression pattern to match the entire JSON object enclosed within curly braces
    pattern = re.compile(b'{(.*?)}')

    # Search for the entire JSON object within curly braces in the byte string
    match = pattern.search(byte_string)

    if match:
        # Extract the JSON object from the match
        json_object = match.group(0).decode('utf-8')
        return json_object
    else:
        return ""


def b64Encode(msg):
    base64_str = msg
    decoded_bytes = base64.b64decode(base64_str)
    decoded_int = int.from_bytes(decoded_bytes, byteorder='big')
    return decoded_int


# Consume messages from the Kafka topic
# try:
for message in consumer:
    # Print the message value as JSON
    json_blog = extract_json_from_byte_string(message.value)
    parsed_message = json.loads(json_blog)
    AUTHOR_ID = parsed_message['AUTHOR_ID']
    # print("AUTHOR_ID:", AUTHOR_ID)
    # print(b64Encode(AUTHOR_ID))
    author = b64Encode(AUTHOR_ID)
    title = parsed_message['TITLE']
    # Define the connection string
    connection_string = 'C##BLOGWEBSITE/123456@localhost:1521/ORCLCDB'

    # Establish a connection to the Oracle database
    connection = cx_Oracle.connect(connection_string)

    # Create a cursor object
    cursor = connection.cursor()

    # Example: Execute a SELECT query
    try:
        cursor.execute(f"""SELECT s.EMAIL
    FROM "C##BLOGWEBSITE".SUBSCRIBERS s
    JOIN "C##BLOGWEBSITE".USER_SUBSCRIBER us ON s.SUBSCRIBER_ID = us.SUBSCRIBER_ID 
    JOIN "C##BLOGWEBSITE".USER u ON us.USER_ID = u.ID 
    JOIN "C##BLOGWEBSITE".BLOG b ON u.ID = b.AUTHOR_ID 
    WHERE b.AUTHOR_ID = {author}""")
        # Fetch and print the results
        for row in cursor.fetchall():
            input_tuple = row
            email_address = input_tuple[0]
            print(email_address)
            print(title)
            # email_receiver = email_address
            # subject = "New blog has been updated!"
            # body = """Hope you fun with my blog"""
            #
            # em = EmailMessage()
            # em['From'] = email_sender
            # em['To'] = email_receiver
            # em['Subject'] = subject
            # em.set_content(body)
            #
            # context = ssl.create_default_context()
            #
            # with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            #     smtp.login(email_sender, email_password)
            #     smtp.sendmail(email_sender, email_receiver, em.as_string())
            #     print("Done!")
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print("Database error:", error.message)

    # Close the cursor and the connection
    cursor.close()
    connection.close()
# except KeyboardInterrupt:
# Close the Kafka consumer on keyboard interrupt
consumer.close()
