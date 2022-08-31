-- Need to specify table because categories and products have "name" column
SELECT categories.name, products.name, amount
FROM products
JOIN categories ON products.category_id = categories.id;

-- Full products select with joins
SELECT p.id AS product_id, p.name AS product_name,
c.id AS category_id, c.name AS category_name,
p.price AS price
FROM products AS p
JOIN categories AS c ON p.category_id = c.id
ORDER BY p.price DESC;
