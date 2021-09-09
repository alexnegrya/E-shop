CREATE TABLE payments
(
    id int GENERATED ALWAYS AS IDENTITY,
    method varchar(100),
    price_id integer NOT NULL,
    -- CONSTRAINTS/KEYS
    CONSTRAINT payments_pkey PRIMARY KEY (id),
    CONSTRAINT payments_price_fkey
        FOREIGN KEY (price_id)
            REFERENCES money(id)
);