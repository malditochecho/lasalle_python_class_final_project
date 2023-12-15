-- queries to initialize the database

CREATE DATABASE IF NOT EXISTS inn_reservation;

CREATE TABLE IF NOT EXISTS inn_customer (
    id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(30),
    phone_number BIGINT,

    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS  inn_rooms (
    id INT NULL AUTO_INCREMENT,
    room_type VARCHAR(1),
    room_price DECIMAL(5,2),
    availability SMALLINT,

    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS  inn_reservation (
    id INT NOT NULL AUTO_INCREMENT,
    room_type INT,
    customer_id INT,
    accommodation_days SMALLINT,
    cost DECIMAL(5,2),
    checkout TINYINT,

    PRIMARY KEY (id),
    FOREIGN KEY (room_type) REFERENCES inn_rooms(id),
    FOREIGN KEY (customer_id) REFERENCES inn_customer(id)
);

INSERT INTO inn_rooms (room_type, room_price, availability) VALUES ('S', 100, 10);
INSERT INTO inn_rooms (room_type, room_price, availability) VALUES ('P', 150, 5);
INSERT INTO inn_rooms (room_type, room_price, availability) VALUES ('O', 200, 5);
INSERT INTO inn_rooms (room_type, room_price, availability) VALUES ('E', 50, 9);