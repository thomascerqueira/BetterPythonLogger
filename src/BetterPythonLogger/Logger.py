import logging
import os
import sys
from typing import Dict
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
from .NoLoggerException import NoLoggerException


class Logger():
    DEBUG_LEVEL = DEBUG
    LOGGER_NAME = "Logger"
    
    class LevelFormatter(logging.Formatter):
        def format(self, record):
            if record.levelno == logging.DEBUG:
                levelname = "\033[1;34mDEBUG\033[1;0m"
            elif record.levelno == logging.INFO:
                levelname = "\033[1;32mINFO\033[1;0m"
            elif record.levelno == logging.WARNING:
                levelname = "\033[1;33mWARNING\033[1;0m"
            elif record.levelno == logging.ERROR:
                levelname = "\033[1;31mERROR\033[1;0m"
            elif record.levelno == logging.CRITICAL:
                levelname = "\033[1;41mCRITICAL\033[1;0m"
            else:
                levelname = "\033[1;0mUNKNOWN\033[1;0m"
            record.levelname = levelname
            return super().format(record)
    
    class NormalFormatter(logging.Formatter):
        def format(self, record):
            if record.levelno == logging.DEBUG:
                levelname = "DEBUG"
            elif record.levelno == logging.INFO:
                levelname = "INFO"
            elif record.levelno == logging.WARNING:
                levelname = "WARNING"
            elif record.levelno == logging.ERROR:
                levelname = "ERROR"
            elif record.levelno == logging.CRITICAL:
                levelname = "CRITICAL"
            else:
                levelname = "UNKNOWN"
            record.levelname = levelname
            return super().format(record).replace("\033[1;32m", "").replace("\033[1;0m", "")
        

    def __init__(self, name, noFile=False):
        if hasattr(self, "logger"):
            return
        
        print(f"Creating logger for {name}")
        
        self.baseLoggerName = name
        self.loggers: Dict[str, logging.Logger] = {}
        
        self.loggers[name] = logging.getLogger(name)
        self.loggers[name].setLevel(self.DEBUG_LEVEL)
        
        if not os.path.exists("log"):
            os.makedirs("log")

        if not noFile:
            self.addFileHandler(f"log/{name}.log")
        self.addStreamHandler()
        
    def getLoggerFromName(self, name):
        """
        Return a logger from its name
        
        :param name: The name of the logger to return
        """
        if name not in self.loggers:
            raise NoLoggerException(f"No logger with name {name}")
        
        return self.loggers.get(name)
        
    def addStreamHandler(self, logger_name=None):
        """
        Allow to add a stream handler to the logger, the output will be printed in the console
        
        :param logger_name: The name of the logger to add the handler
        """
        if logger_name is None:
            logger_name = self.baseLoggerName

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(self.DEBUG_LEVEL)
        stream_handler.setFormatter(self.LevelFormatter("%(asctime)s - %(name)s - [%(levelname)s] - %(message)s"))
        
        logger = self.getLoggerFromName(logger_name)
        logger.addHandler(stream_handler)


    def addFileHandler(self, filename, logger_name=None):
        """
        Allow to add a file handler to the logger, the output will be printed in the file
        
        :param filename: The name of the file to add the handler
        """
        if logger_name is None:
            logger_name = self.baseLoggerName
        
        file_handler = logging.FileHandler(filename)
        file_handler.setLevel(self.DEBUG_LEVEL)
        file_handler.setFormatter(self.NormalFormatter("%(asctime)s - %(name)s - [%(levelname)s] - %(message)s"))
        
        logger = self.getLoggerFromName(logger_name)
        logger.addHandler(file_handler)
        
    def removeFileHandler(self, filename, logger_name=None):
        """
        Remove a file handler from the logger
        
        :param filename: The name of the filehandler to remove
        :param logger_name: The name of the logger to remove the handler
        """
        if logger_name is None:
            logger_name = self.baseLoggerName

        logger = self.getLoggerFromName(logger_name)

        for handler in logger.handlers:
            if isinstance(handler, logging.FileHandler) and handler.baseFilename == filename:
                logger.removeHandler(handler)
                break

    def debug(self, message, logger_name=None):
        """
        Print a debug message
        """
        if logger_name is None:
            logger_name = self.baseLoggerName
            
        logger = self.getLoggerFromName(logger_name)
        logger.debug(message)

    def info(self, message, logger_name=None):
        """
        Print an info message
        """
        if logger_name is None:
            logger_name = self.baseLoggerName
            
        logger = self.getLoggerFromName(logger_name)
        logger.info(message)

    def warning(self, message, logger_name=None):
        """
        Print a warning message
        """
        if logger_name is None:
            logger_name = self.baseLoggerName
        
        logger = self.getLoggerFromName(logger_name)
        logger.warning(message)

    def error(self, message, logger_name=None):
        """
        Print an error message
        """
        if logger_name is None:
            logger_name = self.baseLoggerName
        
        logger = self.getLoggerFromName(logger_name)
        logger.error(message)

    def critical(self, message, logger_name=None):
        """
        Print a critical message
        """
        if logger_name is None:
            logger_name = self.baseLoggerName
        
        logger = self.getLoggerFromName(logger_name)
        logger.critical(message)
    
    def success(self, message, logger_name=None):
        """
        Print a success message this may have some problem with the color on some terminal and in the log file
        """
        if logger_name is None:
            logger_name = self.baseLoggerName
        
        logger = self.getLoggerFromName(logger_name)
        logger.info(f"\033[1;32m{message}\033[1;0m")
        
    def addLogger(self, name, noFile=False):
        """
        This method allow to add a new logger to the class
        
        This will add an filehandler and a streamhandler to the logger 
        
        :param name: The name of the logger to add
        """
        if self.loggers.get(name):
            return
        
        self.loggers[name] = logging.getLogger(name)
        self.loggers[name].setLevel(self.DEBUG_LEVEL)
        
        if not noFile:
            self.addFileHandler(f"log/{name}.log", name)
        self.addStreamHandler(name)

def log_decorator(logger, class_name):
    """
    Function decorator to log the function call
    
    :param class_name: The name of the class if the function is a method of class
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            if class_name:
                logger.debug(f"Calling {class_name}.{func.__name__}")
            else:
                logger.debug(f"Calling {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator