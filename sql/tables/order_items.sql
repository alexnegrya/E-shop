CREATE TABLE order_items
(
    id int GENERATED ALWAYS AS IDENTITY,
    quantity integer NOT NULL,
    product_id integer NOT NULL UNIQUE,
    order_id integer NOT NULL,
    -- CONSTRAINTS/KEYS
    CONSTRAINT order_items_pkey PRIMARY KEY (id),
    CONSTRAINT order_items_product_fkey
        FOREIGN KEY (product_id)
            REFERENCES products(id),
    CONSTRAINT order_items_order_fkey
        FOREIGN KEY (order_id)
            REFERENCES orders(id)
);
