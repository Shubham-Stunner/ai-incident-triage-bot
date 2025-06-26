import os
import json
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


def process_alert_with_ai(alert_data: dict) -> dict:
    """Send alert information to OpenAI and return a summary dictionary."""
    alert_name = alert_data.get("alertname", "")
    description = alert_data.get("annotations", {}).get("description", "")
    severity = alert_data.get("severity", "")

    prompt = (
        "You are an SRE. Here's the alert:\n"
        f"- Alert Name: {alert_name}\n"
        f"- Description: {description}\n"
        f"- Severity: {severity}\n"
        "Suggest the root cause and a fix. "
        "Respond using this JSON format:\n"
        "{\n  \"summary\": \"<short summary>\",\n"
        "  \"probable_cause\": \"<probable cause>\",\n"
        "  \"recommended_fix\": \"<recommended fix>\"\n}"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        content = response.choices[0].message.content.strip()
        summary_dict = json.loads(content)
    except Exception as e:
        # In case of an error we return a simple message
        summary_dict = {
            "summary": "Failed to get AI response",
            "probable_cause": str(e),
            "recommended_fix": "Check OpenAI configuration",
        }
    return summary_dict

