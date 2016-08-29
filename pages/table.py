from lib.driverCommands import DriverCommands
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By


class Table(DriverCommands):

    def table_create_matrix(self):
        self.log.logger('INFO', 'Creating matrix')
        rows = self.get_all_rows()
        matrix = []
        try:
            for row in rows:
                col = row.find_elements(By.TAG_NAME, "td")
                matrix.append(col)
        except StaleElementReferenceException as e:
            self.log.logger('WARNING', e)
            self.table_create_matrix()
        return matrix

    def get_all_rows(self):
        rows = self.find_elements((By.TAG_NAME, 'tr'))
        return rows

    def find_table_record(self, name, records):
        for rec in records:
            try:
                rec_data = rec.text
                if rec_data == 'No matching records found' or rec_data == '':
                    continue
                rec_name = rec_data.split()[0]
                if name == rec_name:
                    self.log.logger('INFO', '%s - I found it!' % rec_name)
                    return True, rec
                elif 'Loading' in rec_name:
                    self.log.logger('INFO', 'List still not fully laod, wait 0.1 sec')
                    self.wait(0.1)
                    new_records = self.get_all_rows()
                    result = self.find_table_record(name, new_records)
                    return result
                else:
                    self.log.logger('INFO', 'Found table record with data: %s' % rec_name)
            except StaleElementReferenceException as e:
                self.log.logger('WARNING', 'Selenium error: %s' % e)
                self.log.logger('INFO', 'Trying again...')
                new_records = self.get_all_rows()
                result = self.find_table_record(name, new_records)
                return result
        else:
            self.log.logger('WARNING', "It's not here!")
            return False, 'Table record: %s not found' % name

