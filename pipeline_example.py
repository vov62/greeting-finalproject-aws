from pymongo import MongoClient
from datetime import datetime, timedelta

# Connect to MongoDB
client = MongoClient('mongodb://127.0.0.1:27017')  # Local MongoDB
db = client['aws']  # Database name
events_collection = db['events']  # Collection name


def add_event(name, date, event_type, greetings):
    """
    Add an event to the database with the new structure.

    Args:
        name (str): Name of the event.
        date (datetime): Date of the event.
        event_type (str): Type of the event (e.g., 'Religious', 'Personal').
        greetings (dict): Dictionary of greetings in multiple languages.
    """
    event = {
        "name": name,
        "date": date,
        "type": event_type,
        "greetings": greetings
    }
    result = events_collection.insert_one(event)
    print(f"Event added with ID: {result.inserted_id}")


def get_events_for_day(day):
    """
    Get all events for a specific day.
    """
    start_of_day = datetime.strptime(day, '%Y-%m-%d')
    end_of_day = start_of_day + timedelta(days=1) - timedelta(milliseconds=1)

    query = {
        "date": {
            "$gte": start_of_day,
            "$lte": end_of_day
        }
    }

    results = events_collection.find(query)
    print(f"Events on {day}:")
    for event in results:
        print(event)


def get_events_for_month(year, month):
    """
    Get all events for a specific month.
    """
    start_of_month = datetime(year, month, 1)
    end_of_month = datetime(year, month + 1, 1) - timedelta(milliseconds=1) if month < 12 else datetime(year + 1, 1, 1) - timedelta(milliseconds=1)

    query = {
        "date": {
            "$gte": start_of_month,
            "$lte": end_of_month
        }
    }

    results = events_collection.find(query)
    print(f"Events for {year}-{month:02d}:")
    for event in results:
        print(event)


if __name__ == "__main__":
    # Add events with the new structure
    add_event(
        "Christmas",
        datetime(2024, 12, 25),
        "Religious",
        {"English": "Merry Christmas!", "Arabic": "عيد ميلاد مجيد"}
    )
    add_event(
        "Eid al-Fitr",
        datetime(2024, 4, 10),
        "Religious",
        {"English": "Happy Eid!", "Arabic": "عيد مبارك"}
    )
    add_event(
        "Mira's Birthday",
        datetime(2024, 2, 15),
        "Personal",
        {"English": "Happy Birthday, Mira!", "Arabic": "عيد ميلاد سعيد يا ميرا!"}
    )

    # Get events for a specific day
    get_events_for_day("2024-12-25")

    # Get events for a specific month
    get_events_for_month(2024, 12)
