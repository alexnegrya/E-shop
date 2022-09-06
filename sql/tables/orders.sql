CREATE TABLE orders
(
    id int GENERATED ALWAYS AS IDENTITY,
    created timestamp,
    updated timestamp,
    payment_id integer NOT NULL UNIQUE,
    client_id integer NOT NULL UNIQUE,
    -- CONSTRAINTS/KEYS
    CONSTRAINT orders_pkey PRIMARY KEY (id),
    CONSTRAINT orders_payment_fkey
        FOREIGN KEY (payment_id)
            REFERENCES payments(id)
                ON DELETE RESTRICT,
    CONSTRAINT orders_client_fkey
        FOREIGN KEY (client_id)
            REFERENCES clients(id)
                ON DELETE CASCADE
);
