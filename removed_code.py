from elemente_extras import *

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


