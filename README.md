# 📌 Documentation: Accessing Office 365 Emails with Microsoft Graph API and Python

## 🛠 1️⃣ Verify and Add API Permissions in Azure
You need to grant your application the `Mail.Read` permission in Application mode.

1. **Go to** [Azure Portal](https://portal.azure.com)
2. **Navigate to** Azure Active Directory → App registrations
3. **Click on your application** (the one with your `Client ID`).
4. **Go to** API permissions → Click on **Add a permission**.
5. **Select** Microsoft Graph → **Application permissions** (⚠️ Not Delegated permissions).
6. **Search for and add** `Mail.Read`.
7. **Click on** **Grant admin consent for [Your Org]** (You need to be an admin for this).
8. **Restart your Python script and test again.**

---

## 🛠 2️⃣ Ensure Authentication is Set to "Application"
In **Azure Active Directory** → **Enterprise Applications**, find your application and ensure authentication is set to **"Application" and not "Delegated"**.

---

## 📌 3️⃣ Python Script to Fetch Emails
Here is a detailed script that connects to Microsoft Graph API and retrieves emails from a specific mailbox.

```python
import msal
import requests

# 🔹 Replace with your Azure credentials
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
TENANT_ID = "your_tenant_id"
USER_EMAIL = "your_email@example.com"

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]

# 🔹 OAuth2 Authentication
app = msal.ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)
token_response = app.acquire_token_for_client(SCOPES)

if "access_token" in token_response:
    access_token = token_response["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # 🔹 URL to retrieve emails
    url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/messages"

    # 🔹 Filter: Retrieve only emails with subjects starting with "backup"
    params = {
        "$filter": "startswith(subject, 'backup')",
        "$top": 10,  # Number of emails to fetch
        "$select": "subject,from"  # Fetch only subject and sender
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        emails = response.json()

        # 🔹 Check if there are emails returned
        if "value" in emails and emails["value"]:
            for email in emails["value"]:
                sender = email["from"]["emailAddress"]["name"]
                subject = email["subject"]
                print(f"📩 From: {sender}, Subject: {subject}")
        else:
            print("🚨 No emails found with 'backup' in the subject.")
    else:
        print(f"❌ API Error ({response.status_code}): {response.text}")
else:
    print("❌ Authentication Error:", token_response.get("error_description"))
```

---

## 🛠 4️⃣ Code Explanation

### 1️⃣ **Authentication with Microsoft Graph API**
- **`msal.ConfidentialClientApplication`**: Used to obtain an **access token** in application mode.
- **Scopes (`SCOPES`)**: Uses `https://graph.microsoft.com/.default` to include all defined permissions.
- **Token response**: Checks if the token is retrieved before making requests.

### 2️⃣ **API Request to Fetch Emails**
- **`url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/messages"`**: Targets the mailbox of `your_email@example.com`.
- **Request Parameters**:
  - **`$filter`**: Filters emails where the subject starts with "backup".
  - **`$top=10`**: Limits the number of emails returned to 10.
  - **`$select=subject,from`**: Retrieves only the subject and sender.

### 3️⃣ **Processing the Response**
- **If `response.status_code == 200`**: Displays retrieved emails.
- **If no emails match the filter**: Displays a message.
- **Error handling**:
  - **Authentication error** (incorrect credentials, insufficient permissions).
  - **API error** (e.g., access denied).

---

## 🚀 **Summary and Testing**
✅ **Configure Azure (`Mail.Read` permission, Grant Admin Consent)**  
✅ **Verify authentication is in Application mode**  
✅ **Run the script and fetch filtered emails**  

🎯 **If you get a `403 Access Denied` error:**
- Ensure `Mail.Read` is set as an **Application permission**.
- Make sure **Grant Admin Consent** has been approved in Azure.
- Verify that your **access token is valid**.

💡 **Tip:** To test your token, run:
```bash
curl -X GET "https://graph.microsoft.com/v1.0/users/your_email@example.com/messages" \
   -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
➡️ **If you receive `403`, it's a permission issue!**

---

🔹 **With this documentation, you can easily retrieve emails from Office 365 using Python!** 🚀

