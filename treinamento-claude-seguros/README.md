# Dominando o Claude — Programa Executivo (Seguro Garantia)

Versão interativa local do treinamento **"Dominando o Claude"** (caso fictício
Bastião Seguradora S.A.), no mesmo formato do curso `.md`: conteúdo dos slides +
exercícios mão na massa, com **botões Copiar**, **seções colapsáveis** (Debrief /
Bônus), **tooltips de glossário** (subscrição, sinistralidade, índice combinado,
MCP, Haiku/Sonnet/Opus, LGPD…), navegação e **acompanhamento de progresso**
(salvo no navegador).

Gerado a partir do guia do facilitador (`Guia_Treinamento_Claude_Seguros-2.docx`)
e dos slides (`Treinamento_Claude_Seguros_Slides.pptx`). Os arquivos de apoio do
caso (edital/tomador, condições gerais e a planilha da carteira) são
disponibilizados para download na página **Recursos**.

## Como rodar

```bash
cd treinamento-claude-seguros
python3 -m http.server 8090     # abra http://localhost:8090
```

> Use o servidor local (acima) em vez de `file://` para os downloads e os
> caminhos relativos funcionarem.

## Estrutura

```
treinamento-claude-seguros/
├── index.html              # home: objetivos + agenda em uma página
├── modulos/
│   ├── index.html          # os 10 módulos em 3 atos + barra de progresso
│   └── modulo-00..09.html   # um módulo por etapa do programa
├── recursos.html           # downloads (arquivos da Bastião + prompts + checklist)
├── referencia.html         # apêndices: caso, modelos, personalização, Skills, governança
├── arquivos/               # os arquivos para download
├── assets/styles.css       # tema editorial (Fraunces + Inter + JetBrains Mono; navy/ouro)
├── assets/app.js           # copiar, tooltips, progresso
└── build.py                # gera tudo a partir do conteúdo
```

## Mapa dos módulos (13 — núcleo + aprofundamentos)

| # | Módulo | Ato |
|---|--------|-----|
| 00 | Abertura — por que importa | I — Fundamentos |
| 01 | Conhecendo o Claude (o que é, faz, modelos) | I |
| 02 | Fundamentos sem jargão + Exercício 1 | I |
| 03 | O brief executivo + Exercício 2 | I |
| 04 | Casos de uso: ler, calcular, risco, precificar (4A–4D) | II — Mão na massa |
| 05 | **Data room & verificação** *(aprofundamento)* — dados complexos, cruzamento, pegar o erro | II |
| 06 | Construir algo de verdade (4 trilhas) | II |
| 07 | **Casos de uso executivos** *(aprofundamento)* — comitê, ranqueamento, reunião→ação, loop | II |
| 08 | **Projetos: o cérebro do time** *(aprofundamento)* — a estratégia de Projetos | III — Ir além e governar |
| 09 | Personalização e Skills (usar + construir + biblioteca) | III |
| 10 | Conexões (MCP) com o mcp-brasil | III |
| 11 | Riscos e governança | III |
| 12 | Plano 30-60-90 e fechamento | III |

O **núcleo** (módulos sem o selo *aprofundamento*) é a espinha dorsal; os aprofundamentos
estendem o programa.

## Dados do caso (data room)

A planilha rica e os documentos extras são gerados por `gen_dataroom.py`:

```bash
python3 gen_dataroom.py   # cria Bastiao_DataRoom.xlsx (8 abas, ~220 apólices) + docs + gabarito
python3 build.py          # gera o site (copia os materiais originais de ../junto)
```

- `Bastiao_DataRoom.xlsx` — 8 abas, **com erros e lacunas plantados** (para o exercício de verificação).
- `Bastiao_Editais_Comparacao.md`, `Bastiao_Balancos_Tomadores.md`, `Bastiao_Circular_Regulatoria.md` — para cruzamento/comparação/tradução.
- `Bastiao_Apolice_Escaneada.html` — apólice “escaneada” para o exercício de Visão (print/PDF).
- `Bastiao_Gabarito_Facilitador.md` — gabarito dos erros plantados (**só para o facilitador**).
- `biblioteca-de-skills.md` — 8 Skills por papel (geradas pelo `build.py`).

## Editar / regenerar

Conteúdo, glossário, módulos e apêndices vivem em `build.py`; os dados do caso em
`gen_dataroom.py`. As fontes vêm do Google Fonts (internet na 1ª carga).
