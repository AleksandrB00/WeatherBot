from sqlalchemy import create_engine, Column, Integer, String, DateTime,  ForeignKey
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from config import DATABASE
from datetime import datetime
#dont forget pip install psycopg2

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

def main():
    #Создаем объект Engine, который будет использоваться объектами ниже для связи с БД
    engine = create_engine(DATABASE)
    
    #Метод create_all создает таблицы в БД , определенные с помощью  DeclarativeBase
    DeclarativeBase.metadata.create_all(engine)
    
    # Создаем фабрику для создания экземпляров Session. Для создания фабрики в аргументе 
    # bind передаем объект engine
    Session = sessionmaker(bind=engine)
    
    # Создаем объект сессии из вышесозданной фабрики Session
    session = Session()

    #Создаем новую запись.
    new_user = TelegramUsers(tg_user_id=13654, user_city=None, reports=[WeatherReports(temp=20, feels_like=15, wind_speed=2, pressure_mm=760, city='Калининград')])
    
    # Добавляем запись
    session.add(new_user)
    
    #Благодаря этой строчке мы добавляем данные а таблицу
    session.commit()
    
    #А теперь попробуем вывести все посты , которые есть в нашей таблице
    #for data in session.query(TelegramUsers):
        #print(data)

if __name__ == "__main__":
    main()