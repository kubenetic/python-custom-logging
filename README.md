This project is a simple tutorial about how QueueHandlers and QueueListeners works together, and how to implements a
custom handler to perform some action when a log is written to a queue. In the project I gather the logs in a queue
and write all logs through a custom handler into a SQLite database. Write all logs with WARNING level or higher to a
file and write all logs with INFO level or higher to the console.