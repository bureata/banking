from data_validators import *
from exceptions import *


class Client:

    def __init__(self, name, cnp, phone, address, balance=0.0, deleted=None):
        self.name = name
        self.cnp = cnp
        self.phone = phone
        self.address = address
        self.balance = balance
        self.transactions = []
        self.deleted = deleted

    def withdrawal(self, amount):

        if self.balance < amount:
            raise NotEnoughFunds

        self.balance -= amount
        self.transactions.append(Transaction("withdrawal", self.name, amount))

    def deposit(self, amount):

        self.balance = self.balance + amount
        self.transactions.append(Transaction("deposit", self.name, amount))

    def transfer(self, receiver, amount):
        if self.balance < amount:
            raise NotEnoughFunds
        self.balance = self.balance - amount
        receiver.balance = receiver.balance + amount
        self.transactions.append(Transaction("transfer", self.name, amount, receiver.name))
        receiver.transactions.append(Transaction("transfer", self.name, amount, receiver.name))


class Transaction:

    def __init__(self, transaction_type, sender, amount, receiver=None, timestamp=None):
        if timestamp is None:
            self.timestamp = transaction_timestamp()
        else:
            self.timestamp = timestamp
        self.transaction_type = transaction_type
        self.sender = sender
        self.amount = amount
        self.receiver = receiver

    def __str__(self):
        if self.receiver is None:
            return self.sender + "|" + str(self.amount) + "|" + self.transaction_type

        return self.sender + "|" + str(self.amount) + "|" + self.receiver + "|" + self.transaction_type


def transaction_timestamp():
    dt = datetime.datetime.now()
    dt_format = "%Y%m%d%H%M%S"
    str_dt = dt.strftime(dt_format)
    return int(str_dt)


def create_client(client_data: dict, clients_collection):
    """
    Instantiates a client object and register client data into the database.
    :param client_data: dict A dictionary with all data necessary to instantiate a Client object.
    :param clients_collection: mongoDB_object Connection object to a specific collection on a mongoDB database.
    """

    for value in client_data.values():
        if type(value) != str:
            raise UserDataWrongType('Data supplied as client data is of wrong type.')
    client_check = clients_collection.find_one({"cnp": client_data["cnp"]},
                                               {"_id": 0,
                                                "name": 1,
                                                "cnp": 1})
    if client_check is not None:
        raise ClientAlreadyExists
    phone_check = clients_collection.find_one({"phone": client_data["phone"]},
                                              {"_id": 0,
                                               "name": 1,
                                               "cnp": 1})
    if phone_check is not None:
        raise PhoneAlreadyInUse
    new_client = Client(client_data["name"], client_data["cnp"], client_data["phone"], client_data["address"])
    clients_collection.insert_one(new_client.__dict__)
    return new_client


def delete_client(nume_client, clients_collection):  # TODO
    # TODO implement logic to prevent closing an account that has money left or debt
    print(nume_client)
    clients_collection.update_one({"name": nume_client}, {"deleted": True})
    # sold = verifica_sold(nume_client, dict_clients)
    # if sold < 0:
    #     print(f'Pentru inchiderea contului este necesara achitarea sumei restante de: {sold}.')
    # elif sold > 0:
    #     print(f'Contul figureaza cu o sold de {sold}, care va fi restituita clientului.')
    # else:
    #     print(f'Soldul este 0. Contul va fi sters, impreuna cu informatiile despre client.')


def delete_client_data():
    # TODO implement a function that will be automatically triggered
    #   and will delete data for an account that was deleted x days ago
    pass


def client_obj_constructor(cnp, clients_collection):
    client_data = clients_collection.find_one({"cnp": cnp,
                                               "deleted": {"$eq": None}
                                               },
                                              {"_id": 0,
                                               "name": 1,
                                               "cnp": 1,
                                               "phone": 1,
                                               "address": 1,
                                               "balance": 1,
                                               "transactions": 1})
    if client_data is None:
        raise ClientNotFound
    client = Client(client_data["name"],
                    client_data["cnp"],
                    client_data["phone"],
                    client_data["address"],
                    client_data["balance"])
    if len(client_data["transactions"]) > 0:
        for transaction in client_data["transactions"]:
            client.transactions.append(
                Transaction(transaction["transaction_type"],
                            transaction["sender"],
                            transaction["amount"],
                            transaction["receiver"],
                            transaction["timestamp"]))
    return client


def money_transfer(sender, receiver, amount, clients_collection):  # TODO
    # TODO use parameter sender_id instead of sender_name
    #   create and raise exception for not enough funds
    #   create and raise exception for amount < 0
    """
    Make a transaction between two clients as long as the sender has enough funds.
    :param amount: float Amount to be transferred.
    :param sender: str Sender object.
    :param receiver: str Receiver object.
    :param clients_collection: mongoDB_object Connection object to a specific collection on a mongoDB database.
    """
    if amount <= 0:
        raise AmountNotPositive
    print(f"{sender.name}'s initial balance: {sender.balance}")
    print(f"{receiver.name}'s initial balance: {receiver.balance}")
    sender.transfer(receiver, amount)
    print(f"{sender.name}'s final balance: {sender.balance}")
    print(f"{receiver.name}'s final balance: {receiver.balance}")
    db_register_balance_transactions(sender, clients_collection)
    db_register_balance_transactions(receiver, clients_collection)


def db_register_balance_transactions(client, clients_collection):
    client_transactions = []
    for item in client.transactions:
        client_transactions.append(item.__dict__)
    clients_collection.update_one({"name": client.name},
                                  {"$set": {"balance": client.balance, "transactions": client_transactions}})


def retrieve_clients(name_filter, clients_collection):

    clients_names = clients_collection.find({'name': {'$regex': name_filter, '$options': 'i'},
                                             "deleted": {"$eq": None}
                                             },
                                            {"_id": 0, "name": 1, "cnp": 1})
    clients_list = []
    for name in clients_names:
        clients_list.append({name["name"]: name["cnp"]})

    if len(clients_list) == 0:
        raise NoClientsForFilter(f'No clients for <{name_filter}> filter.')
    return clients_list
