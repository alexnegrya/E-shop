CREATE TABLE categories
(
    id int GENERATED ALWAYS AS IDENTITY,
    name varchar(50),
    /*
    Columns "updated" and "created" not really needed,
    because categories are only name and
    will rarety be updated.
    But I add these columns for the convenience of searching.
    */
    created timestamp,
    updated timestamp,
    parent_category_id integer,
    -- CONSTRAINTS/KEYS
    CONSTRAINT categories_pkey PRIMARY KEY (id),
    CONSTRAINT categories_parent_category_fkey
        FOREIGN KEY (parent_category_id)
            REFERENCES categories(id)
                ON DELETE CASCADE
);
