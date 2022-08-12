CREATE TABLE money
(
    id int GENERATED ALWAYS AS IDENTITY,
    amount integer,
    -- CONSTRAINTS/KEYS
    CONSTRAINT money_pkey PRIMARY KEY (id)
);
