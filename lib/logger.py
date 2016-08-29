"""Class for logging

usage: Logger.logeer('INFO', 'Some logs')

"""

import logging
import inspect


class Logger(object):
    def __init__(self):
        self.FORMAT = '%(asctime)s - %(levelname)s: %(message)s'
        self.format = logging.basicConfig(
            filename=None,
            level=logging.INFO,
            format=self.FORMAT)

    @staticmethod
    def logger(level, *msg):
        """

        :param level: logs level - string - can be: 'INFO', 'DEBUG', 'WARNING', 'ERROR', 'CRITICAL'
        :param msg: your logs
        """
        level = level.upper()
        if level == 'INFO':
            logging.info(msg)
        elif level == 'DEBUG':
            logging.debug(msg)
        elif level == 'WARNING':
            logging.warning(msg)
        elif level == 'ERROR':
            logging.error(msg)
        elif level == 'CRITICAL':
            logging.critical(msg)
        else:
            raise ValueError('Unknown log level %s, available: INFO, WARNING, DEBUG, ERROR, CRITICAL' % msg)


def whoami():
    """
    prints current function name in runtime
    """
    name = inspect.stack()[1][3]
    print('-' * 42 + '-' * len(name))
    print('*' * 20, name, '*' * 20)
    print('-' * 42 + '-' * len(name))
    Logger.logger('INFO', name)
