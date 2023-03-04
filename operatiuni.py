from data_validators import *
from exceptions import *


class Client:

    def __init__(self, name, cnp=None, phone=None, address=None, balance=0, deleted=False):
        self.name = name
        self.cnp = cnp
        self.phone = phone
        self.address = address
        self.balance = balance
        self.transactions = []
        self.deleted = deleted

    def withdrawal(self, amount):  # TODO raise exception if not enough funds

        if self.balance < amount:
            print("not enough funds")
            return

        self.balance = self.balance - amount
        self.transactions.append(Transaction("withdrawal", self.name, amount))

    def deposit(self, amount):

        self.balance = self.balance + amount
        self.transactions.append(Transaction("deposit", self.name, amount))

    def transfer(self, receiver, amount):  # TODO raise exception if not enough funds
        if self.balance < amount:
            print("not enough funds")
            return
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


def create_client(clients_collection):  # TODO modify the function so clients can be created from the api too
    """
    Creating a client object in memory and putting it in the database too.
    :param clients_collection: mongoDB_object Connection object to a specific collection on a mongoDB database.
    """
    # clients_collection = db["clients"]
    cnp = input('Intordu CNP: ')
    name = name_validator('Numele noului client: ')
    phone = input('Numar de telefon: ')
    address = input('Adresa: ')

    new_client = Client(name, cnp, phone, address)
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


def client_obj_constructor(client_name, clients_collection):  # TODO take the client_id parameter instead of client_name
    client_data = clients_collection.find_one({"name": client_name},
                                              {"_id": 0, "name": 1, "balance": 1, "transactions": 1})
    client = Client(client_data["name"], balance=client_data["balance"])
    if len(client_data["transactions"]) > 0:
        for transaction in client_data["transactions"]:
            client.transactions.append(
                Transaction(transaction["transaction_type"],
                            transaction["expeditor"],
                            transaction["suma"],
                            transaction["destinatar"],
                            transaction["timestamp"]))
    return client


def balance_change(client, amount, clients_collection):  # TODO
    # TODO take client_id as parameter instead of client_name
    #   refactor the exception for invalid amount
    """
    This function modifies the balance of a client.
    :param clients_collection: mongoDB_object Connection object to a specific collection on a mongoDB database.
    :param client: Client Object of the client.
    :param amount: float The amount for the modification.
    """

    if amount < 0:
        client.withdrawal(amount)
    elif amount > 0:
        client.deposit(amount)
    else:
        raise Exception("invalid amount")

    transactions_list = []  # TODO make a separate function for this and use it in transfer function too
    for item in client.transactions:
        transactions_list.append(item.__dict__)
    clients_collection.update_one({"name": client.name},
                                  {"$set": {"balance": client.balance, "transactions": transactions_list}})


def transfer(amount, sender_name, receiver_name, clients_collection):  # TODO
    # TODO use parameter sender_id instead of sender_name
    #   create and raise exception for not enough funds
    #   create and raise exception for amount < 0
    """
    Make a transaction between two clients as long as the sender has enough funds.
    :param amount: float Amount to be transferred.
    :param sender_name: str Unique identifier for the sender.
    :param receiver_name: str Unique identifier for the receiver.
    :param clients_collection: mongoDB_object Connection object to a specific collection on a mongoDB database.
    """
    if amount <= 0:
        print('The amount to be transferred must be positive.')
    else:
        sender = client_obj_constructor(sender_name, clients_collection)
        receiver = client_obj_constructor(receiver_name, clients_collection)
        if sender.balance >= amount:  # TODO raise exception and ditch the if-else
            print(f"{sender.name}'s initial balance: {sender.balance}")
            print(f"{receiver.name}'s initial balance: {receiver.balance}")
            sender.transfer(receiver, amount)
            print(f"{sender.name}'s final balance: {sender.balance}")
            print(f"{receiver.name}'s final balance: {receiver.balance}")

            sender_transactions = []
            for item in sender.transactions:
                sender_transactions.append(item.__dict__)
            clients_collection.update_one({"name": sender.name},
                                          {"$set": {"balance": sender.balance, "transactions": sender_transactions}})

            print(receiver.transactions)

            receiver_transactions = []
            for item in receiver.transactions:
                receiver_transactions.append(item.__dict__)
            clients_collection.update_one({"name": receiver.name}, {
                "$set": {"balance": receiver.balance, "transactions": receiver_transactions}})
        else:
            print('Expeditorul nu are fonduri suficiente. Transferul nu a fost efectuat.')


def retrieve_clients(name_filter, clients_collection):
    clients_names = clients_collection.find({'name': {'$regex': name_filter, '$options': 'i'}},
                                            {"_id": 0, "name": 1, "cnp": 1})
    clients_list = []
    for name in clients_names:
        clients_list.append({name["name"]: name["cnp"]})

    if len(clients_list) == 0:
        raise NoClientsForFilter(f'No clients for <{name_filter}> filter.')
    return clients_list
