import pika

from rich import print


def send_message(
    host: str,
    port: int,
    username: str,
    password: str,
    exchange_name,
    exchange_type,
    message,
    routing_key=None,
    durable: bool = True,
    exchange_headers: dict = None,
    message_headers: dict = None
) -> None:
    connection_params = pika.ConnectionParameters(
        host=host,
        port=port,
        credentials=pika.PlainCredentials(username=username, password=password)
    )
    connection = pika.BlockingConnection(connection_params)

    channel = connection.channel()

    # Declare an exchange based on the exchange type
    channel.exchange_declare(
        exchange=exchange_name,
        exchange_type=exchange_type,
        durable=durable,
        arguments=exchange_headers
    )

    # Publish the message to the exchange
    properties = pika.BasicProperties(headers=message_headers) if message_headers else None
    channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=message, properties=properties)

    print(f"[x] Sent '{message}' to the {exchange_name} exchange with routing key '{routing_key}'")

    connection.close()


def receive_message(
    host: str,
    port: int,
    username: str,
    password: str,
    queue_name: str,
    message_callback,
    durable: bool = True,
    arguments: dict = None
) -> None:
    connection_params = pika.ConnectionParameters(
        host=host,
        port=port,
        credentials=pika.PlainCredentials(username=username, password=password)
    )
    connection = pika.BlockingConnection(connection_params)

    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(
        queue=queue_name,
        durable=durable,
        arguments=arguments
    )

    def callback(ch, method, properties, body: bytes):
        print(f"[x] Received '{body.decode('utf-8')}'")
        message_callback(ch, method, properties, body)

    print(f"[:] Start listen '{queue_name}'")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)
    channel.start_consuming()
