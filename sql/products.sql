CREATE TABLE products
(
    id integer,
    name varchar(100),
    created timestamp,
    updated timestamp,
    category_id integer NOT NULL,
    price_id integer NOT NULL,
    -- CONSTRAINTS/KEYS
    CONSTRAINT products_pkey PRIMARY KEY (id)
);
