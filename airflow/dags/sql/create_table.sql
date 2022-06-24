CREATE TABLE IF NOT EXISTS exchange_rates (
	currency varchar(3) NOT NULL DEFAULT 'USD'::character varying,
	byn numeric(8, 3) NOT NULL,
    eur numeric(8, 3) NOT NULL,
	rub numeric(8, 3) NOT NULL,
	uah numeric(8, 3) NOT NULL,
	responce_date date NOT NULL
)