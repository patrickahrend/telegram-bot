from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/contacts.readonly"]

creds = None


def main():
    """Shows basic usage of the People API.
    Prints the name of the first 10 connections.
    """

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
    return creds


def getContactInfo(connection_name):
    creds = main()
    service = build("people", "v1", credentials=creds)
    print("List 10 connection names")
    results = (
        service.people()
        .connections()
        .list(
            resourceName="people/me",
            pageSize=1000,
            personFields="names,biographies,emailAddresses,phoneNumbers",
        )
        .execute()
    )
    connections = results.get("connections", [])

    for person in connections:
        names = person.get("names", [])
        bios = person.get("biographies", [])
        if names:
            print(names)
        if bios:
            print(bios)
        if connection_name in connections:
            print("yes")
        # names = person.get("names", [])
        # bios = person.get("biographies", [])
        # mails = person.get("emailAddresses", [])
        # cells = person.get("phoneNumbers", [])
        # # checks for none
        # if names:
        #     name = names[0].get("displayName")
        # else:
        #     return " No contact found"
        # if bios:
        #     bio = bios[0].get("value")
        # else:
        #     bio = " This contact does not have a bio "
        # if mails:
        #     mail = mails[0].get("value")
        # else:
        #     mail = "No mail found"
        # if cells:
        #     cell = cells[0].get("value")
        # else:
        #     cell = " No cellphone number found"

    # resultStr = ""
    # resultStr = (
    #     name + "\n" + "Cell:" + cell + "\n" + "Email:" + mail + "\n" + "Notes:" + bio
    # )
    # return resultStr


def callfun():
    res = getContactInfo("Patrick")
    print(res)


if __name__ == "__main__":
    callfun()
