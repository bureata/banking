lungime_rand = 100
rand_1 = 'MBBank                                                             Raport tranzactii pentru perioada'
nr_spatii_rand_2 = 79
nr_caractere_fixe_rand_antet = 45
pozitie_coloana2_date_client = 56
pozitie_detalii_cap_tabel = 26
pozitie_sfarsit_debit = 81
cap_tabel = 'Data                     Detalii tranzactie                                 Debit             Credit'
spatii_data_tranzactie = 7
spatii_detalii_tranzactie = 25

rand_acronim = 'MBBank'
rand_sold_initial = 'Sold initial:            '
rand_sold_final = 'Sold final:              '
footer = """
Andrada Perlea             Semnatura                             Mirela Ilie            Semnatura

Sef Serviciu Dezvoltare Produse                                  Sef Serviciu Relatii Clienti
MBBank                                                           MBBank
Sucursala Bucuresti                                              Sucursala Bucuresti
"""


def constructor_extras(nume_client, clients_collection):
    date_client = clients_collection.find_one({"name": nume_client}, {"_id": 1, "adresa": 1})
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
            tranzactie["transaction_type"]) - spatii_inainte_de_tranzactie - len(data_formatata) + 1
        spatii_detalii = pozitie_detalii_cap_tabel - 1
        print(
            f'{data_formatata}{" " * spatii_inainte_de_tranzactie}{tranzactie["transaction_type"]}{" " * spatii_dupa_tranzactie}{abs(tranzactie["suma"])}')
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

def formatere_data_extras_cont(string_date_time, dt_in_format="%Y%m%d%H%M%S", dt_out_format="%d %B %Y"):
    """
    Functie care primeste o data intr-un anumit format si o returneaza intr-un alt format la alegere (de exemplu este primita in formatul cu care este introdusa in fisierul de tranzactii si o returneaza in formatul cu care va fi afisata in extrasul de cont, pentru o citire mai usoara. Functia poate primi cele 2 formate, sau le va folosi pe cele default (cele din exemplu) in caz contrar.
    :param string_date_time: str Data in formatul din fisierul cu tranzactii
    :param dt_in_format: str Formatul in care se primeste data
    :param dt_out_format: str Formatul in care se returneaza data
    :return data: str Data in formatul dorit
    """
    back_to_dt = datetime.datetime.strptime(string_date_time, dt_in_format)
    str_out_date = datetime.datetime.strftime(back_to_dt, dt_out_format)
    return str_out_date


def formatare_data_cautare(data_format_input, in_format="%d.%m.%Y", out_format="%Y%m%d%H%M%S"):
    dt_obj = datetime.datetime.strptime(data_format_input, in_format)
    return datetime.datetime.strftime(dt_obj, out_format)


def formatere_data_antet(data, in_format="%Y%m%d%H%M%S", out_format="%d.%m.%Y"):
    dt_obj = datetime.datetime.strptime(data, in_format)
    return datetime.datetime.strftime(dt_obj, out_format)

def tranzactii_in_perioada(nume_client, clients_collection):
    data_inceput = date_validator('Introdu data de inceput in formatul "zz.ll.aaaa" (enter pentru inceput): ')
    data_sfarsit = date_validator('Introdu data de sfarsit in formatul "zz.ll.aaaa" ("prezent" pentru data curenta): ')
    date_client = clients_collection.find_one({"nume": nume_client}, {"_id": 0, "tranzactii": 1})
    lista_tranzactii = []

    for item in date_client["tranzactii"]:
        if int(data_inceput) <= int(item["timestamp"]) <= int(data_sfarsit):
            lista_tranzactii.append(item)

    perioada = (formatere_data_antet(data_inceput), formatere_data_antet(data_sfarsit))
    return lista_tranzactii, perioada


