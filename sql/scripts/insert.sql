-- !!! In this script, queries are written for TEST-ONLY database tables for project models !!!


-- ! With this syntax is important to observe sequence of inserting data !
/* 
    First needed to insert category and money because product columns
    "category_id" and "price_id" need categories.id and money.id
*/


-- Inserting addresses
-- Mix Markt (supermarket)
INSERT INTO addresses(country, city, street, number)
VALUES('Germany', '12679 Berlin, Carree Marzahn', 'Jan-Petersen-Straße', '18');
-- SELA (clothing store)
INSERT INTO addresses(country, city, street, number)
VALUES('Россия 628611, Ханты-Мансийский АО - Югра', 'г. Нижневартовск', 'ул. Ленина', '15/1');
-- NL Collection (shoe store)
INSERT INTO addresses(country, city, street, number)
VALUES('Moldova', 'Chișinău 2001', 'Bulevardul Ștefan cel Mare și Sfînt', '62');

-- Inserting shops
INSERT INTO shops(working_hours, address_id) VALUES
(
    '{{00:00:00, 23:59:999, 23:59:999}, {00:00:00, 23:59:999, 23:59:999}, {00:00:00, 23:59:999, 23:59:999}, 
    {00:00:00, 23:59:999, 23:59:999}, {00:00:00, 23:59:999, 23:59:999}, {00:00:00, 23:59:999, 23:59:999}, 
    {00:00:00, 23:59:999, 23:59:999}}', 1
);
INSERT INTO shops(working_hours, address_id) VALUES
(
    '{{10:00:00, 18:00:00, 08:00:00}, {10:00:00, 18:00:00, 08:00:00}, {10:00:00, 18:00:00, 08:00:00}, 
    {10:00:00, 18:00:00, 08:00:00}, {10:00:00, 18:00:00, 08:00:00}, {10:00:00, 16:00:00, 06:00:00}, 
    {10:00:00, 16:00:00, 06:00:00}}', 2
);
INSERT INTO shops(working_hours, address_id) VALUES
(
    '{{08:00:00, 19:00:00, 11:00:00}, {08:00:00, 19:00:00, 11:00:00}, {08:00:00, 19:00:00, 11:00:00}, 
    {08:00:00, 19:00:00, 11:00:00}, {08:00:00, 19:00:00, 11:00:00}, {00:00:00, 00:00:00, 00:00:00}, 
    {00:00:00, 00:00:00, 00:00:00}}', 3
);

-- Inserting categories
INSERT INTO categories(name, created) VALUES('Smartphones', now());
INSERT INTO categories(name, created) VALUES('Tablets', now());
INSERT INTO categories(name, created) VALUES('Laptops', now());

-- Inserting clients
INSERT INTO clients(full_name, created, address_id) VALUES('Doe John', now(), 1);
INSERT INTO clients(full_name, created, address_id) VALUES('Небесный Алексей', now(), 2);
INSERT INTO clients(full_name, created, address_id) VALUES('Popa Ion', now(),  3);

-- Inserting contacts
INSERT INTO contacts(type, value, client_id) VALUES('phone', '30-2045678956', 1);
INSERT INTO contacts(type, value, client_id) VALUES('email', 'alexeynebo@mail.ru', 2);
INSERT INTO contacts(type, value, client_id) VALUES('gmail', 'ionpopa@gmail.com', 3);

-- Inserting currencies
INSERT INTO currencies VALUES(978, 'EUR', 1, 21.0060);
INSERT INTO currencies VALUES(840, 'USD', 1, 17.7198);
INSERT INTO currencies VALUES(643, 'RUB', 1, 0.2436);

-- Inserting money
-- Money for products
INSERT INTO money(amount, currency_char_code) VALUES(1000,'USD');
INSERT INTO money(amount, currency_char_code) VALUES(1500,'EUR');
INSERT INTO money(amount, currency_char_code) VALUES(1700,'EUR');
INSERT INTO money(amount, currency_char_code) VALUES(15000,'RUB');
INSERT INTO money(amount, currency_char_code) VALUES(60000,'RUB');
INSERT INTO money(amount, currency_char_code) VALUES(2000,'USD');
-- Money for payments
INSERT INTO money(amount, currency_char_code) VALUES(0, 'USD');
INSERT INTO money(amount, currency_char_code) VALUES(0, 'EUR');
INSERT INTO money(amount, currency_char_code) VALUES(0, 'RUB');
-- Money for services
INSERT INTO money(amount, currency_char_code) VALUES(100, 'USD');
INSERT INTO money(amount, currency_char_code) VALUES(50, 'EUR');

