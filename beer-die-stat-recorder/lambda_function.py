
# Imports
import sys
sys.path.append('dependencies')
import os

import boto3
from twilio.rest import Client
from twilio.twiml.messaging_response import Message, MessagingResponse

from helpers import *

# Get environment variables
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")

# Commands
COMMANDS = {
    "New NAME": 'Create your new player profile. You can also use this command to blank your profile',
    "Remove": 'Deletes your old player profile',
    "Seedings": 'Gives the current tournament seeding based on BDSM score',
    "NAME": 'Returns the recorded stats and BDSM for a particular player (NAME)',
    "Stats": 'Returns all your stats, as well as your BDSM score',
    "Skunks": "Returns all players' skunks",
    "Plunks": "Returns all players' plunks",
    "Drops": "Returns all players' drops",
    "Self-plunks": "Returns all players' self-plunks",
    "Fifas": "Returns all players' FIFAs",
    "Add # losses": 'Record losses',
    "Add # wins": 'Record wins',
    "Add # drops": 'Record easy drops',
    "Add # plunks": 'Record plunks',
    "Add # self-plunks": 'Record self-plunks',
    "Add # skunks": 'Record skunks',
    "Add # fifas": "Record FIFAs",
    "Hi": 'Returns description of API service and instructions for giving commands, formatting texts, etc.',
    "Commands": 'Returns all the possible commands the user can input (with descriptions)',
}



# lambda function
def lambda_handler(event, context):
    
    # Set up db table
    dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
    table = dynamodb.Table("beer_die_stats_spring_2023")

    # Decode message
    request_message = decode(event['Body']).upper().strip(' ').split(' ')
    
    # Parse first word from request_message
    word1 = request_message[0]
    
    # Get phone number
    number = str(event["From"])
    
    # For messages of length 1
    if len(request_message) == 1:
        # Develope message based on command
        message = ''
        if word1 == 'COMMANDS':
            message += commands(COMMANDS) 
        elif word1 == 'HI':
            message += hi()
        elif word1 == 'REMOVE':
            message += remove(number, table)
        elif word1 == 'SEEDINGS':
            message += seedings(table)
        elif word1 == 'STATS':
            json = read(number, table)
            message += stats(json, table)
        elif word1 == 'SKUNKS':
            message += skunks(table)
        elif word1 == 'PLUNKS':
            message += plunks(table)
        elif word1 == 'DROPS':
            message += drops(table)
        elif word1 == 'SELF-PLUNKS':
            message += selfPlunks(table)
        elif word1 == 'FIFAS':
            message += fifas(table)
        else:
            scan = table.scan()
            for i in scan['Items']:
                if i["info"]["name"] == word1:
                    message += stats(i, table)
            if len(message) == 0:
                message += "Invalid message! That command/name was not found in our database. Text in 'Commands' to get a list of valid texts"

        # Respond
        response(message, number, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                
    # For messages of length 2
    elif len(request_message) == 2:
        word2 = request_message[1]
        
        # Develope message based on command
        message = ''
        if word1 == 'NEW':
            message = new(number, word2, table)
        else:
            message += "Invalid message! That command/name was not found in our database. Text in 'Commands' to get a list of valid texts"
        
        # Respond
        response(message, number, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    # For messages of length 3
    elif len(request_message) == 3:
        word2, word3 = request_message[1], request_message[2]
        
        # Develope message based on command
        message = ''
        if word1 == 'ADD':
            json = read(number, table)
            if not json:
                message = "No profile found for you! First, type in 'New NAME' (NAME being your first name)"
            elif word3 == 'LOSSES' or word3 == 'LOSS':
                message = update(number, word2, json, 'losses', table)
            elif word3 == 'WINS' or word3 == 'WIN':
                message = update(number, word2, json, 'wins', table)
            elif word3 == 'DROPS' or word3 == 'DROP':
                message = update(number, word2, json, 'drops', table)
            elif word3 == 'PLUNKS' or word3 == 'PLUNK':
                message = update(number, word2, json, 'plunks', table)
            elif word3 == 'SELF-PLUNKS' or word3 == 'SELF-PLUNK':
                message = update(number, word2, json, 'self_plunks', table)
            elif word3 == 'SKUNKS' or word3 == 'SKUNK':
                message = update(number, word2, json, 'skunks', table)  
            elif word3 == 'FIFAS' or word3 == 'FIFA':
                message = update(number, word2, json, 'fifas', table)   
            else: 
                message += "Invalid message! That command/name was not found in our database. Text in 'Commands' to get a list of valid texts"
        else: 
            message += "Invalid message! That command/name was not found in our database. Text in 'Commands' to get a list of valid texts"

        # Respond or send error message if necessary
        response(message, number, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            
    # Send error message if necessary
    else:
        response("Invalid message! That command/name was not found in our database. Text in 'Commands' to get a list of valid texts", number, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
