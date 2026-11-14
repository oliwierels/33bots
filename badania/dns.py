# -*- coding: utf-8 -*-
"""Publiczne rekordy DNS czterech domen: serwery nazw i to, czy istnieje rekord TXT
potwierdzający własność w Google (sama liczba rekordów, bez ich wartości).
Uruchomienie: python3 dns.py <plik wyjściowy>"""
import json, sys, urllib.request

DOMENY = ['33bots.pl', '33bots.de', '33bots.at', '33bots.lt']


def pytaj(nazwa, typ):
    adres = f'https://dns.google/resolve?name={nazwa}&type={typ}'
    with urllib.request.urlopen(adres, timeout=20) as o:
        d = json.load(o)
    return [x.get('data', '') for x in d.get('Answer', [])]


wynik = {}
for d in DOMENY:
    txt = pytaj(d, 'TXT')
    wynik[d] = {
        'serwery_nazw': sorted(x.rstrip('.') for x in pytaj(d, 'NS')),
        'rekordy_txt': len(txt),
        'txt_google_site_verification': sum(1 for x in txt if 'google-site-verification=' in x),
    }
    print(d, wynik[d])
json.dump(wynik, open(sys.argv[1], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
