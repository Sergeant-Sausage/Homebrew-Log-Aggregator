## pip install requests msal if you don't have them already

import requests
import json
import msal

## Load creds from config file (use the template if you don't know how to create one)
with open ("config.json") as f:
    config = json.load(f)

TENANT_ID = config["tenant_id"]
CLIENT_ID = config["client_id"]
CLIENT_SECRET = config["client_secret"]

## Will add more to the scope later, testing basic logic for pulling logs

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]
ENDPOINT = "https://graph.microsoft.com/v1.0/auditLogs/signIns"

## Authenticate using creds from config.json

app = msal.ConfidentialClientApplication(
    CLIENT_ID,
    authority=AUTHORITY,
    client_credential=CLIENT_SECRET
)
result = app.acquire_token_for_client(scopes=SCOPE)

## Pull 25 most recent sign-ins and dump to a file called "entra_signins.json"

if "access_token" in result:
    headers = {
        "Authorization": f"Bearer {result['access_token']}",
        "Content-Type": "application/json"
    }
    params = {
        "$top": 25
    }
    response = requests.get(ENDPOINT, headers=headers, params=params)

## write to file, and report error if one is encountered
    
    if response.status_code == 200:
        signins = response.json().get("value", [])
        with open("entra_signins.json", "w") as f:
            json.dump(signins, f, indent=2)
        print(f"Pulled {len(signins)} sign-in records.")
    else:
        print(f"API error {response.status_code}: {response.text}")
else:
    print("Auth failed:", result.get("error_description"))
