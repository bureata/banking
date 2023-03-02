import datetime


def introdu_nume(mesaj):
    lista_ord = list(range(65, 91)) + list(range(97, 123)) + [45, 32]
    while True:
        caractere_potrivite = True
        nume = input(mesaj)
        for caracter in nume:
            if ord(caracter) not in lista_ord:
                caractere_potrivite = False
                print('Numele poate contine doar litere, spatii sau "-"')
        if caractere_potrivite == True:
            break
    return nume  # .capitalize()


def introdu_numar(mesaj):
    lista_caractere = "0123456789.,-"
    while True:
        numar = input(mesaj)
        numar_valid = True
        if numar.count('.') > 1 or numar.count(',') > 1 or numar.count('.') + numar.count(',') > 1 or numar.count(
                '-') > 1:
            numar_valid = False
        else:
            if ',' in numar:
                numar_list = list(numar)
                numar_list[numar_list.index(',')] = '.'
                numar = ''.join(numar_list)
            if '-' in numar and numar[0] != '-':
                numar_valid = False

        for caracter in numar:
            if caracter not in lista_caractere:
                numar_valid = False
        if numar_valid:
            break
        else:
            print('Numarul introdus nu este valid')
    return float(numar)


def introdu_data(mesaj, out_format="%Y%m%d%H%M%S", data_sfarsit=False):
    dt_in_format = "%d.%m.%Y"
    dt_check_format = "%d %B %Y"
    exit_loop = False
    while True:
        data = input(mesaj)
        if data == 'exit':
            break
        elif data == 'prezent':
            dt_obj = datetime.datetime.now()
            exit_loop = True
        elif data == '':
            dt_obj = datetime.datetime.strptime('01.01.1000', dt_in_format)
            exit_loop = True
        else:
            try:
                dt_obj = datetime.datetime.strptime(data, dt_in_format)
                month_date = datetime.datetime.strftime(dt_obj, dt_check_format)
                choice = input(f'"{month_date}" este data dorita (da/nu)?: ')
                if choice == 'da':
                    exit_loop = True
            except:
                print('Data introdusa nu este intr-un format valid.')
        if exit_loop:
            data_formatata = datetime.datetime.strftime(dt_obj, out_format)
            if data_sfarsit == True:
                data_formatata = str(int(data_formatata) + 235959)
            return data_formatata


def formatere_data_antet(data, in_format="%Y%m%d%H%M%S", out_format="%d.%m.%Y"):
    dt_obj = datetime.datetime.strptime(data, in_format)
    return datetime.datetime.strftime(dt_obj, out_format)


def transaction_timestamp():
    dt = datetime.datetime.now()
    dt_format = "%Y%m%d%H%M%S"
    str_dt = dt.strftime(dt_format)
    return int(str_dt)


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


def tranzactii_in_perioada(nume_client, clients_collection):
    data_inceput = introdu_data('Introdu data de inceput in formatul "zz.ll.aaaa" (enter pentru inceput): ')
    data_sfarsit = introdu_data('Introdu data de sfarsit in formatul "zz.ll.aaaa" ("prezent" pentru data curenta): ')
    date_client = clients_collection.find_one({"nume": nume_client}, {"_id": 0, "tranzactii": 1})
    lista_tranzactii = []

    for item in date_client["tranzactii"]:
        if int(data_inceput) <= int(item["timestamp"]) <= int(data_sfarsit):
            lista_tranzactii.append(item)

    perioada = (formatere_data_antet(data_inceput), formatere_data_antet(data_sfarsit))
    return lista_tranzactii, perioada