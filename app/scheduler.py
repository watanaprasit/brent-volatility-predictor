from apscheduler.schedulers.background import BackgroundScheduler
from crud import fetch_data
from model import train_model


def scheduled_update():
    fetch_data()  # Update dataset
    train_model()  # Retrain model
    print("Daily update complete.")

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_update, "interval", days=1)
    scheduler.start()

    try:
        print("Scheduler running. Press Ctrl+C to exit.")
        while True:
            pass  # Keep the scheduler running
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
