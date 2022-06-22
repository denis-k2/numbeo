CREATE TABLE avg_climate (
    city_id integer NOT NULL,
    month smallint NOT NULL,
    {climate_params}
    sys_updated_date date,
    sys_updeted_by varchar(30),
    CONSTRAINT fk_city_id FOREIGN KEY (city_id) REFERENCES public.cities (city_id)
);