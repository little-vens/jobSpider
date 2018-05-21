#!/usr/bin/env python3
#encoding: utf-8

# from urllib.request import urlopen
# import json
#
# def getCountry(ipAdress):
#     data = urlopen("http://freegeoip.net/json/"+ ipAdress)
#     jsonObj = json.loads(data.read().decode('utf-8'))
#     return jsonObj.get('country_code')
#
# if __name__ == '__main__':
#     print(getCountry('222.186.160.70'))

import scrapy

class testSpider(scrapy.Spider):
    name = "test"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]
        # for url in urls:
        #     yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text':quote.css('span.text::text').extract_first(),
                'author':quote.css('small.author::text').extract_first(),
                'tags':quote.css('div.tags a.tag::text').extract(),
            }

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            # next_page = response.urljoin(next_page)
            # yield scrapy.Request(next_page, callback=self.parse)
            yield response.follow(next_page, callback=self.parse)

        '''
        A shortcut for creating Requests:
        # for href in response.css('li.next a.attr('href')'):
        #     yield response.follow(href, callback=self.parse)
          
        # for a in response.css('li.next a'):
        #     yield response.follow(a, callback=self.parse)
        '''

        #yield dict(text=text, author=author, tags=tags)
        # page = response.url.split('/')[-2]
        # filename = 'qutoes-%s' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Save file %s' % filename)

class AuthorSpider(scrapy.Spider):
    name = 'author'

    start_urls = [
        'http://quotes.toscrape.com/'
    ]

    def parse(self, response):
        #follow links to author page
        for href in response.css('.author + a::attr(href)'):
            yield response.follow(href, callback=self.parse_author)

        #follow pagination links
        for href in response.css('li.next a::attr(href)'):
            yield response.follow(href, callback=self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            response.css(query).extract_first().strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text')
        }