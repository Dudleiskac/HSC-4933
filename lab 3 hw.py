from anonymate.anonymizer import Anonymizer

anonymizer= Anonymizer()

profiles= {}
encrypt_choice=input("do you want to encrypt the data? yes/no")
if encrypt_choice == "yes":
        encrypted_data=anonymizer.encrypt_text(str(profiles))
        print("\nData is encrypted.")
        print(encrypted_data)
        print(encrypt_choice)
print("\nAvailable profiles:")
for i, profile in enumerate(profiles):
        print(i + 1, profile["name"])
profile_choice= int(input("\nSelect a profile number:"))
selected_profile= profiles[profile_choice - 1]
print("\nWhat information would you like to see?")
print("1. Name")
print("2. DoB")
print("3. Sex")
print("4. Blood Type")
information_choice= input("Enter your choice (1-4):")
selected_profile=[]
if information_choice=="1":
    print("Name:",selected_profile["name"])
elif information_choice=="2":
    print("DoB:", selected_profile["birthdate"])
elif information_choice=="3":
    print("Sex:", selected_profile["sex"])
elif information_choice=="4":
    print("Blood Type:",
          selected_profile["blood_type"])
else:
    print("Invaild choice")




