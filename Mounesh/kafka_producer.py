from confluent_kafka import Producer
import json

# Kafka producer configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'python-producer'
}

producer = Producer(conf)

def send_message(sender, recipient, message):
    data = {
        "sender": sender,
        "recipient": recipient,
        "message": message
    }
    producer.produce('sample-topic', value=json.dumps(data), callback=delivery_report)
    producer.flush()

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

if __name__ == "__main__":
    send_message("user1", "user2", "Hello from user1!")
