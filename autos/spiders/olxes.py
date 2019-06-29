# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
from scrapy.http import Request

class OlxesSpider(scrapy.Spider):
    name = 'olxes'
    allowed_domains = ['es.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios?ctp=8']
    # sedan -> ctp=8
    # 2015 - 2019 -> rs=34&re=37
    # km 20.000 - 60.000 -> ms=20000&me=60000
    # preço 25.000 a 40.000 -> ps=25000&pe=40000
    # característica -> q=gas
    # TODO 1: colocar parametros de busca num arquivo json
    #base_url = 'https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios?'
    base_url = 'olx.com.br/autos-e-pecas/carros-vans-e-utilitarios?'
    # assemble search parameters
    states = ['es','rj','mg']
    search = ['ctp=8','rs=33','ms=20000&me=65000','ps=24000&pe=40000']
    search = "&".join(search)
    start_urls = []
    for s in states:
        start_urls.append('https://'+s+'.'+base_url+search)

    def parse(self, response):
        ads=response.xpath('//ul[@id="main-ad-list"]/li[@class="item"]')
        i = 0
        for adSel in ads:
            # i = i +1
            # if i>=5:
            #     break 
            ad_url = adSel.xpath('./a/@href').get()
            request = Request(ad_url, callback=self.parseDetails,dont_filter=True)
            yield request
        next_page= response.xpath('//li/a[@rel="next"]/@href').get()
        if next_page:
            yield Request(next_page, callback=self.parse,dont_filter=True)

    def parseDetails(self,response):
        ad = {}
        ad['title'] = response.xpath("//*[@id='ad_title']/text()").get().strip().strip(',')
        ad['price'] = response.xpath("//span[@class='actual-price']/text()").get().strip()
        detailsSel = response.xpath("//div[@class='OLXad-details mb30px']/div/ul/li")
        for det in detailsSel:
            key = det.xpath('./p/span/text()').get().strip()[:-1]
            if (key in ['Ano','Combustível','Categoria','Modelo']):
                value = det.xpath('./p/strong/a/text()').get().strip()
            else:
                value = det.xpath('./p/strong/text()').get().strip()
            ad[key] = value
        ad['city'] = response.xpath("//div[@class='OLXad-location mb20px']//ul/li/p/strong/a/text()").get().strip()
        ad['url'] = response.url
        # ad['seller'] = response.xpath('//div[@class="box-user-info fixedBox"]/div/div/div/div[1]/div/span/text()').get()
        # ad['phone'] = response.xpath('//div[@class="box-user-info fixedBox"]/div/div/div/div[3]/a/div[2]/text()').get()
        yield ad


        









