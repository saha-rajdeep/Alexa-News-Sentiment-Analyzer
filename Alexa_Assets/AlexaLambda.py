"""Uncle Sam.

This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import math
import random
import string
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr


# ------- Skill specific business logic -------

SKILL_NAME = "Uncle Sam"

# When editing your questions pay attention to your punctuation.
# Make sure you use question marks or periods.
# Make sure the first answer is the correct one.


def lambda_handler(event, context):
    """
    Route the incoming request based on type (LaunchRequest, IntentRequest, etc).
    The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])
    print("event:" + json.dumps(event))

    """
    Uncomment this if statement and populate with your skill's application ID
    to prevent someone else from configuring a skill that sends requests
    to this function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """Called when the session starts."""
    print("on_session_started requestId=" +
          session_started_request['requestId'] + ", sessionId=" +
          session['sessionId'])


def on_launch(launch_request, session):
    """Called when the user launches the skill without specifying what they want."""
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """Called when the user specifies an intent for this skill."""
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

   
    # Dispatch to your skill's intent handlers
    print("***********************intent section***************************")
    print(intent_name)
    if intent_name == "NewsIntent":
        return handle_answer_request(intent, session)
    elif intent_name == "PositiveIntent":
        return handle_positive_request(intent, session)   
    elif intent_name == "NegativeIntent":
        return handle_negative_request(intent, session) 
    elif intent_name == "NeutralIntent":
        return handle_neutral_request(intent, session) 
    elif intent_name == "AMAZON.HelpIntent":
        return handle_get_help_request(intent, session)
    elif intent_name == "AMAZON.StopIntent":
        return handle_finish_session_request(intent, session)
    elif intent_name == "AMAZON.CancelIntent":
        return handle_finish_session_request(intent, session)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """
    Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior -------------


def get_welcome_response():
    """If we wanted to initialize the session to have some attributes we could add those here."""
    intro = ("Just ask {} to know about news analytics. ".format(SKILL_NAME)) 
    should_end_session = False

    speech_output = intro 
    reprompt_text = intro
    attributes = {"speech_output": speech_output,
                  "reprompt_text": speech_output
                  }

    return build_response(attributes, build_speechlet_response(
        SKILL_NAME, speech_output, reprompt_text, should_end_session))



def handle_answer_request(intent, session):
    #print("in handle_answer_rerquest:" + intent)
    attributes = {}
    should_end_session = False
    user_gave_up = intent['name']
    speech_output = ("No News Analytics found, press iot button to start analysis ")
    reprompt_text = "Maybe all is well with world, maybe not, just ask {}".format(SKILL_NAME)
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('news')
    #Scanning the table to get all rows in one shot
    response =table.scan()
    print(response)
    if response['Count'] > 0:
        num_positive=0
        num_negative=0
        num_neutral=0
        
        items=response['Items']
        for row in items:
            sentiment=row['sentiment']
            if sentiment == 'NEGATIVE':
                num_negative += 1
            elif sentiment == 'POSITIVE': 
                num_positive += 1
            elif sentiment == 'NEUTRAL': 
                num_neutral += 1
                
        speech_output=("There are " + str(num_neutral) + " neutral, " + str(num_negative) + 
                     " negative, and " + str(num_positive) + " positive news today")
        print(speech_output)
    
    return build_response(
            {},
            build_speechlet_response(
                SKILL_NAME, speech_output, reprompt_text, should_end_session
            ))
            
def handle_positive_request(intent, session):
    print("in handle_positive_rerquest:")
    attributes = {}
    should_end_session = False
    #answer = intent['slots'].get('year', {}).get('value')
    #print("slot value from question:" + answer)
    user_gave_up = intent['name']
    speech_output = ("World peace achieved. Free pizza for everyone. Happiness index all time high. Yup, this is Fake News!")
    reprompt_text = "Maybe all is well with world, maybe not, just ask {}".format(SKILL_NAME)
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('news')
    #Querying the table 
    response = table.query(
                KeyConditionExpression=Key('sentiment').eq('POSITIVE')
                )
    print(response)            
    if response['Count'] > 0:
        items=response['Items']
        speech_output=""
        for row in items:
            title=row['title']
            #sometimes news headlines don't end with a period, in those cases
            #adding period to create a pause in alexa before reading next title
            if title.endswith('.') or title.endswith('?') or title.endswith('!'):
                speech_output=title+speech_output
            else:
                speech_output=title+". "+speech_output
        print(speech_output)
    
    return build_response(
            {},
            build_speechlet_response(
                SKILL_NAME, speech_output, reprompt_text, should_end_session
            ))            


def handle_negative_request(intent, session):
    #print("in handle_positive_rerquest:")
    attributes = {}
    should_end_session = False
    user_gave_up = intent['name']
    speech_output = ("No negative News found, what a great day indeed")
    reprompt_text = "Maybe all is well with world, maybe not, just ask {}".format(SKILL_NAME)
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('news')
    #Querying the table 
    response = table.query(
                KeyConditionExpression=Key('sentiment').eq('NEGATIVE')
                )
    if response['Count'] > 0:
        items=response['Items']
        speech_output=""
        for row in items:
            title=row['title']
            #sometimes news headlines don't end with a period, in those cases
            #adding period to create a pause in alexa before reading next title
            if title.endswith('.') or title.endswith('?') or title.endswith('!'):
                speech_output=title+speech_output
            else:
                speech_output=title+". "+speech_output
        print(speech_output)
    
    return build_response(
            {},
            build_speechlet_response(
                SKILL_NAME, speech_output, reprompt_text, should_end_session
            ))            


def handle_neutral_request(intent, session):
    #print("in handle_positive_rerquest:")
    attributes = {}
    should_end_session = False
    user_gave_up = intent['name']
    speech_output = ("No neutral News found")
    reprompt_text = "Maybe all is well with world, maybe not, just ask {}".format(SKILL_NAME)
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('news')
    #Querying the table 
    response = table.query(
                KeyConditionExpression=Key('sentiment').eq('NEUTRAL')
                )
    if response['Count'] > 0:
        items=response['Items']
        speech_output=""
        for row in items:
            title=row['title']
            #sometimes news headlines don't end with a period, in those cases
            #adding period to create a pause in alexa before reading next title
            if title.endswith('.') or title.endswith('?') or title.endswith('!'):
                speech_output=title+speech_output
            else:
                speech_output=title+". "+speech_output
        print(speech_output)
    
    return build_response(
            {},
            build_speechlet_response(
                SKILL_NAME, speech_output, reprompt_text, should_end_session
            ))            




def handle_get_help_request(intent, session):
    attributes = {}
    speech_output = "Just ask {} for news analytics!".format(SKILL_NAME)
    reprompt_text = "what can I help you with?"
    should_end_session = False
    return build_response(
        attributes,
        build_speechlet_response(SKILL_NAME, speech_output, reprompt_text, should_end_session)
    )


def handle_finish_session_request(intent, session):
    """End the session with a message if the user wants to quit the app."""
    #attributes = session['attributes']
    attributes=""
    reprompt_text = None
    speech_output = "Thanks for using {}. Have a Great Day.".format(SKILL_NAME)
    should_end_session = True
    return build_response(
        attributes,
        build_speechlet_response_without_card(speech_output, reprompt_text, should_end_session)
    )


def is_answer_slot_valid(intent):
    if 'Answer' in intent['slots'].keys() and 'value' in intent['slots']['Answer'].keys():
        return True
    else:
        return False


# --------------- Helpers that build all of the responses -----------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_speechlet_response_without_card(output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': attributes,
        'response': speechlet_response
    }

