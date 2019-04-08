from scrapy.http import Request

import scrapy
import json

class ArchiveSpider(scrapy.Spider):
    name = "archive"
    allowed_domains = ["archive.org"]
    start_urls = ['https://web.archive.org/__wb/calendarcaptures?url=https%3A%2F%2Fwww.forbes.com%2Fnba-valuations%2Flist%2F&selected_year='+str(x) for x in range(2016,2020)]

    def parse(self, response):
        for i in json.loads(response.body):
            for j in i:
                for k in j:
                    if k and ('ts' in k):
                        for url_date in k['ts']:
                            url = "https://web.archive.org/web/%s/http://www.forbes.com/nba-valuations/list/" % url_date
                            # yield Request(url, callback=self.parse_item)
                            yield {
                                'url': url
                            }
    # def parse_item(self, response):
    #     for item in response.xpath():
    #         yield {
    #             'team': item.xpath().extract_first(),
    #             'income': item.xpath().extract_first(),
    #         }