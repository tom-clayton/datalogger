
# pm_logger.py An example of using the datalogger library

from datalogger import Logger, run
from i2clogger import i2c
from adafruit_pm25.i2c import PM25_I2C
from adafruit_htu21d import HTU21D
from mqttlogger import start_mqtt

HEADERS = ["PM10", "PM25", "PM100", "temperature", "humidity"] 
PREPEND_NAME = True

I2C_SENSOR_NAME = "front"
TIMER = 60 * 10

MQTT_SENSOR_NAME = "back"
TOPIC = "back/output"

pm25 = PM25_I2C(i2c, None)
htu21 = HTU21D(i2c)

class I2CLogger(Logger):      
    def collect_data(self):
        """Acquire data from sensor"""
        try:
            data = pm25.read()
        except RuntimeError:
            self.error("pm25 read error")
            return None
        return [
            data["pm10 env"],
            data["pm25 env"],
            data["pm100 env"],
            f"{htu21.temperature:.2f}",
            f"{htu21.relative_humidity:.2f}",
        ]
        
if __name__ == '__main__':
    i2c_logger = I2CLogger(
        I2C_SENSOR_NAME,   
        HEADERS, 
        prepend_name=PREPEND_NAME,
        timer=TIMER
    )
    
    mqtt_logger = Logger(
        MQTT_SENSOR_NAME,
        HEADERS, 
        prepend_name=PREPEND_NAME,
        topic=TOPIC
    )
    
    start_mqtt(mqtt_logger)
    run(i2c_logger)
