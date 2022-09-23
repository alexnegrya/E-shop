-- ! With this syntax is important to observe sequence of inserting data !
-- First needed to insert category because product column "category_id"
-- needs categories.id


-- Inserting addresses
-- Mix Markt (supermarket)
INSERT INTO addresses(country, city, street, number)
VALUES('Germany', '12679 Berlin, Carree Marzahn', 'Jan-Petersen-Straße', '18');
-- SELA (clothing store)
INSERT INTO addresses(country, city, street, number)
VALUES('Россия 628611, Ханты-Мансийский АО - Югра',
'г. Нижневартовск', 'ул. Ленина', '15/1');
-- NL Collection (shoe store)
INSERT INTO addresses(country, city, street, number)
VALUES('Moldova', 'Chișinău 2001', 'Bulevardul Ștefan cel Mare și Sfînt', '62');

-- Inserting shops
INSERT INTO shops(working_hours, address_id) VALUES
(
    '{{00:00, 23:59}, {00:00, 23:59}, {00:00, 23:59},
    {00:00, 23:59}, {00:00, 23:59}, {00:00, 23:59},
    {00:00, 23:59}}', 1
);
INSERT INTO shops(working_hours, address_id) VALUES
(
    '{{10:00, 18:00}, {10:00, 18:00}, {10:00, 18:00},
    {10:00, 18:00}, {10:00, 18:00}, {10:00, 16:00},
    {10:00, 16:00}}', 2
);
INSERT INTO shops(working_hours, address_id) VALUES
(
    '{{08:00, 19:00}, {08:00, 19:00}, {08:00, 19:00},
    {08:00, 19:00}, {08:00, 19:00}, {00:00, 00:00},
    {00:00, 00:00}}', 3
);

-- Inserting categories
INSERT INTO categories(name, created) VALUES('Smartphones', now());
INSERT INTO categories(name, created) VALUES('Tablets', now());
INSERT INTO categories(name, created) VALUES('Laptops', now());

-- Inserting clients
INSERT INTO clients(email, first_name, last_name, password, created, address_id)
VALUES('johndoe@gmail.com', 'John', 'Doe', 'john1290', now(), 1);
INSERT INTO clients(email, first_name, last_name, password, created, address_id)
VALUES('alexeynebo@mail.ru', 'Алексей', 'Небесный', 'alexeyn_120', now(), 2);
INSERT INTO clients(email, first_name, last_name, password, created, address_id)
VALUES('ionut931@outlook.com', 'Ion', 'Popa', 'IoNpSocial', now(), 3);

-- Inserting contacts
INSERT INTO contacts(type, value, client_id) VALUES('Phone', '30-2045678956',
1);
INSERT INTO contacts(type, value, client_id) VALUES('Telegram', '@alexeynebo',
2);
INSERT INTO contacts(type, value, client_id) VALUES('Gmail', 'ionpopa@gmail.com',
3);

-- Inserting services
INSERT INTO services(name, description, price)
VALUES('Express delivery', 'Your products will be delivered in 1-3 days.', 100);
INSERT INTO services(name, description, price)
VALUES('Delivery to the door',
'Your products will be delivered to the door of your home.', 50);

-- Inserting products
INSERT INTO products(name, created, price, category_id)
VALUES('iPhone XI', now(), 1000, 1);
INSERT INTO products(name, created, price, category_id)
VALUES('iPhone XII', now(), 1500, 1);
INSERT INTO products(name, created, price, category_id)
VALUES('Lenovo Pad Pro', now(), 1700, 2);
INSERT INTO products(name, created, price, category_id)
VALUES('Lenovo AIII', now(), 15000, 2);
INSERT INTO products(name, created, price, category_id)
VALUES('Acer Gaming Pro X', now(), 60000, 3);
INSERT INTO products(name, created, price, category_id)
VALUES('Asus Ultimate', now(), 2000, 3);

-- Inserting stock items
INSERT INTO stock_items(quantity, product_id) VALUES(26, 1);
INSERT INTO stock_items(quantity, product_id) VALUES(54, 2);
INSERT INTO stock_items(quantity, product_id) VALUES(100, 3);
INSERT INTO stock_items(quantity, product_id) VALUES(351, 4);
INSERT INTO stock_items(quantity, product_id) VALUES(30, 5);
INSERT INTO stock_items(quantity, product_id) VALUES(10, 6);

-- Inserting ratings
INSERT INTO ratings(stars, review, product_id, client_id)
VALUES(7, 'Good iPhone, but the price is slightly higher than the quality. 
The sound of the previous model was also better.', 1, 1);
INSERT INTO ratings(stars, review, product_id, client_id)
VALUES(10, 'Very good laptop for gaming and work. I have no complaints.', 6, 1);
INSERT INTO ratings(stars, review, product_id, client_id)
VALUES(9, 'Plus - the price and quality match.
 Minus - the camera could have been made better for that kind of money.', 2, 2);
INSERT INTO ratings(stars, review, product_id, client_id)
VALUES(6, 'Tablet is good for work, has good screen, but it not for games. 
I am upset because I like to play on tablets.', 3, 2);
INSERT INTO ratings(stars, review, product_id, client_id)
VALUES(8, 'I took this tablet, because it has good price. 
It has a big and light screen, good sound and quality camera for this price. 
Who have small incomes and need a tablet, recommend this tablet.', 4, 3);
INSERT INTO ratings(stars, review, product_id, client_id)
VALUES(7, 'Laptop is very good, 
but it was delivered not on time and packed poorly, 
which is why it was scratched.', 5, 3);

-- Inserting payments
INSERT INTO payments(method, price) VALUES('PayPal', 0);
INSERT INTO payments(method, price) VALUES('WebMoney', 0);
INSERT INTO payments(method, price) VALUES('QIWI', 0);

-- Inserting orders
INSERT INTO orders(created, payment_id, client_id) VALUES(now(), 1, 1);
INSERT INTO orders(created, payment_id, client_id) VALUES(now(), 2, 2);
INSERT INTO orders(created, payment_id, client_id) VALUES(now(), 3, 3);

-- Inserting order items
INSERT INTO orders_items(quantity, product_id, order_id) VALUES(1, 1, 1);
INSERT INTO orders_items(quantity, product_id, order_id) VALUES(1, 6, 1);
INSERT INTO orders_items(quantity, product_id, order_id) VALUES(1, 2, 2);
INSERT INTO orders_items(quantity, product_id, order_id) VALUES(1, 3, 2);
INSERT INTO orders_items(quantity, product_id, order_id) VALUES(1, 4, 3);
INSERT INTO orders_items(quantity, product_id, order_id) VALUES(1, 5, 3);

-- Updating orders total cost
UPDATE payments
SET price = 3000
WHERE id = 1;
UPDATE payments
SET price = 3200
WHERE id = 2;
UPDATE payments
SET price = 75000
WHERE id = 3;
