# Atrapa odbiorcy formularza: zapisuje otrzymane zgłoszenia do pliku i odpowiada jak prawdziwy.
# Dzięki niej testy API nie wysyłają niczego do CRM.  python3 odbiorca.py <port> <plik> [kod]
import json, sys
from http.server import BaseHTTPRequestHandler, HTTPServer
port, plik, kod = int(sys.argv[1]), sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 200
class H(BaseHTTPRequestHandler):
    def do_POST(self):
        cialo = self.rfile.read(int(self.headers.get('Content-Length', 0))).decode('utf-8')
        with open(plik, 'a', encoding='utf-8') as f:
            f.write(json.dumps({'origin': self.headers.get('Origin'), 'pola': json.loads(cialo)}, ensure_ascii=False) + '\n')
        self.send_response(kod); self.send_header('Content-Type', 'application/json'); self.end_headers()
        self.wfile.write(b'{"ok":true}')
    def log_message(self, *a): pass
HTTPServer(('127.0.0.1', port), H).serve_forever()
