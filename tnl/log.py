"""
Logging system for TNL
"""
import sys
from datetime import datetime

class LogConsumer:
    """Base class for log consumers"""
    def log_string(self, message):
        """Override this to handle log messages"""
        pass

class ConsoleLogConsumer(LogConsumer):
    """Logs to console"""
    def log_string(self, message):
        print(message, file=sys.stderr)

class Log:
    """Simple logging system"""
    _consumers = []
    
    @staticmethod
    def add_consumer(consumer):
        """Add a log consumer"""
        Log._consumers.append(consumer)
    
    @staticmethod
    def printf(fmt, *args):
        """Log a formatted message"""
        if args:
            message = fmt % args
        else:
            message = fmt
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        full_message = f"[{timestamp}] {message}"
        
        for consumer in Log._consumers:
            consumer.log_string(full_message)

# Global logging function
def logprintf(fmt, *args):
    """Global log function"""
    Log.printf(fmt, *args)

# Add default console consumer
Log.add_consumer(ConsoleLogConsumer())
