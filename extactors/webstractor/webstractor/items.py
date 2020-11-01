# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AutotestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nombre = scrapy.Field()
    marca = scrapy.Field()
    modelo = scrapy.Field()
    cal_general = scrapy.Field()
    cal_vida = scrapy.Field()
    cal_diseño = scrapy.Field()
    cal_manejo = scrapy.Field()
    cal_performance = scrapy.Field()
    a_favor = scrapy.Field()
    en_contra = scrapy.Field()

class OpinautosItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    #informacion de automovil
    nombre = scrapy.Field()
    marca = scrapy.Field()
    modelo = scrapy.Field()

    #informacion de opinion
    estrellas = scrapy.Field()
    opinion = scrapy.Field()
    votos = scrapy.Field()
    fecha = scrapy.Field()


class MotorpasionItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nombre = scrapy.Field()
    version = scrapy.Field()
    cal_general = scrapy.Field()
    cal_acabados = scrapy.Field()
    cal_seguridad = scrapy.Field()
    cal_equipamiento = scrapy.Field()
    cal_Infotenimiento = scrapy.Field()
    cal_comportamiento = scrapy.Field()
    cal_motor = scrapy.Field()
    cal_transmision = scrapy.Field()
    cal_consumo = scrapy.Field()
    cal_espacio = scrapy.Field()
    cal_precio = scrapy.Field()
    a_favor = scrapy.Field()
    en_contra = scrapy.Field()


class QuecocheItem(scrapy.Item):
    # define the fields for your item here like:
    nombre = scrapy.Field()
    marca = scrapy.Field()

    puntuacion = scrapy.Field()
    informativo = scrapy.Field()

    cal_pequeño_y_manejable = scrapy.Field()
    cal_deportivo = scrapy.Field()
    cal_bueno_y_barato = scrapy.Field()
    cal_practico = scrapy.Field()
    cal_ecologico = scrapy.Field()
    cal_atractivo = scrapy.Field()
    
    lo_mejor = scrapy.Field()
    lo_malo = scrapy.Field()