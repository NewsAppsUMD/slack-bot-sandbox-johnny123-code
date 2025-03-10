import requests
import os
from slack import WebClient
from slack.errors import SlackApiError

# Load API keys from environment variables
CONGRESS_API_KEY = os.getenv("CONGRESS_API_KEY")
SLACK_API_TOKEN = os.getenv("SLACK_API_TOKEN")

# Initialize Slack client
slack_client = WebClient(token=SLACK_API_TOKEN)

# Congress API details
BASE_URL = "https://api.congress.gov/v3"
ENDPOINT = "/committee-report"
HEADERS = {"X-API-Key": CONGRESS_API_KEY}

# Function to get committee reports
def fetch_committee_reports(congress_number=118):
    url = f"{BASE_URL}{ENDPOINT}?congress={congress_number}&format=json"

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return data.get("reports", [])  # Get list of reports
    except requests.exceptions.RequestException as e:
        print(f"Error fetching reports: {e}")
        return []

# Function to send reports to Slack
def post_reports_to_slack(reports):
    channel = "slack-bots"

    for report in reports[:5]:  # Limit to 5 reports
        citation = report.get("citation", "No citation available")
        report_url = report.get("url", "No URL available")
        message = f"📜 *New Committee Report*\n> *Citation:* {citation}\n🔗 [View Report]({report_url})"

        try:
            slack_client.chat_postMessage(channel=channel, text=message)
            print("Message sent successfully!")
        except SlackApiError as e:
            print(f"Slack API Error: {e.response['error']}")

# Fetch and send reports
reports = fetch_committee_reports()
if reports:
    post_reports_to_slack(reports)
else:
    print("No reports found.")