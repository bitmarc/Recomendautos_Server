import scrapy
import json
from urllib.parse import urljoin
from webstractor.items import QuecocheItem

class Webstractor4Spider(scrapy.Spider):
    name='quecochemecompro'
    item_count=0
    allowed_domain=['https://www.quecochemecompro.com']

    custom_settings = {
        'ITEM_PIPELINES': {
            'webstractor.pipelines.WebstractorQuecochePipeline': 400
        }}

    page=1
    def start_requests(self):
        urls = ['https://www.quecochemecompro.com/api/v1/cards/search.json?search_type=vn&order=preferencias&min_power=%3C60&max_power=%3E300&max_consumption=12&min_price=7000&max_price=999999&page=']
        end_url='&ads=1&includes=html_specs,fuels'
        header={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
            'Accept': '*/*',
            'Content-Type':'application/json',
            'Authorization':'sj-@az<kf_gsd23kjhfgwkh2478r23876348&/&%&$&=fkbj'
            }
        for url in urls:
            while self.page < 21: #total de 20 paginas
                start_url=url
                start_url +=str(self.page)
                endpoint_url=start_url+end_url
                next=scrapy.Request(
                    url=endpoint_url,
                    method='GET',
                    headers=header,
                    body=json.dumps({
                        'search_type':'vn',
                        'order':'preferencias',
                        'min_power':'<60',
                        'max_power':'>300',
                        'max_consumption':'12',
                        'min_price':'7000',
                        'max_price':'999999',
                        'page':str(self.page),
                        'ads':'1',
                        'includes':[
                            'html_specs',
                            'fuel'
                        ]}),
                    callback=self.parse_auto)
                if next is not None:
                    yield next
                    self.page+=1
                else:
                    print('la pagina no existe')
                    self.page+=1

    
    def parse_auto(self, response):
        count=0
        jsonresponse = json.loads(response.text)
        total_current_items=jsonresponse['header']['pagination']['total_current_items']
        while count < total_current_items:
            slug=jsonresponse['data'][count]['slug']
            url_auto='https://www.quecochemecompro.com/precios/'
            url_auto+=str(slug)
            yield scrapy.Request(url=url_auto, callback=self.parse)
            count+=1

    def parse(self,response):
        auto_item=QuecocheItem()
        auto_item['nombre']=response.xpath('//h1[@class="card-title h1"]/text()').extract()
        auto_item['marca']=response.xpath('//*[@id="main-content"]/article/section[1]/ol/li[2]/a/span/text()').extract()
        auto_item['puntuacion']=response.xpath('//div[@class="score-count"]/text()').extract()
        auto_item['informativo']=response.xpath('//div[@class="advice_text"]/text()').extract()
        auto_item['cal_pequeño_y_manejable']=response.xpath('//div[@class="subjetive-chart"]/div[1]/span[@class="chart-bar-bullet"]/text()').extract()
        auto_item['cal_deportivo']=response.xpath('//div[@class="subjetive-chart"]/div[2]/span[@class="chart-bar-bullet"]/text()').extract()
        auto_item['cal_bueno_y_barato']=response.xpath('//div[@class="subjetive-chart"]/div[3]/span[@class="chart-bar-bullet"]/text()').extract()
        auto_item['cal_practico']=response.xpath('//div[@class="subjetive-chart"]/div[4]/span[@class="chart-bar-bullet"]/text()').extract()
        auto_item['cal_ecologico']=response.xpath('//div[@class="subjetive-chart"]/div[5]/span[@class="chart-bar-bullet"]/text()').extract()
        auto_item['cal_atractivo']=response.xpath('//div[@class="subjetive-chart"]/div[6]/span[@class="chart-bar-bullet"]/text()').extract()
        auto_item['lo_mejor']=response.xpath('//div[@class="better"]/p/text()').extract()
        auto_item['lo_malo']=response.xpath('//div[@class="worst"]/p/text()').extract()
        yield auto_item
