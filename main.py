import csv
import bcrypt
import re
from balance_manager import get_balance, set_initial_balance, update_balance

def check_credentials(username, password):
    """ Check if the credentials match one credential in the CSV file """
    with open('userpasswords.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['username'] == username and bcrypt.checkpw(password.encode('utf-8'), row['password'].encode('utf-8')):
                return True
    return False

def hash_password(password):
    """Hashing the password for storing"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password

def validate_credentials(username, password):
    """Validate username and password against defined rules"""
    if len(username) < 8 or len(password) < 8:
        print("Username and password must be at least 8 characters long.")
        return False
    if not re.search(r'\d', username) or not re.search(r'\d', password):
        print("Username and password must contain at least one number.")
        return False
    if username == password:
        print("Username and password must not be the same")
        return False
    return True

def signup():
    """ Allow a new user to register and save their hashed credentials to the CSV file """
    print("Sign up for BlombergBank")
    username = input("Choose a username: ")
    password = input("Choose a password: ")

    if not validate_credentials(username, password):
        return False

    # Check if username already exists
    with open('userpasswords.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['username'] == username:
                print("Username already exists. Please try a different username.")
                return False

    hashed_password = hash_password(password)

    # Append new user credentials to the CSV file
    with open('userpasswords.csv', 'a', newline='') as csvfile:
        fieldnames = ['username', 'password']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'username': username, 'password': hashed_password.decode('utf-8')})

    # Set initial balance for the new user
    set_initial_balance(username, initial_balance=100.0)  # You can modify the initial balance as needed

    print("Registration successful. You can now login.")
    return True

def login():
    """ Prompt user for username and password and check them against hashed values """
    print("Hello, and welcome to BlombergBank!")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if check_credentials(username, password):
        after_login_success(username)
        return True
    else:
        print("Invalid username or password.")
        return False

def after_login_success(username):
    """Handle post-login user interactions"""
    print(f"Welcome back, {username}!")
    balance = get_balance(username)
    print(f"Your current balance is: ${balance:.2f}")
    update = input("Do you want to deposit or withdraw money? Type 'deposit' or 'withdraw' or 'no': ")
    if update.lower() == 'deposit':
        amount = float(input("Enter the amount to deposit: "))
        if update_balance(username, amount):
            print("Deposit successful.")
            print(f"New balance: ${get_balance(username):.2f}")
        else:
            print("Deposit failed.")
    elif update.lower() == 'withdraw':
        amount = -float(input("Enter the amount to withdraw: "))
        if update_balance(username, amount):
            print("Withdrawal successful.")
            print(f"New balance: ${get_balance(username):.2f}")
        else:
            print("Withdrawal failed.")

if __name__ == '__main__':
    while True:
        choice = input("Do you want to (1) Login or (2) Sign Up? Enter 1 or 2: ")
        if choice == '1':
            if login():
                break
        elif choice == '2':
            if signup():
                break
        else:
            print("Please enter a valid option (1 or 2).")
