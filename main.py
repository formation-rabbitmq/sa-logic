from rabbitmq import receive_message


if __name__ == "__main__":
	receive_message(
		queue_name="sa.message.queues.direct.analyses"
	)
