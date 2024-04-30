import json
import traceback
from asyncio import AbstractEventLoop

import aio_pika
from aio_pika import IncomingMessage
from aio_pika.abc import AbstractRobustConnection

from app.repositories.db_receipt_repo import ReceiptRepo
from app.services.receipt_service import ReceiptService
from app.settings import settings


# async def send_to_receipt_queue(data: dict):
#     try:
#         # Установка соединения с RabbitMQ
#         connection = await aio_pika.connect_robust(settings.amqp_url)
#
#         async with connection:
#             # Создание канала
#             channel = await connection.channel()
#
#             # Объявление очереди, если её нет
#             queue = await channel.declare_queue('receipt_created_queue', durable=True)
#
#             for key, value in data.items():
#                 if isinstance(value, UUID):
#                     data[key] = str(value)
#                 elif isinstance(value, datetime):
#                     data[key] = value.isoformat()
#
#             # Отправка данных в очередь
#             await channel.default_exchange.publish(
#                 aio_pika.Message(body=json.dumps(data).encode()),
#                 routing_key='receipt_created_queue'
#             )
#             print(" [x] Sent %r" % data)
#
#     except aio_pika.exceptions.AMQPError as e:
#         print(f"Error occurred while sending data to queue: {e}")
#
#     finally:
#         # Закрытие соединения после отправки данных в очередь
#         await connection.close()


async def process_created_receipt(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        print("\n/// process_created_receipt ///\n ")
        ReceiptService(ReceiptRepo()).create_receipt(
            data['ord_id'], data['type'], data['rec'], data['customer_info'])
        await msg.ack()
    except:
        traceback.print_exc()
        await msg.ack()


async def consume(loop: AbstractEventLoop) -> AbstractRobustConnection:
    connection = await aio_pika.connect_robust(settings.amqp_url, loop=loop)
    channel = await connection.channel()

    receipt_created_queue = await channel.declare_queue('receipt_created_queue', durable=True)

    await receipt_created_queue.consume(process_created_receipt)

    print('Started RabbitMQ consuming...')

    return connection
