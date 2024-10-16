
# i2clogger.py only import if i2c logging is required.

import board
import busio

i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

