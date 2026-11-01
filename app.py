"""Servidor local do Preço Justo. Execute: python app.py."""
import json
import secrets
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
import engine
import storage

ROOT = Path(__file__).parent
TOKEN = secrets.token_urlsafe(24)

class Handler(BaseHTTPRequestHandler):
    def resposta(self, status, dados):
        corpo = json.dumps(dados, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(corpo)

    def do_GET(self):
        rota = urlparse(self.path).path
        if rota == '/api/historico':
            return self.resposta(200, {'registros': storage.listar(), 'nucleo': engine.disponivel()})
        arquivos = {'/': ('web/index.html', 'text/html'), '/app.js': ('web/app.js', 'text/javascript'), '/style.css': ('web/style.css', 'text/css')}
        if rota not in arquivos:
            return self.resposta(404, {'erro': 'Página não encontrada.'})
        arquivo, tipo = arquivos[rota]
        corpo = (ROOT / arquivo).read_text(encoding='utf-8').replace('__TOKEN__', TOKEN).encode()
        self.send_response(200)
        self.send_header('Content-Type', tipo + '; charset=utf-8')
        self.end_headers()
        self.wfile.write(corpo)

    def do_POST(self):
        if self.headers.get('X-App-Token') != TOKEN:
            return self.resposta(403, {'erro': 'Recarregue a página para continuar.'})
        try:
            tamanho = int(self.headers.get('Content-Length', '0'))
            if tamanho < 1 or tamanho > 1_000_000:
                raise ValueError('Arquivo ou pedido acima do limite de 1 MB.')
            dados = json.loads(self.rfile.read(tamanho))
            if self.path == '/api/cadastro':
                storage.salvar([dados])
                return self.resposta(200, {'ok': True})
            if self.path == '/api/importar':
                registros = engine.importar(dados['csv'])
                storage.salvar(registros)
                return self.resposta(200, {'quantidade': len(registros)})
            if self.path == '/api/analisar':
                from datetime import date
                inicio, fim = date.fromisoformat(dados['inicio']), date.fromisoformat(dados['fim'])
                if inicio > fim:
                    raise ValueError('O início deve vir antes do fim.')
                precos = [r['preco_centavos'] for r in storage.listar()
                          if r['produto'] == dados['produto'] and inicio <= date.fromisoformat(r['data']) <= fim]
                if not precos:
                    raise ValueError('Não há preços no período selecionado.')
                return self.resposta(200, engine.analisar(precos, dados['oferta_centavos']))
            self.resposta(404, {'erro': 'Operação não encontrada.'})
        except (ValueError, KeyError, TypeError) as erro:
            self.resposta(400, {'erro': str(erro)})

if __name__ == '__main__':
    print('Preço Justo: http://127.0.0.1:8501 — Ctrl+C para encerrar', flush=True)
    ThreadingHTTPServer(('127.0.0.1', 8501), Handler).serve_forever()
