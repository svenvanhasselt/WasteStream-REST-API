from flask import request
from seenons_api.utils.postalcode_checks import is_within_postalrange, match_postcode

# Check if the available days of the provider match the query
def company_days_available(days_available, weekday_query):
    valid_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    days_available = [day.strip() for day in days_available.split(',')] #Split available days of provider and create a list
    weekday_query = [word.lower() for word in weekday_query] #Turn all letters of the weekdays query to lowercase

    for day in days_available:
            for valid_day in valid_days:
                if valid_day in day.lower() and valid_day in weekday_query:
                        return True
    return False

# Search the database for available streams against the given postcode and optional weekdays
def search_database(postcode, db):
    column_names = ["Id", "Name", "Provider", "Asset", "Postal range", "Available days", "Time slots"]
    results = []
    weekday_query = request.args.getlist('weekdays[]')
    cursor = db.cursor()

    cursor.execute("""
            SELECT 
                a.id AS availability_id,
                lp.name AS provider_name,
                wt.name AS waste_stream_name,
                at.name AS asset_name,
                a.postal_range,
                a.available_days,
                a.time_slots
            FROM 
                availability a
            JOIN 
                logistics_provider lp ON a.provider_id = lp.id
            JOIN 
                asset_types at ON a.asset_type_id = at.id
            JOIN
                waste_streams wt ON a.waste_stream_id = wt.id
        """)
    rows = cursor.fetchall()

    # Loop through the available streams and check against the given postcode and optional weekday query
    for row in rows:
        postal_range = row['postal_range']

        if '-' in postal_range and is_within_postalrange(postcode, postal_range) or \
        match_postcode(postcode, postal_range) is True:
            if not weekday_query or weekday_query and company_days_available(row['available_days'], weekday_query):
                results.append(dict(zip(column_names, row)))
    cursor.close()
    return results