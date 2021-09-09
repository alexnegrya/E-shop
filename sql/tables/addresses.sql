CREATE TABLE addresses
(
    id int GENERATED ALWAYS AS IDENTITY,
    country varchar(250),
    city varchar(250),
    street varchar(100),
    number varchar(10),
    -- CONSTRAINTS/KEYS
    CONSTRAINT addresses_pkey PRIMARY KEY (id)
);
