import re
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os.path

SCOPES = ["https://www.googleapis.com/auth/contacts"]


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
            message, ["your", "name"], "My name is Patrick's Bot, nice to meet you!"
        ),
        process_message(message, ["help", "me"], "I will do my best to assist you!"),
    ]

    response_scores = []
    for response in response_list:
        response_scores.append(response[0])

    winning_response = max(response_scores)
    matching_response = response_list[response_scores.index(winning_response)]

    if winning_response == 0:
        bot_response = "I didn't understand what you wrote."
    else:
        bot_response = matching_response[1]

    if "soc:lu:" in message:
        name = message.split(":")
        name = name[2]
        note = getContactInfo(name)
        bot_response = " " + note
    print("Bot response:", bot_response)
    return bot_response


def main():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def getContactInfo(name: str) -> str:
    creds = main()
    service = build("people", "v1", credentials=creds)
    results = (
        service.people()
        .searchContacts(
            pageSize=30,
            query=name,
            readMask="biographies,emailAddresses,phoneNumbers,organizations",
        )
        .execute()
    )
    result = " "

    if results.get("results"):
        quer = results["results"]
        for person in quer:
            header = person.get("person", [])
            result += "\n" + "This is the person found:" + "\n"
            if header:
                if header.get("phoneNumbers") is not None:
                    result += "Cell: " + header.get("phoneNumbers")[0]["value"]
                else:
                    result += "No Cell found"
                if header.get("emailAddresses") is not None:
                    result += ", Mail: " + header.get("emailAddresses")[0]["value"]
                else:
                    result += ", No Mail found"
                if header.get("organizations") is not None:
                    result += ", Company: " + header.get("organizations")[0]["name"]
                else:
                    result += ", No Company found"
                if header.get("biographies") is not None:
                    result += ", Note: " + header.get("biographies")[0]["value"]
                else:
                    result += ", No Bio found"

            else:
                print("The person does not have content ")
        return result
    else:
        result = "Sorry I could not find a person under that Name."
        return result

