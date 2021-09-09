CREATE TABLE ratings
(
    id int GENERATED ALWAYS AS IDENTITY,
    stars decimal CHECK (stars >= 0 AND stars <= 10) NOT NULL,
    review varchar(500),
    product_id integer NOT NULL,
    client_id integer NOT NULL,
    -- CONSTRAINTS/KEYS
    CONSTRAINT ratings_pkey PRIMARY KEY (id),
    CONSTRAINT ratings_product_fkey
        FOREIGN KEY (product_id)
            REFERENCES products(id),
    CONSTRAINT ratings_client_fkey
        FOREIGN KEY (client_id)
            REFERENCES clients(id)
);
