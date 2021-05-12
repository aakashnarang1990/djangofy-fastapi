from fastapi import APIRouter

router = APIRouter()


@router.get("/test_2/", tags=["admin"])
async def route_test2():
    return {"message": "Hello World"}