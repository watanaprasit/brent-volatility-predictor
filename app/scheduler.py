from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from zoneinfo import ZoneInfo  # Use zoneinfo for time zone handling
from crud import fetch_data  # Make sure to import the fetch_data function
from model import train_model
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)

# Define the Singapore timezone using zoneinfo
SGT = ZoneInfo("Asia/Singapore")

def scheduled_update():
    """
    This function fetches the data, updates the CSV, and trains the model for the previous day's Brent Crude Oil closing data.
    """
    # Log the start of the task
    logging.info(f"Starting daily update for the past day: {datetime.now(SGT)}")
    
    # Update the dataset with the latest data
    fetch_data()  # This will update the CSV with new data from Yahoo Finance
    # Retrain the model with the updated data
    train_model()  # Retrains the model
    
    logging.info("Daily update complete.")

def log_job_status(event):
    """
    Log job status (whether it was executed or there was an error)
    """
    if event.exception:
        logging.error(f"Job failed: {event.job_id}")
    else:
        logging.info(f"Job completed: {event.job_id}")

if __name__ == "__main__":
    # Set up the scheduler with Singapore timezone
    scheduler = BackgroundScheduler(timezone=SGT)

    # Add the job to run daily at 2 PM Singapore Time
    scheduler.add_job(scheduled_update, "cron", hour=14, minute=0, second=0, id="daily_update_job")

    # Add a listener to log job status
    scheduler.add_listener(log_job_status, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    # Start the scheduler
    scheduler.start()

    # Keep the scheduler running
    try:
        logging.info("Scheduler running. Press Ctrl+C to exit.")
        while True:
            pass  # Keeps the scheduler running
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


