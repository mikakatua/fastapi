from sqlmodel import Field, Relationship, SQLModel


class RowId(SQLModel):
    id: int | None = Field(default=None, primary_key=True)


class TeamBase(SQLModel):
    name: str = Field(max_length=40, index=True)
    headquarters: str = Field(max_length=40)


class Team(TeamBase, RowId, table=True):
    __tablename__ = "teams"

    heroes: list["Hero"] = Relationship(back_populates="team")


class TeamCreate(TeamBase):
    pass


class TeamPublic(TeamBase):
    id: int


class TeamUpdate(SQLModel):
    name: str | None = None
    headquarters: str | None = None


class HeroBase(SQLModel):
    name: str = Field(max_length=40, index=True)
    secret_name: str = Field(max_length=40)
    age: int | None = Field(default=None, index=True)

    team_id: int | None = Field(default=None, foreign_key="teams.id")


class Hero(HeroBase, RowId, table=True):
    __tablename__ = "heroes"
    hashed_password: str = Field(max_length=64)

    team: Team | None = Relationship(back_populates="heroes")


class HeroCreate(HeroBase):
    password: str = Field(max_length=40)


class HeroPublic(HeroBase):
    id: int


class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None
    password: str | None = None


class HeroPublicWithTeam(HeroPublic):
    team: TeamPublic | None = None


class TeamPublicWithHeroes(TeamPublic):
    heroes: list[HeroPublic] = []
