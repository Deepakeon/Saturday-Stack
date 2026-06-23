import os.path

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow   # type: ignore
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def authenticate_with_google() -> Credentials | None:
  creds: Credentials | None = None

  if os.path.exists("credentials/token.json"):
    creds = Credentials.from_authorized_user_file("credentials/token.json", SCOPES)

  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials/gcp-oauth.keys.json", SCOPES
      )
      creds = flow.run_local_server(port=0)

    with open("credentials/token.json", "w") as token:
      token.write(creds.to_json())
    
  return creds
    
