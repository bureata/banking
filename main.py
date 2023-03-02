
from flask import Flask, jsonify, request
from flasgger import Swagger
import pymongo
from operatiuni import *
from input_utils import introdu_nume, introdu_numar
# from IPython.display import clear_output
from admin_date import *
from mongo_pass import *

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

    try:
        clients_names = afiseaza_clienti(filtru, clients_collection)
        return jsonify(clients_names)
    except:
        return {"error_message": "niciun client pentru filtrul introdus"}, 404


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
        return {"error_message": "valoarea trebuie sa fie un numar real"}, 400
    except Exception as e:
        return {"error_message": str(e)}, 400

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
    # try:
    #     clients_names = afiseaza_clienti(filtru, clients_collection)
    #     return jsonify(clients_names)
    # except:
    #     return {"error_message": "niciun client pentru filtrul introdus"}, 404

app.run(debug=True)

