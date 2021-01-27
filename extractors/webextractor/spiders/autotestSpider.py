import scrapy
from scrapy.linkextractors import LinkExtractor 
from webextractor.items import AutotestItem
import json
import urllib

class autoSpider(scrapy.Spider):
    name='autotest'
    item_count = 0
    page=0

    custom_settings = {
        'ITEM_PIPELINES': {
            'webstractor.pipelines.WebstractorAutotestPipeline': 400
        }}

    allowed_domain = ['https://autotest.com.ar']

    def start_requests(self):
        urls = ['https://autotest.com.ar/pruebas',
        'https://autotest.com.ar/wp-admin/admin-ajax.php']
        header={
            'User-Agent': 'Scrapy spider',
            'Accept': '*/*',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
            }
        for url in urls:
            if self.page < 1:
                yield scrapy.Request(url=url, callback=self.parse_auto)
                self.page+=1
            else:
                while self.page < 19:
                    next=scrapy.Request(
                    url=url,
                    method='POST',
                    headers=header,
                    body=urllib.parse.urlencode({
                        'action': 'loadmore',
                        'query': '{"post_type":"pruebas","error":"","m":"","p":0,"post_parent":"","subpost":"","subpost_id":"","attachment":"","attachment_id":0,"name":"","pagename":"","page_id":0,"second":"","minute":"","hour":"","day":0,"monthnum":0,"year":0,"w":0,"category_name":"","tag":"","cat":"","tag_id":"","author":"","author_name":"","feed":"","tb":"","paged":0,"meta_key":"","meta_value":"","preview":"","s":"","sentence":"","title":"","fields":"","menu_order":"","embed":"","category__in":[],"category__not_in":[],"category__and":[],"post__in":[],"post__not_in":[],"post_name__in":[],"tag__in":[],"tag__not_in":[],"tag__and":[],"tag_slug__in":[],"tag_slug__and":[],"post_parent__in":[],"post_parent__not_in":[],"author__in":[],"author__not_in":[],"ignore_sticky_posts":false,"suppress_filters":false,"cache_results":true,"update_post_term_cache":true,"lazy_load_term_meta":true,"update_post_meta_cache":true,"posts_per_page":10,"nopaging":false,"comments_per_page":"10","no_found_rows":false,"order":"DESC"}',
                        'page': self.page}),
                    callback=self.parse_auto)
                    if next is not None:
                        yield next
                        self.page+=1
                        print('\n pagina: ',self.page)
                    else:
                        print('la pagina no existe')
                        self.page=19



    def parse_auto(self,response):
        urls_autos=response.xpath('//h3[@class="news-title"]/a/@href').getall()
        for url in urls_autos:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        auto_item=AutotestItem()
        nombre=response.xpath('//div[@class="row blog-content"]/div[@class="ptitle hidden-xs"]/h1/text()').extract_first()
        marca=response.xpath('normalize-space(//div[@class="datap"]/p[1]/text())').extract_first()
        modelo=response.xpath('normalize-space(//div[@class="datap"]/p[2]/text())').extract_first()
        cal_general=response.xpath('//div[@class="ptotal"]/text()').extract()[0].strip()
        cal_vida=response.xpath('//div[@class="ptotal"]/text()').extract()[1].strip()
        cal_diseño=response.xpath('//div[@class="ptotal"]/text()').extract()[2].strip()
        cal_manejo=response.xpath('//div[@class="ptotal"]/text()').extract()[3].strip()
        cal_performance=response.xpath('//div[@class="ptotal"]/text()').extract()[4].strip()
        a_favor=response.xpath("//div[@class='afavor']/p/text()").extract()
        en_contra=response.xpath("//div[@class='encontra']/p/text()").extract()
        
        auto_item['nombre']=nombre
        auto_item['marca']=marca
        auto_item['modelo']=modelo
        auto_item['cal_general']=cal_general
        auto_item['cal_vida']=cal_vida
        auto_item['cal_diseño']=cal_diseño
        auto_item['cal_manejo']=cal_manejo
        auto_item['cal_performance']=cal_performance
        auto_item['a_favor']=a_favor
        auto_item['en_contra']=en_contra
        yield auto_item
