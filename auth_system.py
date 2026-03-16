#MENU SYSTEM With Persistent Memory
#1. -LOGIN | 2. CREATE AN ACCOUNT | 3. EXIT

import json                                     #LOADS PYTHON BUILT-IN JSON LIBRARY
import hashlib                                  #LOADS PYTHON CRYPTOGRAPHY TOOL
import secrets                                  #GENERATES SECURE RANDOM VALUES (SALT)
import time                                     #GRANT ACCESS TO CURRENT TIME IN SECONDS


#LOAD USERS FROM JSON FUNCTION

def load_users():

    try:
        with open("users.json","r") as file:     #OPEN FILE IN "R" = READ MODE
            users = json.load(file)             #CONVERTS JSON INTO PYTHON DICTIONARY
            return users
    except FileNotFoundError:
        return {}                               #RETURNS EMPTY DICTIONARY IF FILE NOT FOUND

#SAVE USERS TO JSON FUNCTION

def save_users(users):

    with open("users.json", "w") as file:       #OPENS USER JSON
        json.dump(users, file, indent=4)        #WRITES DICTIONARY INTO FILE

users = load_users()                            #CREATES VARIABLE FOR USERS TO LOAD FROM JSON
failed_attempts ={}                             #ADDS FAILED ATTEMPTS DICTIONARY
lockout_until ={}                               #ADDS FAILURE LOCKOUT TIMER DICTIONARY

#LOGIN FUNCTION

def login():                                    #CREATES LOGIN AS A FUNCTION

    username = input("Enter username: ")        #STORES USERNAME INPUT
    password = input("Enter password ")         #STORES PASSWORD INPUT

    if username not in users:
        print("Username not found.")
        return

    current_time = time.time()                  #CREATES VARIABLE FOR CURRENT TIME

    if username in lockout_until and current_time < lockout_until[username]:        #LOCKOUT ENTRY + LOCKOUT TIME = STILL LOCKED
        remaining = int(lockout_until[username] - current_time)                     #CALCULATES REMAINING TIME
        print(f"Account is locked. Try again in {remaining} seconds.")
        return

    stored_salt = users[username]["salt"]
    stored_hash = users[username]["hash"]

    if stored_hash == hashed_password(password, stored_salt):
        print("Login successful.")
        failed_attempts[username] = 0
    else:
        print("Incorrect password")

        if username not in failed_attempts:                                         #ENSURES USER HAS COUNTER
            failed_attempts[username] = 0                                                                

        failed_attempts[username] += 1                                              #ADDS 1 TO COUNT AFTER FAILED ATTEMPT

        remaining_attempts = 3 - failed_attempts[username]

        if failed_attempts[username] >=3:                                           #LOCKS ACCOUNT FOR 60 SECONDS AFTER 3 FAILURES
            lockout_until[username] = current_time + 60
            failed_attempts[username] = 0
            print("Too many failed attempts. Account locked for 60 seconds.")
        else:
            print(f"Attempts remaining: {remaining_attempts}")

#PASSWORD HASHING

def hashed_password(password, salt):

    combined = salt + password

    return hashlib.sha256(combined.encode()).hexdigest()        #CONVERTS STRING TO BYTES USES SHA-256 ALGORITHM

#ACCOUNT CREATION FUNCTION

def create_account():

    username = input("Choose a username: ")    #USERNAME IS CREATED

    if username in users:                      #CHECKS FOR DUPLICATE USERNAME
        print("Username already exists.")
        return

    while True:
        print("Choose a password that is:\n Atleast 8 Characters \n One uppercase \n One lowercase \n One digit \n and contains one of these Special Character !@#$ \n")

        password = input("Enter password: ")

        valid, message = validate_password(password)

        print(message)

        if not valid:
            continue

        confirmed_password = input("Confirm password: ")

        if password != confirmed_password:
            print("Passwords do not match. Try again.")
            continue

        salt = secrets.token_hex(16)                                #CREATES A RANDOM SECURE SALT

        hashed = hashed_password(password, salt)
        
        users[username] = {                  #ADDS A NEW ENTERY TO THE DICTIONARY (HASH & SALT)
            "salt" : salt,
            "hash" : hashed
        }
        save_users(users)                           #WRITES THE UPDATED DICTIONARY TO JSON

        print("Account created successfully.")
        break
    
#PASSWORD VALIDATION FUNCTION

def validate_password(password):

    if not (8 <= len(password) <= 20):
        return False, "Password must be between 8 and 20 characters."

    if not any(char.isupper() for char in password):
        return False, "Password must contain an uppercase letter."

    if not any(char.islower() for char in password):
        return False, "Password must contain a lowercase letter."

    if not any(char.isdigit() for char in password):
        return False, "Password must contain a digit."
    
    if not any(char in "!@#$" for char in password):
        return False, "Password must contain of these special characters !@#$."

    else:
        return True, "Password accepted."

#MENU LOOP

while True:

    print("\nMenu")
    print("1 - Login")
    print("2 - Create Account")
    print("3 - Exit")

    choice = input("Choose an option: ")

#HANDLE CHOICES

    if choice == "1":
        login()

    elif choice == "2":
        create_account()

    elif choice == "3":
        print("Goodbye")
        break

    else:
        print("Invalid Option")



