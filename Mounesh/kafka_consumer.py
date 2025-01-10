from confluent_kafka import Consumer, KafkaException, KafkaError
import json
from database import store_message

# Kafka consumer configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'message_group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)

def consume_messages():
    consumer.subscribe(['sample-topic'])

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            elif msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print(f"End of partition reached {msg.topic()}/{msg.partition()}")
                else:
                    raise KafkaException(msg.error())
            else:
                data = json.loads(msg.value().decode('utf-8'))
                sender = data['sender']
                recipient = data['recipient']
                message = data['message']
                store_message(sender, recipient, message)
                print(f"Message stored: {data}")

    except KeyboardInterrupt:
        print("Consumer interrupted")
    finally:
        consumer.close()

if __name__ == "__main__":
    consume_messages()
