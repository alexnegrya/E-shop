CREATE TABLE money
(
    id integer,
    amount integer,
    /*
    Three characters is enought for valutes in standarts:
    1) ISO 3166-1 (two characters)
    2) ISO 4217 (three characters)
    */
    currency_code varchar(3),
    -- CONSTRAINTS/KEYS
    CONSTRAINT money_pkey PRIMARY KEY (id)
);
