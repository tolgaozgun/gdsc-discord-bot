
import csv


def check_registered_email(email_to_check, filename='emails.csv'):
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if email_to_check.lower() in [field.lower() for field in row]:
                return True
    return False
