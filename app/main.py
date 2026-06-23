from gmail.auth import authenticate_with_google
from gmail.service import GmailService

if __name__ == "__main__":
    creds = authenticate_with_google()
    gmail_service = GmailService(creds=creds)
    messages = gmail_service.fetch_messages(q="substack", max_results=1)
    
    print(messages)