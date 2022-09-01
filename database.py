from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#dont forget pip install psycopg2
DATABASE = {
    'drivername': 'postgres', 
    'host': 'localhost',
    'port': '5432',
    'username': 'postgres',
    'password': 'postgres',
    'database': 'test'
}

DeclarativeBase = declarative_base()


class WeatheReports(DeclarativeBase):
    __tablename__ = 'WeatheReports'

    id = Column(Integer, primary_key=True)
    tg_user_id = Column('tg_id', Integer)
    date = Column('date', String)

    def __repr__(self):
        return "".format(self.code)


def main():
    #Создаем объект Engine, который будет использоваться объектами ниже для связи с БД
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/test')
    
    #Метод create_all создает таблицы в БД , определенные с помощью  DeclarativeBase
    DeclarativeBase.metadata.create_all(engine)
    
    # Создаем фабрику для создания экземпляров Session. Для создания фабрики в аргументе 
    # bind передаем объект engine
    Session = sessionmaker(bind=engine)
    
    # Создаем объект сессии из вышесозданной фабрики Session
    session = Session()

    #Создаем новую запись.
    new_post = WeatheReports(tg_id=13654, date="today")
    
    # Добавляем запись
    session.add(new_post)
    
    #Благодаря этой строчке мы добавляем данные а таблицу
    session.commit()
    
    #А теперь попробуем вывести все посты , которые есть в нашей таблице
    for post in session.query(WeatheReports):
        print(post)

if __name__ == "__main__":
    main()