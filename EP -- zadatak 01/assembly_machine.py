import time
import threading
from datetime import datetime
import paho.mqtt.client as mqtt

def process_command(split_values):
    """
    Processes the command received from the control topic.

    Args:
        split_values (list): The command split into parts.

    """
    print(split_values)
    command = split_values[0]

    if command == 'RUN_TIME':
        processing_time = int(split_values[2])
        machine.processing_time = processing_time
    elif command == 'MESSAGE':
        machine.message = split_values[2]
    elif command == 'STOP':
        client.unsubscribe('stamping')
    elif command == 'START':
        client.subscribe('stamping')

class AssemblyMachine:
    """
    Represents an assembly machine that processes orders.
    """

    def __init__(self, id=3, processing_time=1):
        """
        Initializes an AssemblyMachine object.

        Args:
            id (int): The ID of the assembly machine.
            processing_time (int): The time taken by the machine to process an order.
        """
        self.name = 'Assembly Machine'
        self.id = id
        self.topic = 'assembly'
        self.processing_time = processing_time
        self.message = f'{self.name} - Order processed.'
    
    def run(self, client):
        """
        Simulates the processing of an order by the assembly machine.

        Args:
            client (mqtt.Client): The MQTT client for publishing messages.

        """
        global orders, completed_orders
        print(f"{self.name} - Processing order...")
        time.sleep(self.processing_time)  # Simulating work time
        orders -= 1
        completed_orders += 1
        print(f"{self.name} - Order processed. Remaining orders:", orders)
        print(f"{self.name} - Total orders processed:", completed_orders)
        lock.release()  # Release the lock after completing do_work()
        

        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("[%d.%m.%Y. %H:%M:%S]")

        message = f'{formatted_datetime} - {self.message}'

        client.publish(self.topic, message)

machine = AssemblyMachine()

# MQTT broker information
broker_address = "localhost"
broker_port = 1883
topics = ['control', 'bodyshop']

# Global variables
orders = 0
completed_orders = 0
received_orders = 0
ORDER_LIMIT = 10
lock = threading.Lock()

# Callback function when a message is received
def on_message(client, userdata, msg):
    """
    Callback function triggered when a message is received.

    Args:
        client (mqtt.Client): The MQTT client.
        userdata: User-defined data.
        msg (mqtt.MQTTMessage): The received message.

    """
    global orders, received_orders
    if msg.topic == 'bodyshop':
        orders += 1
        received_orders += 1
        print("New order received. Total orders:", received_orders)

        if lock.acquire(blocking=False):  # Try to acquire the lock
            threading.Thread(target=machine.run, args=(client,)).start()
        else:
            print("Waiting for previous order processing to complete...")
    elif msg.topic == 'control':
        raw_command = msg.payload.decode()
        split_values = raw_command.split("#")
        if split_values[1] != 'ALL':
            id = int(split_values[1])
            if id == machine.id:
                process_command(split_values)
        else:
            process_command(split_values)
    else:
        print('Unkown topic...')

# MQTT client setup and subscription
client = mqtt.Client()
client.on_message = on_message
client.connect(broker_address, broker_port)
for topic in topics:
    client.subscribe(topic)
client.loop_start()

# Main loop to check the order limit
while completed_orders < ORDER_LIMIT:
    time.sleep(0.1)  # Small delay to reduce CPU usage

client.publish(machine.topic, 'NOTICE: ALL MATERIAL PROCESSING COMPLETED!')

# Cleanup
client.loop_stop()
client.disconnect()