all_person_fields = [
    "addresses",
    "ageRanges",
    "biographies",
    "birthdays",
    "calendarUrls",
    "clientData",
    "coverPhotos",
    "emailAddresses",
    "events",
    "externalIds",
    "genders",
    "imClients",
    "interests",
    "locales",
    "locations",
    "memberships",
    "metadata",
    "miscKeywords",
    "names",
    "nicknames",
    "occupations",
    "organizations",
    "phoneNumbers",
    "photos",
    "relations",
    "sipAddresses",
    "skills",
    "urls",
    "userDefined",
]


class Contacts:
    def __init__(self):
        # The file token.pickle stores the user's access and refresh tokens,
        # and is created automatically when the authorization flow completes
        # for the first time.
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
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        creds = creds
        self.service = build("people", "v1", credentials=creds)

    def __strip_body(self, body):
        bad = set(["metadata", "coverPhotos", "photos"])
        tokeep = set(all_person_fields) - bad
        ret = {k: v for k, v in body.items() if k in tokeep}

        # all the other fields are lists of dicts, we must drop the metadata
        # key from any of those dicts
        for k, v in ret.items():
            for i in v:
                i.pop("metadata", None)

        # for some reason some of my contacts have more than one name.  remove
        # anything except the first.  same problem with genders and birthdays
        ret["names"] = [ret["names"][0]]
        if "genders" in ret:
            ret["genders"] = [ret["genders"][0]]
        if "birthdays" in ret:
            ret["birthdays"] = [ret["birthdays"][0]]

        return ret

    def get(self, rn):
        """Return a person body, stripped of resourceName/etag etc"""

        p = (
            self.service.people()
            .get(resourceName=rn, personFields=",".join(all_person_fields))
            .execute()
        )
        return self.__strip_body(p)

    def searchContact(self, name):
        result = (
            self.service.people()
            .searchContacts(
                pageSize=30,
                query=name,
                readMask="biographies,emailAddresses,phoneNumbers",
            )
            .execute()
        )
        return result

    # def filterInf(self, name):
    #     res = self.searchContact(name)

    #     for person in res:
    #         names = person.get("names", [])
    #         bios = person.get("biographies", [])
    #         mails = person.get("emailAddresses", [])
    #         cells = person.get("phoneNumbers", [])
    #         if names:
    #             name = names[0].get("displayName")
    #             print(name)
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
    # cell = " No cellphone number found"

    # resultStr = ""
    # resultStr = (
    #     name
    #     + "\n"
    #     + "Cell:"
    #     + cell
    #     + "\n"
    #     + "Email:"
    #     + mail
    #     + "\n"
    #     + "Notes:"
    #     + bio
    # )
    # return resultStr

    def callfun(self, name):
        res = self.filterInf(name)
        print(res)
