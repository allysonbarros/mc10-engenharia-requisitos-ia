"""Casos gerados pelo PROMPT B (orientado a invariante e máquina de estados).

Cada teste nomeia a invariante que tenta furar, não a rota que chama.
"""

from __future__ import annotations

import sqlite3
from concurrent.futures import ThreadPoolExecutor

import eventus
from conftest import webhook


def test_inv1_corrida_de_inscricoes_nao_excede_a_capacidade(client, evento):
    """SPEC-001/I1: vagas ocupadas nunca passam da capacidade."""
    evento("ev-001", capacidade=5)

    def inscrever(i: int) -> int:
        return client.post(
            "/eventos/ev-001/inscricoes", json={"participante": f"P{i}"}
        ).status_code

    with ThreadPoolExecutor(max_workers=20) as pool:
        codigos = list(pool.map(inscrever, range(20)))

    assert codigos.count(201) == 5
    assert codigos.count(409) == 15
    assert client.get("/eventos/ev-001").json()["vagas_ocupadas"] == 5


def test_inv1_webhook_aprovado_apos_expiracao_nao_cria_overbooking(client, evento, monkeypatch):
    """A reserva expira aos 15 min; o webhook chega na retentativa, depois disso."""
    evento("ev-001", capacidade=1)
    monkeypatch.setattr(eventus, "TTL_RESERVA_SEGUNDOS", 0)

    ana = client.post("/eventos/ev-001/inscricoes", json={"participante": "Ana"}).json()
    assert client.post("/jobs/expirar-reservas").json()["expiradas"] == 1

    # a vaga liberada é tomada por outra pessoa
    bruno = client.post("/eventos/ev-001/inscricoes", json={"participante": "Bruno"}).json()
    webhook(client, event_id="evt-b", pagamento_id=bruno["pagamento_id"], status="aprovado")

    # só agora chega o webhook do pagamento da Ana, aprovado
    webhook(client, event_id="evt-a", pagamento_id=ana["pagamento_id"], status="aprovado")

    evento_final = client.get("/eventos/ev-001").json()
    assert evento_final["confirmadas"] <= evento_final["capacidade"]


def test_inv2_mesmo_pagamento_em_dois_eventos_gera_um_unico_recebimento(client, evento, db):
    """O gateway reenvia a notificação com event_id novo; o pagamento é o mesmo."""
    evento("ev-001", capacidade=1)
    criada = client.post("/eventos/ev-001/inscricoes", json={"participante": "Ana"}).json()

    webhook(client, event_id="evt-1", pagamento_id=criada["pagamento_id"], status="aprovado")
    webhook(client, event_id="evt-2", pagamento_id=criada["pagamento_id"], status="aprovado")

    con = sqlite3.connect(db)
    total = con.execute(
        "SELECT COUNT(*) FROM recebimentos WHERE pagamento_id = ?", (criada["pagamento_id"],)
    ).fetchone()[0]
    con.close()
    assert total == 1


def test_inv3_webhook_de_pagamento_desconhecido_nao_muda_estado(client, evento, db):
    evento("ev-001", capacidade=1)
    client.post("/eventos/ev-001/inscricoes", json={"participante": "Ana"})

    r = webhook(client, event_id="evt-x", pagamento_id="pay-inexistente", status="aprovado")

    assert r.json()["resultado"] == "pagamento_desconhecido"
    assert client.get("/eventos/ev-001").json()["confirmadas"] == 0


def test_inv4_expiracao_nao_toca_inscricao_ja_confirmada(client, evento, monkeypatch):
    evento("ev-001", capacidade=1)
    monkeypatch.setattr(eventus, "TTL_RESERVA_SEGUNDOS", 0)

    criada = client.post("/eventos/ev-001/inscricoes", json={"participante": "Ana"}).json()
    webhook(client, event_id="evt-1", pagamento_id=criada["pagamento_id"], status="aprovado")

    assert client.post("/jobs/expirar-reservas").json()["expiradas"] == 0
    assert client.get(f"/inscricoes/{criada['inscricao_id']}").json()["status"] == "confirmada"
