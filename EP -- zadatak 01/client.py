import paho.mqtt.client as mqtt

# MQTT broker information
broker_address = "localhost"
broker_port = 1883
topics = ['control', 'stamping', 'bodyshop', 'assembly']

# Callback function when a message is received
def on_message(client, userdata, msg):
    print(msg.payload.decode())

# MQTT client setup and subscription
client = mqtt.Client()
client.on_message = on_message
client.connect(broker_address, broker_port)
for topic in topics:
    client.subscribe(topic)
client.loop_start()

try:
    while True:
        # Your code here
        pass
except KeyboardInterrupt:
    print("\nKeyboard interrupt received. Exiting...")

# Cleanup
client.loop_stop()
client.disconnect()