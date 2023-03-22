# TODO implement two languages for the front end part

from flask import Flask, jsonify, request
from flasgger import Swagger
import pymongo
from operations import *
from mongo_credentials import *

app = Flask(__name__)
swagger = Swagger(app)

db_client = pymongo.MongoClient(pass_text)

db = db_client["bankingDB"]
clients_collection = db["clients"]


@app.route("/api/client/<client_cnp>", methods=["GET"])
def check_balance(client_cnp):
    """
    Returns the balance of a client
    ---
    parameters:
        - name: client_cnp
          in: path
          description: "cnp of the client"
          type: string
          required: true
    responses:
        200:
            description: "58"
        404:
            description: User not found.
    """
    try:
        client_data = clients_collection.find_one({"cnp": client_cnp, "deleted": {"$eq": None}},
                                                  {"_id": 0, "balance": 1})
        try:
            balance = client_data["balance"]
        except Exception:
            raise ClientNotFound
        print(balance)
        return jsonify(balance)
    except BankException as excep:
        print(f'error {type(excep).__name__}: {excep.message["error_message"]}')
        return excep.message, excep.error_code


@app.route("/api/client/filtru/<name_filter>", methods=["GET"])
def search_clients(name_filter):
    """
    Show the clients based on name filter (show all for no filter).
    ---
    parameters:
        - name: name_filter
          in: path
          description: "filter for narrowing the search by name"
          type: string
          required: true
    responses:
        200:
            description: Will list a table with names and unique ID-s matching the provided filter.
        404:
            description: User not found.
    """

    try:
        clients_data = retrieve_clients(name_filter, clients_collection)
    except BankException as excep:
        print(f'error {type(excep).__name__}: {excep.message["error_message"]}')
        return excep.message, excep.error_code
    else:
        return jsonify(clients_data)


@app.route("/api/client/deposit", methods=["POST"])
def deposit():
    """
    Register a deposit for a client.
    ---
    parameters:
        - name: transaction_data
          in: body

    responses:
        200:
            description: Deposit registered.
        400:
            description: Dataset not valid.
    """
    transaction_data = request.get_json()
    try:
        if transaction_data["amount"] <= 0:
            raise AmountNotPositive
        client = client_obj_constructor(transaction_data["client_cnp"], clients_collection)
        client.deposit(transaction_data["amount"])
        db_register_balance_transactions(client, clients_collection)
        return {"message": "Deposit successfully ."}, 200
    except BankException as excep:
        print(f'error {type(excep).__name__}: {excep.message["error_message"]}')
        return excep.message, excep.error_code


@app.route("/api/client/withdrawal", methods=["POST"])
def withdrawal():
    """
    Register a withdrawal for a client.
    ---
    parameters:
        - name: transaction_data
          in: body

    responses:
        200:
            description: Withdrawal registered.
        400:
            description: Dataset not valid.
    """
    transaction_data = request.get_json()
    try:
        if transaction_data["amount"] <= 0:
            raise AmountNotPositive
        client = client_obj_constructor(transaction_data["client_cnp"], clients_collection)
        client.withdrawal(transaction_data["amount"])
        db_register_balance_transactions(client, clients_collection)
        return {"message": "Deposit successfully ."}, 200
    except BankException as excep:
        print(f'error {type(excep).__name__}: {excep.message["error_message"]}')
        return excep.message, excep.error_code


@app.route("/api/client", methods=["POST"])
def register_client():
    """
    Register a new client into the database.
    ---
    parameters:
        - name: client_data
          in: body

    responses:
        200:
            description: An user object.
        400:
            description: Dataset not valid.
    """

    try:
        client_data = request.get_json()
        if len(client_data.keys()) < 4:
            raise UserDataMissingArgument
        create_client(client_data, clients_collection)
    except BankException as excep:
        print(f'error {type(excep).__name__}: {excep.message["error_message"]}')
        return excep.message, excep.error_code
    else:
        return client_data, 200


@app.route("/api/client/delete/<client_cnp>", methods=["PUT"])
def delete_client(client_cnp):
    """
    Mark a client as deleted and assign a deletion timestamp
        (it will be actually deleted after a certain period has passed).
    ---
    parameters:
        - name: client_cnp
          in: path

    responses:
        200:
            description: client deleted.
        400:
            description: Client not found.
    """
    try:
        clients_collection.update_one({"cnp": client_cnp},
                                      {"$set": {"deleted": transaction_timestamp()}})
        return {"message": "Client deleted."}, 200
    except BankException as excep:
        print(f'error {type(excep).__name__}: {excep.message["error_message"]}')
        return excep.message, excep.error_code


@app.route("/api/client/transfer", methods=["PUT"])
def transfer():
    """
    Transfer money.
    ---
    parameters:
        - name: transfer_data
          in: body
    responses:
        200:
            description: An user object.
        404:
            description: User not found.
    """

    try:
        transfer_data = request.get_json()
        sender = client_obj_constructor(transfer_data["sender_cnp"], clients_collection)
        receiver = client_obj_constructor(transfer_data["receiver_cnp"], clients_collection)
        money_transfer(sender, receiver, transfer_data["amount"], clients_collection)

    except BankException as excep:
        print(f'error {type(excep).__name__}: {excep.message["error_message"]}')
        return excep.message, excep.error_code
    else:
        return {"message": "transfer succeeded"}, 200


@app.route("/api/client/statement/<client_cnp>", methods=["GET"])
def statement(client_cnp):
    """
    Returns the statement of a client.
    ---
    parameters:
        - name: client_cnp
          in: path
          description: "cnp of the client"
          type: string
          required: true
    responses:
        200:
            description: "a statement"
        404:
            description: User not found.
    """
    try:
        client_statement = clients_collection.find_one({"cnp": client_cnp, "deleted": {"$eq": None}},
                                                       {"_id": 0, "transactions": 1})["transactions"]
        return jsonify(client_statement)
    except TypeError:
        print('Client not found.')
        return {"error_message": "client not found"}, 404


app.run(debug=True)

# db_client.close()  # TODO implement logic for db connection close
