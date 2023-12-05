from rabbitmq import send_message


if __name__ == "__main__":
	send_message(
		exchange_name="sa.message.queues.direct.logic",
		exchange_type="direct",
		message="Résultat d'analyse de sentiment",
		routing_key="logic"
	)
