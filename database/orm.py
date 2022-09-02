from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from .settings import DATABASE
from .models import DeclarativeBase, TelegramUsers, WeatherReports
#dont forget pip install psycopg2


def add_user(tg_user_id):
    engine = create_engine(DATABASE)
    DeclarativeBase.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(TelegramUsers).filter(TelegramUsers.tg_user_id == tg_user_id).first()
    if user is None:
        new_user = TelegramUsers(tg_user_id=tg_user_id)
        session.add(new_user)
        session.commit()
    

def set_user_city(tg_user_id, city):
    engine = create_engine(DATABASE)
    DeclarativeBase.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    stmt = select(TelegramUsers).where(TelegramUsers.tg_user_id == tg_user_id)
    user = session.scalars(stmt).one()
    user.user_city = city
    session.commit()

def create_weather_report(tg_user_id, temp, feels_like, wind_speed, pressure_mm, city):
    engine = create_engine(DATABASE)
    DeclarativeBase.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    user = select(TelegramUsers).where(TelegramUsers.tg_user_id == tg_user_id)
    user_data = session.scalars(user).one()
    new_report = WeatherReports(temp=temp, feels_like=feels_like, wind_speed=wind_speed, pressure_mm=pressure_mm, city=city, owner=user_data.id)
    session.add(new_report)
    session.commit()

#Нaдо переработать функцию, похоже, что нет никакой связи в таблицах
def get_reports(tg_user_id):
    engine = create_engine(DATABASE)
    DeclarativeBase.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    user = select(TelegramUsers).where(TelegramUsers.tg_user_id == tg_user_id)
    user_data = session.scalars(user).one()
    reports = session.query(WeatherReports).filter(WeatherReports.owner == user_data.id)
    return reports

#set_user_sity(12345, 'Калининград')


#add_user(12345)

#create_weather_report(12345, 18, 13, 2, 750, 'Калининград')

#print(get_reports(12345))










'''def main():
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
    main()'''