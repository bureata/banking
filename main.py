# TODO implement two languages for the front end part

from flask import Flask, jsonify, request
from flasgger import Swagger
import pymongo
from operatiuni import *
from mongo_credentials import *

app = Flask(__name__)
swagger = Swagger(app)

db_client = pymongo.MongoClient(pass_text)

db = db_client["bankingDB"]
clients_collection = db["clients"]


@app.route("/api/client/<client_name>", methods=["GET"])
def check_balance(client_name):
    """
    Returns the balance of a client
    ---
    parameters:
        - name: client_name
          in: path
          description: "name of the client"
          type: string
          required: true
    responses:
        200:
            description: "58"
        404:
            description: User not found.
    """
    try:
        balanta = clients_collection.find_one({"nume": client_name}, {"_id": 0, "balanta": 1})["balanta"]
        print(balanta)
        return jsonify(balanta)
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
    except NoClientsForFilter as e:
        print(f'Exception: {e}')
        return {"error_message": str(e)}, 404
    else:
        return jsonify(clients_data)


@app.route("/api/client/<client_name>/<value>", methods=["PUT"])
def change_balance(client_name, value):
    """
    Modify the balance for a specific client.
    ---
    parameters:
        - name: client_name
          in: path
          description: "client name"
          type: string
          required: true
        - name: value
          in: path
          description: "value of the modification"
          type: string
          required: true
    responses:
        200:
            description: An user object.
        404:
            description: User not found.
    """

    try:
        balance_change(client_obj_constructor(client_name, clients_collection), float(value), clients_collection)
        return {"message": "Balance was successfully modified."}, 200
    except TypeError:
        print('Client does not exist.')
        return {"error_message": "Client not found in the database."}, 404
    except ValueError as e:
        print(str(e))
        return {"error_message": "Value must be a number."}, 400
    except Exception as e:
        return {"error_message": str(e)}, 404


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
    client_data = request.get_json()
    print(client_data)
    return {}, 200


app.run(debug=True)
