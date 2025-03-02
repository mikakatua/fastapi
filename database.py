import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, Session, create_engine, inspect
from models import Hero, Team

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/database.db")
engine = create_engine(DATABASE_URL, echo=False)


def init_db():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    if len(tables) == 0:
        SQLModel.metadata.create_all(engine)
        create_heroes()


def get_session():
    with Session(engine) as session:
        yield session


def create_heroes():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(
            name="Z-Force", headquarters="Sister Margaret's Bar")

        hero_deadpond = Hero(
            name="Deadpond", secret_name="Dive Wilson", hashed_password="DUMMY", team=team_z_force
        )
        hero_rusty_man = Hero(
            name="Rusty-Man", secret_name="Tommy Sharp", age=48, hashed_password="DUMMY", team=team_preventers
        )
        hero_spider_boy = Hero(
            name="Spider-Boy", secret_name="Pedro Parqueador", hashed_password="DUMMY")
        hero_spider_boy.team = team_preventers
        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        session.commit()

        hero_black_lion = Hero(
            name="Black Lion", secret_name="Trevor Challa", hashed_password="DUMMY", age=35)
        hero_sure_e = Hero(name="Princess Sure-E",
                           secret_name="Sure-E", hashed_password="DUMMY")
        team_wakaland = Team(
            name="Wakaland",
            headquarters="Wakaland Capital City",
            heroes=[hero_black_lion, hero_sure_e],
        )
        session.add(team_wakaland)
        session.commit()

        hero_tarantula = Hero(
            name="Tarantula", secret_name="Natalia Roman-on", hashed_password="DUMMY", age=32)
        hero_dr_weird = Hero(
            name="Dr. Weird", secret_name="Steve Weird", hashed_password="DUMMY", age=36)
        hero_cap = Hero(
            name="Captain North America", secret_name="Esteban Rogelios", hashed_password="DUMMY", age=93
        )

        team_preventers.heroes.append(hero_tarantula)
        team_preventers.heroes.append(hero_dr_weird)
        team_preventers.heroes.append(hero_cap)
        session.add(team_preventers)
        session.commit()
