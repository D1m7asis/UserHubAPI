import asyncio
import json
import logging
from contextlib import asynccontextmanager
import aio_pika
from src.app.db import SessionLocal
from src.app.models.user import UserAction
from src.app.worker.worker_handlers import (
    handle_create,
    handle_update,
    handle_delete,
    handle_read,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("worker")


async def process_message(message: aio_pika.IncomingMessage):
    """Полная обработка сообщений с бизнес-логикой"""
    async with message.process():
        try:
            data = json.loads(message.body.decode())
            action = data.get("action")
            payload = data.get("data", {})

            logger.critical(f"payload {payload}")

            async with SessionLocal() as session:
                if action == UserAction.CREATE:
                    await handle_create(session, payload)
                elif action == UserAction.READ:
                    await handle_read(session, payload.get("user_id"))
                elif action == UserAction.UPDATE:
                    await handle_update(session, payload.get("user_id"), payload)
                elif action == UserAction.DELETE:
                    await handle_delete(session, payload.get("user_id"))
                else:
                    raise ValueError(f"Unknown action: {action}")

                await session.commit()
                logger.info(f"Successfully processed {action} action")

        except Exception as e:
            logger.error(f"Failed to process message: {e}", exc_info=True)
            await message.reject(requeue=False)
            raise


@asynccontextmanager
async def rabbitmq_connection():
    """Контекстный менеджер для подключения к RabbitMQ"""
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
    try:
        yield connection
    finally:
        await connection.close()


async def run_worker():
    """Основной рабочий цикл"""
    while True:
        try:
            async with rabbitmq_connection() as connection:
                channel = await connection.channel()
                queue = await channel.declare_queue("user_actions", durable=True)

                logger.info("Worker started and listening for messages...")
                await queue.consume(process_message)

                # Бесконечный цикл ожидания
                while True:
                    await asyncio.sleep(1)

        except asyncio.CancelledError:
            logger.info("Worker stopped by user")
            break
        except Exception as e:
            logger.error(f"Error occurred: {e}. Restarting in 5 seconds...")
            await asyncio.sleep(5)


async def main():
    """Точка входа с обработкой graceful shutdown"""
    worker_task = asyncio.create_task(run_worker())

    try:
        await worker_task
    except KeyboardInterrupt:
        worker_task.cancel()
        try:
            await worker_task
        except asyncio.CancelledError:
            logger.info("Worker shutdown complete")


if __name__ == "__main__":
    asyncio.run(main())
