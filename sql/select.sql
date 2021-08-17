-- Need to specify table because categories and products have "name" column
SELECT categories.name, products.name, amount, currency_code
FROM products
JOIN categories ON products.category_id = categories.id
JOIN money ON products.price_id = money.id;
