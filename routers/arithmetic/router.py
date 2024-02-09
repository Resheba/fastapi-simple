from typing import Annotated
from uuid import UUID
from celery.result import AsyncResult
from fastapi import APIRouter, Path, Query

from .schemas import TaskBaseSchema
from .tasks import ArithmTaskManager, TaskType


router: APIRouter = APIRouter(
    prefix='/arithm',
    tags=['Arithmetic']
    )


@router.get('/status',
            tags=['get'],
            response_model=TaskBaseSchema,
            name='Получить статус задачи'
            )
async def arithm_status_get(task_id: Annotated[UUID, Query(alias='task')]):
    task: AsyncResult = AsyncResult(id=str(task_id))
    return TaskBaseSchema(
        id=task.id,
        status=task.status,
        result=task.get() if task.successful() else None
    )


@router.get('/create/{task_type}',
            tags=['get'],
            response_model=TaskBaseSchema,
            name='Создать задачу'
            )
async def arithm_create_get(task_type: Annotated[TaskType, Path()], a: Annotated[int, Query()], b: Annotated[int, Query()]):
    task_func = getattr(ArithmTaskManager, task_type.value)
    task: AsyncResult = task_func.delay(a, b)
    return TaskBaseSchema(id=task.id, status=task.status)
