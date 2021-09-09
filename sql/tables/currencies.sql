CREATE TABLE currencies
(
    num_code varchar(3) UNIQUE CHECK (char_length(num_code) = 3),
    /*
    Three characters is enought for valutes in standarts:
    1) ISO 3166-1 (two characters)
    2) ISO 4217 (three characters)
    */
    char_code varchar(3) NOT NULL UNIQUE CHECK (char_length(char_code) = 3),
    nominal integer NOT NULL,
    rate numeric(7, 4) NOT NULL,
    -- CONSTRAINTS/KEYS
    CONSTRAINT currencies_pkey PRIMARY KEY (num_code)
);
