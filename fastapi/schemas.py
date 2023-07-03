from datetime import date

from pydantic import BaseModel, Field


class NumbeoRange(BaseModel):
    lower: int | float
    upper: int | float


class NumbeoPrice(BaseModel):
    category: str
    params: str
    cost: int | float
    range: NumbeoRange | None


class NumbeoCost(BaseModel):
    currency: str
    last_update: date
    prices: list[NumbeoPrice] = Field(max_items=57)


class NumbeoCityIndex(BaseModel):
    cost_of_living_index: float | None
    rent_index: float | None
    cost_of_living_plus_rent_index: float | None
    groceries_index: float | None
    local_purchasing_power_index: float | None
    quality_of_life_index: float | None
    property_price_to_income_ratio: float | None
    traffic_commute_time_index: float | None
    climate_index: float | None
    safety_index: float | None
    health_care_index: float | None
    pollution_index: float | None


class ClimateMonth(BaseModel):
    january: float | None
    february: float | None
    march: float | None
    april: float | None
    may: float | None
    june: float | None
    july: float | None
    august: float | None
    september: float | None
    october: float | None
    november: float | None
    december: float | None


class AvgClimate(BaseModel):
    high_temp: ClimateMonth
    low_temp: ClimateMonth
    pressure: ClimateMonth
    wind_speed: ClimateMonth
    humidity: ClimateMonth
    rainfall: ClimateMonth
    rainfall_days: ClimateMonth
    snowfall: ClimateMonth
    snowfall_days: ClimateMonth
    sea_temp: ClimateMonth
    daylight: ClimateMonth
    sunshine: ClimateMonth
    sunshine_days: ClimateMonth
    uv_index: ClimateMonth
    cloud_cover: ClimateMonth
    visibility: ClimateMonth
    measures: dict


class City(BaseModel):
    city_id: int
    city: str
    iso_code: str | None
    alpha_3: str

    class Config:
        orm_mode = True


class CityComplete(City):
    country: str
    numbeo_cost: NumbeoCost | None
    numbeo_indices: NumbeoCityIndex | None
    avg_climate: AvgClimate | None


class NumbeoCountryIndex(BaseModel):
    cost_of_living: float | None
    rent: float | None
    cost_of_living_plus_rent: float | None
    groceries: float | None
    restaurant_pric: float | None
    local_purchasing_power: float | None
    quality_of_lif: float | None
    purchasing_power: float | None
    health_car: float | None
    property_price_to_income_ratio: float | None
    traffic_commute_tim: float | None
    pollutio: float | None
    climat: float | None
    avg_salary_usd: float | None
    safety: float | None


class LegatumRank(BaseModel):
    rank_2007: int
    rank_2008: int
    rank_2009: int
    rank_2010: int
    rank_2011: int
    rank_2012: int
    rank_2013: int
    rank_2014: int
    rank_2015: int
    rank_2016: int
    rank_2017: int
    rank_2018: int
    rank_2019: int
    rank_2020: int
    rank_2021: int
    score_2007: str
    score_2008: str
    score_2009: str
    score_2010: str
    score_2011: str
    score_2012: str
    score_2013: str
    score_2014: str
    score_2015: str
    score_2016: str
    score_2017: str
    score_2018: str
    score_2019: str
    score_2020: str
    score_2021: str


class LegatumCategory(BaseModel):
    param1: LegatumRank = Field(alias="Safety and Security")
    param2: LegatumRank = Field(alias="Personal Freedom")
    param3: LegatumRank = Field(alias="Governance")
    param4: LegatumRank = Field(alias="Social Capital")
    param5: LegatumRank = Field(alias="Investment Environment")
    param6: LegatumRank = Field(alias="Enterprise Conditions")
    param7: LegatumRank = Field(alias="Infrastructure and Market Access")
    param8: LegatumRank = Field(alias="Economic Quality")
    param9: LegatumRank = Field(alias="Living Conditions")
    param10: LegatumRank = Field(alias="Health")
    param11: LegatumRank = Field(alias="Education")
    param12: LegatumRank = Field(alias="Natural Environment")


class Country(BaseModel):
    alpha_3: str
    country: str

    class Config:
        orm_mode = True


class CountryComplete(Country):
    numbeo_indices: NumbeoCountryIndex | None
    legatum_indices: LegatumCategory | None


# dictionary template to create the 'avg_climate' json-response in main.py
avg_climate_dict = {
    "high_temp": {},
    "low_temp": {},
    "pressure": {},
    "wind_speed": {},
    "humidity": {},
    "rainfall": {},
    "rainfall_days": {},
    "snowfall": {},
    "snowfall_days": {},
    "sea_temp": {},
    "daylight": {},
    "sunshine": {},
    "sunshine_days": {},
    "uv_index": {},
    "cloud_cover": {},
    "visibility": {},
    "measures":
        {
            "high_temp": "Average high temperature, °C",
            "low_temp": "Average low temperature, °C",
            "pressure": "Average pressure, mbar",
            "wind_speed": "Average wind speed, km/h",
            "humidity": "Average humidity, %",
            "rainfall": "Average rainfall, mm",
            "rainfall_days": "Average rainfall days, days",
            "snowfall": "Average snowfall, mm",
            "snowfall_days": "Average snowfall days, days",
            "sea_temp": "Average sea temperature, °C",
            "daylight": "Average daylight, hours",
            "sunshine": "Average sunshine, hours",
            "sunshine_days": "Average sunshine days, days",
            "uv_index": "Average UV index",
            "cloud_cover": "Average cloud cover, %",
            "visibility": "Average visibility, km"
        }
}
