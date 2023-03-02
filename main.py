
from flask import Flask, jsonify
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

app.run(debug=True)

