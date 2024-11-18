import csv

def get_balance(username):
    """Retrieve the current balance for a user"""
    with open('userbalances.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['username'] == username:
                return float(row['balance'])
    return None  # Return None if the user is not found

def update_balance(username, amount):
    """Update the balance for a user"""
    rows = []
    found = False
    with open('userbalances.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['username'] == username:
                row['balance'] = str(float(row['balance']) + amount)
                found = True
            rows.append(row)

    if found:
        with open('userbalances.csv', 'w', newline='') as csvfile:
            fieldnames = ['username', 'balance']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        return True
    else:
        return False

def set_initial_balance(username, initial_balance=0.0):
    """Set the initial balance for a new user"""
    with open('userbalances.csv', 'a', newline='') as csvfile:
        fieldnames = ['username', 'balance']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'username': username, 'balance': str(initial_balance)})