import logging
import sys
from logging.handlers import QueueHandler, QueueListener
from multiprocessing import Queue

from sqlite_log_handler import SQLiteLogHandler


def setup_queue_listener(logging_queue: Queue) -> QueueListener:
    """
    Setup the queue listener with the logging queue.

    Args:
        logging_queue (Queue): Logging queue

    Returns:
        QueueListener: Queue listener
    """

    logging_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(module)s : %(message)s')

    # Setup STDOUT handler that responsible for printing all log messages on INFO level and above to the console
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.setLevel(logging.INFO)
    stdout_handler.setFormatter(logging_formatter)

    # Setup STDERR handler that responsible for printing all log messages on WARN level and above to the console
    stderr_handler = logging.FileHandler('error.log', encoding='utf-8')
    stderr_handler.setLevel(logging.WARN)
    stderr_handler.setFormatter(logging_formatter)

    # Setup SQLite handler that responsible for storing all log messages on DEBUG level and above to the SQLite database
    sqlite_log_handler = SQLiteLogHandler('log.db')
    sqlite_log_handler.setLevel(logging.DEBUG)
    sqlite_log_handler.setFormatter(logging_formatter)

    handlers = [stdout_handler, stderr_handler, sqlite_log_handler]

    # Setup the queue listener, add handlers
    log_listener = logging.handlers.QueueListener(logging_queue, *handlers)
    log_listener.respect_handler_level = True
    log_listener.start()

    return log_listener


def setup_logger(logging_queue: Queue) -> logging.Logger:
    """
    Setup the logger with the logging queue.

    Args:
        logging_queue (Queue): Logging queue

    Returns:
        logging.Logger: Logger
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    queue_handler = QueueHandler(logging_queue)
    logger.addHandler(queue_handler)

    return logger
