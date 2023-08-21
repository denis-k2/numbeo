from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

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


class Month(Base):
    __tablename__ = "month_aux"
    __table_args__ = {'extend_existing': True}

    month: Mapped[int] = mapped_column(primary_key=True)
    month_name: Mapped[str]
