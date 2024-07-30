from typing import Optional

from sqlmodel import Field, Session,SQLModel, create_engine, select

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    headquarters: str

sqlite_file_name = "/home/franposada/projects/sqlmodel/db/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def create_heroes():
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="SpiderMan", secret_name="Peter Parker")
    hero_3 = Hero(name="Black Widow", secret_name="Natasha Romanoff",age=35)
    hero_4 = Hero(name="SuperMan", secret_name="Clark Kent")
    hero_5 = Hero(name="WonderWoman,", secret_name="Diana Prince",age=30)
    hero_6 = Hero(name="Batman", secret_name="Bruce Wayne",age=40)
    hero_7 = Hero(name="Flash", secret_name="Barry Allen",age=25)

    with Session(engine) as session:  
        session.add(hero_1)  
        session.add(hero_2)  
        session.add(hero_3)
        session.add(hero_4)
        session.add(hero_5)
        session.add(hero_6)
        session.add(hero_7)  

        # print("After adding to the session")  
        # print("Hero 1:", hero_1)  
        # print("Hero 2:", hero_2)  
        # print("Hero 3:", hero_3)  

        session.commit()  

        # print("After committing the session")  
        # print("Hero 1:", hero_1)  
        # print("Hero 2:", hero_2)  
        # print("Hero 3:", hero_3)  

        # print("After committing the session, show IDs")  
        # print("Hero 1 ID:", hero_1.id)  
        # print("Hero 2 ID:", hero_2.id)  
        # print("Hero 3 ID:", hero_3.id)  

        # print("After committing the session, show names")  
        # print("Hero 1 name:", hero_1.name)  
        # print("Hero 2 name:", hero_2.name)  
        # print("Hero 3 name:", hero_3.name)  

        # session.refresh(hero_1)  
        # session.refresh(hero_2)  
        # session.refresh(hero_3)  

        # print("After refreshing the heroes")  
        # print("Hero 1:", hero_1)  
        # print("Hero 2:", hero_2)  
        # print("Hero 3:", hero_3)  
    

    # print("After the session closes")  
    # print("Hero 1:", hero_1)  
    # print("Hero 2:", hero_2)  
    # print("Hero 3:", hero_3)  

def select_heroes():
    with Session(engine) as session:
        statement = select(Hero)
        heroes = session.exec(statement)
        for hero in heroes:
            print(hero)

def select_list_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        print(heroes)

def select_hero_by_name(name: str):
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == name)
        results = session.exec(statement)
        for hero in results:
            print(hero)

def select_first_row():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Deadpond")
        results = session.exec(statement)
        hero = results.first()
        print(hero)

def select_only_one():
    #this will raise an error if there is more than one result. It is a way 
    #to know that the database is not consistent
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Deadpond")
        results = session.exec(statement)
        hero = results.one()
        print(hero)

def select_by_id_using_get(id: int):
    #returns None if the id is not found, not an error
    with Session(engine) as session:
        hero = session.get(Hero, id)
        print(hero)

    # get the same result as this but above is more efficient:
    # with Session(engine) as session:
    #     statement = select(Hero).where(Hero.id == 1)
    #     results = session.exec(statement)
    #     hero = results.first()
    #     print("Hero:", hero)

def select_with_limit():
    with Session(engine) as session:
        statement = select(Hero).limit(2)
        results = session.exec(statement)
        heroes = results.all()
        print(heroes)

def select_with_offset_and_limit(offset: int):
    with Session(engine) as session:
        statement = select(Hero).offset(offset=offset).limit(2)
        results = session.exec(statement)
        heroes = results.all()
        print(heroes)
        
def select_with_where_limit_offset():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.age > 30).offset(1).limit(2)
        results = session.exec(statement)
        heroes = results.all()
        print(heroes)

def update_hero(hero_id: int, new_age: int):
    with Session(engine) as session:
        statement = select(Hero).where(Hero.id == hero_id)
        results = session.exec(statement)
        hero = results.one()
        print("Before update:", hero)

        hero.age = new_age
        session.add(hero) #This puts it in that temporary place in the session before committing.
        session.commit() #This saves the updated hero to the database.
        session.refresh(hero) #Refresh the hero object to have the recent data.
        print("After update:", hero)

def delete_hero(hero_id: int):
    with Session(engine) as session:
        statement = select(Hero).where(Hero.id == hero_id)
        results = session.exec(statement)
        hero = results.one()
        print("Before delete:", hero)

        session.delete(hero)
        session.commit()
        print("After delete:", hero)

        statement = select(Hero).where(Hero.id == hero_id)
        results = session.exec(statement)
        hero = results.first()

        if hero is None:
            print("Hero deleted successfully")



def main():
    create_db_and_tables()
    create_heroes()
    select_heroes()

if __name__ == "__main__":
    main()