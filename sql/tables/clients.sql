CREATE TABLE clients
(
    id int GENERATED ALWAYS AS IDENTITY,
    full_name varchar(50),
    created timestamp,
    updated timestamp,
    address_id integer NOT NULL,
    -- CONSTRAINTS/KEYS
    CONSTRAINT clients_pkey PRIMARY KEY (id),
    CONSTRAINT clients_address_fkey
        FOREIGN KEY (address_id)
            REFERENCES addresses(id)
);
