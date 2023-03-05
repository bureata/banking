class NoClientsForFilter(ValueError):
    pass


class UserDataMissingArgument(KeyError):
    pass


class UserDataWrongType(ValueError):
    pass


class NotEnoughFunds(ValueError):
    pass


class ClientAlreadyExists(ValueError):
    pass


class PhoneAlreadyInUse(ValueError):
    pass


class AmountZero(ValueError):
    pass