import database
import os


# Read the 'reservation_file.txt' file, add every line into a list and return the list
def read_file(path):
    reservations = []
    with open(path, "r") as file:
        for line in file:
            reservations.append(line.strip())
    return reservations


#  Delete the content of the 'reservation_file.txt' file
def delete_file(path):
    os.remove(path)


def process_file_reservations(path):
    try:
        reservations = read_file(path)
    except FileNotFoundError:
        print("\nThere is no reservation file to process.\n")
        return

    for reservation in reservations:
        # split the line into a dictionary for a customer and a reservation
        customer = {
            "first_name": reservation.split(",")[0],
            "last_name": reservation.split(",")[1],
            "email": reservation.split(",")[2],
            "phone_number": reservation.split(",")[3],
        }
        reservation = {
            "room_type": reservation.split(",")[4],
            "accommodation_days": reservation.split(",")[5],
        }

        # check if customer exists in database and create if it doesn't exist
        customer_id = database.check_if_customer_exists(customer["phone_number"])
        if customer_id == None:
            customer_id = database.create_customer(customer)
        customer["id"] = customer_id

        # create reservation
        database.create_reservation(customer_id, reservation)
        database.decrease_room_availability

    delete_file("reservation_file.txt")


# Check in
def check_in():
    print("\n----------------")
    print("CHECKIN PROCESS")
    print("----------------")
    print("Enter the customer's phone number:")
    phone_number = input()
    # check if customer exists
    customer_id = database.check_if_customer_exists(phone_number)
    if customer_id == None:  # if customer doesn't exist
        print("\n------------")
        print("NEW CUSTOMER")
        print("------------")
        print("Enter the customer's first name:")
        first_name = input()
        print("Enter the customer's last name:")
        last_name = input()
        print("Enter the customer's email:")
        email = input()
        customer = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
        }
        customer_id = database.create_customer(customer)  # create the customer
    else:
        print(f"\nWelcome back!")
    print("\nWhich kind of room would you like to book?")
    print("1. Premium")
    print("2. Standard")
    print("3. Economy")
    print("4. Ocean view")
    room_type = input("\nEnter your choice: ")
    while room_type not in ["1", "2", "3", "4"]:
        print("Invalid choice. Try again.")
        room_type = input("\nEnter your choice: ")
    if room_type == "1":
        room_type = "P"
    elif room_type == "2":
        room_type = "S"
    elif room_type == "3":
        room_type = "E"
    elif room_type == "4":
        room_type = "O"
    availability = database.check_amount_of_available_rooms(room_type)

    # check if there are available rooms of the selected type
    if availability < 1:
        print("There are no available rooms of this type.")
        return  # it should return to the main menu because there are no available rooms
    else:
        print("How many days would you like to stay?")
        accommodation_days = input("\nEnter your choice: ")
        reservation = {
            "room_type": room_type,
            "accommodation_days": accommodation_days,
        }
        database.create_reservation(customer_id, reservation)  # create a reservation
        database.decrease_room_availability(
            room_type
        )  # decrease the availability of the room by one
        print(f"\nCustomer checked-in successfully!\n")


# Check out
def check_out():
    print("\n----------------")
    print("CHECKOUT PROCESS")
    print("----------------")
    print("Enter the customer's phone number:")
    phone_number = input()
    # check if customer exists
    customer_id = database.check_if_customer_exists(phone_number)
    if customer_id == None:  # if customer doesn't exist
        print("Customer doesn't exist.")
        return
    else:  # if customer exists
        reservation = database.get_reservation_info_by_customer_id(customer_id)
        if reservation == None:  # if customer doesn't have a reservation
            print("\nCustomer doesn't have a reservation.\n")
            return
        else:  # if customer has a reservation
            database.check_out_reservation(reservation["id"])
            database.increase_room_availability(reservation["room_type"])
            print("\nCustomer checked out successfully!")
        print("\n-----------------------------")
        print("Your invoice information is: ")
        print("-----------------------------")
        print(f"Name: {reservation['first_name']} {reservation['last_name']}")
        print(f"Accommodation: {reservation['accommodation_days']} days")
        print(
            f"Room Type: {database.get_room_type_full_name(reservation['room_type'])}"
        )
        print(f"Total Cost: CAD${reservation['cost']}")
        print("\nThank you and see you next time!\n")


# Menu
def main_menu():
    print("--------------------------")
    print("WELCOME TO THE LIRS SYSTEM")
    exit_application = False
    while not exit_application:
        print("--------------------------")
        print("Choose an option:")
        print("1. Check-in")
        print("2. Check-out")
        print("3. Exit")
        choice = input("\nEnter your choice: ")

        if choice == "1":
            check_in()
        elif choice == "2":
            check_out()
        elif choice == "3":
            print("Thank you for using the LIRS system.")
            exit_application = True
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    process_file_reservations("reservation_file.txt")
    main_menu()
