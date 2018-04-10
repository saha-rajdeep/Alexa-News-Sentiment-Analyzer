DynamoDB Table:
DynamoDB - Create a DynamoDB table named "news" with Partition key "sentiment" and check "Add sort key" and add timestamp. Please refer to the screenshot dynamotable_news.jpg for reference.


Register at newsapi.org for your own API Key:
Once you get your key replace <your API key here> in insertDynamoIOT.py lambda

Lambdas:
There are two Lambdas - IOTLambda.py and AlexaLambda.py. Assign the arn of IOTLambda.py to IOT button and AlexaLambda.py to Alexa skill endpoint. 



If you DON'T have an IOT button:
Not to worry, we can simulate iot button. Create IOTLambda.py and then 

1. Configure a test event named "singleclick" with below json:

{
  "clickType": "SINGLE"
}

This testevent will act as IOT button single click. If you run this test, it'd grab the news headlines, gather sentiment and insert into DynamoDB

2. Configure a test event named "doubleclick" with below json:

{
  "clickType": "DOUBLE"
}

This testevent will act as IOT button double click. If you run this test, it'd delete all the existing news from DynamoDB

High Level Design Diagrams:
IOT button design diagram is kept at iot_button_design.png and Alexa design illustrated in alexa_design.png

Contact: If you like what you see and want to connect with me, send a linkedin invite to https://www.linkedin.com/in/rajdeep-saha-4ba24744/