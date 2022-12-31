INSERT INTO airline VALUES ('China Eastern');
INSERT INTO airport VALUES ('JFK', 'John F. Kennedy', 'New York');
INSERT INTO airport VALUES ('PVG', 'Shanghai Pudong Internatial', 'Shanghai');
INSERT INTO customer VALUES ('sy3031@nyu.edu', 'Chenny' , 'Chenny12345', '370', 'Jay Street', 'Brooklyn', 'NY', '201-410-3608', 'December 20, 2025', 'USA', 'September 11, 2002');
INSERT INTO customer VALUES ('pl1234@nyu.edu', 'Phil' , 'Phil12345', '371', 'Jay Street', 'Brooklyn', 'NY', '201-411-3618', 'December 25, 2025', 'USA', 'March 25, 2002');
INSERT INTO customer VALUES ('jl3456@nyu.edu', 'Joe' , 'Joe12345', '320', 'Jay Street', 'Brooklyn', 'NY', '201-956-2291', 'December 25, 2023', 'USA', 'December 10, 2001');
INSERT INTO airplane VALUES ('123', 'China Eastern', '500');
INSERT INTO airplane VALUES ('234', 'China Eastern', '700');
INSERT INTO airplane VALUES ('345', 'China Eastern', '650');
INSERT INTO airline_staff VALUES ('Johnny1235', 'fioanfo1', 'Johnny', 'Adams', 'September 13, 1984', 'China Eastern');
INSERT INTO flight VALUES (12345,'China Eastern', '2018-01-01', '3:00 p.m.', 'JFK', 'PVG', '2018-01-01', '7:00 p.m.', 200, '123' , 'delayed');
INSERT INTO flight VALUES (23456,'China Eastern', '2018-01-01', '2:00 p.m.', 'JFK', 'PVG', 'March 6, 2021', '6:00 p.m.', 250, '123' , 'on time');
INSERT INTO ticket VALUES ('948412', 250.0, 'Debit',40454041023920,'Chenny Yun', '06/2022', '2018-01-01','12:00 p.m.', 'China Eastern', 12345, 'sy3031@nyu.edu');

INSERT INTO ticket VALUES ('948413', 250, 'Debit',40454041023920,'Chenny Yun', '06/2022', '2019-01-01','12:00 p.m.', 'China Eastern', 12345, 'sy3031@nyu.edu');
