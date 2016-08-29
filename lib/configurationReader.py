import os
import json
from lib.randomDataGenerator import FileManager

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configuration')
fileManager = FileManager()


def load_configuration_from_file(file_name):
    """Function opens json file from configuration directory

        :param file_name: config file name

        :return: data from json file in object.attribute format
    """
    file_path = os.path.join(CONFIG_PATH, file_name)
    fileManager.check_if_file_exists(file_path)
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)
    return config
