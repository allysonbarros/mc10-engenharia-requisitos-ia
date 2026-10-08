"""Eventus — serviço de inscrição em evento pago (recorte para testes de integração).

Dados fictícios. Recorte deliberado: reserva de vaga, webhook do gateway e job
de expiração. É o trecho que concentra as decisões do SPEC-001/I1
("vagas confirmadas nunca excedem a capacidade").
"""

from __future__ import annotations

import hashlib
import hmac
import sqlite3
import uuid
from datetime import UTC, datetime, timedelta

from fastapi import FastAPI, Header, Request
from fastapi.responses import JSONResponse

SEGREDO_WEBHOOK = b"fake-segredo-gateway"
TTL_RESERVA_SEGUNDOS = 15 * 60

ESQUEMA = """
CREATE TABLE eventos (
    id TEXT PRIMARY KEY,
    capacidade INTEGER NOT NULL,
    vagas_ocupadas INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE inscricoes (
    id TEXT PRIMARY KEY,
    evento_id TEXT NOT NULL,
    participante TEXT NOT NULL,
    status TEXT NOT NULL,
    pagamento_id TEXT NOT NULL,
    reservada_ate TEXT NOT NULL
);
CREATE TABLE webhooks_processados (event_id TEXT PRIMARY KEY);
CREATE TABLE recebimentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pagamento_id TEXT NOT NULL,
    inscricao_id TEXT NOT NULL
);
"""


def assinar(corpo: bytes) -> str:
    return hmac.new(SEGREDO_WEBHOOK, corpo, hashlib.sha256).hexdigest()


