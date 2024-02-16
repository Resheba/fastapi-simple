from fastapi import APIRouter, Depends


router: APIRouter = APIRouter(
    prefix='/auth',
    tags=['Auth']
)
