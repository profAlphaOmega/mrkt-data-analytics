#!/usr/bin/env python
#
from datetime import datetime
from flask import request

from src.utils import *
from src.exceptions.api_exceptions import *
from src.clients.bq import BigQueryClient
from src.table_managers import TableManager

from google.cloud import bigquery


class Optimizely:
    """
    Optimizely State Class

        Has two methods and GET and a POST. User sends the required x-mat-tenant header in either route.
        This class is used to grab and set the users latest Optimizely test variation object

     """
    def __init__(self):
        return

    @staticmethod
    def get_state(table_name):
        """

                :param table_name:
                :return: 200 if all is well,
        """
        try:
            if request.method == 'OPTIONS':
                response = make_resp(msg="OK", status_code=200)
                response.headers['Access-Control-Allow-Origin'] = '*'
                response.headers['Access-Control-Allow-Headers'] = 'Cache-Control, Content-Type, x-mat-tenant'
                response.headers['Access-Control-Allow-Methods'] = 'OPTIONS, GET'
                return response

            logging.info(f"ENTER: {table_name}")

            # Create Insert Timestamp
            t = datetime.utcnow().isoformat()
            logging.info(f"Request time: {t}")

            # Get tenantid from headers, it is required
            try:
                tenantid = request.headers['x-mat-tenant']
            except Exception:
                logging.error(f"Tenant {tenantid} not found")
                raise ItemNotFoundError("Tenant not found")
            logging.info(f"tenantid: {tenantid}")

            # Find table and create client
            table = TableManager.get_table(table_name=table_name)
            bq_client = BigQueryClient(
                project_id=table["project_id"],
                dataset_name=table["dataset"],
                table_name=table["table_name"]
            )
            logging.info(f"Client Created")

            # Query that finds the 'state' value for a given tenant, get the latest record
            logging.info(f"Fetching State for {tenantid}...")
            query = """
                SELECT state FROM `redacted`
                WHERE uid = @redacted
                ORDER BY inserted_at DESC
                LIMIT 1
                """

            # SQL Injection Protection
            query_params = [
                bigquery.ScalarQueryParameter('tenantid', 'STRING', tenantid)
            ]
            job_config = bigquery.QueryJobConfig()
            job_config.query_parameters = query_params

            # Query
            logging.info(f"Querying...")
            result = bq_client.query(query, job_config=job_config)

            # Return Result (Iterator) or '{}' if nothing found
            state = '{}'
            for row in result:
                if row is not None:
                    state = row[0]
            logging.info(f"Result: {state}")

            return make_resp(msg=f"{state}", status_code=200)

        except Exception as ex:
            logging.error(ex)

    @staticmethod
    def set_state(table_name):
        try:
            if request.method == 'OPTIONS':
                response = make_resp(msg="OK", status_code=200)
                response.headers['Access-Control-Allow-Origin'] = '*'
                response.headers['Access-Control-Allow-Headers'] = 'Cache-Control, Content-Type, x-mat-tenant'
                response.headers['Access-Control-Allow-Methods'] = 'OPTIONS, POST'
                return response

            logging.info(f"ENTER: {table_name}")

            # Create Insert Timestamp
            t = datetime.utcnow().isoformat()
            logging.info(f"Request time: {t}")

            # Get tenatid via headers, it is required
            try:
                tenantid = request.headers['x-mat-tenant']
            except Exception:
                logging.error(f"Tenant {tenantid} not found")
                raise ItemNotFoundError
            logging.info(f"tenantid: {tenantid}")

            # Get Payload
            d = request.get_json()
            logging.info(f"Payload {d}")
            if not d:
                logging.error("No Payload detected")
                raise ItemNotFoundError

            # Find proper table data and Create a BQ Client
            table = TableManager.get_table(table_name=table_name)
            bq_client = BigQueryClient(
                project_id=table["project_id"],
                dataset_name=table["dataset"],
                table_name=table["table_name"]
            )
            logging.info(f"Client Created")

            # Insert run time and tenantid to payload
            d.update({"inserted_at": t})
            d.update({"uid": tenantid})

            # Payload data is mapped to columns and mutated to a tuple from json
            logging.info(f"Mapping data to columns")
            data = create_object(table["columns"], d)

            # Insert Row
            logging.info(f"Inserting data: {data}")
            resp = bq_client.insert_records(data)

            # Response from insert, False means it worked
            if resp:
                logging.error(f"RESP: {resp}")
                return make_resp(msg="There was an Internal Error", status_code=500)
            logging.info(f"RESP: {resp}")

            return make_resp(msg="OK", status_code=200)

        except Exception as ex:
            logging.error(ex)

