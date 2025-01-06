
# mqttlogger.py only import if mqtt logging is required.

from datalogger import Logger
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
KEEPALIVE = 60

loggers = []

def on_connect(client, userdata, flags, rc, properties):
    """(re)subscribe to all topics"""
    for logger in loggers:
        client.subscribe(logger.topic)

def on_message(self, userdata, msg):
    """direct messge to relevant logger"""
    for logger in loggers:
        if msg.topic == logger.topic:
            logger.callback(msg.payload.decode())

def start_mqtt(new_loggers, broker=BROKER, port=PORT):
    """register loggers, connect to broker and start loop thread"""
    
    loggers.extend(
        [new_loggers] if isinstance(new_loggers, Logger) else new_loggers
    )
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port, KEEPALIVE)
    print(
        f"MQTT loggers started: {', '.join([l.name for l in loggers])}"
    )
    client.loop_start()

