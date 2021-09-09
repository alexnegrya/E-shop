-- Need to specify table because categories and products have "name" column
SELECT categories.name, products.name, amount, currency_code
FROM products
JOIN categories ON products.category_id = categories.id
JOIN money ON products.price_id = money.id;

-- Full products select with joins
SELECT p.id AS product_id, p.name AS product_name,
c.id AS category_id, c.name AS category_name,
m.id AS price_id, m.amount AS price_amount, m.currency_code AS price_currency
FROM products AS p
JOIN categories AS c ON p.category_id = c.id
JOIN money AS m ON p.price_id = m.id
ORDER BY m.amount DESC;