def criar_app(caminho_db: str) -> FastAPI:
    app = FastAPI()

    def conectar() -> sqlite3.Connection:
        con = sqlite3.connect(caminho_db, timeout=10, isolation_level=None)
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA journal_mode=WAL")
        con.execute("PRAGMA busy_timeout=10000")
        return con

    @app.post("/eventos/{evento_id}/inscricoes")
    def criar_inscricao(evento_id: str, payload: dict) -> JSONResponse:
        participante = payload.get("participante")
        if not isinstance(participante, str) or not participante.strip():
            return JSONResponse({"erro": "participante obrigatório"}, status_code=422)

        con = conectar()
        try:
            con.execute("BEGIN IMMEDIATE")
            cur = con.execute(
                "UPDATE eventos SET vagas_ocupadas = vagas_ocupadas + 1 "
                "WHERE id = ? AND vagas_ocupadas < capacidade",
                (evento_id,),
            )
            if cur.rowcount == 0:
                con.execute("ROLLBACK")
                existe = con.execute(
                    "SELECT 1 FROM eventos WHERE id = ?", (evento_id,)
                ).fetchone()
                if existe is None:
                    return JSONResponse({"erro": "evento não encontrado"}, status_code=404)
                return JSONResponse({"erro": "sem vagas"}, status_code=409)

            inscricao_id = str(uuid.uuid4())
            pagamento_id = "pay-" + uuid.uuid4().hex[:12]
            ate = datetime.now(UTC) + timedelta(seconds=TTL_RESERVA_SEGUNDOS)
            con.execute(
                "INSERT INTO inscricoes VALUES (?, ?, ?, 'aguardando_pagamento', ?, ?)",
                (inscricao_id, evento_id, participante, pagamento_id, ate.isoformat()),
            )
            con.execute("COMMIT")
        finally:
            con.close()

        return JSONResponse(
            {
                "inscricao_id": inscricao_id,
                "status": "aguardando_pagamento",
                "pagamento_id": pagamento_id,
                "reservada_ate": ate.isoformat(),
            },
            status_code=201,
        )

    @app.get("/inscricoes/{inscricao_id}")
    def ler_inscricao(inscricao_id: str) -> JSONResponse:
        con = conectar()
        try:
            linha = con.execute(
                "SELECT id, status, evento_id FROM inscricoes WHERE id = ?", (inscricao_id,)
            ).fetchone()
        finally:
            con.close()
        if linha is None:
            return JSONResponse({"erro": "não encontrada"}, status_code=404)
        return JSONResponse(dict(linha))

    @app.post("/webhooks/pagamento")
    async def receber_webhook(
        request: Request, x_signature: str = Header(default="")
    ) -> JSONResponse:
        corpo = await request.body()
        if not hmac.compare_digest(assinar(corpo), x_signature):
            return JSONResponse({"erro": "assinatura inválida"}, status_code=401)

        payload = await request.json()
        event_id = payload.get("event_id")
        pagamento_id = payload.get("pagamento_id")
        status = payload.get("status")
        if not event_id or not pagamento_id or status not in {"aprovado", "recusado"}:
            return JSONResponse({"erro": "payload inválido"}, status_code=422)

        con = conectar()
        try:
            con.execute("BEGIN IMMEDIATE")
            ja_visto = con.execute(
                "SELECT 1 FROM webhooks_processados WHERE event_id = ?", (event_id,)
            ).fetchone()
            if ja_visto is not None:
                con.execute("ROLLBACK")
                return JSONResponse({"resultado": "ignorado_idempotencia"})

            con.execute("INSERT INTO webhooks_processados VALUES (?)", (event_id,))
            inscricao = con.execute(
                "SELECT id, status FROM inscricoes WHERE pagamento_id = ?", (pagamento_id,)
            ).fetchone()
            if inscricao is None:
                con.execute("COMMIT")
                return JSONResponse({"resultado": "pagamento_desconhecido"})

            if status == "aprovado":
                con.execute(
                    "UPDATE inscricoes SET status = 'confirmada' WHERE id = ?",
                    (inscricao["id"],),
                )
                con.execute(
                    "INSERT INTO recebimentos (pagamento_id, inscricao_id) VALUES (?, ?)",
                    (pagamento_id, inscricao["id"]),
                )
            else:
                con.execute(
                    "UPDATE inscricoes SET status = 'recusada' WHERE id = ?",
                    (inscricao["id"],),
                )
            con.execute("COMMIT")
        finally:
            con.close()

        return JSONResponse({"resultado": "processado"})

    @app.post("/jobs/expirar-reservas")
    def expirar_reservas() -> JSONResponse:
        agora = datetime.now(UTC).isoformat()
        con = conectar()
        try:
            con.execute("BEGIN IMMEDIATE")
            vencidas = con.execute(
                "SELECT id, evento_id FROM inscricoes "
                "WHERE status = 'aguardando_pagamento' AND reservada_ate < ?",
                (agora,),
            ).fetchall()
            for linha in vencidas:
                con.execute(
                    "UPDATE inscricoes SET status = 'expirada' WHERE id = ?", (linha["id"],)
                )
                con.execute(
                    "UPDATE eventos SET vagas_ocupadas = vagas_ocupadas - 1 WHERE id = ?",
                    (linha["evento_id"],),
                )
            con.execute("COMMIT")
        finally:
            con.close()
        return JSONResponse({"expiradas": len(vencidas)})

    @app.get("/eventos/{evento_id}")
    def ler_evento(evento_id: str) -> JSONResponse:
        con = conectar()
        try:
            evento = con.execute(
                "SELECT id, capacidade, vagas_ocupadas FROM eventos WHERE id = ?", (evento_id,)
            ).fetchone()
            confirmadas = con.execute(
                "SELECT COUNT(*) AS n FROM inscricoes "
                "WHERE evento_id = ? AND status = 'confirmada'",
                (evento_id,),
            ).fetchone()["n"]
        finally:
            con.close()
        if evento is None:
            return JSONResponse({"erro": "não encontrado"}, status_code=404)
        return JSONResponse({**dict(evento), "confirmadas": confirmadas})

    return app
