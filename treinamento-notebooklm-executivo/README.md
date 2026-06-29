# Dominando o NotebookLM · Executivo

Curso executivo sobre o **NotebookLM** (Google) — a ferramenta que lê a SUA pilha de
documentos e responde **ancorada nas fontes**, com citações verificáveis. Mesma engine
e identidade visual das trilhas de Claude; site **separado**.

Fio condutor: as **mesmas fontes fictícias da Aurora S.A.** usadas na trilha Claude V2
(release, transcrição de call, mercado, concorrentes) — dando continuidade: o executivo
joga os mesmos documentos no NotebookLM e vê a ferramenta sob outra ótica.

> O NotebookLM evolui rápido (Audio/Video Overview, limites, planos, política de dados).
> O conteúdo traz o aviso "confirme o vigente nas fontes oficiais", como nas outras trilhas.

## Como rodar

```bash
cd treinamento-notebooklm-executivo
python3 build.py          # site multipágina + materiais
python3 build_single.py   # → treinamento-aluno.html + treinamento-facilitador.html
python3 -m http.server 8092   # abra http://localhost:8092
```

## Módulos (13)

| # | Módulo | Ato |
|---|--------|-----|
| 00 | Abertura — por que o NotebookLM é diferente | I — Fundamentos |
| 01 | Conhecendo o NotebookLM | I |
| 02 | Fundamentos (ancoragem, "só sabe o que você deu") | I |
| 03 | Montar seu primeiro notebook | I |
| 04 | Perguntar com citações | II — O trabalho |
| 05 | Briefing, FAQ e linha do tempo (Notebook Guide) | II |
| 06 | **Audio Overview** (o "podcast" das fontes) | II |
| 07 | Mapa mental & descoberta *(aprof)* | II |
| 08 | Do notebook ao entregável | II |
| 09 | Base de conhecimento do time *(aprof)* | III — Ir além e governar |
| 10 | **NotebookLM × Claude** (quando usar cada um) | III |
| 11 | Riscos e governança | III |
| 12 | Plano 30-60-90 | III |

Mais as páginas **Dicas** (10 dicas próprias do NotebookLM) e **Referência** (apêndices).

## Fontes do caso Aurora (subir no notebook)

`Aurora_Release_Resultados.md`, `Aurora_Transcricao_Call.md`, `Aurora_Mercado.md`,
`Aurora_Concorrentes.md` — em `arquivos/`. Materiais gerados pelo `build.py`:
biblioteca de perguntas, guia de montagem de notebook e checklist de governança.

As demais trilhas (Claude Seguros e Claude Executivo V2) permanecem **intocadas**.
