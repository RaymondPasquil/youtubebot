from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import os

# Path to credentials folder
CREDENTIALS_FOLDER = "credentials/"

def authenticate_youtube(client_secret_file):
    flow = InstalledAppFlow.from_client_secrets_file(
        os.path.join(CREDENTIALS_FOLDER, client_secret_file),
        scopes=["https://www.googleapis.com/auth/youtube.force-ssl"]
    )
    creds = flow.run_local_server(port=0)

    # Save credentials
    token_file = client_secret_file.replace('.json', '_token.pickle')
    with open(os.path.join(CREDENTIALS_FOLDER, token_file), 'wb') as token:
        pickle.dump(creds, token)

    print(f"Authenticated and saved token for {client_secret_file}")

# Authenticate each account
for file in os.listdir(CREDENTIALS_FOLDER):
    if file.endswith(".json"):
        authenticate_youtube(file)

print("All accounts authenticated successfully!")
