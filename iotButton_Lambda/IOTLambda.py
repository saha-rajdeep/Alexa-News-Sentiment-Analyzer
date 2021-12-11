import requests
import json
import datetime
import boto3

#this lambda gets triggered from an IOT button, if IOT button is pressed once
#it grabs today's headlines, does sentiment analysis using AWS Comprehend
#and saves the news along with sentiment into a dynamodb table
#lambda is optimized
def lambda_handler(event, context):
    # TODO implement
    print("button pressed")
    print(event)
    if event['clickType']=='SINGLE':
        findNews()
    else:
        deleteNews()
    
    return 'End of News Sentiment IOT function'


def deleteNews():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('news')
    #Scanning the table to get all rows in one shot
    response =table.scan()
    if 'Items' in response:
        items=response['Items']
        for row in items:
            sentiment=row['sentiment']
            timestamp=row['timestamp']
            delresponse = table.delete_item(
                Key={
                'sentiment': sentiment,
                'timestamp':timestamp
                    }
                    ) 

def findNews():
    #News credit to newsapi.org
    #Fetch headlines using the API
    #IMPORTANT: Register in newsapi.org to get your own API key, it's super easy!
    response = requests.get("https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=<your API key here>")
    d=response.json()
    if (d['status']) == 'ok':
        for article in d['articles']:
            print(article['title'])
            newsTitle=article['title']
            timestamp=article['publishedAt']
            sentiment=json.loads(getSentiment(newsTitle))
            print(sentiment['Sentiment'])
            insertDynamo(sentiment['Sentiment'],newsTitle,timestamp)

#getSentiment function calls AWS Comprehend to get the sentiment
def getSentiment(newsTitle):
    comprehend = boto3.client(service_name='comprehend')
    return(json.dumps(comprehend.detect_sentiment(Text=newsTitle, LanguageCode='en'), sort_keys=True))

#inserts headline along with sentiment into Dynamo    
def insertDynamo(sentiment,newsTitle,timestamp):
    print("inside insert dynamo function")
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('news')
    response = table.put_item(
       Item={
        'sentiment': sentiment,
        'title': newsTitle,
        'timestamp' : timestamp
       }
       )
      
