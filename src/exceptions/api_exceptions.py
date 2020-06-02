"""api error module that contains various error classes
All of the error classes defined here represents the various
api errors that can occur.
"""

# from sentry_sdk import capture_exception
# from sentry_sdk import capture_message

# Configure Login of GCP

# Create two different funnels
#  - Log the error to Sentry
#  - Log the error to GCP Console

class ApiError(Exception):
    """The generic api error class"""
    def to_dict(self):
        """sets the message value"""
        # capture_message(self.message)
        return dict(message=self.message)


class ItemNotFoundError(ApiError):
    """Error class for when item not found"""
    status_code = 404
    message = "The requested resource was not found."
    # capture_message(message)


class BadRequestError(ApiError):
    """Error class for when bad request is made.
     This error can be raised when our clients make
      invalid calls to our api or when our code makes
       invalid calls against clients our api is dependant on"""
    status_code = 400

    def __init__(self, message):
        super(BadRequestError, self).__init__()
        # capture_message(message)
        self.message = message
        


class ServiceNotAvailableError(ApiError):
    """Error class for when service is not available. This error is raised
    when the api clients we depend on are temporarily unavailable"""
    status_code = 503

    def __init__(self, message):
        super(ServiceNotAvailableError, self).__init__()
        # capture_message(message)
        self.message = message
