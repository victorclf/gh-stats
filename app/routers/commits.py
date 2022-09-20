from fastapi import APIRouter

router = APIRouter(
    prefix="/commits",
    tags=["commits"]
)


@router.get("/")
async def main():
    return 'TODO'
