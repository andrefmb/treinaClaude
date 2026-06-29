#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Construtor do treinamento "Dominando o Claude · Executivo" (V2 — geral/cross-setor).
Caso fictício: Aurora S.A. (varejo de bens de consumo). Site separado da V1.
Rode: python3 gen_dataroom.py && python3 build.py && python3 build_single.py
Sirva: python3 -m http.server 8091
"""
import html as _html
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# GLOSSÁRIO (executivo, cross-setor)
# ---------------------------------------------------------------------------
GLOSSARY = {
    "Projeto": "Uma pasta de contexto dentro do Claude: tudo o que você sobe ali fica disponível em todas as conversas daquele Projeto. Você não reenvia os arquivos a cada pergunta — e é onde ficam as instruções padrão do time.",
    "Contexto": "Tudo o que o Claude consegue enxergar agora — a conversa, os arquivos que você subiu e as instruções — somado ao conhecimento geral do treino. Sem o relatório, os números e o público, a resposta sai genérica.",
    "Alucinação": "Quando o Claude afirma um número, um fato ou uma citação que soam perfeitos e estão errados, com total convicção. Nada de valor avança sem verificação na fonte.",
    "Brief": "O pedido bem feito: contexto + tarefa + materiais + restrições + formato/público. A habilidade que mais melhora o resultado. Atalho que vale por todos: diga o público e o formato.",
    "Margem EBITDA": "De cada R$ 100 de receita, quanto sobra de geração de caixa operacional (antes de juros, impostos e depreciação). 8% = R$ 8. Quanto maior, mais eficiente é a operação.",
    "Market share": "A fatia de um mercado que uma empresa detém, em %. Ganhar share é crescer mais rápido que o mercado; perder share é o contrário.",
    "TAM": "Total Addressable Market — o tamanho total do mercado que dá para atender, em R$. Ajuda a dimensionar a oportunidade e a ambição.",
    "DRE": "Demonstração do Resultado — o “quanto entrou e quanto saiu” de um período: receita, custos, despesas e lucro. Mostra se a operação deu lucro.",
    "Pre-mortem": "Um exercício em que você imagina que a decisão JÁ fracassou e pergunta “o que deu errado?” — para achar os riscos antes que aconteçam.",
    "Skill": "Um pacote reutilizável de instruções (e modelos) que ensina o Claude a fazer uma tarefa recorrente do SEU jeito, com consistência. Em vez de reescrever o brief toda semana, você empacota o padrão.",
    "MCP": "Model Context Protocol — o padrão aberto que liga o Claude a fontes e sistemas. No Claude aparece como Conectores: em vez de só trabalhar no que você cola, ele lê direto das fontes aprovadas.",
    "Conector": "A ponte que dá ao Claude acesso a uma fonte ou sistema (e-mail, agenda, Drive, Slack, ou um sistema interno via MCP), com a sua permissão e governança — de preferência só leitura.",
    "Haiku": "O modelo mais rápido e leve da família Claude. Bom para triagem, classificação, resumos curtos e extração em volume.",
    "Sonnet": "O modelo versátil do dia a dia: escrita, análise, raciocínio de várias etapas e criação de documentos. É por onde você começa.",
    "Opus": "O modelo de raciocínio profundo: documentos longos e decisões de alto risco, como uma análise estratégica a partir de relatório + dados.",
    "LGPD": "Lei Geral de Proteção de Dados. Dados pessoais de clientes, colaboradores e terceiros só entram em ferramentas aprovadas e com base legal — vazamento é risco material e de board.",
    "Deep Research": "Modo em que o Claude pesquisa a web a fundo, cruzando muitas fontes para uma resposta abrangente — útil em análise de mercado e due diligence, sempre com verificação das fontes.",
    "Cowork": "O aplicativo de desktop do Claude: vive na sua máquina, lê os seus arquivos reais e cria documentos reais na sua pasta. Bom para delegar tarefas de várias etapas.",
    "Artefato": "Uma saída interativa que o Claude gera e você abre/baixa ali mesmo — um painel, uma calculadora, um gráfico, um simulador — e que dá para compartilhar.",
    "Visão": "A capacidade de o Claude ler imagens: relatórios e contratos escaneados, fotos, prints e slides — útil para material não digitalizado.",
    "Cenário de estresse": "Um teste que pergunta “e se piorar?”: recalcula resultados sob uma hipótese adversa (ex.: a receita cai 10%) para medir a resiliência do negócio.",
    "Aurora": "Aurora S.A. (fictícia) — a empresa do caso: varejo de bens de consumo (eletrônicos, casa e estilo de vida), com lojas e e-commerce. Receita ~R$ 4,2 bi; crescimento desacelerando e um concorrente digital ganhando share.",
}


def g(term, label=None):
    label = label or term
    return ('<span class="term">' + _html.escape(label)
            + '<span class="tip"><strong>' + _html.escape(term) + '</strong>'
            + _html.escape(GLOSSARY[term]) + '</span></span>')


# ---------------------------------------------------------------------------
# Helpers de bloco (engine)
# ---------------------------------------------------------------------------
def H2(t): return "<h2>" + t + "</h2>"
def H3(t): return "<h3>" + t + "</h3>"
def P(t):  return "<p>" + t + "</p>"
def ic(t): return '<code class="inline">' + _html.escape(t) + "</code>"


def codeblock(text):
    return '<div class="codeblock"><pre>' + _html.escape(text.strip("\n")) + "</pre></div>"


def prompt(code, label="Cole no Claude", note=None):
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


def exfiles(files, label="Arquivos deste exercício"):
    chips = "".join(fileref(f) for f in files)
    return ('<div class="exfiles"><span class="exfiles-label">' + _html.escape(label)
            + "</span>" + chips + "</div>")


# ---------------------------------------------------------------------------
# Shell
# ---------------------------------------------------------------------------
DISCLAIMER = (
    "Caso fictício Aurora S.A. — empresa, números e concorrentes são ilustrativos, criados "
    "apenas para o treinamento. Regra do dia: use dados públicos ou fictícios; nunca cole "
    "dados pessoais (LGPD) ou confidenciais em ferramentas que a empresa ainda não aprovou."
)
DISCLAIMER2 = (
    "Os recursos, modelos e políticas do Claude evoluem rapidamente. Antes de aplicar, "
    "confirme o que está vigente nas fontes oficiais e na política interna de IA e LGPD da "
    "sua organização (ver Referência)."
)


def nav(active, depth=0):
    up = "../" if depth else ""
    def cls(name): return ' class="active"' if active == name else ""
    return (
        '<header class="topbar">'
        '<a class="brand" href="' + up + 'index.html">'
        '<span class="mark">Dominando o Claude</span>'
        '<span class="sub">Executivo</span></a>'
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
        '<p style="font-size:0.8rem">Programa hands-on · liderança · versão executiva · '
        "todos os dados do caso são fictícios.</p>"
        "</div></footer>"
    )


def page(title, body, active="", depth=0):
    up = "../" if depth else ""
    return (
        "<!DOCTYPE html>\n"
        '<html lang="pt-BR"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        "<title>" + _html.escape(title) + " · Dominando o Claude</title>"
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

# ---------------------------------------------------------------------------
# Conteúdo dos módulos
# ---------------------------------------------------------------------------
def m00():
    b = []
    b.append(P("Objetivo: conectar a IA ao que pesa na mesa de um executivo e instalar o "
               "modelo mental do dia."))
    b.append(H2("O trabalho do executivo é ler, cruzar e decidir"))
    b.append(P("<strong>Ler</strong> — relatórios, resultados, contratos, estudos de "
               "mercado; muita informação, pouco tempo. <strong>Cruzar</strong> — o número "
               "contra a meta, a empresa contra a concorrência, a decisão contra o risco. "
               "<strong>Decidir e comunicar</strong> — é aqui que está o valor."))
    b.append(callout("O Claude faz a leitura e o cruzamento em minutos — e libera você para o "
                     "julgamento, que continua humano. O custo de não ter essa fluência é "
                     "competitivo, não tecnológico.", label="A ideia central", kind="gold"))
    b.append(H2("Trate o Claude como um analista sênior"))
    b.append(table(["O que ele é", "O que isso significa"],
                   [["Lê e organiza muito rápido", "Resume, extrai e estrutura grandes documentos em minutos."],
                    ["Não conhece o seu contexto", "Não sabe da sua empresa, metas e prioridades — a menos que você conte."],
                    ["Pode errar com confiança", "Às vezes afirma um número ou fato errados com total convicção."],
                    ["Você sempre revisa", "A entrega é um rascunho de analista. A decisão e a responsabilidade são suas."]]))
    b.append(H2("O caso de hoje: a Aurora S.A."))
    b.append(P("Vamos usar o mesmo caso <strong>fictício</strong> o dia todo. A <strong>"
               + g("Aurora", "Aurora S.A.") + "</strong> é uma varejista de bens de consumo "
               "(eletrônicos, casa e estilo de vida), com lojas e e-commerce, receita "
               "~R$ 4,2 bi."))
    b.append(P("O dilema: o <strong>crescimento desacelerou</strong> (e ficou negativo), a "
               "<strong>margem está sob pressão</strong> e um concorrente nativo digital "
               "(<strong>MercadoVivo</strong>) <strong>ganha share</strong> rápido. A pergunta "
               "do board: acelerar o digital? É sobre a Aurora que você vai ler o relatório, "
               "montar o deck e analisar a concorrência e o mercado."))
    b.append(callout("“Não estou aprendendo a usar uma ferramenta. Estou aprendendo a delegar "
                     "a leitura e a revisar melhor a decisão.”", label="Frase para fixar", kind="gold"))
    return "".join(b)


def m01():
    b = []
    b.append(P("Um panorama rápido: o que é o Claude, o que ele faz e quais modelos existem."))
    b.append(H2("O que é o Claude"))
    b.append(P("O Claude é um assistente de IA criado pela Anthropic — uma empresa de pesquisa "
               "focada em segurança de IA. Você conversa em linguagem natural e ele lê, "
               "escreve, analisa e raciocina sobre textos, documentos e dados. Está no "
               "navegador, no app, no celular e integrado a outras ferramentas."))
    b.append(H2("O que o Claude faz"))
    b.append(table(["Capacidade", "Para um executivo"],
                   [["Ler e resumir documentos", "Relatórios, resultados, contratos, estudos."],
                    ["Analisar dados e planilhas", "Resultados, mercado, concorrência."],
                    ["Criar arquivos", "Decks em PowerPoint, planilhas, memos em Word, PDFs."],
                    ["Pesquisar na web", "Mercado, concorrência e regulação — com fontes."],
                    ["Ver imagens (" + g("Visão", "visão") + ")", "Slides, relatórios escaneados, prints."],
                    ["Conectar a sistemas", "E-mail, agenda, Drive — com governança."]]))
    b.append(H2("Os modelos do Claude"))
    b.append(table(["Modelo", "Quando usar"],
                   [[g("Haiku") + " — rápido e leve", "Triagem, resumos curtos, extração em volume."],
                    [g("Sonnet") + " — o padrão versátil", "A maioria do dia a dia: escrita, análise, documentos. Comece aqui."],
                    [g("Opus") + " — raciocínio profundo", "Documentos longos e decisões de alto risco."]]))
    b.append(callout("Comece no Sonnet; suba para o Opus em documento longo ou decisão "
                     "difícil; use o Haiku no volume simples. (Confirme nomes, planos e "
                     "limites atuais — ver Referência.)", label="Regra prática", kind="gold"))
    return "".join(b)


def m02():
    b = []
    b.append(P("As três coisas que mais mudam a qualidade do que você obtém."))
    b.append(P("<strong>1. " + g("Contexto", "Contexto é tudo") + ".</strong> Sem o "
               "relatório, os números e o público, a resposta é genérica. Dê o material e "
               "diga quem vai ler."))
    b.append(P("<strong>2. Ele pode errar com confiança.</strong> A " + g("Alucinação", "alucinação")
               + ": parece certo e está errado. Nada de valor vai adiante sem verificação na fonte."))
    b.append(P("<strong>3. Ele é probabilístico.</strong> Pergunte duas vezes e terá "
               "variações — ótimo para gerar opções, exige cuidado quando você precisa de exatidão."))
    b.append(handson("Exercício — poder e limite", "Mão na massa",
                     prompt("Explique, em 4 frases, o que um CEO de varejo olha para decidir\n"
                            "se acelera ou não a entrada no digital. Depois, liste 3 afirmações\n"
                            "suas das quais você tem MENOS certeza e que eu deveria verificar.")
                     + details("Reflexão",
                               P("Ao pedir que o Claude aponte as próprias incertezas, você já "
                                 "instala o hábito mais importante: olhar a resposta com senso "
                                 "crítico. Quais das três afirmações você conferiria antes de "
                                 "levar adiante?"), tag="Reflexão")))
    return "".join(b)


def m03():
    b = []
    b.append(P("A habilidade que mais melhora resultados: saber pedir. Um bom " + g("Brief", "brief")
               + " não é “escrever bonito”; é dar contexto, público e formato."))
    b.append(H2("Anatomia de um bom brief"))
    b.append(table(["Elemento", "Pergunta que responde", "Exemplo (Aurora)"],
                   [["Contexto / papel", "Quem é você e qual a situação?", "“Você assessora o comitê executivo de uma varejista.”"],
                    ["Tarefa", "O que quero, exatamente?", "“Resuma o release de resultados e aponte os riscos.”"],
                    ["Materiais", "Com base em quê?", "“Use o arquivo do release no Projeto.”"],
                    ["Restrições", "Que limites respeitar?", "“Máximo 1 página; marque o que eu devo verificar.”"],
                    ["Formato / público", "Para quem e em que forma?", "“Em tópicos, para o board.”"]]))
    b.append(callout("Se só lembrar de uma coisa: diga o público e o formato.", label="O atalho que vale por todos", kind="gold"))
    b.append(H2("O salto de qualidade"))
    b.append('<div class="compare">'
             '<div class="col weak"><div class="k">Pedido fraco</div>'
             '<p>“Analise o resultado da Aurora.”</p>'
             '<p style="color:var(--muted);font-size:.9rem">Resposta genérica, sem foco no que você decide.</p></div>'
             '<div class="col strong"><div class="k">Com brief</div>'
             '<p>“Resuma o release em 6 tópicos para o board, destacando a tendência de '
             'receita e margem e os 3 maiores riscos, e diga o que devo verificar.”</p>'
             '<p style="color:var(--muted);font-size:.9rem">Pronto para a reunião — e com o que conferir.</p></div></div>')
    b.append(H3("Iteração é vantagem"))
    b.append(P("“Mais curto, foque na recomendação.” · “Adicione o cenário pessimista.” · "
               "“Transforme em 6 tópicos de fala.” · “Aja como um board cético e ataque esta análise.”"))
    b.append(handson("Exercício — uma linha vs. um brief", "Mão na massa",
                     exfiles(["Aurora_Release_Resultados.md"])
                     + prompt("Fale sobre o resultado da Aurora.", label="Versão fraca")
                     + prompt("Você assessora o comitê executivo da Aurora. Com base no\n"
                              "\"Aurora_Release_Resultados\", resuma em até 6 tópicos para o\n"
                              "board: tendência de receita e margem, o avanço do digital, a\n"
                              "ameaça da concorrência e as prioridades. Ao final, liste o que\n"
                              "eu devo conferir antes de apresentar.", label="Versão brief")
                     + details("Reflexão",
                               P("Compare as duas respostas: a segunda chega pronta para a "
                                 "reunião e já diz o que conferir — e a única coisa que mudou "
                                 "foi o contexto que você deu."), tag="Reflexão")))
    return "".join(b)


def m04():
    b = []
    b.append(P("O trabalho número um do executivo com IA: transformar um relatório longo na "
               "leitura executiva que alimenta a decisão."))
    b.append(exfiles(["Aurora_Release_Resultados.md", "Aurora_DataRoom.xlsx"]))
    b.append(H2("Resumo executivo de um relatório"))
    b.append(prompt("Com base no \"Aurora_Release_Resultados\", produza um resumo executivo de\n"
                    "1 página com: (1) os números-chave (receita, margem, lucro); (2) a\n"
                    "tendência ao longo do ano; (3) os 5 pontos de atenção mais relevantes;\n"
                    "(4) as prioridades. Cite de onde tirou cada ponto e marque [VERIFICAR]\n"
                    "nos números que dependem de fonte externa."))
    b.append(H2("Cruzar o relatório com os números"))
    b.append(prompt("Agora cruze o release com as abas \"DRE 2025\" e \"Resultados\n"
                    "Trimestrais\" do Aurora_DataRoom.xlsx. A narrativa do release bate com\n"
                    "os números da planilha? Aponte qualquer divergência."))
    b.append(callout("Confira os números na fonte antes de citar. A IA computa e resume; o "
                     "executivo interpreta e responde.", label="Cuidado", kind="warn"))
    b.append(details("Reflexão",
                     P("Repare como o Claude ancorou cada achado numa parte do relatório — "
                       "confira esses ponteiros. Você pegou a desaceleração da receita, a "
                       "queda de margem e o avanço do digital? São esses os pontos que iriam "
                       "ao board."), tag="Reflexão"))
    return "".join(b)


def m05():
    b = []
    b.append(P("Do documento ao <strong>deck</strong>: o Claude transforma um relatório numa "
               "apresentação pronta para o board — em PowerPoint de verdade."))
    b.append(callout("O Claude tem " + g("Skill", "Skills") + " prontas de documentos (Word, "
                     "Excel, PowerPoint, PDF). Em Configurações › Capacidades, ligue "
                     "“Execução de código e criação de arquivos” para gerar arquivos.", label="Antes de começar"))
    b.append(exfiles(["Aurora_Release_Resultados.md", "Aurora_DataRoom.xlsx"]))
    b.append(H2("Relatório → deck para o board"))
    b.append(prompt("Com base no \"Aurora_Release_Resultados\" e nas abas \"DRE 2025\" e\n"
                    "\"Resultados Trimestrais\", crie uma apresentação de 7 slides para o\n"
                    "board: capa, destaques do ano, tendência de receita e margem (com\n"
                    "gráfico), o avanço do digital, a ameaça competitiva, as prioridades e\n"
                    "um slide de recomendação. Gere o arquivo .pptx para download."))
    b.append(H2("Iterar o deck"))
    b.append(prompt("Deixe mais executivo: no máximo 5 bullets por slide, um número grande\n"
                    "por slide, e um título que seja a mensagem (não o tema). Refaça o slide\n"
                    "de recomendação como “o que pedimos ao board”."))
    b.append(details("Reflexão",
                     P("Você saiu de um relatório de texto para um deck pronto, sem montar "
                       "slide por slide. Pergunte-se: quantas horas por mês a sua equipe "
                       "gasta formatando apresentações que poderiam começar assim?"), tag="Reflexão"))
    return "".join(b)


def m06():
    b = []
    b.append(P("Aqui o Claude deixa de ser “resumidor” e vira <strong>parceiro de pensamento</strong>. "
               "O objetivo não é a resposta pronta — é melhorar as suas <strong>perguntas</strong>."))
    b.append(exfiles(["Aurora_Concorrentes.md", "Aurora_DataRoom.xlsx"]))
    b.append(H2("Mapear a concorrência"))
    b.append(prompt("Com base no \"Aurora_Concorrentes\" e na aba \"Concorrentes\", monte uma\n"
                    "tabela comparativa (receita, crescimento, margem, canal, força/fraqueza)\n"
                    "e ranqueie a ameaça que cada concorrente representa para a Aurora. Diga\n"
                    "o porquê de cada posição."))
    b.append(H2("O poder das perguntas — seja crítico, não complacente"))
    b.append(P("Use o Claude para atacar a sua própria tese antes que o mercado o faça:"))
    b.append(prompt("Aja como advogado do diabo do comitê. Ataque a tese de que o MercadoVivo\n"
                    "é a maior ameaça. E se o risco real for a CasaBoa no nosso território de\n"
                    "maior margem (Casa & Decoração)? Faça o caso contrário com dados."))
    b.append(prompt("Faça um pre-mortem: estamos em 2027 e a Aurora perdeu a liderança em\n"
                    "Casa & Decoração. Conte a história do que deu errado — e quais sinais\n"
                    "eu deveria estar vendo hoje.", label="Cole no Claude", note="Pre-mortem"))
    b.append(prompt("Quais são as 5 perguntas mais difíceis que eu deveria levar ao board\n"
                    "sobre a estratégia digital — e que eu provavelmente estou evitando?"))
    b.append(details("Reflexão",
                     P("Repare que o valor não veio de uma resposta, e sim de <strong>melhores "
                       "perguntas</strong> e de uma tese testada. A boa decisão começa por uma "
                       "boa pergunta — e o Claude é um sparring incansável para chegar nela. "
                       "(Verifique os fatos que ele usar.)"), tag="Reflexão"))
    return "".join(b)


def m07():
    b = []
    b.append(P("Análise de mercado de verdade: dimensionar a oportunidade e checar a posição "
               "— com o " + g("Deep Research", "Deep Research") + ", sempre verificando as fontes."))
    b.append(exfiles(["Aurora_Mercado.md"]))
    b.append(H2("Do panorama interno à pesquisa externa"))
    b.append(prompt("Leia o \"Aurora_Mercado\" como hipótese inicial. Depois pesquise na web\n"
                    "o tamanho e o crescimento reais do varejo de bens de consumo e do\n"
                    "e-commerce no Brasil, com fontes. Compare com a posição da Aurora\n"
                    "(share por segmento) e aponte onde a hipótese se confirma ou não."))
    b.append(H2("Tendências e oportunidade"))
    b.append(prompt("Liste as 5 tendências que mais afetam a Aurora nos próximos 24 meses,\n"
                    "cada uma com a fonte e o “e daí?” para a nossa estratégia. Termine com\n"
                    "as 3 perguntas que eu deveria responder antes de investir no digital."))
    b.append(callout("Tudo que vier da web precisa de fonte e de checagem — números de "
                     "mercado variam muito entre consultorias. Trate como insumo direcional, "
                     "não como verdade final.", label="Cuidado — verifique as fontes", kind="warn"))
    b.append(details("Reflexão",
                     P("Você usou a IA para sair da sua bolha de dados internos e olhar o "
                       "mercado — em minutos. Pergunte-se: quais decisões você toma hoje sem "
                       "uma leitura de fora que o Claude poderia trazer (com fontes)?"), tag="Reflexão"))
    return "".join(b)


def m08():
    b = []
    b.append(P("Agora, do começo ao fim: produza um entregável que você reconheça como "
               "trabalho de verdade. Escolha uma trilha."))
    b.append(table(["Trilha", "Entregável"],
                   [["Memo de decisão ao board", "1–2 páginas: situação, opções, recomendação e riscos."],
                    ["Deck de estratégia digital", "Apresentação com diagnóstico e proposta."],
                    ["Análise competitiva", "Comparativo + ameaças + movimentos recomendados."],
                    ["Carta aos acionistas", "Comunicação dos resultados em dois tons."]]))
    b.append(H2("Cinco passos do brief ao entregável"))
    b.append(table(["#", "Passo", "O que fazer"],
                   [["1", "Brief", "Contexto + tarefa + materiais + público + formato."],
                    ["2", "Rascunho", "Gere o primeiro e leia criticamente."],
                    ["3", "Iterar", "“Mais curto”, “adicione o cenário de baixa”, “foque na recomendação”."],
                    ["4", "Autocrítica", "“Aponte 3 fraquezas e os números a checar.”"],
                    ["5", "Entregar", "Peça o documento, a planilha ou os slides para download."]]))
    b.append(handson("Brief do memo ao board", "Exemplo · trilha de decisão",
                     exfiles(["Aurora_Release_Resultados.md", "Aurora_Concorrentes.md", "Aurora_DataRoom.xlsx"])
                     + prompt("Você assessora o comitê executivo da Aurora. Com base no release,\n"
                              "nos concorrentes e nos dados, escreva um memo de 1-2 páginas:\n"
                              "(1) situação (resultado e mercado); (2) a ameaça digital;\n"
                              "(3) 3 opções estratégicas com prós/contras; (4) recomendação\n"
                              "clara e o que pedimos ao board; (5) riscos e mitigadores.\n"
                              "Marque [VERIFICAR] nos números externos. Gere como documento.")
                     + details("Reflexão",
                               P("Pare e pergunte-se: quanto tempo isto teria levado sem o "
                                 "Claude? E onde o <strong>seu</strong> julgamento foi "
                                 "insubstituível — na escolha da recomendação e no que aceitar "
                                 "ou corrigir? Essa parte continua sua."), tag="Reflexão")))
    return "".join(b)


def m_cowork():
    b = []
    b.append(P("Até aqui você conversou no navegador. O <strong>" + g("Cowork", "Cowork")
               + "</strong> é o app de desktop que vive na sua máquina: lê os seus arquivos "
               "reais, cria documentos reais na sua pasta e executa tarefas de várias etapas."))
    b.append(table(["Recurso", "O que significa"],
                   [["Lê os arquivos reais", "Aponte uma pasta com relatórios e planilhas — ele trabalha sobre os arquivos."],
                    ["Cria arquivos de verdade", "Gera .docx, .xlsx e .pptx direto na sua pasta."],
                    ["Faz tarefas de várias etapas", "Você delega um fluxo do início ao fim e revisa."]]))
    b.append(callout("O Cowork lê e escreve nos seus arquivos de verdade. Use só uma pasta "
                     "com dados aprovados/fictícios — nunca dados pessoais ou confidenciais "
                     "sem base legal.", label="Governança", kind="warn"))
    b.append(H2("Deixe o Claude te entrevistar"))
    b.append(prompt("Antes de escrever o memo ao board, me faça as perguntas que você precisa\n"
                    "para fazer um bom trabalho — uma de cada vez. Quando tiver o suficiente,\n"
                    "escreva e salve como memo-board.docx na pasta."))
    b.append(H2("Arquivos de contexto: um bom arquivo vale mais que 50 uploads"))
    b.append(P("Dois arquivos curtos mudam todas as respostas: um diz <strong>quem você é</strong> "
               "e o seu contexto; o outro fixa o <strong>seu tom</strong> (e tira o “cheiro de IA”)."))
    b.append(exfiles(["sobre-mim-template.md", "estilo-de-escrita-template.md"]))
    b.append(prompt("Leia sobre-mim.md e estilo-de-escrita.md. Daqui pra frente, escreva tudo\n"
                    "no meu tom e considerando o meu papel e contexto — sem eu repetir."))
    b.append(callout("As <strong>Instruções globais</strong> são a versão “sempre ligada” "
                     "disso: uma configuração única que o Claude lê antes de toda tarefa "
                     "(ver Personalização).", label="Dica"))
    return "".join(b)


def m_projetos():
    b = []
    b.append(P("O " + g("Projeto", "Projeto") + " é o <strong>cérebro compartilhado do time</strong> "
               "— e usá-lo bem é o que faz a IA <em>compor</em> em vez de recomeçar a cada conversa."))
    b.append(H2("Três camadas de memória"))
    b.append(table(["Camada", "O que é", "Analogia"],
                   [["Arquivo solto", "Um documento que você cola; vale só ali.", "Um post-it."],
                    ["Projeto", "Pasta de contexto + instruções + arquivos, do time.", "O manual do time."],
                    [g("Skill", "Skill"), "Um processo da casa que o Claude aplica sozinho.", "Um procedimento da empresa."]]))
    b.append(H2("A estratégia: um Projeto por decisão recorrente"))
    b.append(P("Crie um Projeto por domínio — ex.: “Comitê Executivo — Aurora” — carregado com "
               "relatórios, dados, template do memo e as últimas decisões. As <strong>"
               "instruções de Projeto</strong> impõem o padrão da casa."))
    b.append(handson("Monte um data-room Project", "Mão na massa · Projetos",
                     P("(1) Crie um Projeto. (2) Suba os arquivos do caso. (3) Cole instruções "
                       "de Projeto (estrutura do memo + a regra do [VERIFICAR]). (4) Faça "
                       "perguntas que só funcionam porque o contexto está carregado:")
                     + exfiles(["Aurora_Release_Resultados.md", "Aurora_DataRoom.xlsx",
                                "Aurora_Concorrentes.md", "Aurora_Mercado.md"],
                               label="Suba estes no Projeto")
                     + prompt("1) Resuma nossa posição competitiva em uma página.\n"
                              "2) Escreva o memo da decisão digital no nosso formato padrão.\n"
                              "3) Quais dados nos faltam para decidir com segurança?")
                     + details("Reflexão",
                               P("Você não reenviou arquivo nem reexplicou o formato — o "
                                 "Projeto já sabia. O conhecimento <strong>acumula</strong>: "
                                 "toda resposta que vale a pena vira nota no Projeto, e a "
                                 "próxima pergunta começa de um patamar mais alto."), tag="Reflexão")))
    b.append(callout("Governança do Projeto: um dono, regras claras do que pode entrar "
                     "(dados aprovados) e uma cadência de revisão.", label="Governança", kind="warn"))
    return "".join(b)


def m_pers():
    b = []
    b.append(P("Deixe o Claude do seu jeito e empacote o que se repete em " + g("Skill", "Skills") + "."))
    b.append(H2("Personalização — três níveis"))
    b.append(table(["Nível", "Alcance", "Exemplo"],
                   [["Preferências", "Todas as conversas", "“Recomendação primeiro, depois os porquês. Nunca invente números.”"],
                    ["Instruções de Projeto", "Só naquele " + g("Projeto", "Projeto"), "A estrutura padrão do memo e a política do time."],
                    ["Estilos", "O jeito de escrever", "Um estilo “Aurora” treinado em comunicados antigos."]]))
    b.append(H2("Skills: ensine um fluxo uma vez"))
    b.append(P("Uma " + g("Skill", "Skill") + " é um pacote reutilizável de instruções que "
               "ensina o Claude a fazer uma tarefa recorrente do seu jeito. Você já usou hoje "
               "ao gerar o deck e o memo (Skills de documentos)."))
    b.append(callout("(1) Configurações › Capacidades: ligue “Execução de código e criação de "
                     "arquivos”. (2) Personalizar › Skills: ative as que quiser. O Claude usa "
                     "a Skill sozinho quando faz sentido.", label="Como ligar"))
    b.append(handson("Construa a sua primeira Skill", "Mão na massa · Skills",
                     prompt("Nome: Memo de Decisão Padrão\n"
                            "Descrição: Use para escrever memos de decisão ao board no nosso\n"
                            "formato.\n"
                            "Instruções: estrutura — (1) situação; (2) opções com prós/contras;\n"
                            "(3) recomendação e o que pedimos; (4) riscos. Marque [VERIFICAR]\n"
                            "nos números externos. Tom objetivo; 1-2 páginas.",
                            label="Cole como base da sua Skill")))
    b.append(callout("Há uma <strong>biblioteca de Skills por papel</strong> (resumo de "
                     "relatório, deck ao board, análise de concorrência, memo de decisão, "
                     "brief de reunião, resposta de e-mail, análise de mercado) na página "
                     "<a href='../referencia.html'>Referência</a> e em "
                     "<a href='../recursos.html'>Recursos</a>.", label="Biblioteca de Skills", kind="gold"))
    return "".join(b)


def m_conectores():
    b = []
    b.append(P("Ligar o Claude às suas fontes — e-mail, agenda e sistemas — com governança. "
               "É aqui que ele sai do navegador e entra no seu dia."))
    b.append(H2("Conectores: e-mail, agenda e mais"))
    b.append(P("Em vez de só trabalhar no que você cola, o Claude lê direto das fontes "
               "aprovadas. Em <strong>Personalizar › " + g("Conector", "Conectores")
               + "</strong> (ou pelo “+” no chat) você liga Outlook/Gmail, Google/Microsoft "
               "Agenda, Drive, Slack — autenticando com a sua conta e ligando/desligando por "
               "conversa."))
    b.append(callout("Prefira <strong>permissão de leitura</strong>. O e-mail só-leitura "
                     "resume sem poder enviar; agenda só-leitura lê sem alterar. Conecte "
                     "apenas o que a empresa aprovou e revogue quando quiser.", label="Governança", kind="warn"))
    b.append(H2("O brief do seu dia (Outlook/Calendar)"))
    b.append(prompt("Com a minha agenda e o e-mail conectados (só leitura): me dê o brief do\n"
                    "dia — minhas próximas 8 horas (título, horário e quem), os e-mails das\n"
                    "últimas 24h que pedem ação minha, e o que eu deveria preparar antes de\n"
                    "cada reunião. Uma tela, que eu leia em 60 segundos."))
    b.append(H2("Preparar uma reunião"))
    b.append(prompt("Para a reunião de comitê de hoje: junte os e-mails e documentos\n"
                    "relacionados, faça um resumo de 1 página com o que está em jogo, as\n"
                    "decisões pendentes e 3 perguntas que eu devo fazer. Não envie nada —\n"
                    "me devolva aqui."))
    b.append(handson("Triagem de inbox", "Mão na massa · e-mail",
                     prompt("Verifique as últimas 24h do meu e-mail. Separe em: precisa de\n"
                            "resposta minha, posso delegar, e só FYI. Para os 3 mais urgentes,\n"
                            "rascunhe a resposta no meu tom — sem enviar.")
                     + details("Reflexão",
                               P("Repare quanto da sua manhã é triagem e preparação — e quanto "
                                 "disso o Claude faz em um pedido. O julgamento (o que responder, "
                                 "o que decidir) continua seu; o trabalho braçal, não."), tag="Reflexão")))
    b.append(callout("E-mail e agenda têm dados pessoais (LGPD). Use só contas e conectores "
                     "aprovados; nunca deixe o agente enviar nada em seu nome sem você ler.",
                     label="Atenção", kind="warn"))
    return "".join(b)


def m_plugins():
    b = []
    b.append(P("Quando uma tarefa se repete, você para de pedir e começa a <strong>automatizar"
               "</strong>: empacota em Skills, dispara por comandos e deixa rodando sozinho."))
    b.append(H2("Skill Creator — deixe o Claude construir a Skill"))
    b.append(prompt("Quero uma skill que padronize os nossos resumos de resultados trimestrais.\n"
                    "Me entreviste para entender o formato e então construa a skill para mim."))
    b.append(H2("Claude no Excel"))
    b.append(P("Há um Claude que vive <strong>dentro da planilha</strong>: lê fórmulas, limpa "
               "dados e monta modelos."))
    b.append(exfiles(["Aurora_DataRoom.xlsx"]))
    b.append(prompt("Nesta planilha, crie uma aba \"Resumo\" com receita, margem EBITDA e\n"
                    "crescimento por trimestre, e um gráfico da tendência. Sinalize qualquer\n"
                    "célula cujo valor não bata com a fórmula."))
    b.append(H2("Comandos de barra e tarefas agendadas"))
    b.append(prompt("Crie um comando /resumo-resultados que gere o nosso resumo executivo de\n"
                    "resultados a partir do release e da planilha que eu indicar."))
    b.append(prompt("Agende um briefing toda segunda às 8h: novidades dos nossos concorrentes\n"
                    "e do mercado na semana, e os 3 movimentos que merecem atenção. Me entregue\n"
                    "para revisão."))
    b.append(details("Reflexão",
                     P("Pense numa pergunta que você responde toda semana, sempre igual. Essa "
                       "é a primeira candidata a virar comando ou tarefa agendada. Mas lembre: "
                       "o que roda sozinho precisa de dono e de revisão."), tag="Reflexão"))
    return "".join(b)


def m_nivel4():
    b = []
    b.append(P("Você não precisa programar — mas precisa saber o que existe no <strong>topo da "
               "escada</strong>, porque é onde estão a maior alavanca e o maior risco de "
               "governança. Módulo de <strong>consciência</strong>, não de terminal."))
    b.append(H2("O que mora no Nível 4"))
    b.append(table(["Recurso", "O que é", "Quando importa"],
                   [["Claude Code", "O Claude no terminal, para quem desenvolve.", "TI e dados constroem automações e integrações."],
                    ["Claude Computer", "O Claude controla a tela: clica, digita, navega.", "Tarefas em sistemas sem API — com supervisão."],
                    ["Agentes paralelos", "Vários agentes em lote ao mesmo tempo.", "Processar centenas de documentos de uma vez."],
                    [g("MCP") + " servers", "Integrações com fontes e sistemas internos.", "Ligar o Claude às bases aprovadas (ver Conectores)."],
                    ["Negócio pela linha de comando", "Fluxos inteiros operados via CLI.", "Onde a operação digital ganha escala — com controles."]]))
    b.append(H2("A lente do líder"))
    b.append(table(["Garantia", "Por quê"],
                   [["Rastreabilidade e revisão humana", "Decisões importantes nunca 100% automáticas."],
                    ["Dados aprovados e allowlist", "Agentes só acessam fontes liberadas."],
                    ["Um dono por automação", "Tudo que roda sozinho tem responsável e revisão."],
                    ["Começar pequeno e medir", "Piloto controlado → métrica de valor e risco → escala."]]))
    b.append(details("Reflexão",
                     P("Pense num processo repetitivo, mensurável e de alto volume na sua área. "
                       "É o candidato natural ao Nível 4. Qual o ganho — e qual o portão de "
                       "governança antes de deixá-lo rodar?"), tag="Reflexão"))
    return "".join(b)


def m_gov():
    b = []
    b.append(P("O verdadeiro papel da liderança com IA é governá-la. Aqui calibramos confiança "
               "e disciplina."))
    b.append(H2("Ele pode errar com confiança"))
    b.append(P("Nunca leve adiante um número, um fato ou uma fonte que você não verificou. A "
               "IA acelera o rascunho; a responsabilidade pela verdade continua sua."))
    b.append(callout("Peça um dado obscuro e específico (uma estatística de nicho, uma citação) "
                     "e veja como pode vir plausível e errado — uma " + g("Alucinação", "alucinação")
                     + " ao vivo.", label="Demonstração"))
    b.append(H2("Dados, sigilo e LGPD"))
    b.append(table(["Nível", "O que é"],
                   [["✅ Seguro", "Informação pública, dados fictícios, rascunhos sem dados de pessoas."],
                    ["⚠️ Cautela / aprovação", "Dados de clientes/colaboradores, financeiros não públicos, segredos."],
                    ["⛔ Risco material", "Qualquer dado pessoal ou confidencial em ferramenta não aprovada."]]))
    b.append(callout("Vazamento é risco material e de " + g("LGPD") + ". Confirme qual versão "
                     "corporativa a empresa aprovou.", label="Por que é tema de board", kind="warn"))
    b.append(H2("Governar, não só usar"))
    b.append(table(["Alavanca", "O que significa"],
                   [["Política e ferramentas aprovadas", "O que pode/não pode e quais ferramentas usar."],
                    ["Capacitação por papel", "Cada função sabe o que delegar e como revisar."],
                    ["Pipeline de casos de uso", "Cada caso com dono e métrica — nada de “teatro de IA”."],
                    ["Medição trimestral", "Tempo, qualidade e risco medidos a cada trimestre."]]))
    return "".join(b)


def m_plano():
    b = []
    b.append(P("Saia daqui com três compromissos concretos."))
    b.append(table(["Horizonte", "Compromisso", "Exemplo"],
                   [["Esta semana", "1 tarefa para delegar", "Resumir o relatório/relatórios da semana antes do comitê."],
                    ["Este mês", "1 processo para melhorar", "Padronizar o memo de decisão (instruções de Projeto)."],
                    ["Este trimestre", "1 capacidade no time", "Política de dados/LGPD e capacitação por área."]]))
    b.append(callout("“Não estou aprendendo a usar uma ferramenta. Estou aprendendo a delegar "
                     "a leitura e a revisar melhor a decisão.”", label="Encerramento", kind="gold"))
    b.append(P("Leve a <a href='../recursos.html'>biblioteca de prompts e skills</a> e o "
               "<a href='../referencia.html'>checklist de governança</a>."))
    return "".join(b)


# ---------------------------------------------------------------------------
# Biblioteca de Skills (executiva)
# ---------------------------------------------------------------------------
SKILLS = [
    ("Resumo Executivo de Relatório", "Todos",
     "Use para transformar um relatório/release em resumo executivo de 1 página.",
     "Estrutura: (1) números-chave; (2) tendência; (3) os 5 pontos de atenção; (4) "
     "prioridades. Cite a origem de cada ponto e liste o que verificar."),
    ("Deck para o Board", "Estratégia / Diretoria",
     "Use para gerar uma apresentação para o board a partir de um relatório e dados.",
     "Slides: capa, destaques, tendência (com gráfico), riscos, prioridades, recomendação. "
     "Máx. 5 bullets por slide; título = mensagem. Gere .pptx."),
    ("Análise de Concorrência", "Estratégia / Comercial",
     "Use para comparar concorrentes e ranquear ameaças.",
     "Tabela: receita, crescimento, margem, canal, força/fraqueza. Ranqueie a ameaça e "
     "recomende movimentos. Marque [VERIFICAR] nos números externos."),
    ("Memo de Decisão", "Diretoria / Estratégia",
     "Use para escrever um memo de decisão de 1-2 páginas ao board.",
     "Estrutura: situação; opções com prós/contras; recomendação e o que pedimos; riscos. "
     "Tom objetivo; [VERIFICAR] nos números externos."),
    ("Brief de Reunião", "Todos",
     "Use para preparar uma reunião a partir de e-mails e documentos.",
     "Resumo de 1 página: o que está em jogo, decisões pendentes, e 3 perguntas a fazer. "
     "Não envie nada."),
    ("Resposta de E-mail no meu tom", "Todos",
     "Use para rascunhar respostas de e-mail na minha voz.",
     "Espelhe o meu tom (do estilo-de-escrita.md). Gere a resposta para eu revisar — nunca "
     "envie. Aponte o risco de cada versão se houver."),
    ("Análise de Mercado", "Estratégia",
     "Use para dimensionar e checar um mercado com pesquisa.",
     "Tamanho, crescimento, tendências e posição relativa — com fontes. Termine com as "
     "perguntas que faltam responder. Trate números como direcionais."),
]


def render_skill(nome, papel, desc, instr):
    return ('<div class="callout gold"><span class="label">' + _html.escape(papel) + "</span>"
            "<strong>" + _html.escape(nome) + "</strong>"
            "<p style='margin:.4em 0'><em>Descrição (quando usar):</em> " + _html.escape(desc) + "</p>"
            "<p style='margin:.2em 0'><em>Instruções:</em> " + _html.escape(instr) + "</p></div>")


print("módulos definidos.")

# ---------------------------------------------------------------------------
# Metadados
# ---------------------------------------------------------------------------
# (id, ato, título, subtítulo, função, aprofundamento?)
MODULES = [
    ("00", "I",   "Abertura", "Por que isso importa para um executivo", m00, False),
    ("01", "I",   "Conhecendo o Claude", "O que é, o que faz e os modelos", m01, False),
    ("02", "I",   "Fundamentos sem jargão", "As três verdades que mudam o uso", m02, False),
    ("03", "I",   "O brief executivo", "A habilidade que mais melhora resultados", m03, False),
    ("04", "II",  "Ler relatórios", "Extrair o que importa de um relatório", m04, False),
    ("05", "II",  "Do relatório ao deck", "Gerar uma apresentação para o board (.pptx)", m05, False),
    ("06", "II",  "Concorrência: o poder das perguntas", "Análise crítica e o Claude como sparring", m06, False),
    ("07", "II",  "Análise de mercado", "Dimensionar e checar — com Deep Research", m07, True),
    ("08", "II",  "Construir um entregável", "Do brief ao memo/deck final", m08, False),
    ("09", "III", "Cowork: o Claude no seu computador", "App de desktop, arquivos reais e de contexto", m_cowork, True),
    ("10", "III", "Projetos: o cérebro do time", "A estratégia de Projetos no Claude", m_projetos, True),
    ("11", "III", "Personalização e Skills", "Personalizar, usar e construir Skills", m_pers, False),
    ("12", "III", "Conectores: Outlook, Calendar e e-mail", "O Claude no seu dia, com governança", m_conectores, False),
    ("13", "III", "Plugins, comandos e automações", "Skill Creator, Excel, comandos e agendamentos", m_plugins, True),
    ("14", "III", "Nível 4 — Código e Computador", "O topo da escada, pela lente do líder", m_nivel4, True),
    ("15", "III", "Riscos e governança", "O papel da liderança é governar o uso", m_gov, False),
    ("16", "III", "Plano 30-60-90 e fechamento", "Sair daqui com compromissos concretos", m_plano, False),
]
ACT_NAME = {"I": "Ato I — Fundamentos", "II": "Ato II — O trabalho executivo",
            "III": "Ato III — Ir além e governar"}
ACT_SUB = {"I": "o modelo mental, o Claude e o brief",
           "II": "relatórios, decks, concorrência e mercado — com a Aurora",
           "III": "Cowork, Projetos, Skills, conexões e governança"}


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
         '<p class="lede">Dezessete módulos em três atos. O <strong>núcleo</strong> é a '
         'espinha dorsal (~60% mão na massa); os módulos marcados como <strong>Aprofundamento'
         '</strong> são opcionais e estendem o programa. Fio condutor: a empresa fictícia '
         '<strong>Aurora S.A.</strong></p>']
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
        "<h1>Dominando o <span class='accent'>Claude</span></h1>"
        '<p class="lede">A versão executiva: como usar o Claude no trabalho de liderança — '
        "ler relatórios, montar apresentações, analisar concorrência e mercado, fazer "
        "perguntas melhores e conectar o e-mail e a agenda. O ponto não é virar técnico: é "
        "virar um usuário fluente e um bom governante do uso de IA. Fio condutor: o caso "
        "fictício <strong>Aurora S.A.</strong></p>"
        '<div class="hero-actions">'
        '<a class="btn" href="modulos/index.html">Começar pelo Módulo 00 →</a>'
        '<a class="btn ghost" href="dicas.html">Ver as dicas</a></div></div>'
        + callout("Use dados públicos ou fictícios. Nunca cole dados pessoais (LGPD) ou "
                  "confidenciais em ferramentas que a empresa ainda não aprovou. A disciplina "
                  "começa agora e volta no módulo de governança.", label="A regra de hoje", kind="warn")
        + H2("O que você será capaz de fazer")
        + table(["Ao final, cada participante consegue…", ""],
                [["Ler relatórios e extrair o que importa", "resumo executivo + o que verificar."],
                 ["Produzir apresentações", "do relatório ao deck para o board (.pptx)."],
                 ["Analisar concorrência e mercado", "com olhar crítico e perguntas melhores."],
                 ["Usar o Claude como parceiro de pensamento", "advogado do diabo, pre-mortem."],
                 ["Conectar e-mail e agenda", "brief do dia, preparo de reunião — com governança."],
                 ["Governar o uso de IA", "com cuidado de LGPD, sigilo e verificação."]])
        + H2("A jornada")
        + agenda
        + P("<span style='color:var(--muted)'>O núcleo (módulos sem o selo "
            "<em>aprofundamento</em>) é a espinha dorsal; priorize a mão na massa. Os "
            "aprofundamentos estendem o programa e funcionam como sessões separadas ou consulta.</span>")
    )
    return page("Início", body, active="", depth=0)


# ---------------------------------------------------------------------------
# Dicas
# ---------------------------------------------------------------------------
TIPS = [
    ("Sempre comece pela tarefa.", "“Quero [tarefa] com [critérios de sucesso].”"),
    ("Depois diga: “mas antes, me faça perguntas”.", "Deixe o Claude descobrir o que falta antes de começar."),
    ("Converse, não apenas digite.", "Use o fluxo de voz/diálogo para desenvolver as ideias."),
    ("Peça 3 versões.", "Nunca apenas uma — compare e combine o melhor de cada."),
    ("Quando estiver errado, diga.", "“Você perdeu o ponto. Eu quis dizer ___.”"),
    ("Faça a IA perguntar coisas para você.", "As melhores respostas vêm de boas perguntas."),
    ("Seja específico. Depois seja ainda mais específico.", "Entrada vaga = saída vaga."),
    ("Dê à IA o seu arquivo “sobre mim”.", "Assim ela passa a soar mais como você."),
    ("Não fique refinando para sempre — recomece.", "A mensagem 30 custa muito mais do que a mensagem 1."),
    ("Gere bastante conteúdo. Jogue a maior parte fora.", "O volume faz parte do processo."),
    ("Salve a versão que você gostou.", "“Salve isto como um modelo/template.”"),
    ("Edite você mesmo no final.", "IA para melhorar a qualidade, não para evitar o trabalho."),
    ("Faça o trabalho difícil uma vez só.", "Configure bem uma vez e obtenha resultados melhores para sempre."),
]


def render_tips():
    out = '<ol class="tips">'
    for title, sub in TIPS:
        out += ('<li><span class="tip-t">' + _html.escape(title) + "</span>"
                '<span class="tip-s">' + _html.escape(sub) + "</span></li>")
    return out + "</ol>"


def dicas_body(depth=1):
    b = ['<h1>Como falar com o Claude</h1>',
         '<p class="lede">Uma colinha para o Claude funcionar como <em>você</em>. Vale para '
         "qualquer módulo — volte aqui sempre que precisar.</p>",
         render_tips(),
         callout("Defina claramente a tarefa, forneça contexto, incentive a IA a fazer "
                 "perguntas, gere várias alternativas, refine o que funcionar e transforme os "
                 "melhores resultados em modelos reutilizáveis.", label="Resumo em uma frase", kind="gold"),
         H2("Onde isto aparece no curso"),
         table(["Dica", "Onde praticar"],
               [["Comece pela tarefa · seja específico (1, 7)", "Módulo 03 — O brief executivo"],
                ["“Me faça perguntas” · faça a IA perguntar (2, 6)", "Módulo 06 — o poder das perguntas; Módulo 09 — Cowork"],
                ["Seu arquivo “sobre mim” (8)", "Módulo 09 — arquivos de contexto"],
                ["3 versões · recomece · gere bastante (4, 9, 10)", "Módulo 08 — construir e iterar"],
                ["Salve como template · faça o difícil uma vez (11, 13)", "Módulos 11 e 13 — Skills e automações"]])]
    return "".join(b)


def build_dicas():
    return page("Dicas", dicas_body(depth=1), active="dicas", depth=0)


# ---------------------------------------------------------------------------
# Arquivos
# ---------------------------------------------------------------------------
DATAROOM_FILES = [
    ("Aurora_Release_Resultados.md", "Release de resultados — o relatório-base. Módulos 03–08."),
    ("Aurora_DataRoom.xlsx", "Planilha: resultados, DRE, balanço, mercado, concorrentes — COM erros plantados. Módulos 04–13."),
    ("Aurora_Concorrentes.md", "Perfis dos concorrentes para análise crítica. Módulos 06 e 08."),
    ("Aurora_Mercado.md", "Panorama de mercado para a análise (e verificação). Módulo 07."),
]
GEN_FILES = [
    ("sobre-mim-template.md", "Arquivo de contexto: quem você é e o seu papel (Módulo Cowork)."),
    ("estilo-de-escrita-template.md", "Arquivo de contexto: o seu tom, sem “cheiro de IA” (Módulo Cowork)."),
    ("biblioteca-de-prompts.md", "Biblioteca de prompts executivos, prontos para colar."),
    ("biblioteca-de-skills.md", "Biblioteca de Skills por papel — descrição + instruções."),
    ("checklist-governanca-ia.md", "Checklist de governança de IA para a conversa de board."),
]
FAC_FILES = [
    ("Aurora_Gabarito_Facilitador.md", "Gabarito dos erros plantados no data room — só facilitador."),
]


def _file_rows(files):
    out = ""
    for fname, desc in files:
        out += ('<div class="file-row"><span class="fname">' + _html.escape(fname) + "</span>"
                '<span class="fdesc">' + _html.escape(desc) + "</span>"
                '<a class="btn ghost dl" href="arquivos/' + fname + '" download>Baixar ↓</a></div>')
    return out


def build_recursos():
    b = ['<h1>Recursos para levar</h1>'
         '<p class="lede">Os arquivos do caso Aurora e os materiais do programa. Clique para '
         "baixar e arraste para o seu " + g("Projeto", "Projeto") + " no Claude.</p>"]
    b.append(H2("Caso Aurora (dados e relatórios)"))
    b.append(_file_rows(DATAROOM_FILES))
    b.append(H2("Materiais do programa"))
    b.append(_file_rows(GEN_FILES))
    b.append(H2("Só para o facilitador"))
    b.append(callout("Contém as respostas dos erros plantados no data room. Não distribua "
                     "antes do exercício de verificação.", label="Confidencial", kind="warn"))
    b.append(_file_rows(FAC_FILES))
    return page("Recursos", "".join(b), active="recursos", depth=0)


# ---------------------------------------------------------------------------
# Materiais gerados
# ---------------------------------------------------------------------------
RES_SOBRE = """# sobre-mim.md — template

