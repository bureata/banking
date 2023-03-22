# TODO rewrite this module to act as a data validation tool for the api

import datetime
from exceptions import *


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


def date_to_timestamp(date, out_format="%Y%m%d%H%M%S", end_date=False):
    dt_in_format = "%d.%m.%Y"
    try:
        dt_obj = datetime.datetime.strptime(date, dt_in_format)
        timestamp = datetime.datetime.strftime(dt_obj, out_format)
        if end_date:
            timestamp = str(int(timestamp) + 235959)
        return timestamp
    except Exception:
        raise DateFormatWrong
