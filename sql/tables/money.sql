CREATE TABLE money
(
    id int GENERATED ALWAYS AS IDENTITY,
    amount integer,
    currency_char_code varchar(3) NOT NULL,
    -- CONSTRAINTS/KEYS
    CONSTRAINT money_pkey PRIMARY KEY (id),
    CONSTRAINT money_currency_fkey
        FOREIGN KEY (currency_char_code)
            REFERENCES currencies(char_code)
);
