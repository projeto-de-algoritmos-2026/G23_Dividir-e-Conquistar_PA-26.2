"""Persistência local de observações de preço."""
import sqlite3
from contextlib import closing
from pathlib import Path
from datetime import date

DB = Path(__file__).parent / 'data' / 'precos.sqlite3'

def conectar():
    DB.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.execute('CREATE TABLE IF NOT EXISTS precos (id INTEGER PRIMARY KEY, produto TEXT NOT NULL, loja TEXT NOT NULL, data TEXT NOT NULL, preco_centavos INTEGER NOT NULL CHECK(preco_centavos > 0))')
    return conn

def listar():
    with closing(conectar()) as conn:
        return [dict(r) for r in conn.execute('SELECT * FROM precos ORDER BY data, id')]

def salvar(registros):
    preparados = []
    for r in registros:
        produto, loja = r['produto'].strip(), r['loja'].strip()
        dia = date.fromisoformat(r['data']).isoformat()
        preco = r['preco_centavos']
        if not produto or not loja or type(preco) is not int or preco <= 0:
            raise ValueError('Produto, loja e preço positivo são obrigatórios.')
        preparados.append((produto, loja, dia, preco))
    with closing(conectar()) as conn:
        with conn:
            conn.executemany('INSERT INTO precos (produto,loja,data,preco_centavos) VALUES (?,?,?,?)', preparados)
