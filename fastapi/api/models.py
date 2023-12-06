from sqlalchemy.ext.automap import automap_base

from api.database import engine

Base = automap_base()

Base.prepare(autoload_with=engine)

AvgClimate = Base.classes.avg_climate
NumbeoCategory = Base.classes.numbeo_category
NumbeoStat = Base.classes.numbeo_stat
LegatumIndex = Base.classes.legatum_index
NumbeoIndexByCountry = Base.classes.numbeo_index_by_country
NumbeoIndexByCity = Base.classes.numbeo_index_by_city
State = Base.classes.state
City = Base.classes.city
NumbeoParam = Base.classes.numbeo_param
Country = Base.classes.country
# ExchangeRate = Base.classes.exchange_rate

# add the new table (after alembic) in the "automap style"
MonthAUX = Base.classes.month_aux
