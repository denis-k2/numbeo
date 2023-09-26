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
MonthAUX = Base.classes.month_aux  # added the new table (after alembic) in the "automap style"
# ExchangeRate = Base.classes.exchange_rate


# doesn't work
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
#
# class MonthAUX(Base):
#     __tablename__ = "month_aux"
#     __table_args__ = {"extend_existing": True}
#
#     month_id: Mapped[int] = mapped_column(primary_key=True)
#     month_name: Mapped[str]
#
#     parent_month: Mapped[list["AvgClimate"]] = relationship(back_populates="child_month")
#
#
# AvgClimate.child_month: Mapped["MonthAUX"] = relationship(back_populates="parent_month",
#                                                           primaryjoin="AvgClimate.month == MonthAUX.month_id",
#                                                           remote_side=["MonthAUX.month_id"])
