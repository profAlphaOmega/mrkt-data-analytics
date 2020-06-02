#!/usr/bin/env python
#
# Copyright 2019 Volusion, LLC (http://www.volusion.com)
#
from .tables import tables as tbl
from src.exceptions.api_exceptions import *
import logging


class TableManager:
	tables = {
		"REDACTED": tbl["REDACTED"],
		"REDACTED": tbl["REDACTED"],
		"REDACTED": tbl["REDACTED"],
		"REDACTED": tbl["REDACTED"],
		"REDACTED": tbl["REDACTED"],
		"REDACTED": tbl["REDACTED"],
	}

	@staticmethod
	def get_table(table_name):
		try:
			table = TableManager.tables[table_name]
			return table
		except Exception:
			logging.error(f"Table {table_name} not found in TableManager")
			raise ItemNotFoundError
