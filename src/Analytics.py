#!/usr/bin/env python
#
from datetime import datetime
from flask import request
from src.utils import *
from src.exceptions.api_exceptions import *

from src.clients.bq import BigQueryClient
from src.table_managers import TableManager


class Analytics:
    """
    Analytics Data Insertion Class

        Connects to Google's BigQuery Tables. You must specify the table_name to be looked up in a TableManager file.
        Payload is collected from the POST request and inserted as a row into the respective table

     """
    def __init__(self):
        return

    @staticmethod
    def data_insert(table_name):
        """
        Inserts Payload row into the specified BQ Table

        :param table_name:
        :return: 200 if all is well, 500 if something goes wrong with query
        """
        try:
            if request.method == 'OPTIONS':
                response = make_resp(msg="OK", status_code=200)
                response.headers['Access-Control-Allow-Origin'] = '*'
                response.headers['Access-Control-Allow-Headers'] = 'Cache-Control, Content-Type'
                response.headers['Access-Control-Allow-Methods'] = 'OPTIONS, POST'
                return response

            logging.info(f"Table: {table_name}")

            # Create Insert Timestamp
            t = datetime.utcnow().isoformat()
            logging.info(f"Request time: {t}")

            d = request.get_json()
            logging.info(f"Payload {d}")
            if not d:
                logging.error("No Payload detected")
                raise ItemNotFoundError

            # Find proper table config and Create a BQ Client
            table = TableManager.get_table(table_name=table_name)
            bq_client = BigQueryClient(
                project_id=table["project_id"],
                dataset_name=table["dataset"],
                table_name=table["table_name"]
            )
            logging.info(f"Client Created")

            # insert run time
            d.update({"inserted_at": t})

            # Payload data is mapped to columns and mutated to a tuple from json
            logging.info(f"Mapping data to columns")
            data = create_object(table["columns"], d)

            # Insert Row
            logging.info(f"Inserting data: {data}")
            resp = bq_client.insert_records(data)

            # Handle Response, if False that means all went well
            if resp:
                logging.error(f"RESP: {resp}")
                return make_resp(msg=f"There was an Internal Error", status_code=500)

            logging.info(f"RESP: {resp}")
            return make_resp(msg="OK", status_code=200)

        except Exception as ex:
            logging.error(ex)
