import msal


CLIENT_ID = "ton_client_id"
CLIENT_SECRET = "ton_client_secret"
TENANT_ID = "ton_tenant_id"

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]


app = msal.ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)
token_response = app.acquire_token_for_client(SCOPES)

if "access_token" in token_response:
    access_token = token_response["access_token"]
    print("🔑 Access Token:", access_token)  
else:
    print("❌ Erreur d'authentification:", token_response.get("error_description"))
