CREATE TABLE orders
(
    id int GENERATED ALWAYS AS IDENTITY,
    created timestamp,
    updated timestamp,
    total_cost_id integer NOT NULL,
    payment_id integer NOT NULL,
    client_id integer NOT NULL,
    -- CONSTRAINTS/KEYS
    CONSTRAINT orders_pkey PRIMARY KEY (id),
    CONSTRAINT orders_total_cost_fkey
        FOREIGN KEY (total_cost_id)
            REFERENCES money(id),
    CONSTRAINT orders_payment_fkey
        FOREIGN KEY (payment_id)
            REFERENCES payments(id),
    CONSTRAINT orders_client_fkey
        FOREIGN KEY (client_id)
            REFERENCES clients(id)
);