Quatro a seis linhas bastam. Deixe na pasta onde você trabalha (ou nas Instruções globais).

- **Nome / papel:** [seu nome], [cargo] em [empresa/setor].
- **O que faço:** decido sobre [áreas]; leio relatórios, dados e estudos; levo recomendações ao comitê/board.
- **O que estou resolvendo agora:** [sua prioridade do trimestre].
- **Como gosto de pensar:** começo pela recomendação, depois os porquês; foco no que decide.
- **Como gosto de ser tratado(a):** em português, direto ao ponto, sem jargão; sempre liste o que devo verificar.
- **O que nunca fazer:** inventar números; enviar nada em meu nome sem eu revisar.
"""

RES_ESTILO = """# estilo-de-escrita.md — template (o seu tom, sem "cheiro de IA")

Use isto para o Claude escrever como você — e não como uma IA genérica.

## Como eu escrevo
- Frases curtas e diretas. Uma ideia por frase.
- Voz ativa. Concreto antes de abstrato.
- Português do Brasil, profissional mas humano.
- Abro com a conclusão/recomendação; depois o porquê.

## Evite (sinais de texto de IA)
- "Em um mundo cada vez mais...", "É importante destacar que...", "Não se trata apenas de..."
- Listas de três adjetivos só para encher ("robusto, escalável e inovador").
- Entusiasmo vazio e superlativos ("revolucionário", "incrível").
- Travessões em excesso e fechos genéricos ("Em resumo, ...").

