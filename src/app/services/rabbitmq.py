import json
import logging
from typing import Optional

import aio_pika

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("rabbitmq")

class RabbitMQService:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection: Optional[aio_pika.RobustConnection] = None
        self.channel: Optional[aio_pika.RobustChannel] = None

    async def connect(self):
        """Устанавливаем соединение с RabbitMQ"""
        self.connection = await aio_pika.connect_robust(self.connection_string)
        self.channel = await self.connection.channel()
        logger.info("Connected to RabbitMQ")

    async def publish(self, queue_name: str, message_data: dict):
        """Публикация сообщения в указанную очередь"""
        if not self.connection or self.connection.is_closed:
            await self.connect()

        message = aio_pika.Message(
            body=json.dumps(message_data).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )

        await self.channel.default_exchange.publish(
            message,
            routing_key=queue_name
        )
        logger.info(f"Message published to {queue_name}")

    async def close(self):
        """Закрытие соединения"""
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
            logger.info("Connection closed")

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()