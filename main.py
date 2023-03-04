
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


@app.route("/api/client/<nume_client>", methods=["GET"])
def verifica_sold(nume_client):
    """
    Returneaza balanta unui client
    ---
    parameters:
        - name: nume_client
          in: path
          description: "numele clientului"
          type: string
          required: true
    responses:
        200:
            description: An user object
            # examples: {'name': 'Ion', balance: 200}
        404:
            description: User not found
    """
    try:
        balanta = clients_collection.find_one({"nume": nume_client}, {"_id": 0, "balanta": 1})["balanta"]
        print(balanta)
        return jsonify(balanta)
    except TypeError:
        print('Client inexistent.')
        return {"error_message": "clientul nu a fost gasit in baza de date"}, 404


@app.route("/api/client/filtru/<filtru>", methods=["GET"])
def afiseaza_clientii(filtru):
    """
    Returneaza balanta unui client
    ---
    parameters:
        - name: filtru
          in: path
          description: "filtru"
          type: string
          required: true
    responses:
        200:
            description: An user object
            # examples: {'name': 'Ion', balance: 200}
        404:
            description: User not found
    """

    # clients_names = afiseaza_clienti(filtru, clients_collection)
    # return jsonify(clients_names)

    try:
        clients_names = afiseaza_clienti(filtru, clients_collection)
    except NoClientsForFilter as e:
        print(f'Exception: {e}')
        return {"error_message": str(e)}, 404
    else:
        return jsonify(clients_names)


@app.route("/api/client/<nume_client>/<valoare>", methods=["PUT"])
def modificare_sold(nume_client, valoare):
    """
    Returneaza balanta unui client
    ---
    parameters:
        - name: nume_client
          in: path
          description: "numele clientului"
          type: string
          required: true
        - name: valoare
          in: path
          description: "valoarea cu care se modifica balanta"
          type: string
          required: true
    responses:
        200:
            description: An user object
            # examples: {'name': 'Ion', balance: 200}
        404:
            description: User not found
    """

    try:
        modifica_sold(constructor_client(nume_client, clients_collection), float(valoare), clients_collection)
        return {"message": "Balanta modificata cu succes."}, 200
    except TypeError:
        print('Client inexistent.')
        return {"error_message": "clientul nu a fost gasit in baza de date"}, 404
    except ValueError as e:
        print(str(e))
        return {"error_message": "valoarea trebuie sa fie un numar real"}, 400
    except Exception as e:
        return {"error_message": str(e)}, 4004


@app.route("/api/client", methods=["POST"])
def inregistreaza_client():
    """
    Returneaza balanta unui client
    ---
    parameters:
        - name: date_client
          in: body

    responses:
        200:
            description: An user object
            # examples: {'name': 'Ion', balance: 200}
        404:
            description: User not found
    """
    client_data = request.get_json()
    print(client_data)
    return {}, 200


app.run(debug=True)
