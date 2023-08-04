from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, Path
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/city", response_model=list[schemas.City])
def read_city_list(
        alpha_3: Annotated[str | None, Query(min_length=3, max_length=3)] = None,
        db: Session = Depends(get_db)):
    """
    Returns a list of all cities that are in the numbeo index (database).
    - **alpha_3**: returns a list of cities in the selected country
    """
    if alpha_3:
        db_city_by_country = crud.get_city_by_country(db, alpha_3=alpha_3)
    else:
        db_city_by_country = crud.get_city_list(db)
    if db_city_by_country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return db_city_by_country


@app.get("/country", response_model=list[schemas.Country])
def read_country_list(db: Session = Depends(get_db)):
    """
    Returns a list of all countries with their codes (Alpha-3 ISO 3166-1).
    """
    db_country_list = crud.get_country_list(db)
    return db_country_list


@app.get("/city/{city_id}", response_model=schemas.CityComplete)
def read_city(
        city_id: int,
        numbeo_cost: Annotated[bool, None] = None,
        numbeo_indices: Annotated[bool, None] = None,
        avg_climate: Annotated[bool, None] = None,
        db: Session = Depends(get_db)
):
    """
    Select the desired city from the list by path '/city' and enter its id.
    - **numbeo_cost**: returns current (Numbeo) prices in the city
    - **numbeo_indices**: returns Numbeo's indices for the city
    - **avg_climate**: returns the monthly average of the climate parameters
    """
    db_city = crud.get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    result = {}
    result.update(jsonable_encoder(db_city[0]), country=db_city[1])

    if numbeo_cost:
        db_numbeo_cost = [row._asdict() for row in crud.get_numbeo_stat(db, city_id)]
        result["numbeo_cost"] = {
            "currency": "USD",
            "last_update": db_numbeo_cost[0]["updated_date"],
            "prices": db_numbeo_cost
        }
    if numbeo_indices:
        db_numbeo_indices = crud.get_numbeo_city_indices(db, city_id)
        result["numbeo_indices"] = jsonable_encoder(db_numbeo_indices)
    if avg_climate:
        db_avg_climate = crud.get_climate(db, city_id)
        climate_dict = schemas.avg_climate_dict

        for row in db_avg_climate:
            for key in climate_dict.keys():
                if key == "measures":
                    pass
                else:
                    climate_dict[key][row[1]] = getattr(row[0], key)

        result["avg_climate"] = climate_dict
    return result


@app.get("/country/{alpha_3}", response_model=schemas.CountryComplete)
def read_country(
        alpha_3: Annotated[str, Path(min_length=3, max_length=3)],
        numbeo_indices: Annotated[bool, None] = None,
        legatum_indices: Annotated[bool, None] = None,
        db: Session = Depends(get_db)
):
    """
    Enter the alpha-3 code of the desired country.
    View the country code in the path '/country'.
    - **numbeo_indices**: returns Numbeo's indices for the country
    - **legatum_indices**: returns Legatum's rank and score
      for the country by category and year
    """
    db_country = crud.get_country(db, alpha_3=alpha_3)
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    result = jsonable_encoder(db_country)
    if numbeo_indices:
        db_numbeo_ctry_idx = crud.get_numbeo_ctry_idx(db, alpha_3)
        result["numbeo_indices"] = jsonable_encoder(db_numbeo_ctry_idx)
    if legatum_indices:
        db_legatum_idx = crud.get_legatum_idx(db, alpha_3)
        legatum_dict = {}
        for row in jsonable_encoder(db_legatum_idx):
            legatum_dict[row["pillar_name"]] = row
        result["legatum_indices"] = legatum_dict
    return result
