import json
import os
import re
import csv

FILE_NAME = "contacts.json"


# ---------------- LOAD DATA ----------------
def load_contacts():
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except Exception as e:
        print("Error loading contacts:", e)
        return []


# ---------------- SAVE DATA ----------------
def save_contacts(contacts):
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(contacts, file, indent=4)
    except Exception as e:
        print("Error saving contacts:", e)


# ---------------- GENERATE ID ----------------
def generate_id(contacts):
    return max([c["id"] for c in contacts], default=0) + 1


# ---------------- VALIDATION ----------------
def valid_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)


def valid_phone(phone):
    return phone.isdigit() and 10 <= len(phone) <= 15


# ---------------- DISPLAY ----------------
def display_contacts(data):
    if not data:
        print("No contacts found.")
        return

    print(f"{'ID':<5}{'Name':<20}{'Phone':<15}{'Email':<25}{'City':<15}{'Company'}")
    print("-" * 90)

    for c in data:
        print(f"{c['id']:<5}{c['name']:<20}{c['phone']:<15}{c['email']:<25}{c['city']:<15}{c['company']}")


# ---------------- ADD CONTACT ----------------
def add_contact(contacts):
    print("\n--- Add Contact ---")

    name = input("Name: ").strip()
    phone = input("Phone: ").strip()
    email = input("Email: ").strip()
    city = input("City: ").strip()
    company = input("Company: ").strip()

    if not all([name, phone, email, city, company]):
        print("❌ All fields are required!")
        return

    if not valid_email(email):
        print("❌ Invalid email format!")
        return

    if not valid_phone(phone):
        print("❌ Invalid phone number!")
        return

    contact = {
        "id": generate_id(contacts),
        "name": name,
        "phone": phone,
        "email": email,
        "city": city,
        "company": company
    }

    contacts.append(contact)
    save_contacts(contacts)
    print("✅ Contact added successfully!")


# ---------------- VIEW ----------------
def view_contacts(contacts):
    print("\n--- All Contacts ---")
    display_contacts(contacts)


# ---------------- SEARCH ----------------
def search_contacts(contacts):
    keyword = input("\nEnter search keyword: ").lower()

    results = [
        c for c in contacts
        if keyword in c["name"].lower()
        or keyword in c["phone"]
        or keyword in c["email"].lower()
    ]

    print("\n--- Search Results ---")
    display_contacts(results)


# ---------------- FILTER ----------------
def filter_contacts(contacts):
    print("\n1. Filter by City\n2. Filter by Company")
    choice = input("Choose: ")

    keyword = input("Enter value: ").lower()

    if choice == "1":
        results = [c for c in contacts if keyword in c["city"].lower()]
    elif choice == "2":
        results = [c for c in contacts if keyword in c["company"].lower()]
    else:
        print("❌ Invalid choice")
        return

    print("\n--- Filter Results ---")
    display_contacts(results)


# ---------------- UPDATE ----------------
def update_contact(contacts):
    try:
        cid = int(input("Enter ID to update: "))
    except ValueError:
        print("❌ Invalid ID")
        return

    for c in contacts:
        if c["id"] == cid:
            print("Leave blank to keep old value")

            name = input("New Name: ").strip()
            phone = input("New Phone: ").strip()
            email = input("New Email: ").strip()
            city = input("New City: ").strip()
            company = input("New Company: ").strip()

            if name:
                c["name"] = name
            if phone:
                if not valid_phone(phone):
                    print("❌ Invalid phone!")
                    return
                c["phone"] = phone
            if email:
                if not valid_email(email):
                    print("❌ Invalid email!")
                    return
                c["email"] = email
            if city:
                c["city"] = city
            if company:
                c["company"] = company

            save_contacts(contacts)
            print("✅ Contact updated!")
            return

    print("❌ Contact not found")


# ---------------- DELETE ----------------
def delete_contact(contacts):
    try:
        cid = int(input("Enter ID to delete: "))
    except ValueError:
        print("❌ Invalid ID")
        return

    for c in contacts:
        if c["id"] == cid:
            contacts.remove(c)
            save_contacts(contacts)
            print("✅ Contact deleted!")
            return

    print("❌ Contact not found")


# ---------------- SORT ----------------
def sort_contacts(contacts):
    contacts.sort(key=lambda x: x["name"].lower())
    print("✅ Contacts sorted by name")
    display_contacts(contacts)


# ---------------- EXPORT CSV ----------------
def export_to_csv(contacts):
    if not contacts:
        print("No data to export.")
        return

    try:
        with open("contacts.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=contacts[0].keys())
            writer.writeheader()
            writer.writerows(contacts)
        print("✅ Exported to contacts.csv")
    except Exception as e:
        print("Error exporting:", e)


# ---------------- MAIN MENU ----------------
def main():
    contacts = load_contacts()

    while True:
        print("\n===== CONTACT MANAGER =====")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Search Contacts")
        print("4. Filter Contacts")
        print("5. Update Contact")
        print("6. Delete Contact")
        print("7. Sort Contacts")
        print("8. Export to CSV")
        print("9. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            view_contacts(contacts)
        elif choice == "3":
            search_contacts(contacts)
        elif choice == "4":
            filter_contacts(contacts)
        elif choice == "5":
            update_contact(contacts)
        elif choice == "6":
            delete_contact(contacts)
        elif choice == "7":
            sort_contacts(contacts)
        elif choice == "8":
            export_to_csv(contacts)
        elif choice == "9":
            print("Goodbye 👋")
            break
        else:
            print("❌ Invalid choice")


if __name__ == "__main__":
    main()