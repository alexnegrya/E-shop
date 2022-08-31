CREATE TABLE payments
(
    id int GENERATED ALWAYS AS IDENTITY,
    method varchar(100),
    price integer NOT NULL,
    -- CONSTRAINTS/KEYS
    CONSTRAINT payments_pkey PRIMARY KEY (id)
);