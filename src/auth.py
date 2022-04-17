# pylint: disable=assignment-from-no-return
from __future__ import print_function
import os.path
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

def addNote(name:str): -> str:
    

if __name__ == "__main__":
    s = getContactInfo("Patrick")
    print(s)

