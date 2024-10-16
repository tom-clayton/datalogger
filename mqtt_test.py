
# mqtt_test.py An exapmle that only logs from MQTT without need for parsing

from datalogger import Logger, run
from mqttlogger import start_mqtt

start_mqtt(
	Logger(
		"mqtt_test",
		["temperature", "humidity"],    
		topic="location1/output"
	)
)

run()
