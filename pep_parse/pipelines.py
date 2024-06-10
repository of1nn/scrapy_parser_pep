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
        with open(filename, mode='w', encoding='utf-8') as f:
            f.write('Статус,Количество\n')
            total = 0
            for status, count in self.count_status.items():
                f.write(f'{status},{count}\n')
                total += count
            f.write(f'Total,{total}\n')