## Exemplos do meu tom
> [Cole aqui 1-2 trechos curtos que VOCÊ escreveu — é a melhor calibragem.]
"""

RES_PROMPTS = """# Biblioteca de prompts — executivo

Modelos para colar e adaptar. Substitua o que estiver entre [colchetes].
Use apenas dados fictícios ou públicos.

## Resumir um relatório
Com base em [relatório], produza um resumo executivo de [n] tópicos: números-chave,
tendência e os 5 pontos de atenção. Cite a origem e liste o que devo verificar.

## Relatório → deck
Com base em [relatório] e [dados], crie uma apresentação de [n] slides para [público]:
destaques, tendências (com gráfico), riscos e recomendação. Gere o .pptx.

## Análise de concorrência
Compare [concorrentes] em receita, crescimento, margem e canal. Ranqueie a ameaça
para [empresa] e recomende movimentos. Marque [VERIFICAR] nos números externos.

## Pensar melhor (advogado do diabo / pre-mortem)
Aja como advogado do diabo e ataque esta tese: [tese]. Depois faça um pre-mortem:
"estamos em [ano] e [decisão] fracassou — o que deu errado?".

## Análise de mercado
Dimensione [mercado] (tamanho, crescimento, tendências) com fontes. Compare com a
posição de [empresa] e liste as perguntas que faltam responder. (Direcional: verificar.)

