CREATE TABLE numbeo_params (
    param_id serial NOT NULL,
    category_id int NOT NULL,
    params varchar(100) NOT NULL,
    CONSTRAINT PK_param_id PRIMARY KEY ( param_id ),
    CONSTRAINT fk_category_id FOREIGN KEY ( category_id ) REFERENCES numbeo_categories ( category_id )
);