-- Inserting services
INSERT INTO services(name, description, price_id)
VALUES('Express delivery', 'Your products will be delivered in 1-3 days.', 10);
INSERT INTO services(name, description, price_id)
VALUES('Delivery to the door', 'Your products will be delivered to the door of your home.', 11);

-- Inserting products
INSERT INTO products(name, created, price_id, category_id) VALUES('iPhone XI', now(), 1, 1);
INSERT INTO products(name, created, price_id, category_id) VALUES('iPhone XII', now(), 2, 1);
INSERT INTO products(name, created, price_id, category_id) VALUES('Lenovo Pad Pro', now(), 3, 2);
INSERT INTO products(name, created, price_id, category_id) VALUES('Lenovo AIII', now(), 4, 2);
INSERT INTO products(name, created, price_id, category_id) VALUES('Acer Gaming Pro X', now(), 5, 3);
INSERT INTO products(name, created, price_id, category_id) VALUES('Asus Ultimate', now(), 6, 3);

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
 Minus - the camera could have been made better for such money', 2, 2);
INSERT INTO ratings(stars, review, product_id, client_id)
VALUES(6, 'Tablet is good for work, has good screen, but it not for games. 
I am upset because I like to play on tablets.', 3, 2);
INSERT INTO ratings(stars, review, product_id, client_id)
VALUES(8, 'I took this tablet, because it has good price. 
It has a big and light screen, good sound and quality camera for your money. 
Who have small incomes and need a tablet, recommend this tablet.', 4, 3);
INSERT INTO ratings(stars, review, product_id, client_id)
VALUES(7, 'Laptop is very good, 
but it was delivered not on time and packed poorly, which is why it was scratched.', 5, 3);

-- Inserting payments
INSERT INTO payments(method, price_id) VALUES('PayPal', 7);
INSERT INTO payments(method, price_id) VALUES('WebMoney', 8);
INSERT INTO payments(method, price_id) VALUES('QIWI', 9);

-- Inserting orders
INSERT INTO orders(created, total_cost_id, payment_id, client_id) VALUES(now(), 7, 1, 1);
INSERT INTO orders(created, total_cost_id, payment_id, client_id) VALUES(now(),8, 2, 2);
INSERT INTO orders(created, total_cost_id, payment_id, client_id) VALUES(now(), 9, 3, 3);

-- Inserting order items
INSERT INTO order_items(quantity, product_id, order_id) VALUES(1, 1, 1);
INSERT INTO order_items(quantity, product_id, order_id) VALUES(1, 6, 1);
INSERT INTO order_items(quantity, product_id, order_id) VALUES(1, 2, 2);
INSERT INTO order_items(quantity, product_id, order_id) VALUES(1, 3, 2);
INSERT INTO order_items(quantity, product_id, order_id) VALUES(1, 4, 3);
INSERT INTO order_items(quantity, product_id, order_id) VALUES(1, 5, 3);

-- Updating orders total cost money
UPDATE money
SET amount = 3000
WHERE id = 7;
UPDATE money
SET amount = 3200
WHERE id = 8;
UPDATE money
SET amount = 75000
WHERE id = 9;


/* ///////////////////////////////// Products references scheme /////////////////////////////////

                                       ----------------------
                                       |     categories     |
                                       | ------------------ |
                                       | id | name          |
                                       | ------------------ |
     --------------------------------> | 1  | 'Smartphones' |
     |                                 ----------------------
     | 
     |                             -------------------------------
     |                             |           money             |
     |                             | --------------------------- |
     |                             | id | amount | currency_code |
     |                             | --------------------------- |
     |                       ----> | 1  | 1000   | 'USD'         |
     |                       | --> | 2  | 1500   | 'USD'         |
     |                       | |   -------------------------------
     |                       | |
     |                       | ---------------------------------------------------------------
     |                       --------------------------------------------------------------- |
     |                                                                                     | |
     |  --------------------------------------------------------------------------------   | |
     |  |                                    products                                  |   | |
     |  | ---------------------------------------------------------------------------- |   | |
     |  | id |     name     |        created        | updated | category_id | price_id |   | |
     |  | ---------------------------------------------------------------------------- |   | |
     |  | 1  | 'iPhone XI'  | '2021-01-01 00:00:01' | null    | 1           | 1        |<--- |
     |  | 2  | 'iPhone XII' | '2021-01-01 00:00:01' | null    | 1           | 2        |<-----
     |  --------------------------------------------------------------------------------  
     |                                                          ^                         
     |                                                          |                     
     ------------------------------------------------------------

*/
