CREATE TABLE stock_items
(
    id int GENERATED ALWAYS AS IDENTITY,
    quantity integer,
    product_id integer NOT NULL UNIQUE,
    -- CONSTRAINTS/KEYS
    CONSTRAINT stock_items_pkey PRIMARY KEY (id),
    CONSTRAINT stock_items_product_fkey
        FOREIGN KEY (product_id)
            REFERENCES products(id)
                ON DELETE CASCADE
);
