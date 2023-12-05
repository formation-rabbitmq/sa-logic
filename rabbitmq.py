import pika

from rich import print


def send_message(
    exchange_name,
    exchange_type,
    message,
    routing_key=None,
    passive: bool = False,
    durable: bool = True,
    internal: bool = False,
    auto_delete: bool = False,
    exchange_headers: dict = None,
    message_headers: dict = None
) -> None:
    connection_params = pika.ConnectionParameters(
        host='rabbitmq',
        port=5672,
        credentials=pika.PlainCredentials(username='guest', password='guest')
    )
    connection = pika.BlockingConnection(connection_params)

    channel = connection.channel()

    # Declare an exchange based on the exchange type
    channel.exchange_declare(
        exchange=exchange_name,
        exchange_type=exchange_type,
        durable=durable,
        passive=passive,
        auto_delete=auto_delete,
        internal=internal,
        arguments=exchange_headers
    )

    # Publish the message to the exchange
    properties = pika.BasicProperties(headers=message_headers) if message_headers else None
    channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=message, properties=properties)

    print(f"[x] Sent '{message}' to the {exchange_name} exchange with routing key '{routing_key}'")

    connection.close()


def receive_message(
    queue_name: str,
    passive: bool = False,
    durable: bool = True,
    exclusive: bool = False,
    auto_delete: bool = False,
    headers: dict = None
) -> None:
    connection_params = pika.ConnectionParameters(
        host='rabbitmq',
        port=5672,
        credentials=pika.PlainCredentials(username='guest', password='guest')
    )
    connection = pika.BlockingConnection(connection_params)

    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(
        queue=queue_name,
        passive=passive,
        durable=durable,
        exclusive=exclusive,
        auto_delete=auto_delete,
        arguments=headers
    )

    def callback(ch, method, properties, body: bytes):
        print(f"[x] Received '{body.decode('utf-8')}'")

    print(f"[:] Start listen '{queue_name}'")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
