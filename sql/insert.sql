-- ! With this syntax is important to observe sequence of inserting data !
/* 
    First needed to insert category and money because product columns
    "category_id" and "price_id" need categories.id and money.id
*/

INSERT INTO categories VALUES(1,'Smartphones');

INSERT INTO money VALUES(1,1000,'USD');
INSERT INTO products VALUES(1,'iPhone XI',  '2021-01-01 00:00:01', null, 1,1);

INSERT INTO money VALUES(2,1500,'USD');
INSERT INTO products VALUES(2,'iPhone XII', '2021-01-01 00:00:01', null, 1,2);

/*          
                                       ----------------------
                                       |     categories     |
                                       | ------------------ |
                                       | id | name          |
                                       | ------------------ |
     --------------------------------> | 1  | 'Smartphones' |
     |                                 ----------------------
     | 
     |                             -------------------------------
     |                             |           money             |
     |                             | --------------------------- |
     |                             | id | amount | currency_code |
     |                             | --------------------------- |
     |                       ----> | 1  | 1000   | 'USD'         |
     |                       | --> | 2  | 1500   | 'USD'         |
     |                       | |   -------------------------------
     |                       | |
     |                       | ---------------------------------------------------------------
     |                       --------------------------------------------------------------- |
     |                                                                                     | |
     |  --------------------------------------------------------------------------------   | |
     |  |                                    products                                  |   | |
     |  | ---------------------------------------------------------------------------- |   | |
     |  | id |     name     |        created        | updated | category_id | price_id |   | |
     |  | ---------------------------------------------------------------------------- |   | |
     |  | 1  | 'iPhone XI'  | '2021-01-01 00:00:01' | null    | 1           | 1        |<--- |
     |  | 2  | 'iPhone XII' | '2021-01-01 00:00:01' | null    | 1           | 2        |<-----
     |  --------------------------------------------------------------------------------  
     |                                                          ^                         
     |                                                          |                     
     ------------------------------------------------------------
*/
