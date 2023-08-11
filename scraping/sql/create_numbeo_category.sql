CREATE TABLE numbeo_category (
    category_id serial NOT NULL,
    category varchar(40) NOT NULL,
    CONSTRAINT PK_category_id PRIMARY KEY ( category_id )
);