'''
Clase donde se definen las peticiones del servicio de aws comprehend
'''
import boto3

class Comprehend:
    def __init__(self,service, region, language):
        self.__comprehend = boto3.client(service_name=service, region_name =region)
        self.__language=language

    def getSentiment(self,text):
        response=self.__comprehend.detect_sentiment(Text=text, LanguageCode=self.__language)
        return response

    def getKeyPhrases(self,text):
        response=self.__comprehend.detect_key_phrases(Text=text, LanguageCode=self.__language)
        return response
