from flask import request
from seenons_api.utils.postalcode_checks import is_within_postalrange, match_postcode

def company_days_available(days_available, weekday_query):
    valid_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    days_available = [day.strip() for day in days_available.split(',')] #Split available days of provider and create a list
    weekday_query = [word.lower() for word in weekday_query] #Turn all letters of the weekdays query to lowercase

    for day in days_available:
            for valid_day in valid_days:
                if valid_day in day.lower() and valid_day in weekday_query:
                        return True
    return False

def search_database(postcode, db):
    column_names = ["Id", "Name", "Stream id", "Asset id", "Postal range", "Available days", "Time slots"]
    results = []
    weekday_query = request.args.getlist('weekdays[]')
    cursor = db.cursor()
    #try catch??
    cursor.execute("SELECT * FROM availability")  # Adjust the table name as necessary
    rows = cursor.fetchall()

    for row in rows:
        print(f"Availability ID: {row['id']}")
        print(f"Provider ID: {row['provider_id']}")
        print(f"Waste Stream ID: {row['waste_stream_id']}")
        print(f"Asset Type ID: {row['asset_type_id']}")
        print(f"Postal Code Range: {row['postal_range']}")
        print(f"Available Days: {row['available_days']}")
        print(f"Time Slot Start: {row['time_slots']}")
        print("-" * 20)  # Just a separator for readability
    # for row in rows:
    #     postal_range = row[4]
    #     # Check if there is a '-' in the providers range and is within it's range (eg. 1500-2000)
    #     # Or check if the postcode matches with the providers postcode (eg. 10XX or 1013)
    #     if '-' in postal_range and is_within_postalrange(postcode, postal_range) or \
    #     match_postcode(postcode, postal_range) is True:
    #         #Check if a weekdays query is sent and whether the provider is available those days
    #         if not weekday_query or weekday_query and company_days_available(row[5], weekday_query):
    #             results.append(dict(zip(column_names, row))) 

    # return results