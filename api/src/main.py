import json

import pika
import uvicorn
from core.database import get_db_session
from core.settings import settings
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Note
from sqlalchemy.future import select

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def get_index():
    return {"message": "Hello, World!"}


@app.get("/notes/{note_id}")
async def get_note(note_id, db_session=Depends(get_db_session)):
    async with db_session as session:
        result = await session.scalars(select(Note).where(Note.id == int(note_id)))
        return result.unique().one_or_none()


@app.get("/notes")
async def get_notes(db_session=Depends(get_db_session)):
    async with db_session as session:
        notes = await session.scalars(select(Note))
        return list(notes)


@app.post("/notes")
async def create_note(user_id, content, db_session=Depends(get_db_session)):
    async with db_session as session:
        note = Note(content=content, user_id=user_id)
        session.add(note)
        await session.commit()
        return note


@app.post("/images")
def upload_image():
    parameters = pika.ConnectionParameters(host="rabbitmq")

    with pika.BlockingConnection(parameters=parameters) as connection:
        channel = connection.channel()
        channel.queue_declare(queue="local")

        for idx in range(1_000):
            message = {
                "id": idx,
                # "user_name": createName(),
                # "user_email": createEmail(idx),
            }
            body = json.dumps(message)
            channel.basic_publish(exchange="", routing_key="local", body=body)
            print(f"  [x] Message {idx} sent")

        return {"message": "sent"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=True,
    )
