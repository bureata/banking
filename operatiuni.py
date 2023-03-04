from input_utils import *
from elemente_extras import *
from exceptions import *


class Client:

    def __init__(self, nume, cnp=None, nr_telefon=None, adresa=None, balanta=0, deleted=False):
        self.nume = nume
        self.cnp = cnp
        self.nr_telefon = nr_telefon
        self.adresa = adresa
        self.balanta = balanta
        self.tranzactii = []
        self.deleted = deleted

    #     def __str__(self):

    #         return self.nume + str(self.balanta)

    def retragere(self, suma):

        if self.balanta < suma:
            print("n-ai bani")
            return

        self.balanta = self.balanta - suma
        self.tranzactii.append(Tranzactie("retragere", self.nume, suma))

    def depunere(self, suma):

        self.balanta = self.balanta + suma
        self.tranzactii.append(Tranzactie("depunere", self.nume, suma))

    def transfer(self, destinatar, suma):
        if self.balanta < suma:
            print("No money")
            return
        self.balanta = self.balanta - suma
        destinatar.balanta = destinatar.balanta + suma
        self.tranzactii.append(Tranzactie("transfer", self.nume, suma, destinatar.nume))
        destinatar.tranzactii.append(Tranzactie("transfer", self.nume, suma, destinatar.nume))


class Tranzactie:

    def __init__(self, tip_tranzactie, expeditor, suma, destinatar=None, timestamp=None):
        if timestamp is None:
            self.timestamp = transaction_timestamp()
        else:
            self.timestamp = timestamp
        self.tip_tranzactie = tip_tranzactie
        self.expeditor = expeditor
        self.suma = suma
        self.destinatar = destinatar

    # def dict_mongo(self):
    #     initial_result = self.__dict__
    #     initial_result["expeditor"] = initial_result["expeditor"].nume
    #     if initial_result["destinatar"]:
    #         initial_result["destinatar"] = initial_result["destinatar"].nume
    #     return initial_result

    def __str__(self):
        if self.destinatar == None:
            return self.expeditor + "|" + str(self.suma) + "|" + self.tip_tranzactie

        return self.expeditor + "|" + str(self.suma) + "|" + self.destinatar + "|" + self.tip_tranzactie


def creaza_client(clients_collection):
    """
    Functie care adauga in fisierul "clients.txt" un client, folosind datele de identificare introduse de la tastatura.
    :param dict_clients: dict Dictionarul care stocheaza in memorie datele despre clienti
    """
    # clients_collection = db["clients"]
    cnp = input('Intordu CNP: ')
    nume = introdu_nume('Numele noului client: ')
    telefon = input('Numar de telefon: ')
    adresa = input('Adresa: ')

    new_client = Client(nume, cnp, telefon, adresa)
    clients_collection.insert_one(new_client.__dict__)


def sterge_client(nume_client, clients_collection):
    print(nume_client)
    clients_collection.update_one({"nume": nume_client}, {"deleted": True})
    # sold = verifica_sold(nume_client, dict_clients)
    # if sold < 0:
    #     print(f'Pentru inchiderea contului este necesara achitarea sumei restante de: {sold}.')
    # elif sold > 0:
    #     print(f'Contul figureaza cu o sold de {sold}, care va fi restituita clientului.')
    # else:
    #     print(f'Soldul este 0. Contul va fi sters, impreuna cu informatiile despre client.')


def constructor_client(nume_client, clients_collection):
    date_client = clients_collection.find_one({"nume": nume_client},
                                              {"_id": 0, "nume": 1, "balanta": 1, "tranzactii": 1})
    client = Client(date_client["nume"], balanta=date_client["balanta"])
    if len(date_client["tranzactii"]) > 0:
        for tranz in date_client["tranzactii"]:
            client.tranzactii.append(
                Tranzactie(tranz["tip_tranzactie"], tranz["expeditor"], tranz["suma"], tranz["destinatar"],
                           tranz["timestamp"]))
    return client


def modifica_sold(client, valoare, clients_collection):
    """
    Functie care modifica soldul unui cont
    :param nume_client: text Numele clientului al carui sold trebuie modificat
    :param valoare: float Valoare cu care soldul va fi modificat. Poate fi pozitiva sau negativa.
    :return sold: float Soldul dupa ce a fost facuta mofidicarea
    """

    if valoare < 0:
        client.retragere(valoare)
    elif valoare > 0:
        client.depunere(valoare)
    else:
        raise Exception("valoare invalida")

    tranzactii_list = []
    for item in client.tranzactii:
        tranzactii_list.append(item.__dict__)
    clients_collection.update_one({"nume": client.nume},
                                  {"$set": {"balanta": client.balanta, "tranzactii": tranzactii_list}})


