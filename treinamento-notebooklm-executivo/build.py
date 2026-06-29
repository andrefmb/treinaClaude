#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Construtor do treinamento "Dominando o NotebookLM · Executivo".
Caso fictício: Aurora S.A. (mesmas fontes da trilha Claude V2). Site separado.
Rode: python3 build.py && python3 build_single.py   Sirva: python3 -m http.server 8092
"""
import html as _html
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# GLOSSÁRIO (NotebookLM, executivo)
# ---------------------------------------------------------------------------
GLOSSARY = {
    "Fonte": "Um documento que você adiciona ao notebook — PDF, Google Doc/Slides/Sheets, texto colado, página web, vídeo do YouTube ou áudio. O NotebookLM só responde com base nas fontes que você deu.",
    "Notebook": "Um caderno: um conjunto de fontes sobre um tema, mais o chat e os resumos gerados a partir delas. Você pode ter vários — um por projeto, time ou decisão.",
    "Ancoragem": "O NotebookLM responde apoiado SÓ nas suas fontes (não na internet aberta) e mostra de onde tirou cada afirmação. Isso reduz muito a alucinação — mas ainda confira a citação.",
    "Citação": "O número clicável ao lado de cada frase da resposta: leva direto ao trecho da fonte que embasou aquilo. É o que torna a resposta verificável em segundos.",
    "Notebook Guide": "O painel que o NotebookLM gera automaticamente das suas fontes: resumo, perguntas frequentes, documento de briefing, linha do tempo e índice. (Nomes e formatos variam com o tempo.)",
    "Audio Overview": "Um resumo em áudio, no formato de conversa entre apresentadores de IA, gerado das suas fontes — para ouvir no trajeto. Dá para focar num tema, escolher o idioma e, em alguns casos, interagir.",
    "Video Overview": "Uma versão em vídeo do resumo (narração sobre slides gerados das suas fontes). Recurso mais recente — confirme disponibilidade.",
    "Mapa mental": "Uma visualização das ideias e conexões das suas fontes — bom para enxergar o todo e descobrir o que você não pensou em perguntar.",
    "Alucinação": "Quando uma IA afirma algo que soa perfeito e está errado. A ancoragem do NotebookLM reduz isso, mas não elimina — sempre confira a citação na fonte.",
    "LGPD": "Lei Geral de Proteção de Dados. Dados pessoais de clientes, colaboradores e terceiros só entram em ferramentas aprovadas e com base legal — vazamento é risco material e de board.",
    "NotebookLM Plus": "A versão paga/corporativa (via Google Workspace ou plano premium): mais fontes e áudios, compartilhamento e controles de administração. Confirme limites e disponibilidade atuais.",
    "Aurora": "Aurora S.A. (fictícia) — a empresa do caso: varejo de bens de consumo, lojas + e-commerce, receita ~R$ 4,2 bi, crescimento desacelerando e um concorrente digital ganhando share. As mesmas fontes da trilha Claude.",
    "Claude": "O assistente de IA da Anthropic — um agente que conversa, cria arquivos, conecta sistemas e automatiza. Complementar ao NotebookLM (ver o módulo de comparação).",
}


def g(term, label=None):
    label = label or term
    return ('<span class="term">' + _html.escape(label)
            + '<span class="tip"><strong>' + _html.escape(term) + '</strong>'
            + _html.escape(GLOSSARY[term]) + '</span></span>')


# ---------------------------------------------------------------------------
# Helpers (engine)
# ---------------------------------------------------------------------------
def H2(t): return "<h2>" + t + "</h2>"
def H3(t): return "<h3>" + t + "</h3>"
def P(t):  return "<p>" + t + "</p>"
def ic(t): return '<code class="inline">' + _html.escape(t) + "</code>"


def codeblock(text):
    return '<div class="codeblock"><pre>' + _html.escape(text.strip("\n")) + "</pre></div>"


def prompt(code, label="No NotebookLM, peça", note=None):
    out = '<div class="prompt-label">' + _html.escape(label)
    if note:
        out += ' <span style="color:var(--gold)">· ' + _html.escape(note) + "</span>"
    out += "</div>" + codeblock(code)
    return out


def details(summary, body, tag=None):
    tag_html = '<span class="tag">' + _html.escape(tag) + "</span>" if tag else ""
    return ('<details class="box"><summary>' + tag_html + " " + summary
            + '</summary><div class="box-body">' + body + "</div></details>")


def callout(body, label="Nota", kind=""):
    cls = "callout " + kind if kind else "callout"
    return ('<div class="' + cls + '"><span class="label">' + _html.escape(label)
            + "</span>" + body + "</div>")


def handson(title, head, body):
    return ('<div class="handson"><div class="ho-head">' + _html.escape(head) + "</div>"
            + "<h3>" + _html.escape(title) + "</h3>" + body + "</div>")


def stat(value, label):
    return '<div class="stat"><div class="v">' + value + '</div><div class="l">' + label + "</div></div>"


def table(headers, rows):
    out = '<table class="t"><thead><tr>'
    for h in headers:
        out += "<th>" + h + "</th>"
    out += "</tr></thead><tbody>"
    for r in rows:
        out += "<tr>" + "".join("<td>" + c + "</td>" for c in r) + "</tr>"
    return out + "</tbody></table>"


def fileref(fname, label=None):
    label = label or fname
    return ('<a class="filechip" data-file="' + fname + '" href="../arquivos/' + fname
            + '" download="' + fname + '">📎 ' + _html.escape(label)
            + ' <span class="dl">↓</span></a>')


def exfiles(files, label="Fontes deste exercício"):
    chips = "".join(fileref(f) for f in files)
    return ('<div class="exfiles"><span class="exfiles-label">' + _html.escape(label)
            + "</span>" + chips + "</div>")


# ---------------------------------------------------------------------------
# Shell
# ---------------------------------------------------------------------------
DISCLAIMER = (
    "Caso fictício Aurora S.A. — empresa e números são ilustrativos, criados apenas para o "
    "treinamento. Regra do dia: use fontes públicas ou fictícias; nunca suba dados pessoais "
    "(LGPD) ou confidenciais em ferramentas que a empresa ainda não aprovou."
)
DISCLAIMER2 = (
    "O NotebookLM evolui rápido (fontes aceitas, Audio/Video Overview, limites, planos, "
    "política de dados). Antes de aplicar, confirme o que está vigente nas fontes oficiais do "
    "Google e na política interna de IA e LGPD da sua organização (ver Referência)."
)


def nav(active, depth=0):
    up = "../" if depth else ""
    def cls(name): return ' class="active"' if active == name else ""
    return (
        '<header class="topbar">'
        '<a class="brand" href="' + up + 'index.html">'
        '<span class="mark">Dominando o NotebookLM</span></a>'
        '<nav class="topnav">'
        '<a href="' + up + 'modulos/index.html"' + cls("modulos") + '>Módulos</a>'
        '<a href="' + up + 'dicas.html"' + cls("dicas") + '>Dicas</a>'
        '<a href="' + up + 'recursos.html"' + cls("recursos") + '>Recursos</a>'
        '<a href="' + up + 'referencia.html"' + cls("referencia") + '>Referência</a>'
        "</nav></header>"
    )


def footer(depth=0):
    up = "../" if depth else ""
    return (
        '<footer><div class="wrap">'
        '<p>' + DISCLAIMER + "</p><p>" + DISCLAIMER2 + "</p>"
        '<div class="flinks">'
        '<a href="' + up + 'index.html">Início</a>'
        '<a href="' + up + 'modulos/index.html">Módulos</a>'
        '<a href="' + up + 'dicas.html">Dicas</a>'
        '<a href="' + up + 'recursos.html">Recursos</a>'
        '<a href="' + up + 'referencia.html">Referência</a>'
        "</div>"
        '<p style="font-size:0.8rem">Programa hands-on · liderança · NotebookLM · '
        "todos os dados do caso são fictícios.</p>"
        "</div></footer>"
    )


def page(title, body, active="", depth=0):
    up = "../" if depth else ""
    return (
        "<!DOCTYPE html>\n"
        '<html lang="pt-BR"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        "<title>" + _html.escape(title) + " · Dominando o NotebookLM</title>"
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?'
        "family=Fraunces:ital,opsz,wght@0,9..144,400..700;1,9..144,400..600&"
        "family=Inter:wght@300..700&family=JetBrains+Mono:wght@400..700&display=swap"
        '" rel="stylesheet">'
        '<link rel="stylesheet" href="' + up + 'assets/styles.css">'
        "</head><body>"
        + nav(active, depth)
        + '<main><div class="wrap">' + body + "</div></main>"
        + footer(depth)
        + '<script src="' + up + 'assets/app.js"></script>'
        "</body></html>"
    )


print("engine + shell definidos.")

AURORA_SOURCES = ["Aurora_Release_Resultados.md", "Aurora_Transcricao_Call.md",
                  "Aurora_Mercado.md", "Aurora_Concorrentes.md"]


# ---------------------------------------------------------------------------
# Módulos
# ---------------------------------------------------------------------------
def m00():
    b = []
    b.append(P("Objetivo: entender por que o NotebookLM é uma ferramenta diferente — e por "
               "que isso importa para quem decide com base em muito documento."))
    b.append(H2("Um analista que só lê o que VOCÊ deu"))
    b.append(P("Um chatbot genérico responde a partir de tudo o que viu na internet — e às "
               "vezes inventa. O <strong>NotebookLM</strong> é o oposto: ele responde "
               "<strong>ancorado nas fontes que você sobe</strong> (seus relatórios, "
               "contratos, transcrições) e mostra <strong>de onde tirou cada frase</strong>. "
               "É um analista que leu a sua pilha de documentos — e cita a página."))
    b.append(callout("Para um executivo, isso resolve duas dores de uma vez: <strong>ler "
                     "rápido</strong> uma montanha de material e <strong>confiar mais</strong> "
                     "na resposta, porque cada afirmação vem com a citação para conferir.",
                     label="A ideia central", kind="gold"))
    b.append(H2("O caso de hoje: a Aurora S.A."))
    b.append(P("Vamos usar as mesmas fontes <strong>fictícias</strong> da " + g("Aurora", "Aurora S.A.")
               + " — uma varejista de bens de consumo com crescimento desacelerando e um "
               "concorrente digital ganhando share. Você vai jogar o release, a transcrição "
               "da call, o panorama de mercado e os concorrentes num " + g("Notebook", "notebook")
               + " e fazer o NotebookLM ler tudo por você."))
    b.append(callout("“Não estou aprendendo uma ferramenta. Estou aprendendo a ler uma pilha "
                     "de documentos em minutos — e a confiar na resposta porque ela vem "
                     "citada.”", label="Frase para fixar", kind="gold"))
    return "".join(b)


def m01():
    b = []
    b.append(P("O que é, o que aceita e como difere de um chatbot comum."))
    b.append(H2("O que é o NotebookLM"))
    b.append(P("É uma ferramenta do Google para <strong>pesquisar e raciocinar sobre as suas "
               "próprias fontes</strong>. Você cria um " + g("Notebook", "notebook") + ", "
               "adiciona documentos e passa a conversar com eles: perguntar, resumir, comparar "
               "— sempre com " + g("Citação", "citações") + " que apontam para o trecho de origem."))
    b.append(H2("O que serve de fonte"))
    b.append(table(["Tipo de fonte", "Exemplos"],
                   [["Documentos", "PDF, Google Docs e Slides, texto, Markdown."],
                    ["Planilhas", "Google Sheets / tabelas (suporte varia — confirme o vigente)."],
                    ["Web e vídeo", "Páginas web e vídeos do YouTube (pela URL)."],
                    ["Áudio e texto colado", "Gravações e trechos que você cola direto."]]))
    b.append(callout("Há um limite de fontes por notebook (e de tamanho por fonte), que varia "
                     "entre o plano gratuito e o " + g("NotebookLM Plus") + ". Confirme os "
                     "números atuais — eles mudam.", label="Limites"))
    b.append(H2("Como difere de um chatbot comum"))
    b.append(table(["Chatbot genérico", "NotebookLM"],
                   [["Responde do conhecimento geral da internet", "Responde só das fontes que você deu"],
                    ["Pode inventar e raramente cita", "Mostra a citação para cada afirmação"],
                    ["Ótimo para criar e conversar amplo", "Ótimo para entender um corpo de documentos com confiança"]]))
    return "".join(b)


def m02():
    b = []
    b.append(P("Três verdades que mudam o jeito de usar."))
    b.append(P("<strong>1. Ele é " + g("Ancoragem", "ancorado nas suas fontes") + ".</strong> "
               "Não busca na internet aberta: responde do que você subiu — e cita. Por isso é "
               "confiável para “o que os <em>meus</em> documentos dizem”."))
    b.append(P("<strong>2. Ele só sabe o que você deu.</strong> Faltou uma fonte, faltou a "
               "resposta. Se você perguntar algo que não está nas fontes, ele costuma dizer "
               "que não encontrou — e isso é uma <em>qualidade</em>."))
    b.append(P("<strong>3. Lixo entra, lixo sai.</strong> A resposta é tão boa quanto as "
               "fontes. Curar boas fontes é metade do trabalho. E mesmo com citação, "
               "<strong>confira</strong> — a " + g("Alucinação", "alucinação") + " é rara aqui, "
               "mas não é zero."))
    b.append(handson("Exercício — pergunte o que NÃO está nas fontes", "Mão na massa",
                     P("Depois de montar o notebook (próximo módulo), faça um teste de "
                       "confiança:")
                     + prompt("Qual foi o faturamento da Aurora no primeiro trimestre de 2026?")
                     + details("Reflexão",
                               P("As suas fontes vão só até 2025 — o NotebookLM deve dizer que "
                                 "<strong>não encontrou isso nas fontes</strong>, em vez de "
                                 "inventar. Esse “não sei” é exatamente o comportamento que "
                                 "você quer numa ferramenta de decisão."), tag="Reflexão")))
    return "".join(b)


def m03():
    b = []
    b.append(P("Mãos à obra: criar um notebook e dar a ele a pilha de documentos da Aurora."))
    b.append(H2("Passo a passo"))
    b.append(table(["#", "Passo"],
                   [["1", "Abra o NotebookLM e crie um novo notebook (ex.: “Aurora — resultados 2025”)."],
                    ["2", "Clique em “Adicionar fontes” e suba os arquivos abaixo (ou cole o texto)."],
                    ["3", "Espere o NotebookLM ler — ele já gera um resumo inicial e sugestões."],
                    ["4", "Pronto: agora você conversa com as fontes."]]))
    b.append(exfiles(AURORA_SOURCES, label="Suba estas fontes"))
    b.append(callout("Dê um nome claro ao notebook e mantenha-o focado num tema. Um notebook "
                     "com fontes demais e desconexas responde pior — prefira vários cadernos "
                     "bem curados.", label="Dica de curadoria", kind="tip"))
    b.append(details("Reflexão",
                     P("Repare que você não “treinou” nada — só deu os documentos certos. O "
                       "trabalho de valor aqui é a <strong>curadoria</strong>: quais fontes "
                       "entram. Pergunte-se quais documentos você relê toda semana que "
                       "mereciam virar um notebook."), tag="Reflexão"))
    return "".join(b)


def m04():
    b = []
    b.append(P("O coração do NotebookLM: perguntar e receber respostas <strong>com " + g("Citação", "citação")
               + "</strong> — verificáveis em um clique."))
    b.append(H2("Perguntas que valem a reunião"))
    b.append(prompt("Resuma a situação da Aurora em 5 pontos para quem não leu nada — receita,\n"
                    "margem, digital, concorrência e a decisão em pauta."))
    b.append(prompt("O que a CEO disse sobre entrar no marketplace? Cite a fonte."))
    b.append(prompt("Onde o release e a transcrição da call divergem ou se reforçam?"))
    b.append(callout("Toda resposta vem com números clicáveis: clique e vá ao trecho exato da "
                     "fonte. <strong>Confira a citação</strong> antes de levar adiante — é "
                     "rápido e é o que torna a resposta confiável.", label="Confie, mas confira", kind="warn"))
    b.append(details("Reflexão",
                     P("Repare a diferença para um chatbot comum: aqui você <em>vê</em> de "
                       "onde veio cada afirmação. Em vez de “será que é verdade?”, você "
                       "pergunta “de qual fonte?” — e a resposta está a um clique."), tag="Reflexão"))
    return "".join(b)


def m05():
    b = []
    b.append(P("O NotebookLM gera, sozinho, vários materiais a partir das suas fontes — o "
               + g("Notebook Guide", "Notebook Guide") + " (ou painel de Estúdio)."))
    b.append(table(["Material", "Para que serve ao executivo"],
                   [["Resumo / Briefing", "Uma página com o essencial das fontes — pronta para a reunião."],
                    ["Perguntas frequentes (FAQ)", "Antecipa o que vão te perguntar no comitê."],
                    ["Linha do tempo", "Ordena os fatos — útil em casos, investigações, históricos."],
                    ["Índice / guia de estudo", "Mapa do conteúdo para navegar rápido."]]))
    b.append(H2("Gere e refine"))
    b.append(prompt("Gere um documento de briefing das fontes da Aurora para o board, com os\n"
                    "3 maiores riscos e a decisão em pauta."))
    b.append(prompt("Liste as 8 perguntas mais difíceis que o board pode fazer sobre estes\n"
                    "resultados — e a resposta ancorada nas fontes, com citação.",
                    label="No NotebookLM, peça", note="prep de comitê"))
    b.append(details("Reflexão",
                     P("Você acabou de transformar uma pilha de documentos em um briefing e um "
                       "Q&A de comitê — em minutos, e tudo rastreável às fontes. Esse é o "
                       "ganho diário do NotebookLM."), tag="Reflexão"))
    return "".join(b)


def m06():
    b = []
    b.append(P("O recurso que encanta: o <strong>" + g("Audio Overview", "Audio Overview")
               + "</strong> — um “podcast” gerado das suas fontes, com dois apresentadores de "
               "IA conversando sobre o conteúdo. Para ouvir no carro, na esteira, entre reuniões."))
    b.append(H2("Gere o áudio das fontes da Aurora"))
    b.append(table(["#", "Passo"],
                   [["1", "No notebook, abra o Audio Overview (painel de Estúdio) e gere."],
                    ["2", "Personalize: foque num tema (ex.: “foque na ameaça competitiva”)."],
                    ["3", "Escolha o idioma; baixe para ouvir offline; em alguns casos, entre na conversa e pergunte."]]))
    b.append(prompt("Gere um Audio Overview das fontes da Aurora focado em: o que muda na\n"
                    "estratégia digital e quais decisões o board precisa tomar. Tom executivo,\n"
                    "~10 minutos.", label="Ao personalizar o áudio, peça"))
    b.append(callout("Há também o " + g("Video Overview", "Video Overview") + " (narração sobre "
                     "slides) — recurso mais recente. Confirme a disponibilidade no seu plano.",
                     label="Também existe"))
    b.append(details("Reflexão",
                     P("Pense no seu tempo “morto” — trajetos, espera, exercício. Um briefing "
                       "que você <em>ouve</em> transforma esse tempo em preparação. Qual "
                       "leitura da sua semana você ouviria no caminho?"), tag="Reflexão"))
    return "".join(b)


def m07():
    b = []
    b.append(P("O <strong>" + g("Mapa mental", "mapa mental") + "</strong> mostra as ideias e "
               "conexões das suas fontes de forma visual — bom para enxergar o todo e "
               "<strong>descobrir o que você não pensou em perguntar</strong>."))
    b.append(H2("Explore visualmente"))
    b.append(P("Gere o mapa mental do notebook da Aurora e navegue pelos ramos (resultados, "
               "mercado, concorrência, decisão). Clique num ramo para aprofundar — o "
               "NotebookLM puxa o trecho da fonte correspondente."))
    b.append(prompt("A partir do mapa, o que conecta a queda de margem à estratégia digital?\n"
                    "Mostre o caminho entre os temas, com citações."))
    b.append(details("Reflexão",
                     P("O valor aqui é o <strong>inesperado</strong>: um mapa revela ligações "
                       "que uma lista de perguntas não revelaria. Use-o no início de um tema "
                       "novo, para mapear o terreno antes de mergulhar."), tag="Reflexão"))
    return "".join(b)


def m08():
    b = []
    b.append(P("Fechar o ciclo: tirar do notebook um <strong>entregável</strong> e levá-lo "
               "para onde a decisão acontece."))
    b.append(H2("Do notebook ao memo"))
    b.append(prompt("Com base nas fontes, escreva um memo de 1 página ao board: situação,\n"
                    "3 opções para o digital com prós/contras, recomendação e riscos.\n"
                    "Mantenha as citações para eu conferir."))
    b.append(H2("E daí para o seu fluxo"))
    b.append(P("Copie o briefing/respostas (com as citações conferidas) e leve para onde você "
               "produz o resultado final — por exemplo, peça ao " + g("Claude") + " para "
               "transformar o briefing num <strong>deck para o board</strong> ou numa carta. "
               "O NotebookLM entende as fontes; o Claude monta o entregável e automatiza."))
    b.append(callout("Regra de ouro ao exportar: leve adiante <strong>só o que você conferiu "
                     "na citação</strong>. O grounding ajuda, mas a responsabilidade pela "
                     "verdade continua sua.", label="Antes de exportar", kind="warn"))
    b.append(details("Reflexão",
                     P("Repare no encadeamento: NotebookLM para <em>entender com confiança</em> "
                       "→ Claude para <em>produzir e automatizar</em>. Ferramentas diferentes, "
                       "fluxo único."), tag="Reflexão"))
    return "".join(b)


def m09():
    b = []
    b.append(P("Um notebook não precisa ser só seu. Compartilhado, ele vira a <strong>base de "
               "conhecimento do time</strong> — todos perguntam às mesmas fontes e recebem "
               "respostas citadas."))
    b.append(H2("A estratégia: um notebook por tema recorrente"))
    b.append(table(["Notebook", "Quem usa", "Ganho"],
                   [["“Resultados & mercado”", "Diretoria", "Todos consultam os mesmos números, com citação."],
                    ["“Onboarding da área”", "Novos no time", "Perguntam às políticas e materiais, sem incomodar ninguém."],
                    ["“Due diligence — alvo X”", "M&A / estratégia", "Toda a papelada num lugar, perguntável e rastreável."],
                    ["“Base regulatória”", "Jurídico / compliance", "As normas viram um FAQ vivo, citado."]]))
    b.append(callout("Compartilhar um notebook concede acesso às fontes dentro dele. Defina "
                     "quem pode ver/editar, use só fontes aprovadas e revise o acesso — "
                     "governança vale também aqui (ver módulo de riscos).", label="Governança", kind="warn"))
    b.append(details("Reflexão",
                     P("Pense numa pergunta que o seu time faz repetidamente (“qual é a nossa "
                       "política de X?”, “o que dizem os últimos resultados?”). Essa é a "
                       "primeira candidata a virar um notebook compartilhado."), tag="Reflexão"))
    return "".join(b)


def m10():
    b = []
    b.append(P("NotebookLM e " + g("Claude") + " não competem — se complementam. Saber quando "
               "usar cada um é meio caminho."))
    b.append(table(["Use o NotebookLM quando…", "Use o Claude quando…"],
                   [["Quer entender um corpo de fontes fixo, com citações", "Quer criar um entregável (deck, planilha, memo) ou automatizar"],
                    ["Confiança e rastreabilidade são o ponto", "Precisa de um agente que conecta sistemas e executa tarefas"],
                    ["Quer um briefing ou um áudio das suas fontes", "Quer iterar, gerar opções e produzir o resultado final"],
                    ["O material é uma pilha de relatórios/transcrições", "O trabalho é construir, conectar e publicar"]]))
    b.append(callout("O fluxo campeão para o executivo: <strong>NotebookLM</strong> para "
                     "<em>entender com confiança</em> a pilha de documentos → leva o briefing "
                     "conferido para o <strong>Claude</strong>, que <em>produz e automatiza</em> "
                     "o entregável.", label="O combo", kind="gold"))
    return "".join(b)


def m11():
    b = []
    b.append(P("O grounding reduz a alucinação, mas governança continua sendo papel da "
               "liderança."))
    b.append(H2("Verificar mesmo com citação"))
    b.append(P("O NotebookLM cita — mas uma citação pode embasar mal uma conclusão. Antes de "
               "usar um número externamente, <strong>abra a citação e confira</strong>. A "
               "responsabilidade pela verdade continua sua."))
    b.append(H2("Dados e LGPD"))
    b.append(table(["Nível", "O que é"],
                   [["✅ Seguro", "Fontes públicas, dados fictícios, documentos internos não sensíveis aprovados."],
                    ["⚠️ Cautela / aprovação", "Dados de clientes/colaboradores, financeiros não públicos, contratos sigilosos."],
                    ["⛔ Risco material", "Qualquer dado pessoal ou confidencial num ambiente não aprovado."]]))
    b.append(callout("Em ambiente corporativo, use a versão aprovada (via Google Workspace / "
                     + g("NotebookLM Plus") + "), que traz controles de dados e administração. "
                     "Confirme a política de uso de dados vigente — ela muda, e é tema de "
                     "board.", label="Versão corporativa", kind="warn"))
    b.append(H2("Compartilhamento"))
    b.append(P("Compartilhar um notebook = compartilhar as fontes dentro dele. Conceda o mínimo "
               "necessário, prefira leitura e revise acessos periodicamente."))
    return "".join(b)


def m12():
    b = []
    b.append(P("Saia daqui com três compromissos concretos."))
    b.append(table(["Horizonte", "Compromisso", "Exemplo"],
                   [["Esta semana", "1 pilha de leitura para virar notebook", "Os relatórios da semana antes do comitê."],
                    ["Este mês", "1 notebook compartilhado com o time", "“Resultados & mercado” ou “Onboarding da área”."],
                    ["Este trimestre", "1 hábito novo", "Ouvir o Audio Overview das leituras no trajeto; política de dados definida."]]))
    b.append(callout("NotebookLM para entender com confiança; Claude para produzir e "
                     "automatizar. Junte os dois e a leitura deixa de ser gargalo.",
                     label="Encerramento", kind="gold"))
    b.append(P("Leve a <a href='../recursos.html'>biblioteca de perguntas</a> e o "
               "<a href='../referencia.html'>checklist de governança</a>."))
    return "".join(b)


print("módulos definidos.")

# ---------------------------------------------------------------------------
# Metadados
# ---------------------------------------------------------------------------
MODULES = [
    ("00", "I",   "Abertura", "Por que o NotebookLM é diferente", m00, False),
    ("01", "I",   "Conhecendo o NotebookLM", "O que é, o que aceita como fonte", m01, False),
    ("02", "I",   "Fundamentos sem jargão", "As três verdades que mudam o uso", m02, False),
    ("03", "I",   "Montar seu primeiro notebook", "Criar o caderno e adicionar fontes", m03, False),
    ("04", "II",  "Perguntar com citações", "Respostas ancoradas e verificáveis", m04, False),
    ("05", "II",  "Briefing, FAQ e linha do tempo", "O Notebook Guide gerado das fontes", m05, False),
    ("06", "II",  "Audio Overview", "O “podcast” das suas fontes", m06, False),
    ("07", "II",  "Mapa mental & descoberta", "Enxergar o todo e o que faltou perguntar", m07, True),
    ("08", "II",  "Do notebook ao entregável", "Tirar um memo e levar ao seu fluxo", m08, False),
    ("09", "III", "Base de conhecimento do time", "Notebooks compartilhados", m09, True),
    ("10", "III", "NotebookLM × Claude", "Quando usar cada um", m10, False),
    ("11", "III", "Riscos e governança", "Dados, LGPD, verificação e compartilhamento", m11, False),
    ("12", "III", "Plano 30-60-90 e fechamento", "Sair daqui com compromissos", m12, False),
]
ACT_NAME = {"I": "Ato I — Fundamentos", "II": "Ato II — O trabalho com o NotebookLM",
            "III": "Ato III — Ir além e governar"}
ACT_SUB = {"I": "o que é, por que importa e como montar",
           "II": "perguntar, resumir, ouvir e produzir — com a Aurora",
           "III": "time, comparação com o Claude e governança"}


def slug(mid): return "modulo-" + mid


def build_module(i):
    mid, act, title, subtitle, fn, deep = MODULES[i]
    prev = MODULES[i - 1] if i > 0 else None
    nxt = MODULES[i + 1] if i < len(MODULES) - 1 else None
    deep_pill = " · Aprofundamento" if deep else ""
    head = (
        '<a class="breadcrumb" href="index.html">← Todos os módulos</a>'
        '<div class="meta-pill">' + ACT_NAME[act].split(" —")[0] + " · Módulo " + mid + deep_pill + "</div>"
        '<div class="mod-number">' + mid + "</div>"
        "<h1>" + _html.escape(title) + "</h1>"
        '<p class="subtitle">' + _html.escape(subtitle) + "</p>"
    )
    done = ('<div class="done-bar" data-done-bar><span class="grow">Terminou este módulo? '
            'Marque para acompanhar seu progresso.</span>'
            '<button class="btn" data-done-btn data-mod="' + mid
            + '" type="button">Marcar como concluído</button></div>')
    pn = '<div class="prevnext">'
    if prev:
        pn += ('<a href="' + slug(prev[0]) + '.html"><div class="dir">← Anterior</div><div>'
               + prev[0] + " · " + _html.escape(prev[2]) + "</div></a>")
    else:
        pn += '<a href="index.html"><div class="dir">← Início</div><div>Todos os módulos</div></a>'
    if nxt:
        pn += ('<a class="nx" href="' + slug(nxt[0]) + '.html"><div class="dir">Próximo →</div><div>'
               + nxt[0] + " · " + _html.escape(nxt[2]) + "</div></a>")
    else:
        pn += ('<a class="nx" href="../recursos.html"><div class="dir">Fim →</div>'
               "<div>Recursos para levar</div></a>")
    pn += "</div>"
    return page("Módulo " + mid + " · " + title, head + fn() + done + pn, active="modulos", depth=1)


def build_list():
    total = len(MODULES)
    b = ['<h1>O programa</h1>'
         '<p class="lede">Treze módulos em três atos. O <strong>núcleo</strong> é a espinha '
         'dorsal (~60% mão na massa); os marcados como <strong>Aprofundamento</strong> são '
         'opcionais. Fio condutor: as fontes da empresa fictícia <strong>Aurora S.A.</strong></p>']
    b.append('<div class="progress-bar"><span data-progress-fill></span></div>'
             '<p class="progress-text" data-progress-text>0 de ' + str(total) + ' módulos concluídos</p>')
    b.append('<div data-mod-list>')
    last = None
    for mid, act, title, subtitle, fn, deep in MODULES:
        if act != last:
            if last is not None:
                b.append("</ul>")
            b.append('<div class="act-head"><h2>' + ACT_NAME[act] + "</h2>"
                     '<div class="act-sub">' + ACT_SUB[act] + "</div></div>")
            b.append('<ul class="mod-list">')
            last = act
        badge = (' <span style="font-family:var(--font-mono);font-size:.62rem;text-transform:'
                 'uppercase;letter-spacing:.06em;color:var(--gold);border:1px solid var(--gold);'
                 'border-radius:5px;padding:1px 6px;vertical-align:middle">Aprofundamento</span>'
                 ) if deep else ''
        b.append('<a class="mod-row" data-mod-row="' + mid + '" href="' + slug(mid) + '.html">'
                 '<span class="check">✓</span><span class="num">' + mid + "</span>"
                 '<span class="body"><span class="title">' + _html.escape(title) + badge + "</span><br>"
                 '<span class="desc">' + _html.escape(subtitle) + "</span></span></a>")
    b.append("</ul></div>")
    return page("Módulos", "".join(b), active="modulos", depth=1)


def build_home():
    agenda = '<ul class="agenda">'
    for mid, act, title, subtitle, fn, deep in MODULES:
        tag = (' <span style="font-family:var(--font-mono);font-size:.6rem;text-transform:'
               'uppercase;letter-spacing:.05em;color:var(--gold)">· aprof.</span>') if deep else ''
        agenda += ('<li><span class="ag-num">' + mid + '</span><span class="ag-t">'
                   + _html.escape(title) + tag + "</span></li>")
    agenda += "</ul>"
    body = (
        '<div class="hero">'
        '<div class="kicker">Programa Executivo</div>'
        "<h1>Dominando o <span class='accent'>NotebookLM</span></h1>"
        '<p class="lede">A ferramenta do Google que lê a SUA pilha de documentos e responde '
        "<strong>ancorada nas fontes</strong>, com citações verificáveis. Para o executivo: "
        "digerir relatórios em minutos, gerar briefings, ouvir um “podcast” das suas leituras "
        "e confiar mais na resposta. Fio condutor: as fontes da <strong>Aurora S.A.</strong> "
        "(as mesmas da trilha de Claude).</p>"
        '<div class="hero-actions">'
        '<a class="btn" href="modulos/index.html">Começar pelo Módulo 00 →</a>'
        '<a class="btn ghost" href="dicas.html">Ver as dicas</a></div></div>'
        + callout("Use fontes públicas ou fictícias. Nunca suba dados pessoais (LGPD) ou "
                  "confidenciais em ferramentas que a empresa ainda não aprovou.",
                  label="A regra de hoje", kind="warn")
        + H2("O que você será capaz de fazer")
        + table(["Ao final, cada participante consegue…", ""],
                [["Montar um notebook das suas fontes", "relatórios, transcrições, web, áudio."],
                 ["Perguntar com citações", "respostas ancoradas e verificáveis em um clique."],
                 ["Gerar briefings, FAQ e linha do tempo", "o essencial das fontes, pronto para a reunião."],
                 ["Criar um Audio Overview", "ouvir um resumo das fontes no trajeto."],
                 ["Compartilhar como base do time", "todos perguntam às mesmas fontes."],
                 ["Combinar com o Claude e governar o uso", "entender → produzir; com cuidado de LGPD."]])
        + H2("A jornada")
        + agenda
        + P("<span style='color:var(--muted)'>O núcleo (módulos sem o selo "
            "<em>aprofundamento</em>) é a espinha dorsal; os aprofundamentos estendem o "
            "programa.</span>")
    )
    return page("Início", body, active="", depth=0)


# ---------------------------------------------------------------------------
# Dicas (próprias do NotebookLM)
# ---------------------------------------------------------------------------
TIPS = [
    ("Cure boas fontes.", "A resposta é tão boa quanto as fontes — escolha bem o que entra."),
    ("Um notebook por tema.", "Não misture assuntos: cadernos focados respondem melhor."),
    ("Pergunte e clique na citação.", "Sempre confira o trecho de origem antes de usar."),
    ("Use o Notebook Guide.", "Briefing, FAQ e linha do tempo já vêm prontos — comece por eles."),
    ("Gere um Audio Overview.", "Ouça um resumo das suas fontes no trajeto; personalize o foco."),
    ("Pergunte o que falta.", "“Onde as fontes divergem?”, “o que está faltando aqui?”."),
    ("Comece pelo mapa mental em tema novo.", "Veja o todo antes de mergulhar nas perguntas."),
    ("“Não encontrei” é qualidade.", "Se faltou resposta, falta uma fonte — adicione-a."),
    ("Compartilhe para virar base do time.", "Um notebook por decisão recorrente, com acesso controlado."),
    ("Leve o briefing conferido ao Claude.", "NotebookLM entende; Claude produz e automatiza."),
]


def render_tips():
    out = '<ol class="tips">'
    for title, sub in TIPS:
        out += ('<li><span class="tip-t">' + _html.escape(title) + "</span>"
                '<span class="tip-s">' + _html.escape(sub) + "</span></li>")
    return out + "</ol>"


def dicas_body(depth=1):
    b = ['<h1>Como tirar o máximo do NotebookLM</h1>',
         '<p class="lede">Uma colinha de princípios. Vale para qualquer notebook — volte aqui '
         "sempre que precisar.</p>",
         render_tips(),
         callout("Cure boas fontes, pergunte com citação e confira, use o Guide e o áudio, e "
                 "leve o briefing conferido para onde a decisão acontece.",
                 label="Resumo em uma frase", kind="gold"),
         H2("Onde isto aparece no curso"),
         table(["Dica", "Onde praticar"],
               [["Cure fontes · um notebook por tema (1, 2)", "Módulo 03 — montar o notebook"],
                ["Pergunte e confira a citação (3, 6)", "Módulo 04 — perguntar com citações"],
                ["Notebook Guide e Audio (4, 5)", "Módulos 05 e 06"],
                ["Mapa mental · “não encontrei” (7, 8)", "Módulos 07 e 02"],
                ["Compartilhe · leve ao Claude (9, 10)", "Módulos 09, 08 e 10"]])]
    return "".join(b)


def build_dicas():
    return page("Dicas", dicas_body(depth=1), active="dicas", depth=0)


# ---------------------------------------------------------------------------
# Arquivos
# ---------------------------------------------------------------------------
DATAROOM_FILES = [
    ("Aurora_Release_Resultados.md", "Release de resultados da Aurora. Fonte principal."),
    ("Aurora_Transcricao_Call.md", "Transcrição da teleconferência — ótima para perguntas e áudio."),
    ("Aurora_Mercado.md", "Panorama de mercado. Fonte de contexto."),
    ("Aurora_Concorrentes.md", "Perfis dos concorrentes. Fonte de contexto."),
]
GEN_FILES = [
    ("biblioteca-de-perguntas.md", "Perguntas prontas para fazer a um notebook executivo."),
    ("guia-montar-notebook.md", "Passo a passo para montar um bom notebook."),
    ("checklist-governanca-notebooklm.md", "Checklist de governança para uso do NotebookLM."),
]
FAC_FILES = []


def _file_rows(files):
    out = ""
    for fname, desc in files:
        out += ('<div class="file-row"><span class="fname">' + _html.escape(fname) + "</span>"
                '<span class="fdesc">' + _html.escape(desc) + "</span>"
                '<a class="btn ghost dl" href="arquivos/' + fname + '" download>Baixar ↓</a></div>')
    return out


def build_recursos():
    b = ['<h1>Recursos para levar</h1>'
         '<p class="lede">As fontes do caso Aurora (para subir no seu notebook) e os '
         "materiais do programa.</p>"]
    b.append(H2("Fontes do caso Aurora (suba no notebook)"))
    b.append(_file_rows(DATAROOM_FILES))
    b.append(H2("Materiais do programa"))
    b.append(_file_rows(GEN_FILES))
    return page("Recursos", "".join(b), active="recursos", depth=0)


# ---------------------------------------------------------------------------
# Materiais gerados
# ---------------------------------------------------------------------------
RES_PERGUNTAS = """# Biblioteca de perguntas para um notebook executivo

