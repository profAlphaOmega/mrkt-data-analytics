"""This module holds the big query client object."""
import logging as log

from google.cloud import bigquery
from google.cloud.exceptions import exceptions

from src.exceptions.api_exceptions import BadRequestError
from src.exceptions.api_exceptions import ItemNotFoundError


class BigQueryClient(object):
    """ BigQuery client

        Connects to Google's BigQuery product. You must specify the
            * project_id
            * dataset_name
            * table_name
        and optionally the
            * service_acct_json key.
     """
    _client = None
    project_name = None
    dataset = None

    def __init__(self, project_id, dataset_name, table_name, service_acct_json=None):
        if service_acct_json:
            self._client = bigquery.Client.from_service_account_json(
                service_acct_json)
        else:
            self._client = bigquery.Client(project=project_id)
        self.dataset = self._client.dataset(dataset_name)
        self._table = self._client.get_table(self.dataset.table(table_name))
        # self.project_name = self._client.project

    @property
    def table(self):
        """BigQueryClient's table object"""
        return self._table

    @table.setter
    def table(self, value):
        """BigQueryClient's table object"""
        self._table = self._client.get_table(self.dataset.table(value))

    @property
    def fully_qualified_table(self):
        return ".".join(
            [self.project_name, self.dataset.dataset_id, self.table.table_id]
        )

    def query(self, sql_statement, job_config=None):
        """Runs SQL statement in the Client.

        ARGS:
            sql_statement: raw, non-legacy, sql statement. The table name must
            be bound by ` (backtick) character, the table name qualified as
            project_name.dataset_name.table_name
            job_config: None by default, used to pass configuration for a query. SQL Injection
            parameters are mainly used with the job_config

        RETURNS:
            A iterator object. Iterator returns bq row dictionary.

        Raises:
            ItemNotFoundError: this error is thrown by the big query client
            when api call against a non-existant project, dataset, table has
            been made
        """
        try:
            query_job = self._client.query(sql_statement, job_config=job_config)
            return query_job.result()
        except exceptions.NotFound as query_error:
            error_msg = (f'Reference not found for query:'
                         f'{sql_statement}. Error: {query_error}')
            self._log_raise_exception(error_msg, ItemNotFoundError)

    def insert_records(self, records):
        """Inserts records passed in against set big query table

        Takes the records data and inserts it into its preconfigured
        big query project/dataset/table. If too many requests for insertions
        are made in succession gcp may return a 503 service not available.
        When this happens exponential backoff will happen where sleep time is
        given and retried. The sleep time will continue to increase until it
        reaches 32 seconds then will continue on to the next record. All
        events related to this exponential backoff will be logged.

        ARGS:
            records
                a list of tuples object where each element in the list
                represents a row to be inserted. Each tuple represents the columns
                of a row. The tuples must be in the exact same order as the schema
                in big query table.

        RAISES:
            BadRequestError
                when the inputted schema of the records do not
                match, or when the inputted record is not a list of
                ServiceNotAvailableError: when exponential backoff has reached 32
                seconds but service is still unavailable.

        """
        log.info(f'calling insert. Data: {records}')
        # self._validate_data(records)
        resp = self._client.insert_rows(self.table, {records})
        return resp

    def _validate_data(self, records):
        """ensure records used for insertion is list of tuples"""
        if not all(isinstance(item, tuple) for item in records):
            error_msg = f'Invalid data for insertion: {records}'
            self._log_raise_exception(error_msg, BadRequestError)

    @staticmethod
    def _log_raise_exception(log_msg, exception):
        """log the error message then raise the exception"""
        log.error(log_msg)
        raise exception(log_msg)
