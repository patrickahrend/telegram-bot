import re
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os
import constants as c


GOOGLE_AUTH = c.GOOGLE_AUTH
SCOPES = ["https://www.googleapis.com/auth/contacts.readonly"]

def process_message(message, response_array, response):
    # Splits the message and the punctuation into an array
    list_message = re.findall(r"[\w']+|[.,!?;]", message.lower())

    # Scores the amount of words in the message
    score = 0
    for word in list_message:
        if word in response_array:
            score = score + 1

    # Returns the response and the score of the response
    # print(score, response)
    return [score, response]


def get_response(message):
    # Add your custom responses here
    response_list = [
        process_message(message, ["hello", "hi", "hey"], "Hey there!"),
        process_message(message, ["bye", "goodbye"], "Goodbye!"),
        process_message(message, ["how", "are", "you"], "I'm doing fine thanks!"),
        
        process_message(
            message, ["your", "name"], "My name is Farah, nice to meet you!"
        ),
        process_message(message, ["help", "me"], "I will do my best to assist you!"),
        process_message(message, ["fahard"], google_connection())
        # Add more responses here
    ]

    # Checks all of the response scores and returns the best matching response
    response_scores = []
    for response in response_list:
        response_scores.append(response[0])

    # Get the max value for the best response and store it into a variable
    winning_response = max(response_scores)
    matching_response = response_list[response_scores.index(winning_response)]

    # Return the matching response to the user
    if winning_response == 0:
        bot_response = "I didn't understand what you wrote."
    else:
        bot_response = matching_response[1]

    print("Bot response:", bot_response)
    return bot_response


def google_connection():
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = c.GOOGLE_AUTH

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return creds


# Test your system
# get_response('What is your name bruv?')
# get_response('Can you help me with something please?')
