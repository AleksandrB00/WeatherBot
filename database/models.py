from sqlalchemy import create_engine, Column, Integer, String, DateTime,  ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


DeclarativeBase = declarative_base()

class TelegramUsers(DeclarativeBase):
    __tablename__ = 'TelegramUsers'

    id = Column(Integer, primary_key=True)
    connection_date = Column(DateTime, default=datetime.now, nullable=False)
    tg_user_id = Column(Integer, nullable=False)
    user_city = Column(String)
    reports = relationship('WeatherReports', cascade="all, delete-orphan")

    def __repr__(self):
        return "".format(self.tg_user_id)


class WeatherReports(DeclarativeBase):
    __tablename__ = 'WeatherReports'

    id = Column(Integer, primary_key=True)
    owner  = Column(Integer, ForeignKey("TelegramUsers.id"), nullable=False)
    date = Column(DateTime, default=datetime.now, nullable=False)
    temp = Column(Integer, nullable=False)
    feels_like = Column(Integer, nullable=False)
    wind_speed = Column(Integer, nullable=False)
    pressure_mm = Column(Integer, nullable=False)
    city = Column(String, nullable=False)


    def __repr__(self):
        return "".format(self.owner)
