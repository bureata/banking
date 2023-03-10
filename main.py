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
        balance = clients_collection.find_one({"cnp": client_cnp}, {"_id": 0, "balance": 1})["balance"]
        print(balance)
        return jsonify(balance)
    except TypeError:
        print('Client inexistent.')
        return {"error_message": "clientul nu a fost gasit in baza de date"}, 404


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


@app.route("/api/client/<client_cnp>/<amount>", methods=["PUT"])
def change_balance(client_cnp, amount):
    """
    Modify the balance for a specific client.
    ---
    parameters:
        - name: client_cnp
          in: path
          description: "client unique identification number"
          type: string
          required: true
        - name: amount
          in: path
          description: "value of the balance modification"
          type: string
          required: true
    responses:
        200:
            description: An user object.
        404:
            description: User not found.
    """

    try:
        try:
            amount = float(amount)
        except Exception:
            raise AmountNotNumber
        balance_change(client_obj_constructor(client_cnp, clients_collection), float(amount), clients_collection)
        return {"message": "Balance was successfully modified."}, 200
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
        client_statement = clients_collection.find_one({"cnp": client_cnp},
                                                       {"_id": 0, "transactions": 1})["transactions"]
        return jsonify(client_statement)
    except TypeError:
        print('Client not found.')
        return {"error_message": "client not found"}, 404


app.run(debug=True)

# db_client.close()  # TODO implement logic for db connection close
