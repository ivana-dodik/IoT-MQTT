import time
from datetime import datetime
import paho.mqtt.client as mqtt

def process_command(split_values):
    """
    Process the command received from the control topic.

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
        machine.is_paused = True
    elif command == 'START':
        client.subscribe('stamping')
        machine.is_paused = False

class StampingMachine:
    """
    Represents a stamping machine that creates materials.
    """

    def __init__(self, id, processing_time=4):
        """
        Initializes a StampingMachine object.

        Args:
            id (int): The ID of the stamping machine.
            processing_time (int): The time taken by the machine to create a material.
        """
        self.name = 'Stamping Machine'
        self.id = id
        self.processing_time = processing_time
        self.topic = 'stamping'
        self.message = f'{self.name} - finished creating a material.'
        self.is_paused = False
    
    def run(self, required_products=10):
        """
        Runs the stamping machine to create materials.

        Args:
            required_products (int): The number of materials to be created (default: 10).
        """    
        produced = 0
        while produced < required_products:
            while self.is_paused:
                print('Stamping Machine is paused...')
                time.sleep(1)
            time.sleep(self.processing_time) # Simuliramo proizvodnju materijala/proizvoda
            produced+=1

            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("[%d.%m.%Y. %H:%M:%S]")

            message = f'{formatted_datetime} - {self.message} - ({produced}/{required_products})'
            print(message)
            client.publish(self.topic, message)



# Callback function when a message is received
def on_message(client, userdata, msg):
    if msg.topic == 'control':
        raw_command = msg.payload.decode()
        split_values = raw_command.split("#")
        if split_values[1] != 'ALL':
            id = int(split_values[1])
            if id == machine.id:
                process_command(split_values)
        else:
            process_command(split_values)

broker_address = "localhost"
broker_port = 1883
topic = 'control'

# MQTT client setup and subscription
client = mqtt.Client()
client.on_message = on_message
client.connect(broker_address, broker_port)

client.subscribe(topic)
client.loop_start()

machine = StampingMachine(1)
machine.run()

# Cleanup
client.loop_stop()
client.disconnect()