## Brief do dia (agenda + e-mail)
Com a agenda e o e-mail conectados (só leitura): minhas próximas 8h, os e-mails que
pedem ação minha e o que preparar antes de cada reunião. Uma tela.

## Memo de decisão
Escreva um memo de 1-2 páginas: situação, opções com prós/contras, recomendação e
o que pedimos, riscos. Marque [VERIFICAR] nos números externos.

## Gerar o entregável
Com base na nossa conversa, gere [memo/deck/planilha] pronto para download, com
[formato], para [público].
"""

RES_CHECKLIST = """# Checklist de governança de IA (executivo)

Ponto de partida para a conversa de board sobre uso responsável de IA.

## Dados e LGPD
- [ ] Há lista clara do que pode e do que não pode ser inserido em ferramentas de IA?
- [ ] Dados pessoais (clientes, colaboradores) só entram em ferramentas aprovadas e com base legal?
- [ ] Há minimização de dados e controle de retenção?

## Decisão e responsabilidade
- [ ] Decisões relevantes têm rastreabilidade e revisão humana?
- [ ] Nada é automatizado sem responsável nomeado?
- [ ] Números, fatos e fontes geradas por IA são verificados antes de uso externo?

## Conectores e MCP
- [ ] Conectamos apenas fontes aprovadas, com escopo mínimo (de preferência leitura)?
- [ ] Há processo para provisionar e revogar acessos?
- [ ] Conectores de terceiros passam por avaliação de segurança?

