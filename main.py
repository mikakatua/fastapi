from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import init_db
from routers import heroes, teams


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Initializing Database...")
    init_db()
    yield
    # Runs when the app stops (optional)
    print("🛑 Shutting down application...")


app = FastAPI(lifespan=lifespan)

app.include_router(heroes.router)
app.include_router(teams.router)

# Debugging
# import uvicorn
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