def transfer(valoare, nume_expeditor, nume_destinatar, clients_collection):
    # implementeaza logica pentru situatia "fonduri insuficiente"
    """
    Functie care face transferul unei sume de bani intre 2 conturi, cu conditia ca expeditorul sa dispuna de valoare care trebuie transferata
    :param valoare: float Valoare care urmeaza sa fie transferata
    :param nume_expeditor: str Numele expeditorului
    :param nume_destinatar: str Numele destinatarului
    :param dict_clients: dict Dictionarul care stocheaza in memorie datele despre clienti
    """
    if valoare <= 0:
        print('Valoarea transferata trebuie sa fie pozitiva. Transferul nu a fost efectuat.')
    else:
        expeditor = constructor_client(nume_expeditor, clients_collection)
        destinatar = constructor_client(nume_destinatar, clients_collection)
        if expeditor.balanta >= valoare:
            print(f"Soldul initial al clientului {expeditor.nume}: {expeditor.balanta}")
            print(f"Soldul initial al clientului {destinatar.nume}: {destinatar.balanta}")
            expeditor.transfer(destinatar, valoare)
            print(f"Soldul final al clitransferentului {expeditor.nume}: {expeditor.balanta}")
            print(f"Soldul final al clientului {destinatar.nume}: {destinatar.balanta}")

            tranzactii_expeditor = []
            for item in expeditor.tranzactii:
                tranzactii_expeditor.append(item.__dict__)
            clients_collection.update_one({"nume": expeditor.nume},
                                          {"$set": {"balanta": expeditor.balanta, "tranzactii": tranzactii_expeditor}})

            print(destinatar.tranzactii)

            tranzactii_destinatar = []
            for item in destinatar.tranzactii:
                tranzactii_destinatar.append(item.__dict__)
            clients_collection.update_one({"nume": destinatar.nume}, {
                "$set": {"balanta": destinatar.balanta, "tranzactii": tranzactii_destinatar}})
        else:
            print('Expeditorul nu are fonduri suficiente. Transferul nu a fost efectuat.')


def afiseaza_clienti(filter, clients_collection):
    clients_names = clients_collection.find({'nume': {'$regex': filter, '$options': 'i'}},
                                            {"_id": 0, "nume": 1, "cnp": 1})
    clients_list = []
    for name in clients_names:
        clients_list.append({name["nume"]: name["cnp"]})

    if len(clients_list) == 0:
        raise NoClientsForFilter(f'No clients for <{filter}> filter.')
    return clients_list


def constructor_extras(nume_client, clients_collection):
    date_client = clients_collection.find_one({"nume": nume_client}, {"_id": 1, "adresa": 1})
    tranzactii, perioada = tranzactii_in_perioada(nume_client, clients_collection)
    nume_nr_strada = ['Numele_strazii', '13']
    numarul_contului = 'numarul_contului'
    tip_cont = 'tipul_contului'
    moneda = 'RON'
    cod_client = 'codul_clientului'
    spatii_dupa_nume = pozitie_coloana2_date_client - 1 - len(nume_client)
    spatii_dupa_oras = pozitie_coloana2_date_client - 1 - len(date_client["adresa"])

    print('\n\n')
    print(rand_1)
    print(f"{' ' * 79}{perioada[0]}-{perioada[1]}")
    print('_' * lungime_rand)
    print(f"{nume_client}{' ' * spatii_dupa_nume}Tip Cont:       {tip_cont}")
    print(
        f"str. {nume_nr_strada[0]}, Nr. {nume_nr_strada[1]}                            Numar cont:     {numarul_contului}")
    print(f'{date_client["adresa"]}{" " * spatii_dupa_oras}Moneda:         {moneda}')
    print(f"{' ' * (pozitie_coloana2_date_client - 1)}Cod client:     {cod_client}\n")
    print('_' * lungime_rand)
    print(cap_tabel)
    print('_' * lungime_rand)
    print()
    for tranzactie in tranzactii:
        data_formatata = formatere_data_extras_cont(tranzactie["timestamp"])
        if tranzactie["suma"] < 0:
            pozitie_sfarsit = pozitie_sfarsit_debit
        else:
            pozitie_sfarsit = 100
        spatii_inainte_de_tranzactie = pozitie_detalii_cap_tabel - 2 - len(data_formatata)
        spatii_dupa_tranzactie = pozitie_sfarsit - len(str(tranzactie["suma"])) - len(
            tranzactie["tip_tranzactie"]) - spatii_inainte_de_tranzactie - len(data_formatata) + 1
        spatii_detalii = pozitie_detalii_cap_tabel - 1
        print(
            f'{data_formatata}{" " * spatii_inainte_de_tranzactie}{tranzactie["tip_tranzactie"]}{" " * spatii_dupa_tranzactie}{abs(tranzactie["suma"])}')
        for key in tranzactie.keys():
            # if expeditor
            print(f"{' ' * spatii_detalii}{key}: {tranzactie[key]}")

        print()

    print("""

MBBank
____________________________________________________________________________________________________

Andrada Perlea             Semnatura                             Mirela Ilie            Semnatura

Sef Serviciu Dezvoltare Produse                                  Sef Serviciu Relatii Clienti
MBBank                                                           MBBank
Sucursala Bucuresti  



"""
          )