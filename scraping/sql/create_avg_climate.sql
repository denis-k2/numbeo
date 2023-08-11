CREATE TABLE IF NOT EXISTS avg_climate (
    city_id integer NOT NULL,
    month smallint NOT NULL,
    {climate_params}
    sys_updated_date date,
    sys_updeted_by varchar(30),
    CONSTRAINT pk_avg_climate PRIMARY KEY (city_id, month),
    CONSTRAINT fk_city_id FOREIGN KEY (city_id) REFERENCES public.city (city_id)
);