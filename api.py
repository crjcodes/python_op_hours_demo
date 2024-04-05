import os, sys, logging
from flask import Flask
import api_startup
import manager_operating_hours

print("------------------------------\n")
print(os.getcwd())
print("------------------------------\n")

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

try:
    manager = manager_operating_hours.Manager()
    api_startup.perform_startup_steps(manager, "data_restaurants.csv")

    app = Flask(__name__)


    @app.route("/")
    @app.route('/restaurants/open/<datetime>')
    def handle_restaurants_open(datetime):
        return manager.list_operating_restaurants(datetime)

except Exception as err:
    logging.error(f"Unexpected api failure {err=}, {type(err)=}")
    raise