Cole e adapte. Funcionam melhor quando as fontes certas estão no notebook.

## Entender rápido
- Resuma em 5 pontos para quem não leu nada.
- Quais são os 3 maiores riscos nestas fontes? Cite cada um.
- Faça uma linha do tempo dos fatos.

## Cruzar e checar
- Onde as fontes divergem ou se contradizem?
- O que [pessoa/área] disse sobre [tema]? Cite a fonte.
- O que está faltando aqui para eu decidir com segurança?

## Preparar uma reunião
- Liste as 8 perguntas mais difíceis que o board pode fazer — e a resposta ancorada.
- Gere um documento de briefing de 1 página para o comitê.

## Para ouvir
- Gere um Audio Overview focado em [tema], tom executivo, ~10 min.

> Sempre clique na citação e confira antes de levar adiante.
"""

RES_GUIA = """# Como montar um bom notebook (passo a passo)

1. **Defina o tema** do notebook — um por decisão/assunto (ex.: "Resultados & mercado").
2. **Cure as fontes**: suba só o que é relevante e confiável. Menos e melhor > muito e disperso.
   - Aceita: PDF, Google Docs/Slides, texto, Markdown, web (URL), YouTube, áudio (confirme o vigente).
3. **Deixe o NotebookLM ler** — ele gera um resumo e sugestões iniciais.
4. **Comece pelo Notebook Guide** (resumo, FAQ, linha do tempo) antes de perguntar à toa.
5. **Pergunte e confira a citação** — toda afirmação tem origem clicável.
6. **Gere um Audio Overview** para ouvir o essencial no trajeto.
7. **Compartilhe** (se for do time) com acesso controlado.
8. **Exporte o que conferiu** e leve para onde produz o entregável (ex.: Claude).

