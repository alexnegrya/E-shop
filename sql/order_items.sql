CREATE TABLE order_items
(
    id serial,
    quantity integer NOT NULL,
    order_id integer NOT NULL,
    product_id integer NOT NULL,
    -- CONSTRAINTS/KEYS
    CONSTRAINT order_items_pkey PRIMARY KEY (id),
    CONSTRAINT order_items_order_fkey
        FOREIGN KEY (order_id)
            REFERENCES orders(id),
    CONSTRAINT order_items_product_fkey
        FOREIGN KEY (product_id)
            REFERENCES products(id)
);
