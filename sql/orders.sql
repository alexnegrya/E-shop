CREATE TABLE orders
(
    id serial,
    created timestamp,
    updated timestamp,
    price_id integer NOT NULL,
    client_id integer NOT NULL,
    -- CONSTRAINTS/KEYS
    CONSTRAINT orders_pkey PRIMARY KEY (id),
    CONSTRAINT orders_price_fkey
        FOREIGN KEY (price_id)
            REFERENCES money(id),
    CONSTRAINT orders_client_fkey
        FOREIGN KEY (client_id)
            REFERENCES clients(id)
);
