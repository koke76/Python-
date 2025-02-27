import msal
import requests

# Azure 
CLIENT_ID = ""
CLIENT_SECRET = ""
TENANT_ID = ""
USER_EMAIL = ""

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]

# AUTH 02
app = msal.ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)
token_response = app.acquire_token_for_client(SCOPES)

if "access_token" in token_response:
    access_token = token_response["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # 🔹 URL 
    url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/messages"

    # 🔹 Filtre
    params = {
        "$filter": "startswith(subject, ' ')",
        "$top": 100,  # Nombre d'emails à récupérer
        "$select": "subject,from"  # Récupérer uniquement le sujet et l'expéditeur
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        emails = response.json()

        # 🔹 Vérifier s'il y a des emails retournés
        if "value" in emails and emails["value"]:
            for email in emails["value"]:
                sender = email["from"]["emailAddress"]["name"]
                subject = email["subject"]
                print(f"📩 De: {sender}, Sujet: {subject}")
        else:
            print("🚨 Aucun email trouvé avec '' dans le sujet.")
    else:
        print(f"❌ Erreur API ({response.status_code}): {response.text}")
else:
    print("❌ Erreur d'authentification:", token_response.get("error_description"))
