CREATE TABLE shops
(
    id int GENERATED ALWAYS AS IDENTITY,
    working_hours time[7][2] CHECK (cardinality(working_hours) = 14),
    address_id integer NOT NULL,
    -- CONSTRAINTS/KEYS
    CONSTRAINT shops_pkey PRIMARY KEY (id),
    CONSTRAINT shops_address_fkey
        FOREIGN KEY (address_id)
            REFERENCES addresses(id)
                ON DELETE RESTRICT
);
