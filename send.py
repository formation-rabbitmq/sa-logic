import argparse
from rabbitmq import send_message


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-u", "--username", type=str, default="guest")
	parser.add_argument("-p", "--password", type=str, default="guest")
	parser.add_argument("-rp", "--port", type=int, default=5672)  # rabbitmq port
	parser.add_argument("-rk", "--routing_key", type=str, default="")  # routing key
	parser.add_argument("-f", "--not_durable", action="store_true")

	parser.add_argument("-rh", "--host", type=str, required=True)  # rabbitmq host
	parser.add_argument("-n", "--exchange", type=str, required=True)  # exchange name
	parser.add_argument(
		"-t", "--type", type=str, choices=["direct", 'topic', 'headers', 'fanout'], required=True
	)  # exchange type
	parser.add_argument("-m", "--message", type=str, required=True)  # message

	args: argparse.Namespace = parser.parse_args()

	send_message(
		host=args.host,
		port=args.port,
		username=args.username,
		password=args.password,
		exchange_name=args.exchange,
		exchange_type=args.type,
		message=args.message,
		routing_key=args.routing_key,
		durable=False if args.not_durable else True
	)
