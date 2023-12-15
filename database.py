import mysql.connector

# Create a connection to the MySQL database
connection = mysql.connector.connect(
    host="localhost", user="root", password="lasalle2022", database="inn_reservation"
)


# inn_customer
def create_customer(customer):
    cursor = connection.cursor()
    query = "INSERT INTO inn_customer (first_name, last_name, email, phone_number) VALUES (%s, %s, %s, %s)"
    cursor.execute(
        query,
        (
            customer["first_name"],
            customer["last_name"],
            customer["email"],
            customer["phone_number"],
        ),
    )
    connection.commit()
    return cursor.lastrowid


def check_if_customer_exists(phone_number):
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM inn_customer WHERE phone_number = %s"
    cursor.execute(query, (phone_number,))
    result = cursor.fetchone()
    if result is None:
        return None
    else:
        return result["id"]


# inn_rooms
def get_room_type_id(room_type):
    cursor = connection.cursor()
    query = "SELECT id FROM inn_rooms WHERE room_type = %s"
    cursor.execute(query, (room_type,))
    result = cursor.fetchone()
    return result[0]


def increase_room_availability(room_type):
    cursor = connection.cursor()
    query = "UPDATE inn_rooms SET availability = availability + 1 WHERE room_type = %s"
    cursor.execute(query, (room_type,))
    connection.commit()


def decrease_room_availability(room_type):
    cursor = connection.cursor()
    query = "UPDATE inn_rooms SET availability = availability - 1 WHERE room_type = %s"
    cursor.execute(query, (room_type,))
    connection.commit()


def get_room_type_full_name(room_type):
    if room_type == "P":
        return "Premium"
    elif room_type == "S":
        return "Standard"
    elif room_type == "E":
        return "Economy"
    elif room_type == "O":
        return "Ocean view"


# inn_reservation
def create_reservation(customer_id, reservation):
    cursor = connection.cursor()
    query = "INSERT INTO inn_reservation (room_type, customer_id, accommodation_days, cost, checkout) VALUES (%s, %s, %s, %s, %s)"
    cost = calculate_reservation_cost(
        reservation["accommodation_days"], reservation["room_type"]
    )
    room_type_id = get_room_type_id(reservation["room_type"])
    cursor.execute(
        query,
        (
            room_type_id,
            customer_id,
            reservation["accommodation_days"],
            cost,
            0,
        ),
    )
    connection.commit()


def get_reservation_info_by_customer_id(customer_id):
    cursor = connection.cursor(dictionary=True)
    query = "SELECT reservation.id, customer.first_name, customer.last_name, reservation.accommodation_days, room.room_type, reservation.cost FROM inn_reservation AS reservation JOIN inn_customer customer ON reservation.customer_id = customer.id JOIN inn_rooms room on reservation.room_type = room.id WHERE customer.id = %s AND reservation.checkout = 0"
    cursor.execute(query, (customer_id,))
    result = cursor.fetchone()
    return result


def check_out_reservation(reservation_id):
    cursor = connection.cursor()
    query = "UPDATE inn_reservation SET checkout = 1 WHERE id = %s"
    cursor.execute(query, (reservation_id,))
    connection.commit()


def calculate_reservation_cost(accommodation_days, room_type):
    cursor = connection.cursor()
    query = "SELECT room_price FROM inn_rooms WHERE room_type = %s"
    cursor.execute(query, (room_type,))
    result = cursor.fetchone()
    return result[0] * int(accommodation_days)


def check_amount_of_available_rooms(room_type):
    cursor = connection.cursor()
    query = "SELECT availability FROM inn_rooms WHERE room_type = %s"
    cursor.execute(query, (room_type,))
    result = cursor.fetchone()
    return result[0]
