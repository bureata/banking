from input_utils import introdu_nume, transaction_timestamp
import json


def rescrie_fisier_clienti(dict_clients):
    """
    Functie care scrie pe disk baza de date din memorie
    :param dict_clients: dict Dictionarul care stocheaza in memorie datele despre clienti
    """
    clients = json.dumps(dict_clients, indent=4, separators=(',', ': '))
    with open("clients.json", "w") as fisier_clienti:
        fisier_clienti.write(clients)


def rescrie_fisier_tranzactii(dict_tranzactii):
    """
    Functie care scrie pe disk baza de date din memorie
    :param dict_clients: dict Dictionarul care stocheaza in memorie datele despre clienti
    """
    tranzactii = json.dumps(dict_tranzactii, indent=4, separators=(',', ': '))
    with open("tranzactii.json", "w") as fisier_tranzactii:
        fisier_tranzactii.write(tranzactii)


def tranzactie_deschidere_cont():
    pass


def log_transfer(nume_destinatar, nume_expeditor, valoare, dict_tranzactii, dict_clients):
    timestamp = transaction_timestamp()
    dict_tranzactie_destinatar = {'tip_tranzactie': 'Incasare',
                                  'ordonator': nume_expeditor,
                                  'valoare': valoare,
                                  'sold': dict_clients[nume_destinatar]['sold']
                                  }
    if nume_destinatar not in dict_tranzactii:
        dict_tranzactii[nume_destinatar] = {}
    dict_tranzactii[nume_destinatar][timestamp] = {}
    dict_tranzactii[nume_destinatar][timestamp] = dict_tranzactie_destinatar

    dict_tranzactie_expeditor = {'tip_tranzactie': 'Transfer',
                                 'beneficiar': nume_destinatar,
                                 'valoare': -valoare,
                                 'sold': dict_clients[nume_expeditor]['sold']
                                 }
    if nume_expeditor not in dict_tranzactii:
        dict_tranzactii[nume_expeditor] = {}
    dict_tranzactii[nume_expeditor][timestamp] = {}
    dict_tranzactii[nume_expeditor][timestamp] = dict_tranzactie_expeditor

    rescrie_fisier_tranzactii(dict_tranzactii)


def log_depunere_retragere(nume_client, valoare, dict_tranzactii, dict_clients):
    timestamp = transaction_timestamp()
    if valoare > 0:
        tip_tranzactie = 'Depunere'

    else:
        tip_tranzactie = 'Retragere'
    dict_tranzactie = {'tip_tranzactie': tip_tranzactie,
                       'valoare': valoare,
                       'sold': dict_clients[nume_client]['sold']
                       }

    if nume_client not in dict_tranzactii:
        dict_tranzactii[nume_client] = {}
    dict_tranzactii[nume_client][timestamp] = {}
    dict_tranzactii[nume_client][timestamp] = dict_tranzactie

    rescrie_fisier_tranzactii(dict_tranzactii)


def tranzactie_inchidere_cont():
    pass

