"""Casos gerados pelo PROMPT A (orientado a contrato).

Cada teste nomeia o par rota + código de resposta do contrato.
"""

from __future__ import annotations

from conftest import webhook


def test_inscricao_devolve_201_com_os_campos_do_contrato(client, evento):
    evento("ev-001", capacidade=2)
    r = client.post("/eventos/ev-001/inscricoes", json={"participante": "Ana Fictícia"})
    assert r.status_code == 201
    corpo = r.json()
    assert set(corpo) == {"inscricao_id", "status", "pagamento_id", "reservada_ate"}
    assert corpo["status"] == "aguardando_pagamento"


def test_inscricao_sem_participante_devolve_422(client, evento):
    evento("ev-001", capacidade=2)
    r = client.post("/eventos/ev-001/inscricoes", json={})
    assert r.status_code == 422


def test_inscricao_em_evento_inexistente_devolve_404(client):
    r = client.post("/eventos/ev-404/inscricoes", json={"participante": "Ana"})
    assert r.status_code == 404


def test_inscricao_sem_vaga_devolve_409(client, evento):
    evento("ev-001", capacidade=1)
    client.post("/eventos/ev-001/inscricoes", json={"participante": "Ana"})
    r = client.post("/eventos/ev-001/inscricoes", json={"participante": "Bruno"})
    assert r.status_code == 409


def test_webhook_sem_assinatura_valida_devolve_401(client):
    r = client.post(
        "/webhooks/pagamento",
        json={"event_id": "evt-1", "pagamento_id": "pay-x", "status": "aprovado"},
        headers={"X-Signature": "0" * 64},
    )
    assert r.status_code == 401


def test_webhook_com_status_desconhecido_devolve_422(client):
    r = webhook(client, event_id="evt-1", pagamento_id="pay-x", status="estornado")
    assert r.status_code == 422


def test_webhook_aprovado_confirma_a_inscricao(client, evento):
    evento("ev-001", capacidade=1)
    criada = client.post("/eventos/ev-001/inscricoes", json={"participante": "Ana"}).json()
    r = webhook(client, event_id="evt-1", pagamento_id=criada["pagamento_id"], status="aprovado")
    assert r.status_code == 200
    assert client.get(f"/inscricoes/{criada['inscricao_id']}").json()["status"] == "confirmada"


def test_webhook_repetido_com_mesmo_event_id_nao_reprocessa(client, evento):
    evento("ev-001", capacidade=1)
    criada = client.post("/eventos/ev-001/inscricoes", json={"participante": "Ana"}).json()
    webhook(client, event_id="evt-1", pagamento_id=criada["pagamento_id"], status="aprovado")
    r = webhook(client, event_id="evt-1", pagamento_id=criada["pagamento_id"], status="aprovado")
    assert r.json()["resultado"] == "ignorado_idempotencia"
