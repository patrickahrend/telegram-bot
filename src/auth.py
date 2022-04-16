# pylint: disable=assignment-from-no-return
from __future__ import print_function

import os.path
from attr import field

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/contacts"]


def main():
    """Shows basic usage of the People API.
    Prints the name of the first 10 connections.
    """
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
    return creds


def getContactInfo(name):
    creds = main()
    service = build("people", "v1", credentials=creds)
    results = (
        service.people()
        .searchContacts(
            pageSize=30, query=name, readMask="biographies,emailAddresses,phoneNumbers",
        )
        .execute()
    )
    quer = results["results"]
    print(quer)
    for person in quer:
        header = person.get("person", [])

        if header:
            print(header["phoneNumbers"][0]["value"])
            print(header["emailAddresses"][0]["value"])
            x = header["biographies"][0].get("value")
            print(x)

        else:
            print("Something went wrong")


if __name__ == "__main__":
    getContactInfo("Farhad")

