from flask import request, abort
import re

def check_postcode_pattern(string):
    pattern = r'\d{4}[a-zA-Z]{2}$'
    if re.match(pattern, string):
        return True
    else: 
        return False

def get_postcode():
    postcode = request.args.get('postalcode')
    if postcode:
        if check_postcode_pattern(postcode) == False:
            abort (400, description="Invalid postal code provided")
            return None
        else:
            postcode = ''.join(re.findall(r'\d+', postcode))
            return postcode
    else:
        abort(400, description="No postal code provided")
        return None

def match_postcode(postcode, postal_range):
    if len(postcode) != len(postal_range):
        return False
    for char1, char2 in zip(postcode, postal_range):
        if char1 != char2 and char2 != 'X':
            return False
    return True

def is_within_postalrange(postcode, postal_range):
    start, end = postal_range.split('-')
    if not start.isdigit() or not end.isdigit():
        return False
    if (int(start) <= int(postcode) <= int(end)):
        return True
    return False