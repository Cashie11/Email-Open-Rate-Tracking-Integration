# Email Open Rate Tracking Integration

This integration tracks email campaign open rates by periodically fetching metrics from MailChimp/SendGrid (simulated with dummy data), processing the data to identify low-performing subject lines, and sending a performance report to an external endpoint. It is built as an **Interval Integration** using FastAPI, APScheduler, and httpx.

## Features

- **Fetch Email Metrics:** Simulates retrieving email campaign metrics.
- **Process Metrics:** Identifies campaigns with open rates below a specified threshold.
- **Scheduled Reporting:** Uses APScheduler to run the tracking task at regular intervals.
- **Manual Trigger:** Provides endpoints to manually trigger the tracking task for testing.
- **Integration Ready:** Designed to meet the Telex Integration Settings Spec for deployment.

## Project Structure

```
email-open-rate-tracking/
├── main.py                # Main application code
├── integration.json       # Integration configuration file
├── requirements.txt       # Project dependencies
├── README.md              # Project documentation (this file)
├── .gitignore             # Git ignore file
└── tests/
    └── test_main.py       # Unit tests for the integration
```

## Setup Instructions

### Prerequisites
- Python 3.12 or higher
- Git
- A tool for HTTP requests (e.g., Postman, cURL)

### Installation Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/<your-username>/email-open-rate-tracking.git
   cd email-open-rate-tracking
   ```

2. **Create and Activate a Virtual Environment:**
   * On macOS/Linux:
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```
   * On Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**
   ```bash
   uvicorn main:app --reload
   ```
   The server should start at http://127.0.0.1:8000.

## API Endpoints

### GET /
* **Description:** Health-check endpoint.
* **Request:** `GET http://127.0.0.1:8000/`
* **Response:**
  ```json
  {"message": "Email Open Rate Tracking Integration is running"}
  ```

### POST /trigger-task
* **Description:** Manually triggers the email tracking task.
* **Request:** `POST http://127.0.0.1:8000/trigger-task`
* **Response:**
  ```json
  {"message": "Email Open Rate Tracking task triggered"}
  ```

## Testing

### Running Automated Tests
To run the unit tests:
```bash
python -m pytest
```
All tests should pass, confirming that your functions work as expected.

## Integration Configuration

The `integration.json` file includes the necessary configuration details:

```json
{
  "name": "Email Open Rate Tracking",
  "type": "interval",
  "description": "Tracks email campaign open rates and identifies low-performing subject lines by fetching metrics from MailChimp/SendGrid.",
  "version": "1.0.0",
  "entrypoint": "https://your-deployed-service.com/email-open-rate-tracking",
  "documentation": "https://github.com/<your-username>/email-open-rate-tracking#readme"
}
```

*Note:* Update the `entrypoint` and `documentation` fields with the correct URLs once you deploy the integration.

## Deployment

For deployment:
* Host the integration JSON file on a publicly accessible URL (e.g., via GitHub Pages).
* Deploy your integration to your designated test Telex organization or a staging environment.
* Update the `entrypoint` in the JSON file with your live URL.

## License

This project is licensed under the MIT License.

## Acknowledgements

* Built with FastAPI.
* Scheduling provided by APScheduler.
* HTTP requests handled by httpx.
* Testing with pytest.