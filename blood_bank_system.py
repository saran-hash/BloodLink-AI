from database import Database
from validator import Validator
from notifier import EmailNotifier, WhatsAppNotifier
import mysql.connector

class BloodRequestSystem:
    def __init__(self):
        self.db = Database()
        if not self.db.get_connection():
            print("❌ Could not connect to database. Exiting.")
            exit(1)
        self.cursor = self.db.get_cursor()
        self.email_notifier = EmailNotifier()
        self.whatsapp_notifier = WhatsAppNotifier()

    def __del__(self):
        self.db.close()

    def add_donor(self):
        print("\n=== Add Donor ===")
        name = input("Donor Name: ")
        phone = input("Phone (+91XXXXXXXXXX): ")
        email = input("Email (optional): ")
        blood_group = input("Blood Group (e.g., O+): ").upper()

        if not Validator.validate_phone(phone):
            print("Invalid phone number format!")
            return

        self.cursor.execute("SELECT * FROM donors WHERE phone = %s", (phone,))
        if self.cursor.fetchone():
            print("Donor with this phone number already exists.")
            return

        try:
            self.cursor.execute("INSERT INTO donors (name, phone, email, blood_group) VALUES (%s, %s, %s, %s)",
                                (name, phone, email, blood_group))
            self.db.commit()
            print(" Donor added successfully!")
        except mysql.connector.Error as err:
            print(f" Failed to add donor: {err}")

    def delete_donor(self):
        print("\n=== Delete Donor ===")
        phone = input("Enter Donor Phone (+91XXXXXXXXXX): ")

        self.cursor.execute("SELECT * FROM donors WHERE phone = %s", (phone,))
        donor = self.cursor.fetchone()

        if donor:
            confirm = input(f"Are you sure you want to delete {donor['name']}? (yes/no): ")
            if confirm.lower() == 'yes':
                self.cursor.execute("DELETE FROM donors WHERE phone = %s", (phone,))
                self.db.commit()
                print(" Donor deleted successfully.")
            else:
                print(" Delete cancelled.")
        else:
            print(" Donor not found.")

    def view_donors(self):
        print("\n=== Donor List ===")
        try:
            self.cursor.execute("SELECT name, phone, email, blood_group FROM donors")
            donors = self.cursor.fetchall()
            if not donors:
                print("No donors found.")
                return
            for donor in donors:
                print(f"Name: {donor['name']} | Phone: {donor['phone']} | Email: {donor['email']} | Blood Group: {donor['blood_group']}")
        except mysql.connector.Error as err:
            print(f" Error retrieving donors: {err}")

    def request_blood(self):
        print("\n=== Request Blood ===")
        patient = input("Patient Name: ")
        hospital = input("Hospital Name: ")
        blood_group = input("Required Blood Group (e.g., A+): ").upper()
        contact = input("Contact Number (+91XXXXXXXXXX): ")

        if not Validator.validate_phone(contact):
            print(" Invalid contact number")
            return

        self.cursor.execute("SELECT name, phone, email FROM donors WHERE blood_group = %s", (blood_group,))
        donors = self.cursor.fetchall()

        if not donors:
            print(" No donors found with this blood group")
            return

        for donor in donors:
            message = f"🚨 URGENT: Blood needed for {patient} ({blood_group}) at {hospital}. Contact: {contact}"
            self.whatsapp_notifier.send_notification(donor['phone'], message)
            if donor['email']:
                self.email_notifier.send_notification(donor['email'], donor['name'], patient, blood_group, hospital, contact)

        print("✅ Request processed & donors notified!")
