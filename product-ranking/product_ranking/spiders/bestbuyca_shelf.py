# -*- coding: utf-8 -*-

from .bestbuyca import BestbuycaProductsSpider
from scrapy.http import Request


class BestbuycaShelfPagesSpider(BestbuycaProductsSpider):
    name = 'bestbuyca_shelf_urls_products'
    allowed_domains = ["www.bestbuy.ca"]

    def __init__(self, *args, **kwargs):
        kwargs.pop('quantity', None)
        self.current_page = 1
        self.num_pages = int(kwargs.pop('num_pages', '1'))
        super(BestbuycaShelfPagesSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield Request(url=self.product_url,
                      meta={'search_term': "", 'remaining': self.quantity},
                      )

    def _scrape_next_results_page_link(self, response):
        if self.current_page >= self.num_pages:
            return None
        self.current_page += 1
        return super(BestbuycaShelfPagesSpider, self)._scrape_next_results_page_link(response)
