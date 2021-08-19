CREATE TABLE clients
(
    id serial,
    full_name varchar(50),
    created timestamp,
    updated timestamp,
    -- CONSTRAINTS/KEYS
    CONSTRAINT clients_pkey PRIMARY KEY (id)
);
