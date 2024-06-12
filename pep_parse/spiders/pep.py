import scrapy

from pep_parse.items import PepParseItem
from pep_parse.settings import NAME, START_URL


class PepSpider(scrapy.Spider):
    name = NAME
    allowed_domains = [START_URL]
    start_urls = [f'https://{START_URL}/']

    def parse(self, response):
        all_peps = response.css('tr td a.pep.reference.internal:first-child')
        for pep_link in all_peps:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        data = {
            'number': int(
                response.css(
                    '.breadcrumbs li:nth-child(3)::text'
                ).get().replace('PEP', '').strip()
            ),
            'name': response.css('.page-title::text').get(),
            'status': response.css(
                'dt:contains("Status") + dd abbr::text'
            ).get(),
        }
        yield PepParseItem(data)
