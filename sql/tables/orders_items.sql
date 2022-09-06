CREATE TABLE orders_items
(
    id int GENERATED ALWAYS AS IDENTITY,
    quantity integer CHECK (quantity > 0) NOT NULL,
    product_id integer NOT NULL,
    order_id integer NOT NULL,
    -- CONSTRAINTS/KEYS
    CONSTRAINT order_items_pkey PRIMARY KEY (id),
    CONSTRAINT order_items_product_fkey
        FOREIGN KEY (product_id)
            REFERENCES products(id)
                ON DELETE CASCADE,
    CONSTRAINT order_items_order_fkey
        FOREIGN KEY (order_id)
            REFERENCES orders(id)
                ON DELETE CASCADE
);
