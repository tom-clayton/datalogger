
# datalogger.py needs to be imported for all cases

import time
from datetime import datetime
import os

ERRORFILE = "error.txt"

def run(loggers=[]):
    """loop forever, checking given timed loggers if any"""
    if type(loggers) == Logger:
        loggers = [loggers]
    if loggers:
        print (
            f"Timed loggers started: {', '.join([l.name for l in loggers])}"
        )
        
    while True:
        now = time.time()
        for logger in loggers:
            logger.check(now)
            time.sleep(1)
        if not loggers:
            time.sleep(1)
               
class Logger(object):
    """Base logger class. Can be subclassed or used as is."""
    def __init__(
        self, 
        name, 
        headers, 
        prepend_name=False, 
        timer=None,
        topic=None,
        inc_seconds=False
    ):
        """Initialise class variables, create log file"""
        self.name = name
        self.create_header(headers, prepend_name)
        self.filename = f"output/{name}{datetime.now().strftime('%Y-%m')}.csv"
        if not os.path.isfile(self.filename):
            self.create_file()

        if timer:
            self.timer = timer
            self.start = 0
        
        self.topic = topic or name
        
        self.format = f"%Y-%m-%d %H:%M{':%S' if inc_seconds else ''}"
        
    def create_header(self, headers, prepend_name):
        """Cretate csv header with name prepended if selected"""
        h_string = ", ".join(
            map(
                lambda h:f"{self.name}_{h}", 
                headers
            ) if prepend_name else headers
        )
        self.header = f"Timestamp, {h_string}\n"            
        
    def create_file(self):
        """Create headered file"""
        with open(self.filename, "w") as fo:
            fo.write(self.header)

    def log(self, data):
        """Log data to the file"""
        now = datetime.now()
        filename = f"output/{self.name}{now.strftime('%Y-%m')}.csv"
        if filename != self.filename:
            self.filename = filename
            self.create_file(filename)

        if type(data) == list:
            data = ", ".join(map(str, data))
            
        with open(self.filename, "a") as fo:
            fo.write(f"{now.strftime(self.format)}, {data}\n")

    def error(self, message):
        """Log message to error file"""
        with open(ERRORFILE, "a") as fo:
            fo.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, {message}\n")

    def check(self, now):
        """Initiate logging if timer has expired"""
        if now - self.start >= self.timer:
            self.start = now
            data = self.collect_data()
            if data:
                self.log(data)       

    def collect_data(self, data=None):
        """To be overidden if necesary."""
        return data

    def callback(self, message):
        """Parse data from message if nesesary, then log"""
        self.log(self.collect_data(message)) 

