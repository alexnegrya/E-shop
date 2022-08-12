CREATE TABLE shops
(
    id int GENERATED ALWAYS AS IDENTITY,
    working_hours time[7][3] CHECK (cardinality(working_hours) = 21),
    address_id integer NOT NULL,
    -- CONSTRAINTS/KEYS
    CONSTRAINT shops_pkey PRIMARY KEY (id),
    CONSTRAINT shops_address_fkey
        FOREIGN KEY (address_id)
            REFERENCES addresses(id)
                ON DELETE RESTRICT
);
