from fastapi import APIRouter, HTTPException, Depends, Body, Path
import aiomysql
from typing import Annotated

from db import get_conn
from dependencies import get_current_user
from schemas.user import CurrentUser, MessageResponse
from schemas.task import TaskCreate, TaskOut, TaskUpdate


router = APIRouter(prefix="/tasks", tags=["Tasks"])




@router.post("/", response_model=TaskOut)
async def create_task(
    task: Annotated[TaskCreate, Body()],
    user: Annotated[CurrentUser, Depends(get_current_user)],
    conn: Annotated[object, Depends(get_conn)]
):
    
    async with conn.cursor() as cursor:
        await cursor.execute(
            "INSERT INTO tasks (title, description, user_id) VALUES (%s,%s,%s)",
            (task.title, task.description, user.user_id)
        )

        task_id = cursor.lastrowid
    
    return TaskOut(
        id=task_id,
        title=task.title,
        description= task.description,
        status= "To Do"
    )





@router.get("/all", response_model=list[TaskOut])
async def get_all_tasks(
    user: Annotated[CurrentUser, Depends(get_current_user)],
    conn: Annotated[object, Depends(get_conn)]
):
    async with conn.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute(
            "SELECT id, title, description, status FROM tasks WHERE user_id = %s",
            (user.user_id,)
        )

        return await cursor.fetchall()
    



@router.delete("/{task_id}", response_model=MessageResponse)
async def delete_task(
    task_id: Annotated[int, Path()],
    user: Annotated[CurrentUser, Depends(get_current_user)],
    conn: Annotated[object, Depends(get_conn)]
):
    async with conn.cursor() as cursor:
        await cursor.execute(
            "DELETE FROM tasks WHERE id=%s AND user_id=%s",
            (task_id, user.user_id)

        )

        if cursor.rowcount == 0:
            raise HTTPException(403, "Not allowed or task not found")
        
    return MessageResponse(message="Task deleted successfully")




@router.put("/{task_id}", response_model=TaskOut)
async def update_task(
    task_id: Annotated[int, Path()],
    user: Annotated[CurrentUser, Depends(get_current_user)],
    data: Annotated[TaskUpdate, Body()],
    conn: Annotated[object, Depends(get_conn)]
):
    
    async with conn.cursor() as cursor:
        
        fields = []
        values = []

        if data.title is not None:
            fields.append("title=%s")
            values.append(data.title)
        
        if data.description is not None:
            fields.append("description=%s")
            values.append(data.description)
        
        if data.status is not None:
            fields.append("status=%s")
            values.append(data.status)

        if not fields:
            raise HTTPException(400, "NO fields to update")
        
        values.extend([task_id, user.user_id])

        query = f"""
        UPDATE tasks SET {', '.join(fields)} WHERE id=%s AND user_id=%s
        """


        await cursor.execute(query, values)

        if cursor.rowcount == 0:
            raise HTTPException(403, "Not allowed or task not found")
        

        return TaskOut(
            id=task_id,
            title=data.title,
            description=data.description,
            status=data.status or "To Do"
        )