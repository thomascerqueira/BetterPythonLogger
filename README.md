# BetterPythonLogger

A better python logger for better logging.

## Usage

```python
from BetterPythonLogger import Logger

logger = Logger.Logger("test")

logger.debug("This is a debug message")
```

![alt text](https://github.com/thomascerqueira/BetterPythonLogger/raw/main/doc/usage.png)

**By default this while create a new log file in the log directory**

you can add a file handler to the logger

```python
from BetterPythonLogger import Logger

logger = Logger.Logger("test")

logger.addFileHandler("<filename>", "<logger_name> here will be test")
```

You can add a stream handler to the logger

```python
from BetterPythonLogger import Logger

logger = Logger.Logger("test")

logger.addStreamHandler("<logger_name> here will be test")
```

You can add a logger to the logger

```python

from BetterPythonLogger import Logger

logger = Logger.Logger("test")

logger.addLogger("<logger_name>")
```

This will add a stream handler and a file handler to the newly created logger


If you don't want a file handler you can say noFile=True in the constructor or in the addLogger method

If you don't use any name we will use the name used to create the class.