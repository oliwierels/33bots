# Pobiera aktualne strony dokumentacji Google Search Central i zapisuje je jako tekst.
import html, re, sys, urllib.request
from pathlib import Path
B = 'https://developers.google.com/search/docs/'
STRONY = {
    'spam-policies': 'essentials/spam-policies',
    'helpful-content': 'fundamentals/creating-helpful-content',
    'build-sitemap': 'crawling-indexing/sitemaps/build-sitemap',
    'localized-versions': 'specialty/international/localized-versions',
    'managing-multi-regional': 'specialty/international/managing-multi-regional-sites',
    'search-gallery': 'appearance/structured-data/search-gallery',
    'sd-policies': 'appearance/structured-data/sd-policies',
    'review-snippet': 'appearance/structured-data/review-snippet',
    'faqpage': 'appearance/structured-data/faqpage',
    'local-business': 'appearance/structured-data/local-business',
    'video': 'appearance/structured-data/video',
    'article': 'appearance/structured-data/article',
    'breadcrumb': 'appearance/structured-data/breadcrumb',
    'publication-dates': 'appearance/publication-dates',
    'consolidate-duplicate-urls': 'crawling-indexing/consolidate-duplicate-urls',
    'block-indexing': 'crawling-indexing/block-indexing',
    'http-network-errors': 'crawling-indexing/http-network-errors',
    'title-link': 'appearance/title-link',
    'snippet': 'appearance/snippet',
    'links-crawlable': 'crawling-indexing/links-crawlable',
    'ask-google-to-recrawl': 'crawling-indexing/ask-google-to-recrawl',
    'indexing-api': '../apis/indexing-api/v3/quickstart'.replace('../', ''),
}
kat = Path(sys.argv[1]); kat.mkdir(parents=True, exist_ok=True)
for nazwa, sciezka in STRONY.items():
    adres = (B + sciezka if not sciezka.startswith('apis/') else 'https://developers.google.com/search/' + sciezka) + '?hl=en'
    try:
        s = urllib.request.urlopen(urllib.request.Request(adres, headers={'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'en'}), timeout=40).read().decode('utf-8', 'ignore')
    except Exception as e:
        (kat / f'{nazwa}.txt').write_text(f'BŁĄD {adres}: {e}\n'); print(nazwa, 'błąd', e); continue
    m = re.search(r'<article[^>]*>(.*?)</article>', s, re.S) or re.search(r'<main[^>]*>(.*?)</main>', s, re.S)
    t = m.group(1) if m else s
    t = re.sub(r'<(script|style|devsite-feedback|devsite-thumb-rating|nav)\b.*?</\1>', ' ', t, flags=re.S)
    t = re.sub(r'<(h[1-6])[^>]*>', r'\n\n## ', t); t = re.sub(r'<li[^>]*>', '\n- ', t); t = re.sub(r'<(td|th)[^>]*>', ' | ', t)
    t = re.sub(r'</(p|div|tr|ul|ol|table|h[1-6]|pre|section)>', '\n', t); t = re.sub(r'<br\s*/?>', '\n', t)
    t = html.unescape(re.sub(r'<[^>]+>', '', t)); t = re.sub(r'[ \t]+', ' ', t); t = re.sub(r'\n\s*\n\s*', '\n\n', t).strip()
    data = re.search(r'Last updated ([0-9-]+ UTC)', s)
    (kat / f'{nazwa}.txt').write_text(f'ŹRÓDŁO: {adres}\nLAST UPDATED: {data.group(1) if data else "?"}\n\n{t}\n', encoding='utf-8')
    print(nazwa, len(t.split()), 'słów', data.group(1) if data else '')
