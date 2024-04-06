import os, sys, logging, json

from flask import Flask
from flask import Response

import api_startup
import manager_operating_hours

app = Flask(__name__)
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

try:
    manager = manager_operating_hours.Manager()
    api_startup.perform_startup_steps(manager, "data_restaurants.csv")

    @app.route('/restaurants/open/<datetime>')
    def handle_restaurants_open(datetime):
        logging.debug(f"given date time is [{datetime}")

        try:
            response_data = manager.list_operating_restaurants(datetime)
            response = json.dumps(response_data)
            return Response(
                response,
                200, mimetype='application/json')

        except Exception as err:
            return Response(
                json.dumps({'Error': f'Unable to retrieve restaurants - {err}'}),
                400, mimetype='application/json')


    @app.errorhandler(404)
    def handle_invalid(e):
        return ("Please use the endpoint, /restaurants/open/{datetime}, where datetime is provided in the format. "
                "'YYYY-MM-DD%20HH:MM'"), 404

except Exception as err:
    logging.error(f"Unexpected api failure {err=}, {type(err)=}")
    raise

if __name__ == "__main__":
    app.run()