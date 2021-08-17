CREATE TABLE categories
(
    id integer,
    name varchar(50),
    /*
    Columns "updated" and "created" not really needed,
    because categories are only name and
    will rarety be updated.
    But I add these columns for the convenience of searching.
    */
    created timestamp,
    updated timestamp,
    -- CONSTRAINTS/KEYS
    CONSTRAINT categories_pkey PRIMARY KEY (id)
);
