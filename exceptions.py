class BankException(Exception):
    message = 'blank'
    error_code = 0


class NoClientsForFilter(BankException):
    message = {"error_message": "no clients for filter"}
    error_code = 404


class UserDataMissingArgument(BankException):
    message = {'error message': 'user data missing argument'}
    error_code = 400


class UserDataWrongType(BankException):
    message = {'error message': 'user data passed as wrong type'}
    error_code = 400


class NotEnoughFunds(BankException):
    message = {"error_message": "Not enough funds."}
    error_code = 400


class ClientAlreadyExists(BankException):
    message = {'error message': 'client already has an account'}
    error_code = 400


class PhoneAlreadyInUse(BankException):
    message = {'error message': 'phone number already in use'}
    error_code = 400


class AmountZero(BankException):
    message = {"error_message": "the amount cannot be 0"}
    error_code = 400


class AmountNotNumber(BankException):
    message = {"error_message": "the amount passed must be a number"}
    error_code = 400


class ClientNotFound(BankException):
    message = {"error_message": "client not found in the database"}
    error_code = 404


class AmountNotPositive(BankException):
    message = {"error_message": "the amount for transfer must be positive"}
    error_code = 400