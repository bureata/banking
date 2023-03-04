# TODO rewrite this module to act as a data validation tool for the api

import datetime


def name_validator(mesaj):  # TODO make this compatible with the api (exception raiser to work in the background)
    lista_ord = list(range(65, 91)) + list(range(97, 123)) + [45, 32]
    while True:
        caractere_potrivite = True
        nume = input(mesaj)
        for caracter in nume:
            if ord(caracter) not in lista_ord:
                caractere_potrivite = False
                print('Numele poate contine doar litere, spatii sau "-"')
        if caractere_potrivite:
            break
    return nume  # .capitalize()


def phone_validator(mesaj):  # TODO same as with the name_checker function
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


def date_validator(mesaj, out_format="%Y%m%d%H%M%S", data_sfarsit=False):  # TODO
    # TODO rewrite this to be a validator for the dates send as a period filter
    #   raise exception for invalid format dates
    dt_in_format = "%d.%m.%Y"
    dt_check_format = "%d %B %Y"
    exit_loop = False
    dt_obj = 'defining so pycharm lets me be happy'
    while True:
        data = input(mesaj)
        if data == 'prezent':
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
            except ValueError:
                print('Data introdusa nu este intr-un format valid.')
        if exit_loop:
            data_formatata = datetime.datetime.strftime(dt_obj, out_format)
            if data_sfarsit:
                data_formatata = str(int(data_formatata) + 235959)
            return data_formatata
