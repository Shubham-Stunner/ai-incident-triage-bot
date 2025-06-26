import os
import httpx
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


def send_slack_message(summary_dict: dict) -> None:
    """Send a formatted Slack message using an incoming webhook."""
    if not WEBHOOK_URL:
        print("No Slack webhook URL configured")
        return

    alertname = summary_dict.get("alertname", "")
    service = summary_dict.get("service", "")
    summary = summary_dict.get("summary", "")
    probable_cause = summary_dict.get("probable_cause", "")
    recommended_fix = summary_dict.get("recommended_fix", "")

    message = (
        f":rotating_light: *{alertname}* on `{service}`\n"
        f"*Summary:* {summary}\n"
        f"*Probable Cause:* {probable_cause}\n"
        f"*Recommended Fix:* {recommended_fix}"
    )

    try:
        httpx.post(WEBHOOK_URL, json={"text": message})
    except Exception as e:
        print(f"Failed to send Slack message: {e}")