## Capacidade e valor
- [ ] Cada função sabe o que delegar e como revisar?
- [ ] Há pipeline de casos de uso com dono e métrica?
- [ ] O valor (tempo, qualidade, risco) é medido a cada trimestre?
"""


def build_skills_md():
    out = ["# Biblioteca de Skills — executivo\n",
           "Skills por papel. Cada uma tem NOME, DESCRIÇÃO (quando usar) e INSTRUÇÕES.",
           "Crie em Personalizar › Skills › “+ Criar skill”. Todas com a disciplina [VERIFICAR].\n"]
    for nome, papel, desc, instr in SKILLS:
        out.append("## " + nome + "  _(" + papel + ")_")
        out.append("**Descrição:** " + desc)
        out.append("**Instruções:** " + instr + "\n")
    return "\n".join(out) + "\n"


def build_referencia():
    b = ['<h1>Referência</h1>',
         '<p class="lede">Os apêndices do programa: o caso Aurora, os modelos do Claude, '
         "personalização, Skills, governança e onde confirmar o que está vigente.</p>"]
    bible = (P("Empresa, números e concorrentes são <strong>fictícios</strong>, criados "
               "apenas para o treinamento.")
             + P("<strong>" + g("Aurora", "Aurora S.A.") + ":</strong> varejista de bens de "
                 "consumo (eletrônicos, casa e estilo de vida), lojas + e-commerce, receita "
                 "~R$ 4,2 bi.")
             + table(["Indicador", "Leitura"],
                     [["Receita", "~R$ 4,1 bi, estável (crescimento desacelerou para negativo)."],
                      ["Margem bruta", "~34% → ~30,5%: sob pressão."],
                      ["Margem EBITDA", "~8,4%: ainda positiva, mas apertada."],
                      ["Digital", "E-commerce ~24% da receita e crescendo ~20%."],
                      ["Ameaça", "MercadoVivo cresce ~22% e ganha share (margem baixa)."],
                      ["Decisão em pauta", "Acelerar o digital/marketplace?"]]))
    b.append(details("Apêndice A — O caso Aurora S.A.", bible, tag="Caso"))
    models = (table(["Tier (referência)", "Use para"],
                    [["Haiku", "Triagem, resumos curtos, extração em volume."],
                     ["Sonnet", "A maioria do dia a dia: escrita, análise, documentos."],
                     ["Opus", "Documentos longos e decisões de alto risco."]])
              + callout("Comece no Sonnet; suba para o Opus em documento longo ou decisão "
                        "difícil; desça para o Haiku no volume simples. Os nomes mudam com o "
                        "tempo — confirme os atuais.", label="Regras práticas", kind="gold"))
    b.append(details("Apêndice B — Modelos do Claude", models, tag="Modelos"))
    pers = (H3("Preferências (todas as conversas)")
            + prompt("Sou [cargo] em [setor]. Prefiro respostas em português, diretas e\n"
                     "estruturadas, com a RECOMENDAÇÃO primeiro. Sempre liste o que eu devo\n"
                     "verificar. Não invente números; quando não souber, diga.",
                     label="Exemplo de preferências")
            + H3("Instruções de Projeto (só naquele Projeto)")
            + prompt("Este Projeto é do comitê executivo. Em memos, siga: situação; opções;\n"
                     "recomendação e o que pedimos; riscos. Marque [VERIFICAR] em todo número\n"
                     "de fonte externa.", label="Exemplo de instruções de Projeto"))
    b.append(details("Apêndice C — Personalização", pers, tag="Personalizar"))
    lib = P("Sete Skills prontas. Baixe o pacote em <a href='recursos.html'>Recursos</a> "
            "(<code>biblioteca-de-skills.md</code>).")
    for nome, papel, desc, instr in SKILLS:
        lib += render_skill(nome, papel, desc, instr)
    b.append(details("Apêndice D — Biblioteca de Skills por papel", lib, tag="Skills"))
    chk = (H3("Dados e LGPD")
           + P("Lista clara do que pode entrar? Dados pessoais só em ferramentas aprovadas? "
               "Minimização e retenção?")
           + H3("Decisão · Conectores · Valor")
           + P("Rastreabilidade e revisão humana? Nada automatizado sem responsável? Só "
               "fontes aprovadas, escopo mínimo? Pipeline com dono e métrica? Baixe o "
               "checklist completo em Recursos."))
    b.append(details("Apêndice E — Checklist de governança", chk, tag="Governança"))
    verify = P("O Claude evolui rápido: modelos, planos, limites e políticas mudam. Antes de "
               "aplicar, confirme nas fontes oficiais, nos materiais de prompting da Anthropic "
               "e na política interna de IA e LGPD da sua organização.")
    b.append(details("Apêndice F — Onde verificar", verify, tag="Verificar"))
    return page("Referência", "".join(b), active="referencia", depth=0)


def write_resources():
    d = os.path.join(ROOT, "arquivos")
    os.makedirs(d, exist_ok=True)
    gen = {
        "sobre-mim-template.md": RES_SOBRE,
        "estilo-de-escrita-template.md": RES_ESTILO,
        "biblioteca-de-prompts.md": RES_PROMPTS,
        "biblioteca-de-skills.md": build_skills_md(),
        "checklist-governanca-ia.md": RES_CHECKLIST,
    }
    for name, content in gen.items():
        with open(os.path.join(d, name), "w", encoding="utf-8") as f:
            f.write(content)
    missing = [f for f, _ in DATAROOM_FILES + FAC_FILES
               if not os.path.exists(os.path.join(d, f))]
    if missing:
        print("  AVISO: rode 'python3 gen_dataroom.py' — faltam:", ", ".join(missing))
    return list(gen)


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
    print("Pronto. Sirva com:  python3 -m http.server 8091")


if __name__ == "__main__":
    main()

