from flask import Flask, jsonify, abort, g
from seenons_api.utils.postalcode_checks import get_postcode
from seenons_api.utils.open_db import open_db
from seenons_api.utils.search_database import search_database
from flask_restx import Api, Resource, fields

api = Flask(__name__)
swagger = Api(api, version='1.0', title='Waste Streams API',
              description='API to get waste stream data based on postal codes',
              doc='/docs')  # Swagger UI documentation endpoint



# Define the response model for Swagger documentation
stream_model = swagger.model('WasteStream', {
    'Id': fields.Integer(required=True, description='The waste stream ID'),
    'Name': fields.String(required=True, description='Name of the service provider'),
    'Provider': fields.String(required=True, description='Available waste stream ids'),
    'Asset': fields.String(required=True, description='Available waste asset ids'),
    'Postal range': fields.String(required=True, description='Postal range of provider'),
    'Available days': fields.String(required=True, description='Available days of provider'),
    'Time slots': fields.String(required=True, description='Available time slots of provider'),
})

# Create a parser for query parameters
parser = swagger.parser()
parser.add_argument('postalcode', type=str, required=True, help='Postal code to filter streams')
parser.add_argument('weekdays[]', type=str, action='append', help='Array of weekdays')




@swagger.route('/streams/')
class WasteStreams(Resource):
    @swagger.doc('get_waste_streams')
    @swagger.expect(parser)  # Use the defined parser
    @swagger.marshal_list_with(stream_model)
    def get(self):
        try:
            waste_db = open_db() # Open the database connection
            postcode = get_postcode() # Get the postal code from the query parameters
        except ValueError as e:
            abort(400, description=str(e))
        except Exception as e:
            abort(500, description=str(e))
        try:
            results = search_database(postcode, waste_db) # Search the database for the given postcode and optional weekdays
            if not results:
                raise ValueError("No data found for the given postal code")
            return results
        except ValueError as e:
            abort(404, description=str(e))
        except Exception as e:
            abort(500, description="Internal server error")

@api.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def main():
    api.run(debug=True)

if __name__ == '__main__':
    main()
