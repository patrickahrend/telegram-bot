import re
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = [
    "https://www.googleapis.com/auth/contacts.readonly",
]


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
        process_message(message, ["google"], "Let me take a look"),
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

    if "google:" in message:
        name = message.split(":")
        name = name[1]
        note = google_connection(name)
        bot_response = "Here are the contacts notes:" + " " + note

    print("Bot response:", bot_response)
    return bot_response


def google_connection(con_name):
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("people", "v1", credentials=creds)
        # results = (
        #     service.people()
        #     .connections()
        #     .list(
        #         resourceName="people/me",
        #         pageSize=10,
        #         personFields="names, biographies, emailAddresses, phoneNumbers",
        #     )
        #     .execute()
        # )

        profile = service.people().get('people/me')
        print(profile)
        #connections = results.get("connections", [])

        # for person in connections:
        #     names = person.get("names", [])
        #     bios = person.get("biographies", [])
        #     # emails = person.get("emailAddresses", [])
        #     # phonenumber = person.get("phoneNumbers", [])
        #     returnStr = ""

        #     print("from function body", con_name)
        #     if names:
        #         name = names[0].get("displayName")
        #         returnStr = name
        #     if bios:
        #         bio = bios[0].get("value")
        #         returnStr += bio
        #         # if emails:
        #         #     email = emails[0].get("value")
        #         #     returnStr += email
        #         # if phonenumber:
        #         #     cell = phonenumber[0].get("value")
        #         #     returnStr += cell
        #         # else:
        #         #     returnStr += "Sorry, I could not find a person under that name."

        #     return returnStr

    except HttpError as err:
        print(err)

