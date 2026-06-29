# Dominando o Claude · Executivo (V2)

Versão **executiva geral** do treinamento — cross-setor, focada no trabalho de liderança
(relatórios, apresentações, concorrência, mercado, perguntas melhores, e-mail/agenda).
Site **separado** da V1 (seguro garantia), reusando a mesma engine e identidade visual.

Fio condutor: empresa fictícia **Aurora S.A.** (varejo de bens de consumo; lojas +
e-commerce; crescimento desacelerando e um concorrente digital ganhando share).

## Como rodar

```bash
cd treinamento-claude-executivo-v2
python3 gen_dataroom.py   # gera o data room da Aurora (1ª vez ou ao mudar dados)
python3 build.py          # site multipágina
python3 build_single.py   # → treinamento-aluno.html + treinamento-facilitador.html
python3 -m http.server 8091   # abra http://localhost:8091
```

## Módulos (17 — núcleo + aprofundamentos)

| # | Módulo | Ato |
|---|--------|-----|
| 00 | Abertura (caso Aurora) | I — Fundamentos |
| 01 | Conhecendo o Claude | I |
| 02 | Fundamentos sem jargão | I |
| 03 | O brief executivo | I |
| 04 | **Ler relatórios** | II — O trabalho executivo |
| 05 | **Do relatório ao deck** (.pptx) | II |
| 06 | **Concorrência: o poder das perguntas** | II |
| 07 | **Análise de mercado** (Deep Research) *(aprof)* | II |
| 08 | **Construir um entregável** (memo/deck) | II |
| 09 | Cowork *(aprof)* | III — Ir além e governar |
| 10 | Projetos *(aprof)* | III |
| 11 | Personalização e Skills | III |
| 12 | **Conectores: Outlook, Calendar e e-mail** | III |
| 13 | Plugins, comandos e automações *(aprof)* | III |
| 14 | Nível 4 — Código e Computador *(aprof)* | III |
| 15 | Riscos e governança | III |
| 16 | Plano 30-60-90 | III |

Mais a página **Dicas** (Como falar com o Claude) e **Referência** (apêndices).

## Cobre os pedidos do V2

- **Relatórios** → Módulo 04.
- **Produzir apresentações** (relatório → balanço/resultados em .pptx) → Módulo 05.
- **Concorrência/mercado + o poder das perguntas** (advogado do diabo, pre-mortem) → Módulos 06 e 07.
- **Análise de mercado** → Módulo 07.
- **Outlook / Calendar / e-mail** → Módulo 12.

## Caso Aurora (data room)

Gerado por `gen_dataroom.py`: `Aurora_DataRoom.xlsx` (7 abas: resultados, DRE, balanço,
mercado, concorrentes — **com erros plantados**), `Aurora_Release_Resultados.md`,
`Aurora_Mercado.md`, `Aurora_Concorrentes.md` e o `Aurora_Gabarito_Facilitador.md`
(**só facilitador**). Materiais do programa (prompts, skills, checklist, templates de
contexto) são gerados pelo `build.py`.

A V1 (treinamento-claude-seguros) permanece **intocada**.
