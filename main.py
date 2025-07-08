from datetime import datetime
from fastapi import FastAPI, Request
from dotenv import load_dotenv
import httpx

from openai_handler import process_alert_with_ai
from slack_notify import send_slack_message

load_dotenv()

app = FastAPI()


async def query_loki_logs(instance: str) -> str:
    """Fetch recent logs for the given instance from Loki."""
    if not instance:
        return ""
    url = "http://loki:3100/loki/api/v1/query_range"
    params = {"query": f'{{instance="{instance}"}}', "limit": 20}
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params, timeout=5.0)
            resp.raise_for_status()
            data = resp.json()
            result = data.get("data", {}).get("result", [])
            if result:
                logs = [v[1] for v in result[0].get("values", [])]
                return "\n".join(logs[-5:])
    except Exception as exc:
        return f"Error fetching logs: {exc}"
    return "No logs found"


def generate_tempo_trace_url(service: str) -> str:
    """Return a placeholder Tempo trace URL for the service."""
    ts = int(datetime.utcnow().timestamp())
    return f"http://tempo:3200/trace/{service}/{ts}"


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
    summary.update({
        "alertname": alert_data.get("alertname"),
        "service": alert_data.get("service"),
    })

    instance = labels.get("instance")
    summary["log_snippet"] = await query_loki_logs(instance)
    summary["trace_url"] = generate_tempo_trace_url(alert_data.get("service"))

    send_slack_message(summary)
    return {"status": "processed", "summary": summary}

