**1. DynamoDB Table:**
Create a DynamoDB table named "news" with Partition key "sentiment" and check "Add sort key" and add timestamp. Please refer to the screenshot dynamotable_news.jpg for reference.


**2. Register at newsapi.org for your own API Key:**
Once you get your key replace <your API key here> in IOTLambda.py lambda (under iotButton_Lambda folder).


**3. Lambdas:**
There are two Lambdas - IOTLambda.py (under iotButton_Lambda folder) and AlexaLambda.py (under Alexa_Assets folder). Assign the arn of IOTLambda.py to IOT button and AlexaLambda.py to Alexa skill endpoint. 


**4. If you DON'T have an IOT button:**
Not to worry, we can simulate iot button. Create IOTLambda.py and then do the following: 

A. Configure a test event named "singleclick" with below json:

{
  "clickType": "SINGLE"
}

This testevent will act as IOT button single click. If you run this test, it'd grab the news headlines, gather sentiment and insert into DynamoDB

B. Configure a test event named "doubleclick" with below json:

{
  "clickType": "DOUBLE"
}

This testevent will act as IOT button double click. If you run this test, it'd delete all the existing news from DynamoDB


**5. High Level Design Diagrams:**
IOT button design diagram is kept at iot_button_design.png and Alexa design illustrated in alexa_design.png



**Contact Author:** 
If you like what you see and want to connect with me, send a linkedin invite to https://www.linkedin.com/in/rajdeep-saha-4ba24744/
