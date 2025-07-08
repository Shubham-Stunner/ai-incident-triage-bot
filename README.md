# AI Incident Triage Assistant

This project demonstrates receiving a Prometheus AlertManager payload, using OpenAI to generate a possible root cause and fix, and sending the summary to Slack.

## Setup

1. Install dependencies in a virtual environment:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and fill in your OpenAI API key and Slack webhook URL.

## Running

Start the FastAPI server with:

```bash
uvicorn main:app --reload
```

The server will listen on `http://127.0.0.1:8000` by default.

## Testing the `/alert` endpoint

You can send the sample alert using `curl`:

```bash
curl -X POST -H "Content-Type: application/json" \
     --data @alert_example.json \
     http://127.0.0.1:8000/alert
```

