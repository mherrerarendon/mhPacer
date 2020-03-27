from enum import Enum, unique, auto
import sys


class RPCException(Exception):
    def __init__(self, error_code, message=''):
        if not isinstance(error_code, ErrorCodes):
            msg = 'Error code passed in the error_code param must be of type {0}'
            raise RPCException(ErrorCodes.RPCE_INCORRECT_ERRCODE, msg, ErrorCodes.__class__.__name__)

        self.error_code = error_code
        self.traceback = sys.exc_info()
        msg = '[{0}] {1}'.format(error_code.name, message)
        super().__init__(msg)


@unique
class ErrorCodes(Enum):
    INCORRECT_ERRCODE = auto()
    PARSE_ERR = auto()
    VALUE_PARSE_ERR = auto()
    DISTANCE_UNIT_PARSE_ERR = auto()
    TIME_UNIT_PARSE_ERR = auto()
