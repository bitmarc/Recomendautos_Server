import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.linkextractors import LinkExtractor
from webextractor.items import OpinautosItem

class Webstractor2Spider(scrapy.Spider):
    name='opinautos'
    item_count = 0

    allowed_domain = ['https://www.opinautos.com/']
    #start_url=['https://www.opinautos.com/mx/elegirmarca']

    custom_settings = {
        'ITEM_PIPELINES': {
            'webextractor.pipelines.WebstratorOpinautosPipeline': 400
        }}

    def start_requests(self):
        urls = ['https://www.opinautos.com/mx/elegirmarca']
        for url in urls:
            print('primer y unico url')
            yield scrapy.Request(url=url, callback=self.parse_marca)
    
    def parse_marca(self,response):
        all_div_marcas=response.xpath('//div[@class="ModelsGrid"]/a/@href').getall() # control de marcas
        for div_marca in all_div_marcas:
            yield response.follow(url=div_marca,callback=self.parse_modelo)

    def parse_modelo(self,response):
        all_div_modelos=response.xpath('//div[@class="margin-medium ColumnsMax5"]/div/a/@href').getall()# control de modelos[1:2]
        for div_modelo in all_div_modelos:
            yield response.follow(url=div_modelo,callback=self.parse_auto)
    
    def parse_auto(self,response):
        url_auto=response.xpath('//*[@id="pagecontent"]/div[2]/div[1]/div[3]/div[1]/div[1]/a/@href').get()
        yield response.follow(url=url_auto,callback=self.parse)
        
    def parse(self, response):
        auto_item=OpinautosItem()

        all_entries = response.css('div.WhiteCard.margin-top.desktop-margin15.js-review')

        for entrie in all_entries:
            self.item_count+=1
            nombre=entrie.css('.ModelTrim::text').extract()
            marca=response.xpath('//*[@id="pagecontent"]/div[2]/nav[2]/div[1]/div[2]/div/div/a/span/img/@title').extract()
            modelo=response.xpath('//*[@id="pagecontent"]/div[2]/nav[2]/div[1]/div[2]/div/div/span/a/span/text()').extract()
            estrellas=len(entrie.css('div.margin>div.LeftRightBox>div.LeftRightBox__left.LeftRightBox__left--noshrink>span.align-middle.inline-block>img[src="https://static.opinautos.com/images/design2/icons/icon_star--gold.svg?v=5eb58b"]:only-child').extract())
            votos=entrie.css('div.color-text-gray > span:nth-of-type(2)::text').extract()
            opinion=entrie.css('div.margin>div.Text.margin-top::text').extract()
            datetime=entrie.css('div.AuthorShort.AuthorShort--right.margin-top-small > span::attr(title)').extract()

            auto_item['nombre']=nombre[0].replace(u'\xa0\n', u' ').strip()
            auto_item['marca']=marca
            auto_item['modelo']=modelo
            auto_item['estrellas']=estrellas
            auto_item['opinion']=opinion
            auto_item['votos']=votos
            auto_item['fecha']=datetime
            yield auto_item
        print('::::: autos: ',self.item_count)
        