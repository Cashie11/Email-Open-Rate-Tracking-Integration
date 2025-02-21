# main.py
from fastapi import FastAPI, BackgroundTasks
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio
import datetime
import httpx
from contextlib import asynccontextmanager
import random

# Initialize the background scheduler
scheduler = BackgroundScheduler()

# Simulated function to fetch email metrics from MailChimp/SendGrid API
async def fetch_email_metrics():
    # Simulate delay (e.g., API call latency)
    await asyncio.sleep(1)
    # Return dummy data: a list of campaigns with subject lines and open rates (in percentage)
    dummy_data = [
        {"campaign_id": 1, "subject": "Sale Now On!", "open_rate": random.uniform(10, 80)},
        {"campaign_id": 2, "subject": "Last Chance to Save", "open_rate": random.uniform(10, 80)},
        {"campaign_id": 3, "subject": "New Arrivals Just In", "open_rate": random.uniform(10, 80)},
    ]
    return dummy_data

# Process email metrics and identify low-performing subject lines
def process_email_metrics(metrics, threshold=30.0):
    # Identify campaigns with open rate below the specified threshold
    low_performing = [campaign for campaign in metrics if campaign["open_rate"] < threshold]
    report = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "total_campaigns": len(metrics),
        "low_performing_campaigns": low_performing,
    }
    return report

# Simulated function to send the report to an endpoint (using httpbin.org for testing)
async def send_email_report(report):
    async with httpx.AsyncClient() as client:
        try:
            # For testing, we post to httpbin.org.
            # When ready, replace this URL with your actual endpoint.
            response = await client.post("https://httpbin.org/post", json=report)
            # Debugging output
            print("Response status code:", response.status_code)
            print("Response text:", response.text)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print("Error sending report:", repr(e))
            raise e

# The main task: fetch metrics, process them, and send a report
async def email_open_rate_tracking_task():
    try:
        print("Running Email Open Rate Tracking Task...")
        metrics = await fetch_email_metrics()
        print("Fetched email metrics:", metrics)
        report = process_email_metrics(metrics)
        print("Generated report:", report)
        result = await send_email_report(report)
        print("Report sent:", result)
    except Exception as e:
        print("Email Open Rate Tracking Task failed:", repr(e))

# Schedule the task to run at regular intervals.
# For testing, we schedule it to run every minute (adjust as needed).
def start_scheduler():
    scheduler.add_job(lambda: asyncio.run(email_open_rate_tracking_task()), 'cron', minute='*/1')
    scheduler.start()

# Use FastAPI's lifespan event handler to manage startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize scheduler
    start_scheduler()
    yield
    # Shutdown: gracefully shutdown the scheduler
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

# Root endpoint for a quick health-check
@app.get("/")
def read_root():
    return {"message": "Email Open Rate Tracking Integration is running"}

# Endpoint to manually trigger the task (for testing)
@app.post("/trigger-task")
async def trigger_task(background_tasks: BackgroundTasks):
    background_tasks.add_task(email_open_rate_tracking_task)
    return {"message": "Email Open Rate Tracking task triggered"}
