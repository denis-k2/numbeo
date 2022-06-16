CREATE TABLE numbeo_categories (
    category_id serial NOT NULL,
    category varchar(40) NOT NULL,
    CONSTRAINT PK_category_id PRIMARY KEY ( category_id )
);