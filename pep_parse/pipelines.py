import csv
from collections import defaultdict
from datetime import datetime

from pep_parse.settings import BASE_DIR


class PepParsePipeline:

    def open_spider(self, spider):
        self.count_status = defaultdict(int)

    def process_item(self, item, spider):
        status = item['status']
        self.count_status[status] += 1

        return item

    def close_spider(self, spider):
        time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'{BASE_DIR}/status_summary_{time}.csv'
        self.count_status['Total'] = sum(self.count_status.values())

        with open(filename, mode='w', encoding='utf-8', newline='') as csvfile:
            fieldnames = ['first_name', 'last_name']
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)
            writer.writerows(
                [status, count] for status, count in self.count_status.items()
            )
