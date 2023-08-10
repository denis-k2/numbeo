from sqlalchemy import select
from sqlalchemy.orm import Session, aliased

import api.models as models

city = aliased(models.City)
country = aliased(models.Country)
n_stat = aliased(models.NumbeoStat)
n_param = aliased(models.NumbeoParam)
n_cat = aliased(models.NumbeoCategory)
ni_city = aliased(models.NumbeoIndexByCity)
ni_country = aliased(models.NumbeoIndexByCountry)


def get_city(db: Session, city_id: int):
    stmt = (
        select(city, country.country)
        .where(city.city_id == city_id)
        .join(country, city.country_code == country.country_code)
    )
    return db.execute(stmt).first()


def get_city_list(db: Session):
    stmt = select(city).order_by(city.city_id)
    return db.scalars(stmt).all()


def get_city_by_country(db: Session, country_code: str):
    stmt = (
        select(city)
        .where(city.country_code == country_code.upper())
        .order_by(city.city_id)
    )
    return db.scalars(stmt).all()


def get_country(db: Session, country_code: str):
    return db.get(models.Country, country_code.upper())  # doesn't work with alias


def get_country_list(db: Session):
    stmt = select(country).order_by(country.country_code)
    return db.scalars(stmt).all()


def get_numbeo_stat(db: Session, city_id: int):
    stmt = (
        select(n_cat.category, n_param.param, n_stat.cost, n_stat.range, n_stat.updated_date)
        .where(n_stat.city_id == city_id)
        .join(city, n_stat.city_id == city.city_id)
        .join(n_param, n_stat.param_id == n_param.param_id)
        .join(n_cat, n_param.category_id == n_cat.category_id)
    )
    return db.execute(stmt).all()


def get_numbeo_city_indices(db: Session, city_id: int):
    stmt = select(ni_city).where(ni_city.city_id == city_id)
    return db.scalar(stmt)


def get_climate(db: Session, city_id: int):
    stmt = select(models.AvgClimate, models.Month.month_name) \
        .where(models.AvgClimate.city_id == city_id) \
        .join(models.Month, models.AvgClimate.month == models.Month.month_id) \
        .order_by(models.AvgClimate.month)
    return db.execute(stmt).all()


def get_numbeo_ctry_idx(db: Session, country_code: int):
    stmt = select(ni_country).where(ni_country.country_code == country_code.upper())
    return db.scalar(stmt)


def get_legatum_idx(db: Session, country_code: str):
    stmt = select(models.LegatumIndex).where(models.LegatumIndex.country_code == country_code.upper())
    return db.scalars(stmt).all()
