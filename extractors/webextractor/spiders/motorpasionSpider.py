import scrapy
from urllib.parse import urljoin
from webextractor.items import MotorpasionItem

class Webstractor3Spider(scrapy.Spider):
    name='motorpasion'
    url_connector='pruebas-de-coches/record/'
    item_count = 0
    page=0

    custom_settings = {
        'ITEM_PIPELINES': {
            'webextractor.pipelines.WebstractorMotorpasionPipeline': 400
        }}

    allowed_domain = ['https://www.motorpasion.com.mx']

    def start_requests(self):
        urls = ['https://www.motorpasion.com.mx/categoria/pruebas-de-coches']

        for url in urls:
            while self.page < 40: # control de paginacion
                if self.page==0:
                    yield scrapy.Request(url=url, callback=self.parse_auto)
                    self.page += 20
                else:
                    end_url=self.url_connector
                    end_url +=str(self.page)
                    yield scrapy.Request(url=urljoin(url, end_url), callback=self.parse_auto)
                    self.page += 20
                    print('page : ',self.page)

    
    def parse_auto(self, response):
        urls_autos=response.xpath('//h2[@class="abstract-title"]/a/@href').getall()
        for url in urls_autos:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        auto_item=MotorpasionItem()
        auto_item['nombre']=response.xpath("//div[@class='ficha-titulo']/h2/text()").extract()
        auto_item['version']=response.xpath('//div[@class="ficha-titulo"]/h2/span/text()').extract()
        auto_item['cal_general']=response.xpath('normalize-space(//div[@class="nota-analisis"]/p/text()[2])').extract()
        auto_item['cal_acabados']=response.xpath('//div[@class="nota-analisis"]/div[@class="parcial"]/div[1]/strong/text()').extract()
        auto_item['cal_seguridad']=response.xpath('//div[@class="nota-analisis"]/div[@class="parcial"]/div[2]/strong/text()').extract()
        auto_item['cal_equipamiento']=response.xpath('//div[@class="nota-analisis"]/div[@class="parcial"]/div[3]/strong/text()').extract()
        auto_item['cal_Infotenimiento']=response.xpath('//div[@class="nota-analisis"]/div[@class="parcial"]/div[4]/strong/text()').extract()
        auto_item['cal_comportamiento']=response.xpath('//div[@class="nota-analisis"]/div[@class="parcial"]/div[5]/strong/text()').extract()
        auto_item['cal_motor']=response.xpath('//div[@class="nota-analisis"]/div[@class="parcial"]/div[6]/strong/text()').extract()
        auto_item['cal_transmision']=response.xpath('//div[@class="nota-analisis"]/div[@class="parcial"]/div[7]/strong/text()').extract()
        auto_item['cal_consumo']=response.xpath('//div[@class="nota-analisis"]/div[@class="parcial"]/div[8]/strong/text()').extract()
        auto_item['cal_espacio']=response.xpath('//div[@class="nota-analisis"]/div[@class="parcial"]/div[9]/strong/text()').extract()
        auto_item['cal_precio']=response.xpath('//div[@class="nota-analisis"]/div[@class="parcial"]/div[10]/strong/text()').extract()
        auto_item['a_favor']=response.xpath('//div[@class="nota-analisis"]/div[@class="positivo"]/ul/li/text()').extract()
        auto_item['en_contra']=response.xpath('//div[@class="nota-analisis"]/div[@class="negativo"]/ul/li/text()').extract()
        yield auto_item