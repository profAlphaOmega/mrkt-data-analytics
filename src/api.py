"""This module contains the flask api routing"""
from flask import Blueprint
from flask_cors import CORS
from src.Analytics import Analytics
from src.Optimizely import Optimizely

api = Blueprint('api', __name__, url_prefix='/')
CORS(api)

analytics = Analytics()
optimizely = Optimizely()


# ANALYTICS ROUTES
@api.route('/redacted/path', methods=['OPTIONS', 'POST'])
def site_pageviews():
    return analytics.data_insert("redacted-table")


# OPTIMIZELY ROUTES
@api.route('/opt/redacted/path', methods=['OPTIONS', 'GET'])
def get_optimizely_state():
    return optimizely.get_state("redacted-table")
