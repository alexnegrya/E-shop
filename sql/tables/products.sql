CREATE TABLE products
(
    id int GENERATED ALWAYS AS IDENTITY,
    name varchar(100),
    created timestamp,
    updated timestamp,
    price_id integer NOT NULL,
    category_id integer NOT NULL,
    -- CONSTRAINTS/KEYS
    CONSTRAINT products_pkey PRIMARY KEY (id),
    CONSTRAINT products_price_fkey
        FOREIGN KEY (price_id)
            REFERENCES money(id),
    CONSTRAINT products_category_fkey
        FOREIGN KEY (category_id)
            REFERENCES categories(id)
);
