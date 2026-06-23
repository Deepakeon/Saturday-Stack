from bs4 import BeautifulSoup
import base64
from googleapiclient.discovery import build # type: ignore
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials


class GmailService:

    def __init__(self, creds: Credentials):
        self.service = build("gmail", "v1", credentials=creds)
    
    def extract_body(self, payload):
        body = payload.get("body", {})
        
        if "data" in body:
            return body["data"]

        for part in payload.get("parts", []):
            result = self.extract_body(part)
            if result:
                return result

        return None

    def format_body(self, body):
        decoded_message_data = base64.urlsafe_b64decode(body).decode("utf-8")
        soup = BeautifulSoup(decoded_message_data, "html.parser")
        text = soup.get_text(separator="\n", strip=True)

        return text

    def fetch_messages(self, q: str = "substack", max_results: int = 5):
        try:
            result = self.service.users().messages().list(userId="me", q=q, maxResults=max_results).execute()

            messages = []

            for message in result.get("messages", []):
                base64_message = self.service.users().messages().get(userId="me", id=message["id"], format="full").execute()
                body_data = self.extract_body(base64_message["payload"])

                if body_data:
                    messages.append(self.format_body(body_data))

            return messages

        except HttpError as error:
            print(f"An error occurred: {error}")