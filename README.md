# DESCRIPTION
The project shows how to establish a connection between an mqtt client and a broker
MQTT is a network channel used for communication between two IOT devices
To establish a connection you need a client and a broker.
# REQUIREMENTS

To establish a MQTT connection you need to make some installations
- Install paho 
```
pip install paho-mqtt 
```
- Create an environmental file
- An environmental variable is a variable that can be changed by the system, one does not nned to change it on the code.
create a file with name `.env` 
Example of the contents of a .env file

| The variable           | example                |
| ---------------------- | ---------------------- |
| MQTT_BROKER_ADDRESS    | "broker.emqx.io"       |
| MQTT_PORT              | 1833                   |
| DEVICE_ID              | "device name"          |

