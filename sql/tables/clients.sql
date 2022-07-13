CREATE TABLE clients
(
    id int GENERATED ALWAYS AS IDENTITY,
    email varchar(200) UNIQUE,
    first_name varchar(150),
    last_name varchar(150),
    password varchar(150),
    created timestamp,
    updated timestamp,
    address_id integer,
    -- CONSTRAINTS/KEYS
    CONSTRAINT clients_pkey PRIMARY KEY (id),
    CONSTRAINT clients_address_fkey
        FOREIGN KEY (address_id)
            REFERENCES addresses(id)
);
