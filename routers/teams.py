from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select
from database import get_session
from models import Team, TeamCreate, TeamPublic, TeamPublicWithHeroes, TeamUpdate

router = APIRouter(
    prefix="/teams",
    tags=["teams"]
)


@router.post("/", response_model=TeamPublic, status_code=status.HTTP_201_CREATED)
def create_team(*, session: Session = Depends(get_session), team: TeamCreate):
    db_team = Team.model_validate(team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@router.get("/", response_model=list[TeamPublic])
def read_teams(*, session: Session = Depends(get_session), offset: int = 0, limit: int = Query(default=25, le=100)):
    teams = session.exec(select(Team).offset(offset).limit(limit)).all()
    return teams


@router.get("/{team_id}", response_model=TeamPublicWithHeroes)
def read_team(*, session: Session = Depends(get_session), team_id: int):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.patch("/{team_id}", response_model=TeamPublic)
def update_team(*, session: Session = Depends(get_session), team_id: int, team: TeamUpdate):
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    team_data = team.model_dump(exclude_unset=True)
    db_team.sqlmodel_update(team_data)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@router.delete("/{team_id}")
def delete_team(*, session: Session = Depends(get_session), team_id: int):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    session.delete(team)
    session.commit()
    return {"ok": True}
