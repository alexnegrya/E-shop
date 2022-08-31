CREATE TABLE services
(
    id int GENERATED ALWAYS AS IDENTITY,
    name varchar(50) NOT NULL UNIQUE,
    description varchar(250),
    price integer NOT NULL,
    -- CONSTRAINTS/KEYS
    CONSTRAINT services_pkey PRIMARY KEY (id)
);
