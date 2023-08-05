from sqlalchemy import select
from sqlalchemy.orm import Session, aliased
import api.models as models

c = aliased(models.City)
ns = aliased(models.NumbeoStat)
np = aliased(models.NumbeoParam)
nc = aliased(models.NumbeoCategory)
nci = aliased(models.NumbeoIndexByCountry)


def get_city(db: Session, city_id: int):
    stmt = (
        select(models.City, models.Country.country)
        .where(models.City.city_id == city_id)
        .join(models.Country, models.City.alpha_3 == models.Country.alpha_3)
    )
    return db.execute(stmt).first()


def get_city_list(db: Session):
    stmt = select(models.City).order_by(models.City.city_id)
    return db.scalars(stmt).all()


def get_city_by_country(db: Session, alpha_3: str):
    stmt = (
        select(models.City)
        .where(models.City.alpha_3 == alpha_3.upper())
        .order_by(models.City.city_id)
    )
    return db.scalars(stmt).all()


def get_country(db: Session, alpha_3: str):
    return db.get(models.Country, alpha_3.upper())


def get_country_list(db: Session):
    stmt = select(models.Country).order_by(models.Country.alpha_3)
    return db.scalars(stmt).all()


def get_numbeo_stat(db: Session, city_id: int):
    stmt = (
        select(nc.category, np.params, ns.cost, ns.range, ns.updated_date)
        .where(ns.city_id == city_id)
        .join(c, ns.city_id == c.city_id)
        .join(np, ns.param_id == np.param_id)
        .join(nc, np.category_id == nc.category_id)
    )
    return db.execute(stmt).all()


def get_numbeo_city_indices(db: Session, city_id: int):
    stmt = select(models.NumbeoRankByCity).where(models.NumbeoRankByCity.city_id == city_id)
    return db.scalar(stmt)


def get_climate(db: Session, city_id: int):
    stmt = select(models.AvgClimate, models.Month.month_name) \
        .where(models.AvgClimate.city_id == city_id) \
        .join(models.Month, models.AvgClimate.month == models.Month.month_id) \
        .order_by(models.AvgClimate.month)
    return db.execute(stmt).all()


def get_numbeo_ctry_idx(db: Session, alpha_3: int):
    stmt = select(nci).where(nci.alpha_3 == alpha_3.upper())
    return db.scalar(stmt)


def get_legatum_idx(db: Session, area_code: str):
    stmt = select(models.LegatumIndex).where(models.LegatumIndex.area_code == area_code.upper())
    return db.scalars(stmt).all()
