from pathlib import Path
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow   # type: ignore
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

BASE_DIR = Path(__file__).resolve().parent.parent
CREDENTIALS_DIR = BASE_DIR / "credentials"
TOKEN_PATH = CREDENTIALS_DIR / "token.json"
OAUTH_CREDS_PATH = CREDENTIALS_DIR / "gcp-oauth.keys.json"

def authenticate_with_google() -> Credentials | None:
  creds: Credentials | None = None

  if TOKEN_PATH.exists():
    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          str(OAUTH_CREDS_PATH), SCOPES
      )
      creds = flow.run_local_server(port=0)

    with open(TOKEN_PATH, "w") as token:
      token.write(creds.to_json())
    
  return creds
    
