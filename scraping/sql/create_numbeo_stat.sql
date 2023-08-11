CREATE TABLE numbeo_stat (
    stat_id serial NOT NULL,
    city_id integer NOT NULL,
    param_id integer NOT NULL,
    cost numeric(9,2),
    range numrange,
    updated_date date,
    currency text NULL DEFAULT 'USD'::text,
    sys_updated_date date,
    sys_updated_by varchar(30),
    CONSTRAINT PK_stat_id PRIMARY KEY ( stat_id ),
    CONSTRAINT fk_city_id FOREIGN KEY ( city_id ) REFERENCES public.city ( city_id ),
    CONSTRAINT fk_param_id FOREIGN KEY ( param_id ) REFERENCES public.numbeo_param ( param_id )
);