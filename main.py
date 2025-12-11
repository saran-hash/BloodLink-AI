from blood_bank_system import BloodRequestSystem

def main():
    system = BloodRequestSystem()
    while True:
        print("\n=== Blood Request System ===")
        print("1. Add Donor")
        print("2. Request Blood")
        print("3. Delete Donor")
        print("4. View Donors")
        print("5. Exit")
        choice = input("Choose: ")

        if choice == '1':
            system.add_donor()
        elif choice == '2':
            system.request_blood()
        elif choice == '3':
            system.delete_donor()
        elif choice == '4':
            system.view_donors()
        elif choice == '5':
            print("Exiting")
            break
        else:
            print(" Invalid option")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExited by user.")
