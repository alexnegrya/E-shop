CREATE TABLE services
(
    id int GENERATED ALWAYS AS IDENTITY,
    name varchar(50) NOT NULL UNIQUE,
    description varchar(250),
    price_id integer NOT NULL,
    -- CONSTRAINTS/KEYS
    CONSTRAINT services_pkey PRIMARY KEY (id),
    CONSTRAINT services_price_fkey
        FOREIGN KEY (price_id)
            REFERENCES money(id)
                ON DELETE RESTRICT
);
