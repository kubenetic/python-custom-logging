import logging
import sqlite3
from typing import override


class SQLiteLogHandler(logging.Handler):
    """
    This class is responsible for logging all log events to the SQLite database.
    """

    def __init__(self, db_path):
        super().__init__()

        self.__db_path = db_path

        # Create the database table if it doesn't exist
        db = sqlite3.connect(self.__db_path)
        db.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                message TEXT
            );
        ''')
        db.close()

    @override
    def emit(self, record: logging.LogRecord):
        """
        Process the incoming log record and insert it into the database.

        Args:
            record (logging.LogRecord): Log record to process
        """
        print('emit logrecord')

        log_message = self.format(record)

        try:
            # Test what happens when an exception raised inside the emit method
            if record.levelno == logging.CRITICAL:
                raise Exception(log_message)

            db = sqlite3.connect(self.__db_path)
            db.execute('INSERT INTO logs (message) VALUES (?)', (log_message,))
            db.commit()
            db.close()
        except Exception as e:
            print(f'Error inserting log message into database: {e}')
            self.handleError(record)

    @override
    def handle(self, record: logging.LogRecord):
        """
        Handle the incoming log record.

        Args:
            record (logging.LogRecord): Log record to handle
        """
        print('handle logrecord')
        self.emit(record)

    @override
    def handleError(self, record: logging.LogRecord):
        """
        Handle the error.

        Args:
            record (logging.LogRecord): Log record to handle
        """
        print('handle logrecord error')
        print(self.format(record))

    @override
    def close(self):
        print('close loghandler')
