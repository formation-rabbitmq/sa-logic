import argparse
from pika import BasicProperties

from rabbitmq import receive_message


def callback(ch, method, properties: BasicProperties, body: bytes):
	print("HEADERS", properties.headers, type(properties.headers))


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-u", "--username", type=str, default="guest")
	parser.add_argument("-p", "--password", type=str, default="guest")
	parser.add_argument("-rp", "--port", type=int, default=5672)  # rabbitmq port
	parser.add_argument("-f", "--not_durable", action="store_true")
	parser.add_argument("-q", "--is_quorum", action="store_true")

	parser.add_argument("-rh", "--host", type=str, required=True)  # rabbitmq host
	parser.add_argument("-n", "--queue", type=str, required=True)  # queue name

	args: argparse.Namespace = parser.parse_args()

	receive_message(
		host=args.host,
		port=args.port,
		username=args.username,
		password=args.password,
		queue_name=args.queue,
		message_callback=callback,
		durable=False if args.not_durable else True,
		arguments={"x-queue-type": "quorum"} if args.is_quorum else None
	)
