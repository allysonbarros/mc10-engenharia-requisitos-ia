from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import eventus  # noqa: E402


@pytest.fixture
def db(tmp_path) -> str:
    caminho = str(tmp_path / "eventus.db")
    con = sqlite3.connect(caminho)
    con.executescript(eventus.ESQUEMA)
    con.commit()
    con.close()
    return caminho


@pytest.fixture
def client(db) -> TestClient:
    return TestClient(eventus.criar_app(db))


@pytest.fixture
def evento(db):
    def _criar(evento_id: str = "ev-001", capacidade: int = 1) -> str:
        con = sqlite3.connect(db)
        con.execute("INSERT INTO eventos VALUES (?, ?, 0)", (evento_id, capacidade))
        con.commit()
        con.close()
        return evento_id

    return _criar


def webhook(client: TestClient, **payload):
    """Envia um webhook assinado como o gateway envia."""
    import json

    corpo = json.dumps(payload).encode()
    return client.post(
        "/webhooks/pagamento",
        content=corpo,
        headers={"X-Signature": eventus.assinar(corpo), "content-type": "application/json"},
    )
