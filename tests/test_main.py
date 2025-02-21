import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from main import app, process_email_metrics, fetch_email_metrics

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Email Open Rate Tracking Integration is running"}

@pytest.mark.asyncio
async def test_fetch_email_metrics():
    metrics = await fetch_email_metrics()
    assert isinstance(metrics, list)
    assert len(metrics) > 0
    assert "campaign_id" in metrics[0]
    
def test_process_email_metrics():
    # Create dummy metrics with a low open rate
    dummy_metrics = [
        {"campaign_id": 1, "subject": "Test", "open_rate": 25.0},
        {"campaign_id": 2, "subject": "Test 2", "open_rate": 45.0}
    ]
    report = process_email_metrics(dummy_metrics, threshold=30.0)
    assert report["total_campaigns"] == 2
    assert len(report["low_performing_campaigns"]) == 1
