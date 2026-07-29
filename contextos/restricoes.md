# Restrições e o que evitar

## Restrições conhecidas

- **LGPD / privacidade de dados** — o sistema trata dados pessoais de participantes. A visibilidade desses dados para palestrantes precisa ser explicitamente delimitada (ver questão em aberto #8). Tratar privacidade como restrição desde o desenho, não como enfeite posterior.
- **Requisitos não-funcionais não levantados** — segurança, desempenho, disponibilidade, acessibilidade e privacidade **ainda não foram elicitados** (observação explícita da elicitação). Não assumir que estão cobertos; levantá-los antes de especificar (apoio: `apoio-norma-nfr`).
- **Regras de negócio indefinidas** — não implementar cancelamento, reembolso, lista de espera ou emissão de certificado enquanto as decisões pendentes não forem fechadas. Código sobre premissa inventada é retrabalho garantido.

## Questões em aberto (da elicitação)

Pontos sem definição que **precisam ser resolvidos antes de especificar**:

1. Até quando o participante poderá cancelar a inscrição.
2. Em quais situações há direito a reembolso.
3. Como funciona a lista de espera.
4. Certificados: emitidos automaticamente ou dependem de confirmação de presença.
5. Como serão enviados comprovantes de inscrição e demais notificações.
6. Se a vaga é reservada ao iniciar o pagamento ou só após confirmação.
7. Como tratar inscrição em atividades com horários conflitantes.
8. Quais informações do participante o palestrante pode visualizar.
9. Requisitos de segurança, desempenho, disponibilidade, acessibilidade e privacidade.

> Cada item acima é candidato a virar uma decisão registrada em `decisoes/log.md` (ou um ADR) assim que o negócio responder.

## "Aqui dragões habitam"

`<a preencher>` — sem código legado ainda.
