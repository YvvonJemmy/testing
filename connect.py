import socket
import json
import datetime
import os
import paho.mqtt.client as mqtt
from dataclasses import dataclass, asdict
from dotenv import load_dotenv
load_dotenv()

@dataclass
class NetworkStats:
    time_lost_connection: str(None)
    time_connected: str(None)
    retries: 0
    
 # environmental variables
MQTT_BROKER_ADDRESS = os.environ.get("MQTT_BROKER_ADDRESS")
MQTT_PORT = os.environ.get("MQTT_PORT")
DEVICE_ID = os.environ.get("DEVICE_ID")

# initializing the client
client = mqtt.Client(DEVICE_ID)
output = NetworkStats(None, None, 0)

def on_log(client, userdata,level,buff):
    print(f"log: {buff}")
    print("Connection failed, retrying" in buff)
    if "retrying " in buff:
        output.retries = output.retries +1
        print (f"retries ={output.retries}")


client.on_log = on_log

## establishing connection
def on_connect(client, userdata, flags, rc):
    # rc is connection result
    output.time_connected = f"{datetime.datetime.now()}"

    print(f"connection_time: {output.time_connected }")
    print(f"Connection returned result: {rc}")
    print("last_connection_time: None")
    print (f"retries = {output.retries}")

    # Send the network stats
    client.publish(f'/stats/health/{DEVICE_ID}/network', payload=json.dumps(asdict(output),default = str), qos=0, retain=False)
   
    output.time_lost_connection = None

client.on_connect = on_connect

# runs when a disconnection occurs
def on_disconnect(client, userdata, rc):

    if rc != 0:
        afterdisconnect = datetime.datetime.now()
        output.time_lost_connection = afterdisconnect
        print("disconnection_time:" + afterdisconnect.strftime(" %H:%M:%S"))
        print("unexpected disconnect ")
       
          
        

client.on_disconnect = on_disconnect

# tries to reconnect
client.reconnect_delay_set(min_delay=5, max_delay=120)

# runs when sending a message
def on_message(client, userdata, message):
    print("Received message '" + str(message.payload) + "' on topic '")

client.on_message = on_message


try:
    client.connect(MQTT_BROKER_ADDRESS, port= int(MQTT_PORT), keepalive=60,
               bind_address="")
    
    client.loop_forever()
    
except ValueError:
    print("Invalid Host. Please check your host connection or your port number.")

except socket.gaierror:
    print("Network Error.please check your internet connection.")

