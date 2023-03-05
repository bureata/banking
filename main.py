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
        balance_change(client_obj_constructor(client_cnp, clients_collection), float(amount), clients_collection)
        return {"message": "Balance was successfully modified."}, 200
    except NotEnoughFunds as excep:
        print(type(excep).__name__)
        return {"error_message": "Not enough funds."}, 400
    except AmountZero as excep:
        print(type(excep).__name__)
        return {"error_message": "the amount cannot be 0"}, 400
    except TypeError:
        print('Error: Client does not exist.')
        return {"error_message": "Client not found in the database."}, 404
    except ValueError as excep:
        print(str(excep))
        return {"error_message": "Value must be a number."}, 400
    except Exception as excep:
        print(excep)
        return {"error_message": type(excep).__name__}, 404


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
        create_client(client_data, clients_collection)
    except ClientAlreadyExists as excep:
        print(f'error type: {type(excep).__name__}')
        return {'error message': 'client already has an account'}, 400
    except PhoneAlreadyInUse as excep:
        print(f'error type: {type(excep).__name__}')
        return {'error message': 'phone number already in use'}, 400
    except KeyError as excep:
        print(f'error type: {type(excep).__name__}')
        return {'error message': 'probably user data incomplete'}, 400
    except UserDataWrongType as excep:
        print(f'error type: {type(excep).__name__}')
        return {'error message': 'user data passed as wrong type'}, 400
    except Exception as excep:
        print(f'error type: {type(excep).__name__}')
        return {'error message': type(excep).__name__}, 400
    else:
        return client_data, 200


app.run(debug=True)

# db_client.close()  # TODO implement logic for db connection close
