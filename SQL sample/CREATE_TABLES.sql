USE flight_system;

CREATE TABLE airline (
  name varchar(100) PRIMARY KEY
);

CREATE TABLE airport (
  code varchar(100) PRIMARY KEY,
  name varchar(255),
  city varchar(255)
);

CREATE TABLE airplane (
  id varchar(255),
  airline_name varchar(100),
  number_of_seats int,
  PRIMARY KEY (id, airline_name),
  FOREIGN KEY (airline_name) REFERENCES  airline  (name)
);

CREATE TABLE flight (
  flight_number int,
  airline_name varchar(100),
  departure_date varchar(20),
  departure_time varchar(20),
  arrival_airport varchar(100),
  departure_airport varchar(100),
  arrival_date varchar(20),
  arrival_time varchar(255),
  base_price int,
  airplane_id varchar(255),
  status varchar(255),
  PRIMARY KEY ( flight_number,airline_name, departure_date, departure_time, arrival_airport,departure_airport),
  FOREIGN KEY (airline_name) REFERENCES airline (name),
  FOREIGN KEY (arrival_airport) REFERENCES airport(code),
  FOREIGN KEY (departure_airport) REFERENCES airport(code),
  FOREIGN KEY (airplane_id) REFERENCES airplane(id)
);

CREATE TABLE Airline_Staff (
  username varchar(255) PRIMARY KEY,
  password varchar(255),
  first_name varchar(255),
  last_name varchar(255),
  date_of_birth varchar(255),
  airline_name varchar(255),
  FOREIGN KEY (airline_name) REFERENCES airline (name)
);

CREATE TABLE Airline_Staff_phone_number (
  username varchar(255),
  phone_number varchar(255),
  PRIMARY KEY (username, phone_number), 
  FOREIGN KEY (username) REFERENCES Airline_Staff(username)
);


CREATE TABLE customer (
  email varchar(255) PRIMARY KEY,
  name varchar(255),
  password varchar(255),
  building_number int,
  street varchar(255),
  city varchar(255),
  state varchar(255),
  phone_number varchar(255),
  passport_expiration varchar(255),
  passport_country varchar(255),
  date_of_birth varchar(255)
);

CREATE TABLE rate (
  email varchar(255),
  flight_number int,
  departure_date varchar(20),
  departure_time varchar(20),
  airline_name varchar(10),
  ratings int,
  comment varchar(255),
  PRIMARY KEY (email, flight_number, departure_date, departure_time),
  FOREIGN KEY (email) REFERENCES customer (email),
  FOREIGN KEY (flight_number) REFERENCES flight (flight_number),
  FOREIGN KEY (airline_name) REFERENCES airline(name)

);

CREATE TABLE ticket (
  id varchar(255) PRIMARY KEY,
  sold_price float,
  card_type varchar(255),
  card_number int,
  name_on_card varchar(255),
  expiration_date varchar(255),
  purchase_date varchar(255),
  purchase_time varchar(255),
  airline_name varchar(255),
  flight_number int,
  customer_email varchar(255),
  FOREIGN KEY (flight_number) REFERENCES flight (flight_number),
  FOREIGN KEY (airline_name) REFERENCES airline (name),
  FOREIGN KEY (customer_email) REFERENCES customer (email)
  
);



