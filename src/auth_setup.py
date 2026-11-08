"""Run this ONCE on your own machine to mint a YouTube refresh token.

    python src/auth_setup.py path/to/client_secret.json

It opens a browser, you approve, and it prints the three values to paste into
the repository secrets: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN.
After that the daily job uploads unattended.
"""
import json
import sys

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    secrets_path = sys.argv[1]
    flow = InstalledAppFlow.from_client_secrets_file(secrets_path, SCOPES)
    creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")

    data = json.loads(open(secrets_path, encoding="utf-8").read())
    installed = data.get("installed") or data.get("web")

    if not creds.refresh_token:
        sys.exit("No refresh token returned. Revoke the app's access at "
                 "myaccount.google.com/permissions and run this again.")

    print("\nPaste these into GitHub -> Settings -> Secrets and variables -> Actions\n")
    print(f"YT_CLIENT_ID      = {installed['client_id']}")
    print(f"YT_CLIENT_SECRET  = {installed['client_secret']}")
    print(f"YT_REFRESH_TOKEN  = {creds.refresh_token}")


if __name__ == "__main__":
    main()
