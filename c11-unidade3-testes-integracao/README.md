# Eventus — testes de integração gerados com GenAI

Recorte do Sistema de Gestão de Eventos usado nas atividades anteriores:
reserva de vaga, webhook do gateway de pagamento e job de expiração de
reserva. Dados fictícios.

## Como rodar

```
pip install fastapi httpx pytest
python -m pytest tests -q
```

Saída literal:

```
.........FF..                                                            [100%]
=================================== FAILURES ===================================
________ test_inv1_webhook_aprovado_apos_expiracao_nao_cria_overbooking ________

client = <starlette.testclient.TestClient object at 0x7f39003ffc50>
evento = <function evento.<locals>._criar at 0x7f3900295580>
monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x7f39003a7bb0>

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
>       assert evento_final["confirmadas"] <= evento_final["capacidade"]
E       assert 2 <= 1

tests/test_invariantes.py:48: AssertionError
_____ test_inv2_mesmo_pagamento_em_dois_eventos_gera_um_unico_recebimento ______

client = <starlette.testclient.TestClient object at 0x7f39003caf30>
evento = <function evento.<locals>._criar at 0x7f38dc7a0fe0>
db = '/tmp/pytest-of-root/pytest-2/test_inv2_mesmo_pagamento_em_d0/eventus.db'

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
>       assert total == 1
E       assert 2 == 1

tests/test_invariantes.py:64: AssertionError
=============================== warnings summary ===============================
../../../../usr/local/lib/python3.13/dist-packages/starlette/testclient.py:53
  /usr/local/lib/python3.13/dist-packages/starlette/testclient.py:53: DeprecationWarning: The anyio.abc.BlockingPortal alias is deprecated, use anyio.from_thread.BlockingPortal instead.
    _PortalFactoryType = Callable[[], AbstractContextManager[anyio.abc.BlockingPortal]]

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
FAILED tests/test_invariantes.py::test_inv1_webhook_aprovado_apos_expiracao_nao_cria_overbooking
FAILED tests/test_invariantes.py::test_inv2_mesmo_pagamento_em_dois_eventos_gera_um_unico_recebimento
2 failed, 11 passed, 1 warning in 0.49s
```

## Os dois prompts

- `prompts/prompt-a-contrato.md` — casos derivados do contrato da API
  (um por par rota + código de resposta).
- `prompts/prompt-b-invariantes.md` — casos derivados das invariantes e
  da máquina de estados, com corrida e ordem invertida.

## Resultado da suíte

```
2 failed, 11 passed in 0.56s
```

Os 8 casos do Prompt A passam. Dos 5 casos do Prompt B, 2 falham, e as
duas falhas são defeitos reais do recorte:

| Caso | Invariante | Observado |
|---|---|---|
| `test_inv1_webhook_aprovado_apos_expiracao_nao_cria_overbooking` | confirmadas <= capacidade | `assert 2 <= 1` |
| `test_inv2_mesmo_pagamento_em_dois_eventos_gera_um_unico_recebimento` | 1 pagamento = 1 recebimento | `assert 2 == 1` |

As duas falhas estão preservadas de propósito: são decisão de negócio
pendente, não bug a corrigir em silêncio.

## Lacunas registradas

- LAC-01: webhook aprovado para uma inscrição já `expirada` — confirmar
  (fura a capacidade) ou recusar (deixa quem pagou sem vaga)? A máquina
  de estados não declara transição de saída para `expirada`.
- LAC-02: a idempotência do webhook é por `event_id`. O gateway reenvia
  a mesma notificação com `event_id` novo? Se sim, a chave de
  idempotência precisa ser o `pagamento_id`.
