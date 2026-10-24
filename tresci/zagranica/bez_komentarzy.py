# Komentarze w kodzie kopiowanym z 33bots.pl są po polsku. Na stronach zagranicznych usuwamy te,
# w których są polskie litery, żeby w kodzie strony nie zostawało polskie zdanie. Pozostałe zostają.
import re

POLSKIE = re.compile(r'[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]')
# Komentarz blokowy zaczyna się od „/*” i odstępu, gwiazdki lub nowej linii — 'image/*' w napisie się nie łapie.
BLOK = re.compile(r'[ \t]*/\*[\s*].*?\*/', re.S)
# Komentarz liniowy tylko w całej linii — „//” w adresach i w kodzie zostaje.
LINIA = re.compile(r'(?m)^[ \t]*//[^\n]*\n')
SKRYPT = re.compile(r'(<script\b(?![^>]*application/(?:ld\+)?json)[^>]*>)(.*?)(</script>)', re.S)
STYL = re.compile(r'(<style\b[^>]*>)(.*?)(</style>)', re.S)
# Komentarz HTML razem z wcięciem i końcem linii — bez pustej linii po nim.
HTML = re.compile(r'[ \t]*<!--.*?-->[ \t]*\n?', re.S)


def _bez(wzor, tekst):
    return wzor.sub(lambda m: '' if POLSKIE.search(m.group(0)) else m.group(0), tekst)


def js(tekst):
    return _bez(LINIA, _bez(BLOK, tekst))


def css(tekst):
    return _bez(BLOK, tekst)


def strona(html):
    html = _bez(HTML, html)
    html = SKRYPT.sub(lambda m: m.group(1) + js(m.group(2)) + m.group(3), html)
    return STYL.sub(lambda m: m.group(1) + css(m.group(2)) + m.group(3), html)
