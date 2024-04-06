import sys, logging

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def perform_startup_steps(manager, filename="data_restaurants.csv"):
    try:
        if manager is None:
            raise ValueError("No manager")

        # TODO: FUTURE: name of file input through command-line and configuration
        # TODO: figure out how to reference the file in a data directory, not just source
        manager.ingest_new_data_source(filename)
        logging.debug("manager ingestion happened")

    except Exception as err:
        logging.error(f"Startup failure due to unexpected {err=}, {type(err)=}")
        raise ValueError("Application erred; exiting")