Dica: notebooks focados respondem melhor. Se um tema cresceu demais, divida em dois.
"""

RES_CHECKLIST = """# Checklist de governança — NotebookLM

## Dados e LGPD
- [ ] Só subimos fontes aprovadas? Nada de dado pessoal ou confidencial sem base legal.
- [ ] Em ambiente corporativo, usamos a versão aprovada (Workspace / NotebookLM Plus)?
- [ ] Conhecemos a política de uso de dados vigente do produto?

## Verificação
- [ ] Toda afirmação levada adiante teve a citação conferida na fonte?
- [ ] Tratamos a saída como insumo, não como verdade final?

## Compartilhamento
- [ ] Quem compartilha um notebook sabe que compartilha as fontes dentro dele?
- [ ] Acesso concedido é o mínimo necessário (preferência por leitura)?
- [ ] Há revisão periódica de quem tem acesso a quê?

## Valor
- [ ] Há notebooks "vivos" por tema recorrente (resultados, onboarding, due diligence)?
- [ ] Medimos o tempo economizado e a qualidade das decisões apoiadas?
"""


def write_resources():
    d = os.path.join(ROOT, "arquivos")
    os.makedirs(d, exist_ok=True)
    gen = {
        "biblioteca-de-perguntas.md": RES_PERGUNTAS,
        "guia-montar-notebook.md": RES_GUIA,
        "checklist-governanca-notebooklm.md": RES_CHECKLIST,
    }
    for name, content in gen.items():
        with open(os.path.join(d, name), "w", encoding="utf-8") as f:
            f.write(content)
    missing = [f for f, _ in DATAROOM_FILES if not os.path.exists(os.path.join(d, f))]
    if missing:
        print("  AVISO: faltam fontes:", ", ".join(missing))
    return list(gen)


def build_referencia():
    b = ['<h1>Referência</h1>',
         '<p class="lede">Apêndices: o caso Aurora, os tipos de fonte, NotebookLM × Claude, '
         "governança e onde confirmar o que está vigente.</p>"]
    b.append(details("Apêndice A — O caso Aurora S.A.",
                     P("Empresa e números <strong>fictícios</strong>. " + g("Aurora", "Aurora S.A.")
                       + ": varejo de bens de consumo, lojas + e-commerce, receita ~R$ 4,1 bi, "
                       "crescimento desacelerando, margem sob pressão e o MercadoVivo (digital) "
                       "ganhando share. As fontes são o release, a transcrição da call, o "
                       "panorama de mercado e os concorrentes."), tag="Caso"))
    b.append(details("Apêndice B — Tipos de fonte aceitos",
                     table(["Categoria", "Exemplos"],
                           [["Documentos", "PDF, Google Docs/Slides, texto, Markdown."],
                            ["Planilhas", "Google Sheets / tabelas (suporte varia)."],
                            ["Web e vídeo", "URLs de páginas e do YouTube."],
                            ["Áudio e texto", "Gravações e texto colado."]])
                     + callout("Há limites de número e tamanho de fontes que mudam por plano. "
                               "Confirme os atuais.", label="Limites"), tag="Fontes"))
    b.append(details("Apêndice C — NotebookLM × Claude",
                     table(["NotebookLM", "Claude"],
                           [["Entende um corpo de fontes, com citações", "Cria entregáveis e automatiza"],
                            ["Briefing, FAQ, áudio das fontes", "Decks, planilhas, memos, conexões"],
                            ["Confiança e rastreabilidade", "Ação e produção"]])
                     + P("Fluxo: NotebookLM para entender → Claude para produzir."), tag="Comparação"))
    b.append(details("Apêndice D — Governança",
                     P("Só fontes aprovadas; verificar a citação mesmo com grounding; em "
                       "ambiente corporativo usar a versão aprovada; compartilhar = "
                       "compartilhar as fontes. Baixe o checklist completo em Recursos."),
                     tag="Governança"))
    b.append(details("Apêndice E — Onde verificar",
                     P("O NotebookLM evolui rápido: fontes aceitas, Audio/Video Overview, "
                       "limites, planos e política de dados mudam. Antes de aplicar, confirme "
                       "na documentação oficial do Google e na política interna da sua "
                       "organização."), tag="Verificar"))
    return page("Referência", "".join(b), active="referencia", depth=0)


# ---------------------------------------------------------------------------
# Geração
# ---------------------------------------------------------------------------
def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("  escrito:", path)


def main():
    print("Gerando páginas...")
    write("index.html", build_home())
    write("dicas.html", build_dicas())
    write("recursos.html", build_recursos())
    write("referencia.html", build_referencia())
    write("modulos/index.html", build_list())
    for i in range(len(MODULES)):
        write("modulos/" + slug(MODULES[i][0]) + ".html", build_module(i))
    res = write_resources()
    print("Materiais:", ", ".join(res))
    print("Pronto. Sirva com:  python3 -m http.server 8092")


if __name__ == "__main__":
    main()

