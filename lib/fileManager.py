import os
import csv
import json

test_data_directory = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'test_suites/')


class FileManager(object):
    def __init__(self):
        self.test_data_directory = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
                                                'test_suites/')

    @staticmethod
    def check_if_file_exists(file_path):
        """function checks if searched file exists

            :param file_path: path to file
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError("Configuration file not found!\n%s" % file_path)

    def load_test_data_from_csv_file(self, filename):
        """load test data for testing from file located in test_suites/ directory

        :param filename: string file name with csv extension e.g 'test_data.csv'
        :return: dictionary with test data
        """
        file = os.path.join(test_data_directory, filename)
        data = self.load_data_from_csv_file(file)
        return data

    def load_data_from_csv_file(self, filename):
        """load data from file

        :param filename: path to file
        :return: data from csv file in dictionary format
        """
        self.check_if_file_exists(filename)
        with open(filename, mode='r') as f:
            reader = csv.reader(f)
            dictionary = {}
            for row in reader:
                key = row[1]
                dictionary[key] = str(row[2])
        return dictionary

    @staticmethod
    def load_data_from_json_file(filename):
        """Load data from json file

        :param filename: path to file
        :return: data from json in dictionary format
        """
        with open(filename, 'r') as fp:
            data = json.load(fp)
            return dict(data)

    def load_test_data_from_json_file(self, filename):
        """load test data for testing from file located in test_suites/ directory

        :param filename: string file name with json extension e.g 'test_data.json'
        :return: dictionary with test data
        """
        file = os.path.join(self.test_data_directory, filename)
        return self.load_data_from_json_file(file)

    @staticmethod
    def save_data_to_json_file(filename, data):
        """
        Save data to json file
        :param filename: path to file with file name
        :param data: dictionary
        """
        with open(filename, 'w') as fp:
            json.dump(data, fp)

    def save_test_data_to_json_file(self, filename, data):
        """
        Save test data to json file in test_suite/ directory.

        :param filename: json file name
        :param data: dictionary
        """
        file = os.path.join(self.test_data_directory, filename)
        self.save_data_to_json_file(file, data)
