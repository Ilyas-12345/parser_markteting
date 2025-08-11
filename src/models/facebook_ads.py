from datetime import datetime

from sqlalchemy import Integer, TIMESTAMP, String, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column

from src.db.Base import Base


class FacebookAds(Base):
    __tablename__ = 'facebook_ads_stats'
    __table_args__ = {'schema': 'stats'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date_parsing: Mapped[datetime] = mapped_column(TIMESTAMP)
    article: Mapped[str] = mapped_column(String, nullable=True)
    reach: Mapped[int] = mapped_column(Integer, nullable=True)
    spending: Mapped[float] = mapped_column(DECIMAL, nullable=True)
    clicks: Mapped[int] = mapped_column(Integer, nullable=True)
