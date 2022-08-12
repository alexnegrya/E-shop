CREATE TABLE contacts
(
    id int GENERATED ALWAYS AS IDENTITY,
    type varchar(50),
    value varchar(100),
    client_id integer NOT NULL,
    -- CONSTRAINTS/KEYS
    CONSTRAINT contacts_pkey PRIMARY KEY (id),
    CONSTRAINT contacts_client_fkey
        FOREIGN KEY (client_id)
            REFERENCES clients(id)
                ON DELETE CASCADE
);
