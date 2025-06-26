import os
import httpx
from dotenv import load_dotenv

load_dotenv()

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_slack_message(summary: dict):
    alertname = summary.get("alertname", "N/A")
    service = summary.get("service", "N/A")
    title = summary.get("summary", "No summary")
    cause = summary.get("probable_cause", "Unknown cause")
    fix = summary.get("recommended_fix", "No fix suggested")

    message = {
        "text": f":rotating_light: *Incident Alert: `{alertname}`*",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"🚨 {alertname} on {service}",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Summary:*\n{title}\n\n*Probable Cause:*\n{cause}\n\n*Recommended Fix:*\n{fix}"
                }
            }
        ]
    }

    response = httpx.post(SLACK_WEBHOOK_URL, json=message)
    if response.status_code != 200:
        print("Slack send error:", response.text)