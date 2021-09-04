import requests
import json
import random

class EMail:
    def __init__(self, f, to, subject, text=None, html=None):
        self.From = f
        self.To = to
        self.Subject = subject
        self.Text = text
        self.Html = html

class Dropmail:
    def __init__(self, auth_token):
        self.token = auth_token

    def GetDomains(self):
        r = requests.get("https://dropmail.me/api/graphql/"+self.token+"?query=query%20%7Bdomains%20%7Bid%2C%20name%7D%7D")
        data = json.loads(r.text)

        return data["data"]["domains"]

    def PickRandomDomain(self):
        domains = self.GetDomains()
        domain = random.sample(domains, 1)[0]

        return domain["name"], domain["id"]

    def NewSession(self):
        r = requests.get("https://dropmail.me/api/graphql/"+self.token+"?query=mutation%20%7BintroduceSession%20%7Bid%2C%20expiresAt%2C%20addresses%20%7Baddress%7D%7D%7D")
        data = json.loads(r.text)

        self.SessionId = data["data"]["introduceSession"]["id"]
        self.Address = data["data"]["introduceSession"]["addresses"][0]["address"]

    def GetEmails(self):
        r = requests.get("https://dropmail.me/api/graphql/"+self.token+"?query=query%20%7Bsessions%20%7Bid%2C%20expiresAt%2C%20mails%20%7BrawSize%2C%20fromAddr%2C%20toAddr%2C%20downloadUrl%2C%20text%2C%20headerSubject%7D%7D%7D")
        data = json.loads(r.text)

        sessions = data["data"]["sessions"]

        emails = []

        for s in sessions:
            mails = s["mails"]
            for m in mails:
                mailObject = EMail(m["fromAddr"], m["toAddr"], m["headerSubject"], m["text"])
                emails.append(mailObject)

        return emails

