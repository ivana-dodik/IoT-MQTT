# python3.6

import random

from paho.mqtt import client as mqtt_client


broker = 'localhost'
port = 1883
topic = "bodyshop"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()

# import time
# import threading
# import paho.mqtt.client as mqtt

# # MQTT broker information
# broker_address = "localhost"
# broker_port = 1883
# topic = "orders"

# # Global variables
# orders = 0
# completed_orders = 0
# received_orders = 0
# ORDER_LIMIT = 10
# lock = threading.Lock()

# # Function to simulate work
# def do_work():
#     global orders, completed_orders
#     print("Processing order...")
#     time.sleep(0.5)  # Simulating work time
#     orders -= 1
#     completed_orders += 1
#     print("Order processed. Remaining orders:", orders)
#     print("Total orders processed:", completed_orders)
#     lock.release()  # Release the lock after completing do_work()

# # Callback function when a message is received
# def on_message(client, userdata, msg):
#     global orders, received_orders
#     orders += 1
#     received_orders += 1
#     print("New order received. Total orders:", received_orders)

#     if lock.acquire(blocking=False):  # Try to acquire the lock
#         threading.Thread(target=do_work).start()
#     else:
#         print("Waiting for previous order processing to complete...")

#     # if completed_orders >= ORDER_LIMIT:
#     #     print("Reached the order limit. Unsubscribing...")
#     #     client.unsubscribe(topic)

# # MQTT client setup and subscription
# client = mqtt.Client()
# client.on_message = on_message
# client.connect(broker_address, broker_port)
# client.subscribe(topic)
# client.loop_start()

# # Main loop to check the order limit
# while completed_orders < ORDER_LIMIT:
#     time.sleep(0.1)  # Small delay to reduce CPU usage

# # Cleanup
# client.loop_stop()
# client.disconnect()
