import base64
# #
# # # Base64 encoded string
# # base64_str = "AQ=="
# #
# # # Decode Base64 string to bytes
# # decoded_bytes = base64.b64decode(base64_str)
# #
# # # Convert bytes to integer
# # decoded_int = int.from_bytes(decoded_bytes, byteorder='big')
# #
# # print(decoded_int)
import json

# Sample JSON message
json_message = ('{"ID":"GA==","TITLE":"zxc","SLUG":"zxc","AUTHOR_ID":"AQ==","CREATED_AT":1711536514000,'
                '"IS_ACTIVE":"1","table":"ORCLCDB.C##BLOGWEBSITE.BLOG","scn":"2262843","op_type":"I",'
                '"op_ts":"1711522260000","current_ts":"1711522264773","row_id":"AAAAAAAAAAAAAAAAAA","username":"SYS"}')

# Parse the JSON message
parsed_message = json.loads(json_message)


def b64Encode(msg):
    base64_str = msg
    decoded_bytes = base64.b64decode(base64_str)
    decoded_int = int.from_bytes(decoded_bytes, byteorder='big')
    return decoded_int


# Extract specific field values
ID = parsed_message['ID']
TITLE = parsed_message['TITLE']
SLUG = parsed_message['SLUG']
AUTHOR_ID = parsed_message['AUTHOR_ID']
CREATED_AT = parsed_message['CREATED_AT']
IS_ACTIVE = parsed_message['IS_ACTIVE']
OP_TYPE = parsed_message['op_type']
# Print the extracted field values
print("ID:", ID)
print("TITLE:", TITLE)
print("SLUG:", SLUG)
print("AUTHOR_ID:", AUTHOR_ID)
print("CREATED_AT:", CREATED_AT)
print("IS_ACTIVE:", IS_ACTIVE)
print("OP_TYPE:", OP_TYPE)
print(b64Encode(AUTHOR_ID))

# import re
#
# def extract_json_from_byte_string(byte_string):
#     """
#     Extracts the entire JSON object enclosed within curly braces from a byte string using regular expressions.
#
#     Parameters:
#         byte_string (bytes): The byte string containing JSON text.
#
#     Returns:
#         str: The extracted JSON object as a string, or an empty string if not found.
#     """
#     # Define a regular expression pattern to match the entire JSON object enclosed within curly braces
#     pattern = re.compile(b'{(.*?)}')
#
#     # Search for the entire JSON object within curly braces in the byte string
#     match = pattern.search(byte_string)
#
#     if match:
#         # Extract the JSON object from the match
#         json_object = match.group(0).decode('utf-8')
#         return json_object
#     else:
#         return ""
#
#
# # Byte string containing the JSON message
# byte_string = b'\x00\x00\x00\x00\x06{"ID":"GQ==","TITLE":"qweqwe","SLUG":"qweqwe","AUTHOR_ID":"AQ==","CREATED_AT":1711536514000,"IS_ACTIVE":"1","table":"ORCLCDB.C##BLOGWEBSITE.BLOG","scn":"2265408","op_type":"I","op_ts":"1711522783000","current_ts":"1711522784807","row_id":"AAAAAAAAAAAAAAAAAA","username":"SYS"}'
#
# # Call the function to extract the entire JSON object from the byte string
# json_object = extract_json_from_byte_string(byte_string)
#
# if json_object:
#     print(json_object)
# else:
#     print("No JSON object found in the byte string.")


