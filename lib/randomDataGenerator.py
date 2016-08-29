from lib.logger import Logger
import random
import string
from datetime import datetime
from lib.fileManager import FileManager

log = Logger()


def generate_class_attr_dict(classinstance):
    """
    Function generates dictionary using class instance attributes.
    :param classinstance: Class or class instance
    :return: dictionary
    """
    values = {key: value for key, value in classinstance.__dict__.items() if
              not key.startswith('_') and not callable(value) and not type(value) == staticmethod}
    attr_dict = {}
    for value in values:
        if type(values[value]) is list:
            attr_dict[value] = random.choice(values[value])
        else:
            attr_dict[value] = values[value]
    return attr_dict


def generate_test_data_json(classinstance, file_name):
    """
    Function saves generated dictionary to json file in test_suite/ directory
    :param classinstance: Class or class instance
    :param file_name: json file name
    """
    data = generate_class_attr_dict(classinstance)
    FileManager().save_test_data_to_json_file(file_name, data)


def random_string(length, upper=True):
    """ Generates random string with only ascii letters

    :param length: string len
    :param upper: default True, set False if you want have string in lowercase format
    :return: string
    """
    if upper:
        word = ''.join(random.choice(string.ascii_uppercase) for _ in range(length))
    else:
        word = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
    log.logger('DEBUG', 'random string %s generated' % word)
    return word


def random_digits(length):
    """ Generates random string with digits only. If string start with 0, 0 is removed.

    :param length: string length
    :return: string
    """
    word = ''.join(random.choice(string.digits) for _ in range(length))
    log.logger('DEBUG', 'random string digits %s generated' % word)
    if word.startswith('0'):
        word = word.replace('0', '1')
    return word


def random_currency(mini, maxi):
    """
    Generates random value in currency format with 2 digits after point.
    :param mini: int - minimal value
    :param maxi: int - maximal value
    :return: str - value in format XX.XX
    """
    return str(format(random.uniform(mini, maxi), '.2f'))


def random_chars_digits(length, upper=True):
    """ Generates random string with letters and digits

    :param length: string length
    :param upper: default True, set False if you want have lowercase format
    :return: string
    """
    if upper:
        word = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
    else:
        word = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
    log.logger('DEBUG', 'random string with letters and digits generated: %s' % word)
    return word


def get_date_without_space():
    """
    Generates string with current date and time in format YearMonthDayHourMinuteSecondsMilisec
    :return: string
    """
    data_print = datetime.now()
    data_formatted = str(data_print.strftime('%Y%m%d%H%M%S%f'))
    return data_formatted
