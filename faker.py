import json
import os
from faker import Faker
from anonymate.anonymizer import Anonymizer
from cryptography.fernet import Fernet
KEY_FILE = ("encryption.key")
if os.path.exists(KEY_FILE):
    with open(KEY_FILE, "rb") as f:
        encryption_key = f.read()
else:
    encryption_key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(encryption_key)
fake = Faker()
anonymizer = Anonymizer(encryption_key=encryption_key)
length = int(input("Enter the desired number of synthetic patient datasets you would like:"))
data = []
for _ in range(length):
    data.append(fake.profile())
    print("Unencrypted data:")
data_str = json.dumps(data, default=str)
secure_data=anonymizer.encrypt_text(data_str)
print(secure_data)

def write_to_file_question(question: str) -> bool:
    while True:
        write_decision = input(f"{question} (y/n): ").strip().lower()
        if write_decision in ('y', 'yes'):
            return True
        if write_decision in ('n', 'no'):
            return False
        print("Invaild input. Please enter 'y' or 'n'.")

write_bool = write_to_file_question("Would you like to write this data to file?")
if write_bool==True:
    custom_name=input("Enter the desired name of the file: (no special characters): ")

    file_name = (f"{custom_name}.txt")
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(secure_data)
    print(f"saved to {file_name}")
else:
    print("Data not saved. All data will be lost when application is closed.")







