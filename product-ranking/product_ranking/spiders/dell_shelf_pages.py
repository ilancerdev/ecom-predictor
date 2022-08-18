# # -*- coding: utf-8 -*-

from scrapy.http import Request
from .dell import DellProductSpider
from scrapy.log import ERROR, INFO, WARNING
from product_ranking.items import SiteProductItem

import re
import math
import urlparse
import traceback
import json


class DellShelfPagesSpider(DellProductSpider):
    name = 'dell_shelf_urls_products'
    allowed_domains = ['dell.com']

    DEALS_CATEGORY_URL = "http://www.dell.com/csbapi/en-us/category/deals/{cat_id}?sortby=sort-relevance&page={page_num}"

    ACCESSORIES_CATEGORY_URL = "http://www.dell.com/csbapi/en-us/anavfilter/GetSnPResults?categorypath={cat_id}" \
                               "&sortby=&page={page_num}&categoryid={cat_id}" \
                               "&parentCategoryId=6488&isMerchandizingCategory=False"

    OTHER_CATEOGRY_URL = "http://www.dell.com/csbapi/en-us/anavfilter/GetSnPResults?categorypath={cat_id}" \
                         "&sortby=&appliedRefinements={refine_id}&page={page_num}&categoryid={cat_id}" \
                         "&parentCategoryId=6488&isMerchandizingCategory=False"

    def __init__(self, *args, **kwargs):
        kwargs.pop('quantity', None)
        self.num_pages = int(kwargs.pop('num_pages', 1))
        super(DellShelfPagesSpider, self).__init__(*args, **kwargs)

        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                          "Chrome/61.0.3163.100 Safari/537.36"

    def start_requests(self):
        if 'deals' in self.product_url:
            cat_id = re.search('deals/(.*)', self.product_url, re.DOTALL)
            self.CATEGORY_URL = self.DEALS_CATEGORY_URL
            if cat_id:
                cat_id = cat_id.group(1)
                yield Request(
                    url=self.CATEGORY_URL.format(cat_id=cat_id, page_num=1),
                    meta={
                        'search_term': '',
                        'remaining': self.quantity,
                        'cat_id': cat_id
                    },
                    headers={'User-Agent': self.user_agent}
                )
            else:
                self.log("Error while parsing cat_id")
        elif 'accessories' in self.product_url:
            cat_id = re.search('ar/(.*?)\?', self.product_url, re.DOTALL)
            self.CATEGORY_URL = self.ACCESSORIES_CATEGORY_URL
            if cat_id:
                cat_id = cat_id.group(1)
                yield Request(
                    url=self.CATEGORY_URL.format(cat_id=cat_id, page_num=1),
                    meta={
                        'search_term': '',
                        'remaining': self.quantity,
                        'cat_id': cat_id
                    },
                    headers={'User-Agent': self.user_agent}
                )
            else:
                self.log("Error while parsing cat_id")
        else:
            cat_id = re.search('ar/(.*?)\?', self.product_url, re.DOTALL)
            refine = re.search('appliedRefinements=(.*?)&', self.product_url, re.DOTALL)
            self.CATEGORY_URL = self.OTHER_CATEOGRY_URL
            if cat_id and refine:
                cat_id = cat_id.group(1)
                refine = refine.group(1)
                yield Request(
                    url=self.CATEGORY_URL.format(cat_id=cat_id, page_num=1, refine_id=refine),
                    meta={
                        'search_term': '',
                        'remaining': self.quantity,
                        'cat_id': cat_id,
                        'refine': refine
                    },
                    headers={'User-Agent': self.user_agent}
                )
            else:
                self.log("Error while parsing cat_id or refine")

    def _scrape_total_matches(self, response):
        total_matches = 0
        try:
            data = json.loads(response.body)
            if data.get('ResultText'):
                total_matches = re.search('(\d+)', data.get('ResultsText'), re.DOTALL)
            if total_matches:
                total_matches = total_matches.group(1)
            else:
                total_matches = data.get('TotalResultCount')
            return int(total_matches)
        except:
            self.log("Error while parsing total matches".format(traceback.format_exc()), WARNING)
            return total_matches

    def _scrape_product_links(self, response):
        """
        Scraping product links from search page
        """
        try:
            link_list = []
            data = json.loads(response.body)
            if 'Stacks' in data:
                for result in data.get('Stacks', []):
                    link = result['Stack']['Links']['ViewDetailsLink']['Url']
                    link_list.append(link)
            elif 'Results' in data:
                for result in data.get('Results', {}).get('Stacks', []):
                    if 'Links' in result['Stack']:
                        link = result['Stack']['Links']['ViewDetailsLink']['Url']
                        link_list.append(link)
            for link in link_list:
                res_item = SiteProductItem()
                if link:
                    link = urlparse.urljoin(response.url, link)
                    yield link, res_item
        except:
            self.log("Found no product links in {url}".format(url=response.url), INFO)

    def _scrape_next_results_page_link(self, response):
        meta = response.meta
        cat_id = meta.get('cat_id')
        refine = meta.get('refine')
        current_page = meta.get('current_page', 1)
        if current_page >= self.num_pages:
            return
        total_matches = meta.get('total_matches')
        results_per_page = self._scrape_results_per_page(response)
        if not results_per_page:
            results_per_page = 12
        if (total_matches and results_per_page
            and self.current_page < math.ceil(total_matches / float(results_per_page))):
            current_page += 1
            meta['current_page'] = current_page
            url = self.CATEGORY_URL.format(page_num=current_page, cat_id=cat_id, refine_id=refine)
            return Request(
                url,
                meta=meta,
                dont_filter=True,
            )