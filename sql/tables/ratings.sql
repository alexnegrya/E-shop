CREATE TABLE ratings
(
    id int GENERATED ALWAYS AS IDENTITY,
    stars int CHECK (stars >= 0 AND stars <= 10) NOT NULL,
    review varchar(500),
    created timestamp,
    updated timestamp,
    product_id integer NOT NULL,
    client_id integer NOT NULL,
    -- CONSTRAINTS/KEYS
    CONSTRAINT ratings_pkey PRIMARY KEY (id),
    CONSTRAINT ratings_product_fkey
        FOREIGN KEY (product_id)
            REFERENCES products(id)
                ON DELETE CASCADE,
    CONSTRAINT ratings_client_fkey
        FOREIGN KEY (client_id)
            REFERENCES clients(id)
                ON DELETE CASCADE
);
