from pymongo import MongoClient
from datetime import datetime, timedelta

# Connect to MongoDB
client = MongoClient('mongodb://127.0.0.1:27017')  # Local MongoDB
db = client['aws']  # Database name
events_collection = db['events']  # Collection name


def add_event(name, date, description):
    event = {
        "name": name,
        "date": date,
        "description": description
    }
    result = events_collection.insert_one(event)
    print(f"Event added with ID: {result.inserted_id}")


def get_events_for_day(day):
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
    # Add events
    add_event("AWS Workshop", datetime(2024, 12, 15), "Introduction to AWS services")
    add_event("Year-End Party", datetime(2024, 12, 31), "Celebrate the end of the year")

    # Get events for a specific day
    get_events_for_day("2024-12-15")

    # Get events for a specific month
    get_events_for_month(2024, 12)
