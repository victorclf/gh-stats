from fastapi import FastAPI

from app.routers import commits

description = """
GitHub Analytics

"""

app = FastAPI(
    title="gh-stats",
    description=description,
    version="0.0.1",
    contact={
        "name": "victorclf",
    },
)


app.include_router(commits.router)


@app.get("/")
async def root():
    return {"message": "Okie Dokie"}
