import ast
import asyncio

import aio_pika
import uvicorn
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager


async def on_message(message: aio_pika.IncomingMessage):
    tracker = ast.literal_eval(message.body.decode("utf-8"))
    print(" ", flush=True)
    print(f"  start {tracker["id"]}", flush=True)
    print(tracker, flush=True)
    await asyncio.sleep(1)
    print(f"  end {tracker["id"]}", flush=True)
    print(" ", flush=True)
    await message.ack()


@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    connection = await aio_pika.connect("amqp://guest:guest@rabbitmq/", loop=loop)
    channel = await connection.channel()
    queue = await channel.declare_queue("local")
    await queue.consume(on_message)
    yield
    await connection.close()


app = FastAPI(lifespan=lifespan)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=3004,
        reload=True,
    )
