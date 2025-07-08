import os
import httpx
from dotenv import load_dotenv

load_dotenv()

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


def send_slack_message(summary: dict) -> None:
    """Send formatted alert details to Slack."""
    alertname = summary.get("alertname", "N/A")
    service = summary.get("service", "N/A")
    title = summary.get("summary", "No summary")
    cause = summary.get("probable_cause", "Unknown cause")
    fix = summary.get("recommended_fix", "No fix suggested")
    logs = summary.get("log_snippet", "No logs found")
    trace_url = summary.get("trace_url", "")

    text_parts = [
        f"*Summary:*\n{title}",
        f"*Probable Cause:*\n{cause}",
        f"*Recommended Fix:*\n{fix}",
    ]
    if logs:
        text_parts.append(f"*Logs:*\n{logs}")
    if trace_url:
        text_parts.append(f"*Trace:* <{trace_url}|View Trace>")
    text_block = "\n\n".join(text_parts)

    message = {
        "text": f":rotating_light: *Incident Alert: `{alertname}`*",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"🚨 {alertname} on {service}",
                    "emoji": True,
                },
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": text_block},
            },
        ],
    }

    response = httpx.post(SLACK_WEBHOOK_URL, json=message)
    if response.status_code != 200:        print("Slack send error:", response.text)

