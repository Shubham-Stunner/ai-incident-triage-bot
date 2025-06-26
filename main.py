from fastapi import FastAPI, Request
from dotenv import load_dotenv

from openai_handler import process_alert_with_ai
from slack_notify import send_slack_message

# Load environment variables
load_dotenv()

app = FastAPI()


@app.post("/alert")
async def receive_alert(request: Request):
    """Endpoint to receive Prometheus alert payloads."""
    payload = await request.json()
    alerts = payload.get("alerts", [])
    if not alerts:
        return {"status": "no alerts found"}

    alert = alerts[0]
    labels = alert.get("labels", {})
    annotations = alert.get("annotations", {})

    alert_data = {
        "alertname": labels.get("alertname"),
        "service": labels.get("service"),
        "severity": labels.get("severity"),
        "labels": labels,
        "annotations": annotations,
    }

    summary = process_alert_with_ai(alert_data)
    # Include alert info in summary for slack message
    summary.update({
        "alertname": alert_data.get("alertname"),
        "service": alert_data.get("service"),
    })
    send_slack_message(summary)
    return {"status": "processed", "summary": summary}

