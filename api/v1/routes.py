from fastapi import APIRouter, Depends, HTTPException
from api.v1.implementations import schemas, use_cases

api_router = APIRouter(
    prefix="",
    tags=["land"]
)


@api_router.post("/land/")
async def create_land():
    response = await use_cases.create_land_use_case()
    return response


@api_router.get("/land/")
async def get_land():
    response = await use_cases.get_land_use_case()
    return response


@api_router.put("/land/insert/")
async def insert_action(location: schemas.InsertAction):
    response = await use_cases.insert_content_use_case(location)
    return response


@api_router.put("/land/action/attack/")
async def attack_action(location: schemas.AttackAction):
    response = await use_cases.attack_use_case(location)
    return response


@api_router.put("/land/action/move/")
async def move_action(move: schemas.MoveAction):
    response = await use_cases.move_entity_use_case(move)
    return response


@api_router.delete("/land/")
async def delete_land():
    response = await use_cases.destroy_land_use_case()
    return response
