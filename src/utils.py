from flask import jsonify
import logging


def create_object(mapping, data):
    try:
        tuple_list = [None] * len(mapping)
        for k, v in mapping.items():
            tuple_list[v] = data[k] if k in data else None
        return tuple(tuple_list)
    except Exception:
        logging.error("Error in 'create_object' ")


def make_resp(msg, status_code):
    """builds the return response in json format"""
    response = jsonify(message=msg)
    response.status_code = status_code
    return response
