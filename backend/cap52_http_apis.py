"""Capítulo 52: HTTP e consumo de APIs.

Parte: Backend.
Execute com: python cap52_http_apis.py
"""


# === Um servidor local para praticar ===

import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import httpx2

contador_instavel = {"n": 0}


class Manipulador(BaseHTTPRequestHandler):
    def responder(self, status, corpo):
        dados = json.dumps(corpo).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(dados)))
        self.end_headers()
        self.wfile.write(dados)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/ok":
            self.responder(200, {"mensagem": "olá"})
        elif url.path == "/instavel":
            contador_instavel["n"] += 1
            if contador_instavel["n"] < 3:
                self.responder(503, {"erro": "indisponível"})
            else:
                self.responder(200, {"tentativa": contador_instavel["n"]})
        elif url.path == "/lento":
            time.sleep(1)
            self.responder(200, {})
        elif url.path == "/itens":
            pagina = int(parse_qs(url.query).get("pagina", ["1"])[0])
            proxima = pagina + 1 if pagina < 3 else None
            self.responder(200, {"itens": list(range((pagina - 1) * 3, pagina * 3)), "proxima": proxima})
        else:
            self.responder(404, {"erro": "não encontrado"})

    def do_POST(self):
        tamanho = int(self.headers.get("Content-Length", 0))
        corpo = json.loads(self.rfile.read(tamanho) or b"{}")
        self.responder(201, {"recebido": corpo})

    def log_message(self, *args):
        pass


servidor = ThreadingHTTPServer(("127.0.0.1", 0), Manipulador)
threading.Thread(target=servidor.serve_forever, daemon=True).start()
BASE = f"http://127.0.0.1:{servidor.server_address[1]}"


# === Uma requisição com httpx2 ===

with httpx2.Client(base_url=BASE, timeout=2.0) as cliente:
    resposta = cliente.get("/ok")
    print(resposta.status_code, resposta.headers["content-type"], resposta.json())


# === Erro HTTP não é exceção ===

with httpx2.Client(base_url=BASE, timeout=2.0) as cliente:
    resposta = cliente.get("/nao-existe")
    print(resposta.status_code, resposta.is_success)
    try:
        resposta.raise_for_status()
    except httpx2.HTTPStatusError as erro:
        print("erro HTTP:", erro.response.status_code)


# === Timeout: sempre ===

try:
    httpx2.get(f"{BASE}/lento", timeout=0.2)
except httpx2.TimeoutException as erro:
    print("estourou o tempo:", type(erro).__name__)


# === Retentativas com espera crescente ===

def get_com_retentativas(cliente, caminho, *, tentativas=4, base=0.1, dormir=time.sleep):
    ultima = None
    for numero in range(1, tentativas + 1):
        try:
            ultima = cliente.get(caminho)
            if ultima.status_code < 500:
                return ultima
        except httpx2.TransportError:
            if numero == tentativas:
                raise
        if numero < tentativas:
            dormir(base * 2 ** (numero - 1))
    return ultima


esperas = []
with httpx2.Client(base_url=BASE, timeout=2.0) as cliente:
    resposta = get_com_retentativas(cliente, "/instavel", dormir=esperas.append)
print(resposta.status_code, resposta.json(), esperas)


# === Paginação ===

def todos_os_itens(cliente):
    pagina = 1
    while pagina is not None:
        dados = cliente.get("/itens", params={"pagina": pagina}).json()
        yield from dados["itens"]
        pagina = dados["proxima"]


with httpx2.Client(base_url=BASE, timeout=2.0) as cliente:
    print(list(todos_os_itens(cliente)))


# === Enviar JSON ===

with httpx2.Client(base_url=BASE, timeout=2.0) as cliente:
    resposta = cliente.post("/pedidos", json={"cliente": "Ana", "itens": 2})
    print(resposta.status_code, resposta.json())


# === Várias requisições ao mesmo tempo ===

import asyncio


async def buscar_varios():
    async with httpx2.AsyncClient(base_url=BASE, timeout=2.0) as cliente:
        respostas = await asyncio.gather(*(cliente.get("/ok") for _ in range(3)))
    return [r.status_code for r in respostas]


print(asyncio.run(buscar_varios()))


# === Exercício: Um cliente que traduz erro HTTP em exceção do domínio ===

class ErroDeApi(Exception):
    def __init__(self, status, caminho):
        super().__init__(f"{caminho} respondeu {status}")
        self.status = status


def buscar_json(cliente, caminho):
    resposta = cliente.get(caminho)
    if not resposta.is_success:
        raise ErroDeApi(resposta.status_code, caminho)
    return resposta.json()


with httpx2.Client(base_url=BASE, timeout=2.0) as cliente:
    assert buscar_json(cliente, "/ok") == {"mensagem": "olá"}
    try:
        buscar_json(cliente, "/nao-existe")
    except ErroDeApi as erro:
        assert erro.status == 404
    else:
        raise AssertionError("deveria falhar")
print("ok")
