import multiprocessing

from log_setup import setup_queue_listener, setup_logger

if __name__ == '__main__':
    logging_queue = multiprocessing.Queue()
    listener = setup_queue_listener(logging_queue)
    logger = setup_logger(logging_queue)

    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')

    listener.stop()
