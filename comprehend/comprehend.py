import boto3

class Comprehend:
    def __init__(self,service, region, language):
        self.__comprehend = boto3.client(service_name=service_n, region_name =region_n)

    def getSentiment(self,text):
        response=self.__comprehend.detect_sentiment(Text=text, LanguageCode=language)
        return response

    def getKeyPhrases(self,text):
        response=self.__comprehend.detect_key_phrases(Text=text, LanguageCode=language)
        return response
