from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]

flow = InstalledAppFlow.from_client_secrets_file(
    'backend/credentials.json',
    scopes=SCOPES
)

creds = flow.run_local_server(
    host='localhost',
    port=8080,
    authorization_prompt_message='Please visit this URL: {url}',
    success_message='Authentication successful! You may close this window.',
    open_browser=True
)

print("Authentication successful!")