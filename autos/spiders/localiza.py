# -*- coding: utf-8 -*-
import scrapy


class LocalizaSpider(scrapy.Spider):
    name = 'localiza'
    allowed_domains = ['seminovos.localiza.com']
    start_urls = ['https://seminovos.localiza.com/sedan?ct=1968_1987&st=ES&yr=2015_2019&pc=25000_500000']

    def parse(self, response):
        ads=response.xpath('//div[@id="resultadoPesquisa"]')
        

        
