#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Construtor do treinamento "Dominando o Claude" (Programa Executivo • Seguro Garantia).
Gera o site estático interativo a partir do conteúdo do guia + slides da Bastião.
Rode:  python3 build.py     Sirva:  python3 -m http.server 8090
"""
import html as _html
import os
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
# Pasta com os materiais originais (guia, slides e dados de apoio)
SRC = os.path.join(os.path.dirname(ROOT), "junto")

# ---------------------------------------------------------------------------
# GLOSSÁRIO (definições curtas, no contexto de seguro garantia)
# ---------------------------------------------------------------------------
GLOSSARY = {
    "Projeto": "Uma pasta de contexto dentro do Claude: tudo o que você sobe ali fica disponível em todas as conversas daquele Projeto. Você não reenvia os arquivos a cada pergunta — e é onde ficam as instruções padrão do time.",
    "Contexto": "Tudo o que o Claude consegue enxergar agora — a conversa, os arquivos que você subiu e as instruções — somado ao conhecimento geral do treino. Sem o edital, o balanço e o público, a resposta sai genérica.",
    "Alucinação": "Quando o Claude afirma um número, uma cláusula ou uma citação que soam perfeitos e estão errados, com total convicção. Em subscrição, nada de valor ou cláusula avança sem verificação na fonte.",
    "Brief": "O pedido bem feito: contexto + tarefa + materiais + restrições + formato/público. A habilidade que mais melhora o resultado. Atalho que vale por todos: diga o público e o formato.",
    "Subscrição": "O processo de avaliar, aceitar e precificar um risco (underwriting). O subscritor lê documentos, cruza informações e decide aprovar, aprovar com condições ou recusar — e responde por isso.",
    "Tomador": "No seguro garantia, é quem contrata a garantia (ex.: a construtora) para assegurar ao beneficiário (o órgão/cliente) que vai cumprir o contrato. Se falhar, a seguradora indeniza ou assume a obra.",
    "Construtora Pilar": "Construtora Pilar Engenharia S.A. (fictícia) — o maior tomador da Bastião e o personagem central do caso. Pediu uma nova garantia de R$ 60 mi para uma obra rodoviária; tem crédito frágil (alavancagem ~4,8x, liquidez 0,9) e pode estourar o limite aprovado de R$ 180 mi.",
    "Seguro garantia": "Seguro que garante o cumprimento de uma obrigação contratual. Na Garantia de Execução de Contrato, a seguradora cobre o beneficiário caso o tomador não execute a obra ou serviço contratado.",
    "Sinistralidade": "De cada R$ 100 de prêmio que a seguradora recebe, quanto volta como indenização (sinistro). 42% = R$ 42 a cada R$ 100. Quanto mais alta, mais o risco está se materializando.",
    "Índice combinado": "De cada R$ 100 de prêmio, quanto sai no total — sinistros pagos + despesas da operação. 79% = saem R$ 79 e sobram R$ 21 de lucro. Abaixo de 100% a operação dá lucro; acima, dá prejuízo. Quanto menor, melhor.",
    "IS": "Importância Segurada — o valor máximo coberto por uma apólice. A taxa média ponderada pela IS dá mais peso às apólices grandes ao calcular quanto se cobra pelo risco.",
    "Exposição": "O total de risco que a seguradora assumiu — a soma das garantias em vigor. Medir exposição por setor, região e por tomador mostra onde a carteira está concentrada.",
    "Concentração": "O quanto da carteira está num mesmo setor, região ou tomador. Concentração alta (ex.: Construção e Sudeste) amplia o risco de muitos sinistros ao mesmo tempo.",
    "Perda esperada": "A estimativa de quanto, em média, uma garantia deve custar em sinistro — combina a chance de o tomador falhar com o valor exposto. É a base do prêmio mínimo.",
    "Rating": "A nota de crédito de um tomador (ex.: BB-). Quanto pior o rating, maior a chance de inadimplência e, portanto, maior a perda esperada e o prêmio.",
    "Retomada": "Cláusula de step-in: o direito de a seguradora assumir e concluir a obra (diretamente ou via terceiro) se o tomador falhar, em vez de só pagar uma indenização.",
    "Skill": "Um pacote reutilizável de instruções (e modelos) que ensina o Claude a fazer uma tarefa recorrente do SEU jeito, com consistência. Em vez de reescrever o brief toda semana, você empacota o padrão.",
    "MCP": "Model Context Protocol — o padrão aberto que liga o Claude a fontes e sistemas. No Claude aparece como Conectores: em vez de só trabalhar no que você cola, ele lê direto das fontes aprovadas.",
    "Conector": "A ponte que dá ao Claude acesso a uma fonte ou sistema (Drive, e-mail, Slack, ou um sistema interno via MCP), com a sua permissão e governança — de preferência só leitura.",
    "Haiku": "O modelo mais rápido e leve da família Claude. Bom para triagem, classificação de avisos, resumos curtos e extração de campos em volume.",
    "Sonnet": "O modelo versátil do dia a dia: escrita, análise, raciocínio de várias etapas e criação de documentos. É por onde você começa.",
    "Opus": "O modelo de raciocínio profundo: documentos longos e decisões de alto risco, como o parecer de subscrição a partir de edital + balanço.",
    "LGPD": "Lei Geral de Proteção de Dados. Dados pessoais de segurados, tomadores e terceiros só entram em ferramentas aprovadas e com base legal — vazamento é risco material e de board.",
    "Deep Research": "Modo em que o Claude pesquisa a web a fundo, cruzando muitas fontes para uma resposta abrangente — útil em due diligence e regulação, sempre com verificação das fontes.",
    "Cowork": "Recurso para delegar tarefas de conhecimento de várias etapas ao Claude, como a um assistente que executa um fluxo do início ao fim.",
    "Artefato": "Uma saída que o Claude gera e você pode visualizar/baixar — um documento, uma planilha, um deck, um app de uma página.",
    "Visão": "A capacidade de o Claude ler imagens: apólices e contratos escaneados, fotos e prints — útil para acervos não digitalizados.",
    "Cenário de estresse": "Um teste que pergunta “e se piorar?”: recalcula resultados sob uma hipótese adversa (ex.: a sinistralidade sobe para 48%) para medir a resiliência da carteira.",
}


def g(term, label=None):
    label = label or term
    d = GLOSSARY[term]
    return ('<span class="term">' + _html.escape(label)
            + '<span class="tip"><strong>' + _html.escape(term) + '</strong>'
            + _html.escape(d) + '</span></span>')


# ---------------------------------------------------------------------------
# Helpers de bloco
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
    """Chip de arquivo com link de download (../arquivos/<fname>)."""
    label = label or fname
    return ('<a class="filechip" data-file="' + fname + '" href="../arquivos/' + fname
            + '" download="' + fname + '">📎 ' + _html.escape(label)
            + ' <span class="dl">↓</span></a>')


def exfiles(files, label="Arquivos deste exercício"):
    """Linha com os arquivos que o aluno usa no exercício."""
    chips = "".join(fileref(f) for f in files)
    return ('<div class="exfiles"><span class="exfiles-label">' + _html.escape(label)
            + "</span>" + chips + "</div>")


print("helpers definidos.")

# ---------------------------------------------------------------------------
# Shell da página
# ---------------------------------------------------------------------------
DISCLAIMER = (
    "Caso fictício Bastião Seguradora S.A. — seguradora, tomadores, apólices e números são "
    "ilustrativos, criados apenas para o treinamento. Regra do dia: somente dados fictícios; "
    "nunca cole dados reais de tomadores, segurados ou pessoas (LGPD) em ferramentas não "
    "aprovadas pela empresa."
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
        '<span class="mark">Dominando o Claude</span></a>'
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
        '<p>' + DISCLAIMER + "</p>"
        '<p>' + DISCLAIMER2 + "</p>"
        '<div class="flinks">'
        '<a href="' + up + 'index.html">Início</a>'
        '<a href="' + up + 'modulos/index.html">Módulos</a>'
        '<a href="' + up + 'dicas.html">Dicas</a>'
        '<a href="' + up + 'recursos.html">Recursos</a>'
        '<a href="' + up + 'referencia.html">Referência</a>'
        "</div>"
        '<p style="font-size:0.8rem">Programa hands-on · alta liderança · '
        "versão interativa local.</p>"
        "</div></footer>"
    )


def page(title, body, active="", depth=0, wide=False):
    up = "../" if depth else ""
    wrapcls = "wrap-wide" if wide else "wrap"
    return (
        "<!DOCTYPE html>\n"
        '<html lang="pt-BR"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        "<title>" + _html.escape(title) + " · Dominando o Claude</title>"
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?'
        "family=Fraunces:ital,opsz,wght@0,9..144,400..700;1,9..144,400..600&"
        "family=Inter:wght@300..700&"
        'family=JetBrains+Mono:wght@400..700&display=swap" rel="stylesheet">'
        '<link rel="stylesheet" href="' + up + 'assets/styles.css">'
        "</head><body>"
        + nav(active, depth)
        + '<main><div class="' + wrapcls + '">' + body + "</div></main>"
        + footer(depth)
        + '<script src="' + up + 'assets/app.js"></script>'
        "</body></html>"
    )


print("shell definido.")

# ---------------------------------------------------------------------------
# Conteúdo dos módulos (conteúdo dos slides + exercícios mão na massa)
# ---------------------------------------------------------------------------
def m00():
    b = []
    b.append(P("Objetivo: conectar o tema ao que pesa na liderança de uma seguradora e "
               "instalar o modelo mental do dia."))
    b.append(H2("O trabalho da seguradora é ler, cruzar e julgar"))
    b.append(P("<strong>Ler</strong> — editais, contratos, condições gerais e balanços de "
               "tomadores; centenas de páginas. <strong>Cruzar</strong> — o " + g("Tomador", "tomador")
               + " contra a carteira, o edital contra as condições, o risco contra o limite. "
               "<strong>Julgar</strong> — subscrever, precificar, decidir o sinistro. É aqui "
               "que está o valor."))
    b.append(callout("O Claude faz a leitura e o cruzamento em minutos — e libera o time "
                     "para o julgamento, que continua sendo humano. O custo de não ter essa "
                     "fluência é competitivo, não tecnológico.", label="A ideia central", kind="gold"))
    b.append(H2("Trate o Claude como um analista sênior"))
    b.append(table(
        ["O que ele é", "O que isso significa"],
        [["Lê e organiza muito rápido", "Resume, extrai e estrutura grandes documentos em minutos."],
         ["Não conhece o seu contexto", "Não sabe da sua carteira, políticas e alçadas — a menos que você conte."],
         ["Pode errar com confiança", "Às vezes afirma um número ou cláusula errados com total convicção."],
         ["Você sempre revisa", "A entrega é um rascunho de analista. A decisão e a responsabilidade são suas."]]))
    b.append(P("Em " + g("Subscrição", "subscrição") + " isso é literal: ele lê e organiza; "
               "o subscritor decide e responde."))
    b.append(H2("O caso de hoje: Bastião e a Construtora Pilar"))
    b.append(P("Vamos usar o mesmo caso <strong>fictício</strong> o dia todo. A <strong>"
               "Bastião Seguradora</strong> é uma seguradora de médio porte especializada em "
               + g("Seguro garantia", "seguro garantia") + ". O personagem central é a "
               "<strong>" + g("Construtora Pilar", "Construtora Pilar Engenharia") + "</strong> "
               "— o maior " + g("Tomador", "tomador") + " da casa."))
    b.append(P("A Pilar pediu uma <strong>nova garantia de R$ 60 milhões</strong> para uma "
               "obra rodoviária. O dilema: o crédito dela é frágil (alavancagem ~4,8x, "
               "liquidez 0,9 — abaixo do exigido) e essa nova garantia pode <strong>estourar "
               "o limite aprovado</strong> de R$ 180 milhões. É sobre a Pilar que você vai "
               "ler o edital, calcular a exposição e escrever o parecer — então guarde esse "
               "nome."))
    b.append(callout("Todos os dados do caso (seguradora, tomadores, números) são fictícios, "
                     "criados só para o treinamento. O perfil completo está na página "
                     "<a href='../referencia.html'>Referência</a>.", label="Lembrete"))
    b.append(callout("“Não estou aprendendo a usar uma ferramenta. Estou aprendendo a "
                     "delegar a leitura e a revisar melhor a decisão.”", label="Frase para fixar", kind="gold"))
    return "".join(b)


def m01():
    b = []
    b.append(P("Um panorama rápido: o que é o Claude, o que ele faz e quais modelos existem."))
    b.append(H2("O que é o Claude"))
    b.append(P("O Claude é um assistente de inteligência artificial criado pela Anthropic — "
               "uma empresa de pesquisa focada em segurança de IA. Você conversa em "
               "linguagem natural e ele lê, escreve, analisa e raciocina sobre textos, "
               "documentos e dados. Princípio de design: ser útil, honesto e cuidadoso. "
               "Está disponível no navegador, no app, no celular e integrado a outras "
               "ferramentas."))
    b.append(details("Uma breve história",
                     table(["Quando", "O quê"],
                           [["2021", "A Anthropic é fundada, com foco em IA segura e confiável."],
                            ["2023", "O primeiro Claude é lançado ao público (março)."],
                            ["2024", "Chega a família de três modelos: Haiku, Sonnet e Opus."],
                            ["Hoje", "Geração 4.x, em evolução rápida."]]),
                     tag="Linha do tempo"))
    b.append(H2("O que o Claude faz"))
    b.append(table(["Capacidade", "Em seguros"],
                   [["Conversar e explicar", "Tirar dúvidas, explicar temas e ajudar a pensar."],
                    ["Ler e resumir documentos", "Editais, contratos, balanços e condições gerais."],
                    ["Analisar dados e planilhas", "Carteira, sinistralidade, concentração de risco."],
                    ["Pesquisar na web", "Notícias, regulação e due diligence — com fontes."],
                    ["Criar arquivos", "Pareceres em Word, planilhas, slides e PDFs."],
                    ["Ver imagens (" + g("Visão", "visão") + ")", "Ler documentos escaneados, fotos e prints."]]))
    b.append(P("E mais: " + g("Conector", "conectores") + " a sistemas internos, Claude no "
               "Excel e no PowerPoint, e o " + g("Cowork") + " para delegar tarefas de várias etapas."))
    b.append(H2("Os modelos do Claude"))
    b.append(P("O Claude vem em três “tamanhos” da mesma família — ferramentas para "
               "trabalhos diferentes."))
    b.append(table(["Modelo", "Quando usar"],
                   [[g("Haiku") + " — rápido e leve", "Triagem, resumos curtos, extração e classificação de avisos."],
                    [g("Sonnet") + " — o padrão versátil", "Escrita, análise, várias etapas e criação de documentos. Comece aqui."],
                    [g("Opus") + " — raciocínio profundo", "Documentos longos e decisões de alto risco. Ex.: o parecer de subscrição."]]))
    b.append(callout("Comece no Sonnet; suba para o Opus em documento longo ou decisão "
                     "difícil; use o Haiku no volume simples. O plano Free traz Haiku e "
                     "Sonnet; Pro e Max somam o Opus. (Confirme nomes, planos e limites "
                     "atuais — ver Referência.)", label="Regra prática", kind="gold"))
    return "".join(b)


def m02():
    b = []
    b.append(P("Objetivo: entender as três coisas que mais mudam a qualidade do que você obtém."))
    b.append(H2("Três verdades para usar bem"))
    b.append(P("<strong>1. " + g("Contexto", "Contexto é tudo") + ".</strong> O Claude só "
               "sabe o que está na conversa (mais o conhecimento geral do treino). Sem o "
               "edital, sem o balanço, sem o público, a resposta é genérica. Subir os "
               "documentos e dizer quem vai ler muda tudo."))
    b.append(P("<strong>2. Ele pode errar com confiança.</strong> A " + g("Alucinação", "alucinação")
               + ": parece certo e está errado. Em subscrição é inegociável — você é o "
               "subscritor responsável; nada de valor ou cláusula vai adiante sem "
               "verificação na fonte."))
    b.append(P("<strong>3. Ele é probabilístico.</strong> Pergunte duas vezes e terá "
               "variações — ótimo para gerar opções (cenários, condições, tons de carta) e "
               "exige cuidado quando você precisa de exatidão."))
    b.append(handson("Exercício 1 — Poder e limite", "Mão na massa",
                     prompt("Explique, em 4 frases, o que um subscritor de seguro garantia\n"
                            "olha para decidir sobre uma garantia de execução de contrato.\n"
                            "Depois, liste 3 afirmações suas das quais você tem MENOS\n"
                            "certeza e que eu deveria verificar.")
                     + details("Reflexão",
                               P("Ao pedir que o Claude apontasse as próprias incertezas, "
                                 "você já instalou o hábito mais importante do dia: olhar a "
                                 "resposta com senso crítico. Pergunte-se: o que ele explicou "
                                 "bem? E quais das três afirmações você precisaria conferir na "
                                 "fonte antes de levar adiante?"), tag="Reflexão")))
    return "".join(b)


def m03():
    b = []
    b.append(P("Objetivo: dominar a habilidade que mais melhora resultados — saber pedir. "
               "Um bom " + g("Brief", "brief") + " não é “escrever bonito”; é dar contexto, "
               "público e formato."))
    b.append(H2("Anatomia de um bom brief"))
    b.append(table(["Elemento", "Pergunta que responde", "Exemplo (Bastião)"],
                   [["Contexto / papel", "Quem é você e qual a situação?", "“Você assessora o comitê de subscrição de uma seguradora de garantia.”"],
                    ["Tarefa", "O que quero, exatamente?", "“Resuma o edital e aponte as exigências de garantia.”"],
                    ["Materiais", "Com base em quê?", "“Use o arquivo do dossiê de edital do Projeto.”"],
                    ["Restrições", "Que limites respeitar?", "“Máximo 1 página; marque o que eu devo verificar.”"],
                    ["Formato / público", "Para quem e em que forma?", "“Em tópicos, para o comitê de risco.”"]]))
    b.append(callout("Se só lembrar de uma coisa: diga o público e o formato.", label="O atalho que vale por todos", kind="gold"))
    b.append(H2("O salto de qualidade"))
    b.append('<div class="compare">'
             '<div class="col weak"><div class="k">Pedido fraco</div>'
             '<p>“Analise o edital.”</p><p style="color:var(--muted);font-size:.9rem">'
             'Resposta genérica, sem foco no que você decide.</p></div>'
             '<div class="col strong"><div class="k">Com brief</div>'
             '<p>“Resuma o edital em 6 tópicos para o comitê, destacando as cláusulas de '
             'garantia, e diga o que devo verificar.”</p>'
             '<p style="color:var(--muted);font-size:.9rem">Pronto para a reunião — e com o '
             'que conferir.</p></div></div>')
    b.append(H3("Iteração é vantagem"))
    b.append(P("“Mais curto, foque na recomendação.” · “Adicione o cenário pessimista.” · "
               "“Transforme em 6 tópicos de fala para o comitê.” · “Faça o papel de um "
               "auditor cético e ataque este parecer.”"))
    b.append(handson("Exercício 2 — Uma linha vs. um brief", "Mão na massa",
                     exfiles(["Bastiao_Edital_e_Tomador.md"])
                     + prompt("Fale sobre o edital da Bastião.", label="Versão fraca")
                     + prompt("Você assessora o comitê de subscrição da Bastião.\n"
                              "Com base no arquivo \"Bastiao_Edital_e_Tomador\" do Projeto,\n"
                              "resuma em até 6 tópicos as exigências de garantia do edital\n"
                              "(valor, modalidade, vigência, retomada, multas) para leitura\n"
                              "do comitê. Ao final, liste os pontos que eu devo conferir no\n"
                              "documento original antes de decidir.", label="Versão brief")
                     + details("Reflexão",
                               P("Compare as duas respostas que você obteve: o salto de "
                                 "qualidade está no próprio texto. A segunda chega pronta para "
                                 "a reunião e já diz o que conferir — e a única coisa que "
                                 "mudou foi o contexto que você deu. Era isso que você "
                                 "esperava?"), tag="Reflexão")))
    b.append(callout("Ao voltar do intervalo, deixe a planilha e os dois documentos abertos "
                     "no seu " + g("Projeto", "Projeto") + ".", label="Intervalo"))
    return "".join(b)


def m04():
    b = []
    b.append(P("Objetivo: rodar, com os dados da Bastião, os quatro trabalhos mais valiosos: "
               "ler o documento, calcular a carteira, medir risco e precificar — cada um com "
               "uma reflexão ao final."))
    b.append(H2("A carteira da Bastião, num relance"))
    b.append('<div class="stat-grid">'
             + stat("58% → 79%", "Índice combinado: ainda sobra lucro, mas a folga encolheu")
             + stat("22% → 42%", "Sinistralidade: mais prêmio voltando como sinistro")
             + stat("4,8x", "Alavancagem da Construtora Pilar (liquidez 0,9)")
             + stat("+ R$ 60 mi", "Garantia pedida — empurra a exposição acima do limite")
             + "</div>")
    b.append(callout(
        "Pense sempre em <strong>“de cada R$ 100 de prêmio que a seguradora recebe”</strong>:"
        "<br>• <strong>Sinistralidade</strong> — quanto volta como indenização. 42% = R$ 42. "
        "Quanto mais alto, mais o risco está “acontecendo”."
        "<br>• <strong>Índice combinado</strong> — quanto sai no total (sinistros + despesas). "
        "79% = saem R$ 79 e <strong>sobram R$ 21 de lucro</strong>. Abaixo de 100% dá lucro; "
        "acima, prejuízo — quanto menor, melhor."
        "<br>Os dois números contam a mesma história: a folga está encolhendo — antes sobrava "
        "mais, agora sobra menos.", label="Em português claro", kind="tip"))
    b.append(H2("4A — Ler um grande documento (o documento âncora)"))
    b.append(P("O dossiê tem edital, contrato e balanço do tomador. Transforme em leitura "
               "executiva — ela alimenta os números dos exercícios seguintes."))
    b.append(exfiles(["Bastiao_Edital_e_Tomador.md"]))
    b.append(prompt("Com base no arquivo \"Bastiao_Edital_e_Tomador\" do Projeto,\n"
                    "produza um resumo executivo de 1 página com: (1) objeto e prazo\n"
                    "do contrato; (2) exigências de garantia; (3) os 5 pontos de\n"
                    "atenção de risco mais relevantes que estejam \"escondidos\" no\n"
                    "texto. Cite a seção de onde tirou cada ponto."))
    b.append(details("Reflexão",
                     P("Repare como o Claude leu o documento inteiro e ancorou cada achado na "
                       "seção de origem — confira esses ponteiros. No seu resumo apareceram a "
                       "liquidez 0,9 abaixo do exigido, a alavancagem, as contingências e a "
                       "concentração de recebíveis? São esses os pontos que você levaria ao "
                       "comitê."), tag="Reflexão"))
    b.append(H2("4B — Analisar a carteira e calcular"))
    b.append(P("O trabalho quantitativo do dia a dia: tendências, médias e onde o preço não "
               "cobre o risco."))
    b.append(exfiles(["Bastiao_Carteira_Dados.xlsx"]))
    b.append(prompt("Use as abas \"Resumo da Carteira\" e \"Apólices\".\n"
                    "(1) Descreva a tendência de sinistralidade e índice combinado.\n"
                    "(2) Calcule o prêmio médio e a taxa média ponderada pela IS,\n"
                    "por ramo. (3) Aponte onde podemos estar cobrando barato pelo\n"
                    "risco. Gere um gráfico da sinistralidade por trimestre."))
    b.append(callout("Confira as fórmulas e os números na planilha antes de citar. A IA "
                     "computa; o executivo interpreta.", label="Cuidado — confira os cálculos", kind="warn"))
    b.append(H2("4C — Risco e concentração"))
    b.append(prompt("Use as abas \"Apólices\" e \"Tomadores\". Calcule a exposição\n"
                    "total por setor e por região e o % concentrado em Construção\n"
                    "e no Sudeste. Liste os tomadores acima do limite aprovado.\n"
                    "Por fim, calcule o efeito da nova garantia de R$ 60 mi da\n"
                    "Pilar sobre a exposição e o limite dela."))
    b.append(details("Reflexão",
                     P(g("Concentração", "Concentração") + " e " + g("Exposição", "exposição")
                       + " vs. limite são o vocabulário de risco que vai ao comitê. Olhe o seu "
                       "resultado: a nova garantia de R$ 60 mi faz a "
                       + g("Construtora Pilar", "Pilar") + " estourar o limite? "
                       "É esse número que muda a sua decisão."), tag="Reflexão"))
    b.append(H2("4D — Precificação e cenário de estresse"))
    b.append(prompt("Dois cálculos:\n"
                    "(1) Cenário de estresse: se a sinistralidade do próximo\n"
                    "trimestre subir para 48%, recalcule o índice combinado e o\n"
                    "resultado de subscrição (mantendo as despesas).\n"
                    "(2) Precificação: para a garantia de R$ 60 mi da Pilar\n"
                    "(rating BB-), estime a perda esperada e o prêmio mínimo\n"
                    "para cobri-la com margem. Liste as premissas que usou."))
    b.append(callout("Cenário e preço são o coração da agenda do executivo — mas a "
                     "precificação aqui é direcional. Valide com a atuária e trate os "
                     "números como rascunho. Peça sempre as premissas.", label="Cuidado — precificação é direcional", kind="warn"))
    b.append(details("Bônus (se sobrar tempo) — traduzir as condições gerais",
                     exfiles(["Bastiao_Condicoes_Gerais.md"])
                     + prompt("Com base no arquivo \"Bastiao_Condicoes_Gerais\", explique em\n"
                            "linguagem simples o que está e o que não está coberto, e\n"
                            "extraia as exclusões e as obrigações em listas separadas."),
                     tag="Bônus"))
    b.append(callout("Quer dados mais realistas? O Módulo 05 (Data room &amp; verificação) "
                     "usa uma planilha bem maior — centenas de apólices, série multi-ano, "
                     "sinistros e limites — e treina você a <strong>pegar os erros</strong> "
                     "que o Claude (e os dados) podem trazer.", label="A seguir", kind="gold"))
    return "".join(b)


def m05():
    b = []
    b.append(P("Objetivo: produzir, do documento ao entregável final, algo que o "
               "participante reconheça como trabalho de verdade. Cada um (ou dupla) escolhe "
               "uma trilha."))
    b.append(H2("Escolha sua trilha — quatro entregáveis, um por papel"))
    b.append(table(["Trilha", "Para o papel de", "Entregável"],
                   [["Parecer de subscrição", "Subscrição / Risco", "Parecer de 1-2 páginas sobre a garantia da Pilar, com recomendação e condições."],
                    ["Resumo de sinistros ao comitê", "Sinistros / Diretoria", "Súmula dos sinistros em aberto e proposta de prioridades."],
                    ["Memo de risco ao board", "CEO / Risco / Atuária", "1 página sobre sinistralidade e concentração, com um cenário de estresse."],
                    ["Comunicação ao tomador", "Comercial / CX", "Carta de aprovação condicionada ou de recusa, em dois tons."]]))
    b.append(H2("Cinco passos do brief ao entregável (qualquer trilha)"))
    b.append(table(["#", "Passo", "O que fazer"],
                   [["1", "Brief", "Contexto + tarefa + materiais + público + formato."],
                    ["2", "Rascunho", "Gere o primeiro e leia criticamente."],
                    ["3", "Iterar", "“Mais curto”, “adicione o cenário de baixa”, “inclua condições”."],
                    ["4", "Autocrítica", "“Aponte 3 fraquezas e os números/cláusulas a checar.”"],
                    ["5", "Entregar", "Peça o documento, a planilha ou os slides para download."]]))
    b.append(handson("Brief do parecer de subscrição", "Exemplo · trilha de subscrição",
                     exfiles(["Bastiao_Edital_e_Tomador.md", "Bastiao_Carteira_Dados.xlsx"])
                     + prompt("Você assessora o comitê de subscrição da Bastião. Com base no\n"
                            "dossiê do edital e nas abas Tomadores e Apólices do Projeto,\n"
                            "escreva um parecer de 1-2 páginas com: (1) resumo do risco;\n"
                            "(2) crédito do tomador (alavancagem, liquidez, contingências);\n"
                            "(3) cláusulas-chave do edital (valor, retomada, vigência, multas);\n"
                            "(4) concentração vs. limite aprovado; (5) recomendação clara\n"
                            "(aprovar / aprovar com condições / recusar) e as condições.\n"
                            "Marque com [VERIFICAR] todo número que dependa de fonte externa.\n"
                            "Depois, gere o parecer como documento para download.")))
    b.append(H2("Artifacts — uma ferramenta interativa, não só um texto"))
    b.append(P("Nem todo entregável é um documento. Um <strong>artifact</strong> é uma peça "
               "interativa que o Claude monta e você abre ali mesmo — uma calculadora, um "
               "painel, um gráfico, um simulador — e que dá para compartilhar com o time."))
    b.append(handson("Construa um painel de exposição", "Mão na massa · Artifacts",
                     exfiles(["Bastiao_DataRoom.xlsx"])
                     + prompt("Com os dados desta planilha, crie um painel interativo (artifact)\n"
                              "de uma página: exposição por setor e região, % de concentração\n"
                              "vs. os tetos da casa, e os tomadores acima do limite. Inclua um\n"
                              "filtro por ramo e destaque em vermelho quem estoura o limite.")
                     + details("Reflexão",
                               P("Repare que você ganhou uma <em>ferramenta</em>, não um "
                                 "relatório estático — dá para filtrar e explorar na hora. "
                                 "Pergunte-se: qual número que você hoje pede “de novo, com "
                                 "outro corte” poderia virar um painel que você mesmo mexe?"),
                               tag="Reflexão")))
    b.append(details("Reflexão",
                     P("Pare um instante e pergunte-se: quanto tempo isto teria levado sem o "
                       "Claude? E — mais importante — onde o <strong>seu</strong> julgamento "
                       "foi insubstituível? Foi você quem decidiu o que aceitar, o que "
                       "corrigir e o que verificar. Essa é a parte que continua sua."),
                     tag="Reflexão"))
    return "".join(b)


def m06():
    b = []
    b.append(P("Um tour pelos recursos que tiram o uso do “básico”: personalizar o Claude, "
               "usar " + g("Skill", "Skills") + " prontas e construir a sua."))
    b.append(H2("Deixe o Claude do seu jeito — três níveis"))
    b.append(table(["Nível", "Alcance", "Exemplo (Bastião)"],
                   [["Preferências", "Valem para todas as conversas", "“Recomendação primeiro, depois os porquês. Nunca invente números.”"],
                    ["Instruções de Projeto", "Valem só naquele " + g("Projeto", "Projeto"), "A estrutura padrão do parecer e a política de alçada do time."],
                    ["Estilos", "O jeito de escrever", "Um estilo “Parecer Bastião” treinado em pareceres antigos."]]))
    b.append(callout("Exemplos copiáveis de preferências e instruções de Projeto estão na "
                     "página Referência (Apêndice de personalização).", label="Dica"))
    b.append(H2("Skills: ensine um fluxo uma vez"))
    b.append(P("Uma " + g("Skill", "Skill") + " é um pacote reutilizável de instruções que "
               "ensina o Claude a fazer uma tarefa recorrente do seu jeito. Você já usou "
               "hoje: ao gerar o parecer em Word ou um deck, foram as Skills de documentos "
               "(Word, Excel, PowerPoint, PDF — prontas, da Anthropic)."))
    b.append(callout("(1) Configurações › Capacidades: ligue “Execução de código e criação "
                     "de arquivos”. (2) Personalizar › Skills: ative as que quiser. Pronto: "
                     "o Claude usa a Skill sozinho quando faz sentido — você não precisa "
                     "“chamar”.", label="Como ligar"))
    b.append(handson("Use uma Skill pronta", "Mão na massa · Skills prontas",
                     P("Com as Skills de documentos ligadas, peça:")
                     + prompt("Crie uma apresentação de 5 slides resumindo a análise da\n"
                              "carteira da Bastião: tendência de sinistralidade, as maiores\n"
                              "concentrações e a decisão da Pilar — para o comitê de risco.")))
    b.append(handson("Construa a sua primeira Skill", "Mão na massa · construa a sua",
                     P("Passos: (1) ligue a execução de código; (2) Personalizar › Skills › "
                       "“+ Criar skill”; (3) dê um nome e uma descrição curta — é o que diz "
                       "ao Claude QUANDO usar; (4) escreva as instruções; (5) teste com um "
                       "caso real e ajuste a descrição até a Skill “aparecer” sozinha.")
                     + prompt("Nome: Parecer de Subscrição Padrão Bastião\n"
                              "Descrição: Use para redigir pareceres de subscrição de seguro\n"
                              "garantia no formato e na política de alçada da casa.\n"
                              "Instruções: siga a estrutura — (1) resumo do risco; (2) crédito\n"
                              "do tomador; (3) cláusulas-chave do edital; (4) concentração vs.\n"
                              "limite; (5) recomendação e condições. Marque [VERIFICAR] em todo\n"
                              "número de fonte externa. Tom objetivo; 1-2 páginas.",
                              label="Cole como base da sua Skill")))
    b.append(callout("Preparamos uma <strong>biblioteca de Skills por papel</strong> "
                     "(resumo de edital, parecer, análise de crédito, checagem de "
                     "concentração, súmula de sinistro, memo ao board, carta ao tomador, "
                     "tradução de cláusula) — todas com a disciplina do [VERIFICAR]. Veja a "
                     "página <a href='../referencia.html'>Referência</a> e baixe o pacote em "
                     "<a href='../recursos.html'>Recursos</a> (<code>biblioteca-de-skills.md"
                     "</code>).", label="Biblioteca de Skills", kind="gold"))
    return "".join(b)


def m07():
    b = []
    b.append(P("Ligar o Claude às suas fontes e sistemas — com governança."))
    b.append(H2("MCP: conecte o Claude às fontes"))
    b.append(P("O " + g("MCP") + " é o padrão aberto que liga o Claude às suas fontes e "
               "sistemas — no Claude, aparece como " + g("Conector", "Conectores") + ". Em vez "
               "de só trabalhar no que você cola, ele lê direto das fontes aprovadas."))
    b.append(table(["Exemplos de conexão", "Como conectar"],
                   [["Google Drive, e-mail e agenda", "Personalizar › Conectores (ou o “+” no chat): escolha um pronto do diretório."],
                    ["Slack, GitHub, Jira, Salesforce", "Ou “Adicionar conector” com a URL do servidor; autentica via OAuth."],
                    ["Sistemas internos de apólices/sinistros e BI (via conector personalizado)", "Ligue/desligue por conversa no “+”."]]))
    b.append(H2("Exemplo real — mcp-brasil"))
    b.append(P("O mcp-brasil é um servidor MCP aberto que conecta o Claude a ~70 fontes "
               "públicas oficiais do Brasil (mais de 500 ferramentas). Para o seguro "
               "garantia é ouro: dá para puxar o edital e checar o tomador em fontes oficiais."))
    b.append(table(["Fonte", "Útil para subscrição"],
                   [["PNCP / Compras", "Editais e contratos públicos."],
                    ["Transparência e TCU", "Sanções e empresas inidôneas."],
                    ["DataJud", "Processos e litígios do tomador."],
                    ["BrasilAPI", "CNPJ e dados cadastrais."],
                    ["Banco Central", "Selic, IPCA, câmbio (para precificação)."]]))
    b.append(callout("Roda via Python (uvx) no Claude Desktop ou no Claude Code. Para o "
                     "app/web, o TI publica o servidor num endereço HTTPS e o provisiona "
                     "como conector da organização; depois cada pessoa o liga no “+”. A "
                     "maioria das fontes não exige chave.", label="Como conectar (com o TI)"))
    b.append(handson("Subscrição com dados públicos", "Mão na massa · dados públicos",
                     P("Com o mcp-brasil conectado (o TI/facilitador deixa pronto), peça:")
                     + prompt("Busque no PNCP uma licitação recente de obra de infraestrutura\n"
                              "e resuma objeto, valor e a garantia exigida. Depois, para uma\n"
                              "construtora de capital aberto à sua escolha, traga dados\n"
                              "cadastrais (CNPJ) e verifique sanções públicas; e puxe a Selic\n"
                              "e o IPCA dos últimos 12 meses para a precificação.")
                     + callout("Tudo é dado público oficial — ainda assim, confirme nas "
                               "fontes e nunca cole dados confidenciais de tomadores.",
                               label="Cuidado", kind="warn")))
    b.append(handson("Planeje, não conecte", "Mão na massa · planejamento",
                     P("Hoje não conectamos dados reais. Liste 3 fontes internas que valeria "
                       "conectar via MCP, o ganho de cada uma e o portão de governança (quem "
                       "aprova e qual escopo).")))
    b.append(callout("Só fontes aprovadas; OAuth e escopo mínimo (de preferência leitura), "
                     "com revogação fácil; em Team/Enterprise um Owner provisiona e cada um "
                     "conecta com o seu acesso; o Claude acessa da nuvem da Anthropic, então "
                     "sistemas internos precisam estar acessíveis (allowlist); respeite a "
                     + g("LGPD") + " e o sigilo.", label="MCP com governança", kind="gold"))
    return "".join(b)


def m08():
    b = []
    b.append(P("O verdadeiro papel da liderança com IA é governá-la. Aqui calibramos "
               "confiança e disciplina."))
    b.append(H2("Ele pode errar com confiança"))
    b.append(P("Nunca leve adiante um número, uma cláusula ou uma fonte que você não "
               "verificou. A IA acelera o rascunho; a responsabilidade pela verdade — e pela "
               "subscrição — continua sua."))
    b.append(callout("Peça ao Claude um dado obscuro e específico (uma estatística de nicho, "
                     "uma citação) e mostre à turma como pode vir plausível e errado — uma "
                     + g("Alucinação", "alucinação") + " ao vivo.", label="Demonstração"))
    b.append(H2("Dados, sigilo e LGPD — o que pode entrar nas ferramentas"))
    b.append(table(["Nível", "O que é"],
                   [["✅ Seguro", "Informação pública, dados fictícios, rascunhos sem dados de pessoas."],
                    ["⚠️ Cautela / aprovação", "Dados de segurados, balanços não públicos, sinistros, segredos comerciais."],
                    ["⛔ Risco material", "Tudo que for dado pessoal ou confidencial em ferramenta não aprovada."]]))
    b.append(callout("Vazamento é risco material e de " + g("LGPD") + ". Existem versões "
                     "corporativas com políticas de retenção e privacidade próprias — "
                     "confirme qual a empresa aprovou.", label="Por que é tema de board", kind="warn"))
    b.append(H2("Governar, não só usar"))
    b.append(P("<strong>Regulação e responsabilidade:</strong> decisões de subscrição e "
               "sinistro precisam de rastreabilidade e revisão humana; nunca automatize "
               "negativa de cobertura sem um responsável nomeado; o Claude não substitui "
               "parecer jurídico ou atuarial — é insumo; um humano nomeado responde por cada "
               "decisão apoiada por IA."))
    b.append(P("<strong>Liderar a organização:</strong> a pergunta do C-level não é “como eu "
               "uso”, e sim “como faço a organização usar bem”. Quatro alavancas:"))
    b.append(table(["Alavanca", "O que significa"],
                   [["Política e ferramentas aprovadas", "Lista clara do que pode/não pode e quais ferramentas usar."],
                    ["Capacitação por papel", "Cada função sabe o que delegar e como revisar."],
                    ["Pipeline de casos de uso", "Cada caso com dono e métrica — nada de “teatro de IA”."],
                    ["Medição trimestral", "Tempo, qualidade e risco medidos a cada trimestre."]]))
    b.append(callout("O checklist completo de governança está na página Referência — é o "
                     "ponto de partida para a conversa de board.", label="Leve com você"))
    return "".join(b)


def m09():
    b = []
    b.append(P("Cada participante sai com três compromissos concretos."))
    b.append(H2("Plano 30-60-90 — três compromissos"))
    b.append(table(["Horizonte", "Compromisso", "Exemplo"],
                   [["Esta semana", "1 tarefa para delegar ao Claude", "Resumir os editais da semana antes do comitê."],
                    ["Este mês", "1 processo da sua área para melhorar", "Padronizar o parecer de subscrição (instruções de Projeto)."],
                    ["Este trimestre", "1 capacidade para construir no time", "Definir política de dados/LGPD e treinar a subscrição."]]))
    b.append(callout("“Não estou aprendendo a usar uma ferramenta. Estou aprendendo a "
                     "delegar a leitura e a revisar melhor a decisão.”", label="Encerramento", kind="gold"))
    b.append(P("Leve com você a <a href='../recursos.html'>biblioteca de prompts</a> e o "
               "<a href='../referencia.html'>checklist de governança</a>. Reforce a postura "
               "de subscritor responsável e a regra dos dados."))
    return "".join(b)


# ---------------------------------------------------------------------------
# NOVOS módulos (aprofundamentos)
# ---------------------------------------------------------------------------
def m_dataroom():
    b = []
    b.append(P("Até aqui usamos uma planilha enxuta. Agora vem o teste de verdade: um "
               "<strong>data room</strong> — vários arquivos, centenas de linhas, dados "
               "bagunçados e, de propósito, <strong>alguns erros e lacunas plantados</strong>. "
               "É onde o Claude mostra força — e onde a sua disciplina de verificação ganha dentes."))
    b.append(callout("Baixe na página Recursos: <code>Bastiao_DataRoom.xlsx</code> (8 abas: "
                     "Resumo da Carteira, Apólices, Tomadores, Sinistros, Triângulo de "
                     "Desenvolvimento, Limites e Alçada, Macro) e os documentos "
                     "<code>Bastiao_Editais_Comparacao.md</code> e "
                     "<code>Bastiao_Balancos_Tomadores.md</code>. Suba todos no seu "
                     + g("Projeto", "Projeto") + ".", label="Antes de começar"))
    b.append(exfiles(["Bastiao_DataRoom.xlsx", "Bastiao_Editais_Comparacao.md",
                      "Bastiao_Balancos_Tomadores.md"]))
    b.append(H2("Ler muitos dados de uma vez"))
    b.append(prompt("Você é analista de subscrição da Bastião. Com base na planilha\n"
                    "Bastiao_DataRoom.xlsx, dê um panorama da carteira em 8 tópicos:\n"
                    "tendência de sinistralidade e índice combinado, prêmio total por ramo,\n"
                    "as 3 maiores concentrações (setor, região, tomador) e os tomadores\n"
                    "acima do limite. Gere um gráfico da sinistralidade por trimestre."))
    b.append(H2("Cruzar documentos — a rotina real de subscrição"))
    b.append(P("Subscrição de verdade cruza edital × balanço × carteira. Force esse cruzamento:"))
    b.append(prompt("Cruze três fontes do Projeto: o pedido de R$ 60 mi da Construtora Pilar\n"
                    "(Bastiao_Editais_Comparacao.md, Edital A), o crédito dela\n"
                    "(Bastiao_Balancos_Tomadores.md) e a exposição atual na aba \"Tomadores\".\n"
                    "A nova garantia faz a Pilar estourar o limite aprovado? O crédito sustenta\n"
                    "o pedido? Dê uma recomendação preliminar e marque [VERIFICAR] nos números\n"
                    "que dependem de balanço auditado."))
    b.append(handson("Exercício — pegue o erro do Claude (auditoria de qualidade)",
                     "Mão na massa · verificação",
                     P("Este data room tem inconsistências e lacunas <strong>de propósito</strong>. "
                       "Antes de confiar em qualquer número, peça uma auditoria:")
                     + prompt("Faça uma auditoria de qualidade dos dados de Bastiao_DataRoom.xlsx\n"
                              "antes de eu usar qualquer número. Liste: (1) células onde o valor\n"
                              "calculado não bate (ex.: Prêmio ≠ IS × Taxa; Sinistralidade ≠\n"
                              "Sinistros ÷ Prêmio; Índice Combinado em branco); (2) valores\n"
                              "faltando ou em formato inconsistente (datas, texto onde devia ser\n"
                              "número); (3) duplicidades; (4) classificações suspeitas (tomador\n"
                              "acima do limite marcado como dentro). Para cada achado, diga a aba,\n"
                              "a referência e a correção sugerida.")
                     + details("Reflexão",
                               P("Este data room tem, de propósito, <strong>alguns problemas "
                                 "plantados</strong> — somas que não batem, células em branco, "
                                 "um texto onde deveria haver número, uma data fora do padrão, "
                                 "uma duplicidade e uma classificação de limite errada. "
                                 "Quantos você (e o Claude) conseguiram pegar? Não se preocupe "
                                 "em achar todos — o que importa é sair daqui com o hábito: "
                                 "<strong>pedir a auditoria e conferir na fonte antes de usar "
                                 "qualquer número</strong>.")
                               + callout("A lição do dia, em uma frase: a IA acelera a leitura "
                                         "— a verificação continua sua. Em subscrição, nenhum "
                                         "número vai ao comitê sem ser conferido na fonte.",
                                         label="Por que isso importa", kind="warn"),
                               tag="Reflexão")))
    return "".join(b)


def m_execcases():
    b = []
    b.append(P("O parecer é só um dos entregáveis. O executivo também prepara comitês, "
               "compara opções, transforma reunião em ação e <strong>itera</strong> até "
               "ficar bom. Quatro movimentos que cabem em qualquer área."))
    b.append(H2("1) Preparar o comitê — de 40 páginas a 6 falas"))
    b.append(prompt("Com base no resumo executivo do edital e na análise da carteira que\n"
                    "fizemos, prepare a minha participação no comitê: (1) 6 tópicos de fala\n"
                    "de 20 segundos cada; (2) as 3 perguntas difíceis que vão me fazer e\n"
                    "como responder; (3) um slide-resumo com a recomendação. Tom objetivo."))
    b.append(H2("2) Ranqueamento comparativo"))
    b.append(exfiles(["Bastiao_Balancos_Tomadores.md", "Bastiao_Carteira_Dados.xlsx"]))
    b.append(prompt("Use Bastiao_Balancos_Tomadores.md e a aba \"Tomadores\". Ranqueie os\n"
                    "quatro tomadores do melhor para o pior crédito, em tabela, com uma\n"
                    "justificativa por linha (alavancagem, liquidez, contingências,\n"
                    "concentração) e uma recomendação (aprovar / com condições / recusar)."))
    b.append(H2("3) Reunião → ação"))
    b.append(prompt("Vou colar as notas da reunião do comitê de risco. Extraia: decisões\n"
                    "tomadas, pendências (com responsável e prazo) e os pontos que ficaram\n"
                    "em aberto. Depois, rascunhe o e-mail de follow-up para o time —\n"
                    "me devolva aqui, não envie. [cole as notas abaixo]"))
    b.append(H2("4) O loop: ver → criticar → iterar"))
    b.append(P("O movimento que separa o amador do profissional: em vez de aceitar o "
               "primeiro rascunho, faça o Claude <strong>criticar a própria entrega</strong> "
               "e refazer. Você revisa o julgamento, não o texto."))
    b.append(handson("Exercício — itere um parecer até ficar de comitê",
                     "Mão na massa · loop",
                     P("Pegue o parecer da " + g("Construtora Pilar", "Pilar")
                       + " (ou gere um) e rode o loop pelo menos duas vezes:")
                     + prompt("Aja como um auditor cético de subscrição e ataque este parecer:\n"
                              "aponte as 3 fraquezas mais sérias, os números que faltam\n"
                              "[VERIFICAR] e onde a recomendação está frágil. Depois, reescreva\n"
                              "o parecer corrigindo o que você mesmo apontou.")
                     + details("Reflexão",
                               P("Repare quanto você digitou (pouco) e quanto mudou (muito): o "
                                 "trabalho aconteceu no loop entre você e o artefato. "
                                 "Pergunte-se: quanto tempo isto teria levado sem o Claude? E "
                                 "onde o seu julgamento foi insubstituível?"),
                               tag="Reflexão")))
    return "".join(b)


def m_projetos():
    b = []
    b.append(P("Você já vem usando um " + g("Projeto", "Projeto") + " hoje. Agora a estratégia: "
               "o Projeto é o <strong>cérebro compartilhado do time</strong> — e usá-lo bem é "
               "o que faz a IA <em>compor</em> em vez de recomeçar do zero a cada conversa."))
    b.append(H2("Três camadas de memória"))
    b.append(table(["Camada", "O que é", "Analogia"],
                   [["Arquivo solto", "Um documento que você cola numa conversa; vale só ali.", "Um post-it na mesa do colega."],
                    ["Projeto", "Pasta de contexto + instruções + arquivos, compartilhada pelo time.", "O manual do time."],
                    [g("Skill", "Skill"), "Um processo da casa que o Claude aplica sozinho quando reconhece a tarefa.", "Um procedimento da empresa."]]))
    b.append(P("As três se somam. O Projeto é onde a maior parte do valor de uma seguradora "
               "se acumula, porque o contexto fica disponível para todas as conversas — sem "
               "reenviar arquivo nenhum."))
    b.append(H2("A estratégia: um Projeto por domínio de decisão"))
    b.append(P("Em vez de um Projeto genérico, crie um por <strong>decisão recorrente</strong> "
               "— por exemplo “Comitê de Subscrição — Garantia de Execução”. Dentro dele:"))
    b.append(table(["O que colocar", "Por quê"],
                   [["Condições gerais + política de alçada", "O Claude responde sempre dentro das regras da casa."],
                    ["Template do parecer e do memo", "Saída padronizada, pronta para auditoria e comitê."],
                    ["Glossário interno e últimas decisões", "Coerência com o histórico; menos retrabalho."],
                    ["Instruções de Projeto", "Impõem o padrão — estrutura, tom e a regra do [VERIFICAR]."]]))
    b.append(callout("Exemplo de instruções de Projeto (cole em Configurações do Projeto): "
                     "“Este Projeto é da subscrição de Garantia de Execução. Use sempre as "
                     "condições gerais e a política de alçada anexadas. Em pareceres, siga a "
                     "estrutura: risco · crédito · cláusulas · concentração vs. limite · "
                     "recomendação. Marque [VERIFICAR] em todo número de fonte externa.”",
                     label="Instruções de Projeto", kind="gold"))
    b.append(handson("Exercício — monte um data-room Project", "Mão na massa · Projetos",
                     P("(1) Crie um Projeto “Comitê de Subscrição — Bastião”. (2) Suba todos "
                       "os arquivos do caso (data room, editais, balanços, condições gerais, "
                       "circular). (3) Cole as instruções de Projeto acima. (4) Faça três "
                       "perguntas que só funcionam porque o contexto está carregado:")
                     + exfiles(["Bastiao_DataRoom.xlsx", "Bastiao_Edital_e_Tomador.md",
                                "Bastiao_Condicoes_Gerais.md", "Bastiao_Circular_Regulatoria.md",
                                "Bastiao_Editais_Comparacao.md", "Bastiao_Balancos_Tomadores.md"],
                               label="Suba estes no Projeto")
                     + prompt("1) Qual a nossa exposição total em Construção e quanto sobra\n"
                              "   até o teto de concentração do setor?\n"
                              "2) Dado o pedido da Pilar, redija o parecer no nosso formato\n"
                              "   padrão (sem eu reexplicar a estrutura).\n"
                              "3) O que a Circular 47/2025 muda na decisão da Pilar?")
                     + details("Reflexão",
                               P("Você não reenviou nenhum arquivo nem reexplicou o formato — "
                                 "o Projeto já sabia. Esse é o salto: o conhecimento "
                                 "<strong>acumula</strong>. A regra prática para levar: toda "
                                 "resposta que valha a pena vira uma nota no Projeto; a próxima "
                                 "pergunta começa de um patamar mais alto."), tag="Reflexão")))
    b.append(callout("Governança do Projeto: defina um dono, o que pode (e não pode) entrar "
                     "(dados aprovados, nada de dado pessoal sem base legal) e uma cadência de "
                     "revisão. Um Projeto compartilhado é poderoso — e por isso precisa de "
                     "regra clara de acesso.", label="Governança", kind="warn"))
    return "".join(b)


def m_cowork():
    b = []
    b.append(P("Até aqui você conversou com o Claude no navegador. O <strong>Cowork</strong> "
               "é o aplicativo de desktop que vive na sua máquina: ele lê os seus arquivos "
               "reais, cria documentos reais na sua pasta e executa tarefas de várias etapas "
               "— como um assistente que trabalha ao seu lado."))
    b.append(H2("O que muda com o Cowork"))
    b.append(table(["Recurso", "O que significa"],
                   [["Lê os arquivos reais", "Aponte uma pasta com editais, balanços e a carteira — ele trabalha sobre os arquivos, não sobre o que você cola."],
                    ["Cria arquivos de verdade", "Gera <code>.docx</code>, <code>.xlsx</code> e <code>.pptx</code> direto na sua pasta — o parecer, a planilha, o deck."],
                    ["Faz tarefas de várias etapas", "Você delega um fluxo do início ao fim e revisa o resultado."]]))
    b.append(callout("O Cowork lê e escreve nos seus arquivos de verdade. Use só uma pasta "
                     "com <strong>dados aprovados/fictícios</strong> — nunca aponte para "
                     "pastas com dados de pessoas ou de tomadores sem base legal.",
                     label="Governança", kind="warn"))
    b.append(H2("Deixe o Claude te entrevistar"))
    b.append(P("Em vez de tentar escrever o brief perfeito, peça que ele pergunte primeiro — "
               "ele costuma fazer melhores perguntas do que as que você faria sozinho."))
    b.append(prompt("Antes de escrever o parecer da Pilar, me faça as perguntas que você\n"
                    "precisa para fazer um bom trabalho — uma de cada vez. Quando tiver o\n"
                    "suficiente, escreva o parecer no nosso formato e salve como .docx na pasta."))
    b.append(H2("Arquivos de contexto: um bom arquivo vale mais que 50 uploads"))
    b.append(P("Dois arquivos curtos, deixados na pasta, mudam todas as respostas: um diz "
               "<strong>quem você é</strong> e o <strong>seu contexto</strong>; o outro fixa o "
               "<strong>seu tom</strong> (e tira o “cheiro de IA”)."))
    b.append(exfiles(["sobre-mim-template.md", "estilo-de-escrita-template.md"]))
    b.append(prompt("Leia sobre-mim.md e estilo-de-escrita.md. Daqui pra frente, escreva tudo\n"
                    "no meu tom e considerando o meu papel e contexto — sem eu precisar repetir."))
    b.append(callout("As <strong>Instruções globais</strong> são a versão “sempre ligada” "
                     "disso: uma configuração única (em Preferências) que o Claude lê antes de "
                     "toda tarefa. Veja o Módulo de Personalização.", label="Dica"))
    b.append(handson("Gere um entregável real, de ponta a ponta", "Mão na massa · Cowork",
                     exfiles(["Bastiao_Edital_e_Tomador.md", "Bastiao_Carteira_Dados.xlsx"])
                     + prompt("Com os arquivos desta pasta, escreva o parecer de subscrição da\n"
                              "Pilar no nosso formato e salve como parecer-pilar.docx. Marque\n"
                              "[VERIFICAR] nos números de fonte externa.")
                     + details("Reflexão",
                               P("Repare: o arquivo apareceu na sua pasta, pronto para abrir e "
                                 "editar — não foi um texto que você teve de copiar e colar. "
                                 "Pergunte-se onde, no seu dia, sair do “copia-e-cola” para um "
                                 "arquivo pronto economizaria mais tempo."), tag="Reflexão")))
    return "".join(b)


def m_plugins():
    b = []
    b.append(P("Quando uma tarefa se repete, você para de pedir e começa a <strong>"
               "automatizar</strong>: empacota em Skills, dispara por comandos e deixa "
               "rodando sozinho. Aqui estão as quatro alavancas."))
    b.append(H2("Skill Creator — deixe o Claude construir a Skill"))
    b.append(P("Você não precisa escrever a " + g("Skill", "Skill") + " na mão: descreva a "
               "tarefa e o Claude te entrevista e monta a Skill para você."))
    b.append(prompt("Quero uma skill que padronize as nossas súmulas de sinistro.\n"
                    "Me entreviste para entender o formato e a política, e então\n"
                    "construa a skill para mim."))
    b.append(H2("Claude no Excel"))
    b.append(P("Há um Claude que vive <strong>dentro da planilha</strong>: ele lê as "
               "fórmulas, limpa dados e monta modelos — sem você sair do Excel."))
    b.append(exfiles(["Bastiao_DataRoom.xlsx"]))
    b.append(prompt("Nesta planilha, crie uma aba \"Resumo\" com o prêmio médio e a taxa\n"
                    "média ponderada pela IS por ramo, e um gráfico da sinistralidade por\n"
                    "trimestre. Sinalize qualquer célula cujo valor não bata com a fórmula."))
    b.append(H2("Plugins e comandos de barra"))
    b.append(P("Plugins são pacotes prontos por área (Vendas, Jurídico, Finanças, Dados…) "
               "que adicionam capacidades e <strong>comandos de barra</strong> — atalhos que "
               "você dispara digitando <code>/</code>. Você também cria os seus."))
    b.append(prompt("Crie um comando /parecer que gere um parecer de subscrição no nosso\n"
                    "formato a partir do tomador e do edital que eu indicar — seguindo a\n"
                    "nossa estrutura e a regra do [VERIFICAR]."))
    b.append(H2("Tarefas agendadas — o Claude trabalha enquanto você dorme"))
    b.append(P("O que se repete em um ritmo fixo pode rodar sozinho: um briefing semanal da "
               "carteira, um monitoramento regulatório, um radar de concorrência."))
    b.append(prompt("Agende um briefing toda segunda às 8h: resumo da carteira\n"
                    "(sinistralidade, índice combinado, tomadores acima do limite) e as\n"
                    "novidades regulatórias relevantes da semana. Me entregue para revisão."))
    b.append(details("Reflexão",
                     P("Pense em uma pergunta que você responde toda semana, sempre do mesmo "
                       "jeito. Essa é a primeira candidata a virar um comando ou uma tarefa "
                       "agendada — você responde uma vez e nunca mais reescreve. Mas lembre: "
                       "automação que roda sozinha precisa de um dono e de revisão."),
                     tag="Reflexão"))
    b.append(callout("Comandos e tarefas que disparam sozinhos são poderosos — e por isso "
                     "exigem governança: um responsável nomeado, escopo de dados aprovado e "
                     "revisão humana antes de qualquer uso externo.", label="Governança", kind="warn"))
    return "".join(b)


def m_nivel4():
    b = []
    b.append(P("Você não precisa programar — mas precisa saber o que existe no <strong>topo "
               "da escada</strong>, porque é onde estão a maior alavanca e o maior risco de "
               "governança. Este módulo é de <strong>consciência</strong>, não de terminal."))
    b.append(H2("O que mora no Nível 4"))
    b.append(table(["Recurso", "O que é", "Quando importa para a seguradora"],
                   [["Claude Code", "O Claude no terminal, para quem desenvolve. Edita código e roda comandos.", "TI e dados constroem automações e conectores internos."],
                    ["Claude Computer", "O Claude controla a tela: clica, digita e navega por você.", "Tarefas em sistemas legados sem API — sempre com supervisão."],
                    ["Agentes paralelos", "Vários agentes executando tarefas em lote ao mesmo tempo.", "Processar centenas de documentos/contratos de uma vez."],
                    [g("MCP") + " servers", "Integrações com fontes e sistemas (Playwright, Figma, sistemas internos).", "Ligar o Claude às bases de apólices/sinistros aprovadas (ver Módulo de Conexões)."],
                    ["Negócio pela linha de comando", "Fluxos inteiros (propostas, conteúdo, prospecção) operados via CLI.", "Onde a operação digital pode ganhar escala — com controles."]]))
    b.append(callout("Já encostamos no Nível 4 no curso: o " + g("MCP") + " do Módulo de "
                     "Conexões é exatamente isto — e a ideia de um loop que “pesquisa enquanto "
                     "você dorme” é a mesma das tarefas agendadas. A diferença é a potência e a "
                     "autonomia.", label="Você já viu um pedaço disto"))
    b.append(H2("A lente do líder"))
    b.append(P("No Nível 4 a pergunta deixa de ser “como eu uso” e passa a ser “como a "
               "organização usa <em>com segurança</em>”. O que você precisa garantir:"))
    b.append(table(["Garantia", "Por quê"],
                   [["Rastreabilidade e revisão humana", "Decisões de subscrição/sinistro nunca 100% automáticas."],
                    ["Dados aprovados e allowlist", "Agentes só acessam fontes liberadas; o Claude roda da nuvem da Anthropic."],
                    ["Um dono nomeado por automação", "Tudo que roda sozinho tem responsável e cadência de revisão."],
                    ["Começar pequeno e medir", "Piloto controlado → métrica de valor e risco → escala."]]))
    b.append(details("Reflexão",
                     P("Pense em um processo da sua área que é repetitivo, mensurável e de alto "
                       "volume. Esse é o candidato natural ao Nível 4. Pergunte-se: qual seria o "
                       "ganho — e qual é o portão de governança (quem aprova, quais dados, quem "
                       "revisa) antes de deixá-lo rodar?"), tag="Reflexão"))
    return "".join(b)


# ---------------------------------------------------------------------------
# Biblioteca de Skills por papel
# ---------------------------------------------------------------------------
SKILLS = [
    ("Resumo Executivo de Edital", "Subscrição / Comercial",
     "Use para transformar um edital ou dossiê em resumo executivo de 1 página.",
     "Estrutura: (1) objeto e prazo; (2) exigências de garantia (valor, modalidade, "
     "vigência, retomada, multas); (3) os 5 pontos de risco mais relevantes, cada um com a "
     "seção de origem citada; (4) o que verificar antes de decidir. Tom objetivo; 1 página."),
    ("Parecer de Subscrição Padrão", "Subscrição / Risco",
     "Use para redigir pareceres de subscrição de seguro garantia no formato e na alçada da casa.",
     "Estrutura: (1) resumo do risco; (2) crédito do tomador (alavancagem, liquidez, "
     "contingências); (3) cláusulas-chave do edital; (4) concentração vs. limite aprovado; "
     "(5) recomendação (aprovar / com condições / recusar) e condições. Marque [VERIFICAR] em "
     "todo número de fonte externa. 1–2 páginas."),
    ("Análise de Crédito do Tomador", "Risco / Crédito",
     "Use para avaliar o crédito de um tomador a partir de um balanço.",
     "Extraia e comente: receita, EBITDA e margem; dívida líquida/EBITDA; liquidez corrente e "
     "seca; backlog e concentração; contingências. Conclua com uma nota de crédito preliminar "
     "e os pontos a [VERIFICAR] em balanço auditado."),
    ("Checagem de Concentração", "Risco / Atuária",
     "Use para recalcular exposição e concentração contra os limites da casa.",
     "Calcule exposição por setor, região e tomador; compare com os tetos (tomador R$ 180 mi; "
     "setor 35%; região 45%); liste quem está acima e o efeito de uma nova operação. Apresente "
     "em tabela e aponte o que conferir na planilha."),
    ("Súmula de Sinistro", "Sinistros",
     "Use para resumir um sinistro em aberto para o comitê.",
     "Estrutura: apólice e tomador; data e causa do aviso; valor estimado e reserva; status e "
     "próximos passos; risco de desenvolvimento. Uma tela; destaque o que exige decisão."),
    ("Memo de Risco ao Board", "CEO / Risco",
     "Use para escrever um memorando de risco de 1 página para o board.",
     "Estrutura: situação (sinistralidade, índice combinado, concentração) com números; um "
     "cenário de estresse; a decisão em pauta e a recomendação; riscos e mitigadores. Linguagem "
     "de board, sem jargão. Marque [VERIFICAR] nos números externos."),
    ("Carta ao Tomador", "Comercial / CX",
     "Use para redigir comunicação ao tomador (aprovação condicionada ou recusa).",
     "Gere duas versões — uma direta e uma diplomática — com a mesma substância. Inclua as "
     "condições objetivas quando for aprovação condicionada. Nunca prometa cobertura além da "
     "apólice. Aponte o risco de cada tom."),
    ("Tradução de Cláusula", "Jurídico / Comercial",
     "Use para explicar cláusulas ou normas em linguagem simples para um público.",
     "Explique em linguagem clara para o público indicado; liste exclusões e obrigações em "
     "listas separadas; sinalize conflitos com outros documentos. Não dê parecer jurídico — "
     "trate como insumo a validar."),
]


def render_skill(nome, papel, desc, instr):
    return ('<div class="callout gold"><span class="label">' + _html.escape(papel) + "</span>"
            "<strong>" + _html.escape(nome) + "</strong>"
            "<p style='margin:.4em 0'><em>Descrição (quando usar):</em> " + _html.escape(desc) + "</p>"
            "<p style='margin:.2em 0'><em>Instruções:</em> " + _html.escape(instr) + "</p></div>")


print("módulos definidos.")

# ---------------------------------------------------------------------------
# Metadados + ordem
# ---------------------------------------------------------------------------
# (id, ato, duração, título, subtítulo, função, aprofundamento?)
MODULES = [
    ("00", "I",   "10 min", "Abertura", "Por que isso importa para uma seguradora", m00, False),
    ("01", "I",   "12 min", "Conhecendo o Claude", "O que é, o que faz e os modelos", m01, False),
    ("02", "I",   "14 min", "Fundamentos sem jargão", "As três verdades que mudam o uso", m02, False),
    ("03", "I",   "18 min", "O brief executivo", "A habilidade que mais melhora resultados", m03, False),
    ("04", "II",  "40 min", "Casos de uso — seguro garantia", "Ler, calcular, medir risco e precificar", m04, False),
    ("05", "II",  "30 min", "Data room & verificação", "Dados complexos, cruzamento e pegar o erro", m_dataroom, True),
    ("06", "II",  "30 min", "Construir algo de verdade", "Do documento ao entregável (e artifacts)", m05, False),
    ("07", "II",  "25 min", "Casos de uso executivos", "Comitê, ranqueamento, reunião→ação e o loop", m_execcases, True),
    ("08", "III", "20 min", "Cowork: o Claude no seu computador", "App de desktop, arquivos reais e de contexto", m_cowork, True),
    ("09", "III", "20 min", "Projetos: o cérebro do time", "A estratégia de Projetos no Claude", m_projetos, True),
    ("10", "III", "20 min", "Personalização e Skills", "Personalizar, usar e construir Skills", m06, False),
    ("11", "III", "20 min", "Plugins, comandos e automações", "Skill Creator, Excel, slash commands e agendamentos", m_plugins, True),
    ("12", "III", "18 min", "Conexões (MCP)", "Ligar o Claude às fontes — com o mcp-brasil", m07, False),
    ("13", "III", "15 min", "Nível 4 — Código e Computador", "O topo da escada, pela lente do líder", m_nivel4, True),
    ("14", "III", "16 min", "Riscos e governança", "O papel da liderança é governar o uso", m08, False),
    ("15", "III", "5 min",  "Plano 30-60-90 e fechamento", "Sair daqui com compromissos concretos", m09, False),
]
ACT_NAME = {
    "I":   "Ato I — Fundamentos",
    "II":  "Ato II — Mão na massa: seguro garantia",
    "III": "Ato III — Ir além e governar",
}
ACT_SUB = {
    "I":   "o modelo mental, o Claude e o brief",
    "II":  "ler, calcular, precificar e entregar com os dados da Bastião",
    "III": "personalização, Skills, conexões e governança",
}


def slug(mid): return "modulo-" + mid


def build_module(i):
    mid, act, mins, title, subtitle, fn, deep = MODULES[i]
    prev = MODULES[i - 1] if i > 0 else None
    nxt = MODULES[i + 1] if i < len(MODULES) - 1 else None
    deep_pill = ' · Aprofundamento' if deep else ''
    head = (
        '<a class="breadcrumb" href="index.html">← Todos os módulos</a>'
        '<div class="meta-pill">' + ACT_NAME[act].split(" —")[0] + " · Módulo " + mid + deep_pill + "</div>"
        '<div class="mod-number">' + mid + "</div>"
        "<h1>" + _html.escape(title) + "</h1>"
        '<p class="subtitle">' + _html.escape(subtitle) + "</p>"
    )
    body = head + fn()
    if nxt:
        next_label = "Módulo " + nxt[0] + " · " + nxt[3]
        next_href = slug(nxt[0]) + ".html"
    else:
        next_label = "Concluir — voltar aos módulos"
        next_href = "index.html"
    done = (
        '<div class="done-bar" data-done-bar data-mod="' + mid + '" data-next-label="'
        + _html.escape(next_label) + '" data-next-href="' + next_href + '">'
        '<span class="grow">Terminou este módulo? Marque para acompanhar seu progresso.</span>'
        '<button class="btn" data-done-btn type="button">Marcar como concluído</button></div>'
    )
    pn = '<div class="prevnext">'
    if prev:
        pn += ('<a href="' + slug(prev[0]) + '.html"><div class="dir">← Anterior</div><div>'
               + prev[0] + " · " + _html.escape(prev[3]) + "</div></a>")
    else:
        pn += '<a href="index.html"><div class="dir">← Início</div><div>Todos os módulos</div></a>'
    if nxt:
        pn += ('<a class="nx" href="' + slug(nxt[0]) + '.html"><div class="dir">Próximo →</div><div>'
               + nxt[0] + " · " + _html.escape(nxt[3]) + "</div></a>")
    else:
        pn += ('<a class="nx" href="../recursos.html"><div class="dir">Fim →</div>'
               "<div>Recursos para levar</div></a>")
    pn += "</div>"
    return page("Módulo " + mid + " · " + title, body + done + pn, active="modulos", depth=1)


def build_list():
    total = len(MODULES)
    b = ['<h1>O programa</h1>'
         '<p class="lede">Dezesseis módulos em três atos. O <strong>núcleo</strong> é a espinha '
         'dorsal (~60% mão na massa); os módulos marcados como <strong>Aprofundamento</strong> '
         'são opcionais e estendem o programa. Cada módulo junta o conteúdo essencial e os '
         'exercícios práticos com os dados da Bastião Seguradora (caso fictício).</p>']
    b.append('<div class="progress-bar"><span data-progress-fill></span></div>'
             '<p class="progress-text" data-progress-text>0 de ' + str(total)
             + ' módulos concluídos</p>')
    b.append('<div data-mod-list>')
    last = None
    for mid, act, mins, title, subtitle, fn, deep in MODULES:
        if act != last:
            if last is not None:
                b.append("</ul>")
            b.append('<div class="act-head"><h2>' + ACT_NAME[act] + "</h2>"
                     '<div class="act-sub">' + ACT_SUB[act] + "</div></div>")
            b.append('<ul class="mod-list">')
            last = act
        badge = (' <span style="font-family:var(--font-mono);font-size:.62rem;'
                 'text-transform:uppercase;letter-spacing:.06em;color:var(--gold);'
                 'border:1px solid var(--gold);border-radius:5px;padding:1px 6px;'
                 'vertical-align:middle">Aprofundamento</span>') if deep else ''
        b.append(
            '<a class="mod-row" data-mod-row="' + mid + '" href="' + slug(mid) + '.html">'
            '<span class="check">✓</span><span class="num">' + mid + "</span>"
            '<span class="body"><span class="title">' + _html.escape(title) + badge + "</span><br>"
            '<span class="desc">' + _html.escape(subtitle) + "</span></span></a>")
    b.append("</ul></div>")
    return page("Módulos", "".join(b), active="modulos", depth=1)


def build_home():
    agenda = '<ul class="agenda">'
    for mid, act, mins, title, subtitle, fn, deep in MODULES:
        tag = (' <span style="font-family:var(--font-mono);font-size:.6rem;'
               'text-transform:uppercase;letter-spacing:.05em;color:var(--gold)">· aprof.</span>'
               ) if deep else ''
        agenda += ('<li><span class="ag-num">' + mid + '</span><span class="ag-t">'
                   + _html.escape(title) + tag + "</span></li>")
    agenda += "</ul>"
    body = (
        '<div class="hero">'
        '<div class="kicker">Programa Executivo</div>'
        "<h1>Dominando o <span class='accent'>Claude</span></h1>"
        '<p class="lede">Da prática diária à subscrição assistida por IA — um programa '
        "hands-on para a alta liderança de uma seguradora. O ponto não é virar "
        "técnico: é virar um usuário fluente e um bom governante do uso de IA. Fio condutor: "
        "o caso fictício <strong>Bastião Seguradora S.A.</strong></p>"
        '<div class="hero-actions">'
        '<a class="btn" href="modulos/index.html">Começar pelo Módulo 00 →</a>'
        '<a class="btn ghost" href="recursos.html">Ver recursos</a>'
        "</div></div>"
        + callout("Somente dados fictícios. Nunca cole dados reais de tomadores, segurados "
                  "ou pessoas (dados pessoais — LGPD) em ferramentas que a empresa ainda não "
                  "aprovou. A disciplina começa agora e volta no módulo de governança.",
                  label="A regra de hoje", kind="warn")
        + H2("O que você será capaz de fazer")
        + table(["Ao final, cada participante consegue…", ""],
                [["Delegar como a um analista sênior", "brief claro + revisão crítica."],
                 ["Ler grandes documentos", "editais, contratos, condições gerais, balanços."],
                 ["Apoiar a subscrição", "triagem de risco, leitura de cláusulas, rascunho de parecer."],
                 ["Analisar a carteira", "sinistralidade, concentração, comunicação de decisões."],
                 ["Escolher o modelo e personalizar", "e reconhecer onde entram recursos e Skills."],
                 ["Governar o uso de IA", "com cuidado de LGPD, sigilo e regulação."]])
        + H2("A jornada")
        + agenda
        + P("<span style='color:var(--muted)'>O núcleo (módulos sem o selo "
            "<em>aprofundamento</em>) é a espinha dorsal do programa; priorize a mão na "
            "massa. Os aprofundamentos (data room &amp; verificação, casos executivos e "
            "Projetos) estendem o programa e funcionam bem como sessões separadas ou "
            "material de consulta.</span>")
    )
    return page("Início", body, active="", depth=0)


def _file_rows(files):
    out = ""
    for fname, desc in files:
        out += ('<div class="file-row"><span class="fname">' + _html.escape(fname) + "</span>"
                '<span class="fdesc">' + _html.escape(desc) + "</span>"
                '<a class="btn ghost dl" href="arquivos/' + fname + '" download>Baixar ↓</a></div>')
    return out


def build_recursos():
    b = ['<h1>Recursos para levar</h1>'
         '<p class="lede">Os arquivos do caso Bastião e os materiais para aplicar depois do '
         "treinamento. Clique para baixar e arraste para o seu " + g("Projeto", "Projeto")
         + " no Claude.</p>"]
    b.append(H2("Data room (dados complexos — Módulo 05)"))
    b.append(_file_rows(DATAROOM_FILES))
    b.append(H2("Caso Bastião — materiais originais"))
    b.append(_file_rows(ORIG_FILES))
    b.append(H2("Materiais do programa"))
    b.append(_file_rows(GEN_FILES))
    b.append(H2("Só para o facilitador"))
    b.append(callout("Contém as respostas dos erros plantados no data room. Não distribua "
                     "aos participantes antes do exercício de verificação (Módulo 05).",
                     label="Confidencial", kind="warn"))
    b.append(_file_rows(FAC_FILES))
    b.append(callout("Todos os dados do caso são fictícios, criados apenas para o "
                     "treinamento. Substitua pelos seus próprios materiais — já com dados "
                     "aprovados — quando for aplicar no seu contexto.", label="Sobre os arquivos"))
    return page("Recursos", "".join(b), active="recursos", depth=0)


print("páginas principais definidas.")

# ---------------------------------------------------------------------------
# Arquivos de apoio e materiais
# ---------------------------------------------------------------------------
# Copiados da pasta de materiais originais (../junto)
ORIG_FILES = [
    ("Bastiao_Edital_e_Tomador.md", "Dossiê: edital de licitação + balanço do tomador (Pilar). Módulos 03–06."),
    ("Bastiao_Condicoes_Gerais.md", "Condições gerais da apólice — coberturas, exclusões e obrigações. Módulo 04 (bônus)."),
    ("Bastiao_Carteira_Dados.xlsx", "Planilha enxuta original — abas Resumo da Carteira, Apólices, Tomadores e Sinistros. Módulo 04."),
]
# Gerados pelo gen_dataroom.py (já presentes em /arquivos)
DATAROOM_FILES = [
    ("Bastiao_DataRoom.xlsx", "Data room completo: 8 abas, centenas de apólices, série multi-ano, triângulo, limites e macro — COM erros plantados. Módulo 05."),
    ("Bastiao_Editais_Comparacao.md", "Três editais para comparar e ranquear por risco. Módulos 05 e 07."),
    ("Bastiao_Balancos_Tomadores.md", "Balanços de 4 tomadores para ranqueamento de crédito. Módulos 05 e 07."),
    ("Bastiao_Circular_Regulatoria.md", "Circular regulatória fictícia — tradução técnico→leigo e conformidade. Módulos 07 e 11."),
    ("Bastiao_Apolice_Escaneada.html", "Apólice “escaneada” — abra, imprima em PDF ou tire print para o exercício de Visão."),
]
# Gerados por este build
GEN_FILES = [
    ("sobre-mim-template.md", "Arquivo de contexto: quem você é e o seu papel (Módulo Cowork)."),
    ("estilo-de-escrita-template.md", "Arquivo de contexto: o seu tom, sem “cheiro de IA” (Módulo Cowork)."),
    ("biblioteca-de-prompts.md", "Biblioteca de prompts de seguros, prontos para colar e adaptar."),
    ("biblioteca-de-skills.md", "Biblioteca de Skills por papel — descrição + instruções de cada uma."),
    ("checklist-governanca-ia.md", "Checklist de governança de IA para a conversa de board."),
]
FAC_FILES = [
    ("Bastiao_Gabarito_Facilitador.md", "Gabarito dos erros plantados no data room — só para o facilitador."),
]

RES_PROMPTS = """# Biblioteca de prompts — seguro garantia

Modelos para colar e adaptar. Substitua o que estiver entre [colchetes].
Caso fictício Bastião Seguradora — use apenas dados fictícios ou públicos.

## Resumir um grande documento
Com base em [arquivo], produza um resumo executivo de [n] tópicos com objeto,
prazos e os 5 pontos de atenção de risco mais relevantes. Cite a seção de origem
de cada ponto e liste o que eu devo verificar.

## Triagem de subscrição
Você é analista de subscrição. Avalie [tomador/operação] cruzando [documento] com
[abas da planilha]. Aponte crédito, exposição vs. limite e 3 condições/mitigadores.
Dê uma recomendação preliminar.

## Calcular a carteira
Use [abas]. Calcule [prêmio médio / taxa média ponderada pela IS / exposição por
setor] e descreva a tendência de [métrica]. Gere um gráfico e aponte onde cobramos
barato pelo risco. Liste o que conferir.

## Risco e concentração
Use [abas]. Calcule a exposição por setor e região e o % concentrado em
[setor/região]. Liste quem está acima do limite e calcule o efeito de [nova
operação] sobre a exposição e o limite.

## Precificação e cenário de estresse
(1) Cenário: se [métrica] for [valor], recalcule [índice combinado / resultado].
(2) Para [operação, rating], estime a perda esperada e o prêmio mínimo com margem.
Liste as premissas. (Direcional: validar com a atuária.)

## Traduzir cláusulas
Explique [cláusula/condições gerais] em linguagem simples para [público]. Liste
exclusões e obrigações em listas separadas e sinalize conflitos com [outro documento].

## Comunicar decisão
Escreva duas versões de [carta/decisão]: uma direta, uma diplomática. Mesma
substância, público [quem]. Aponte o risco de cada tom.

## Gerar o entregável
Com base na nossa conversa, gere [parecer/carta/planilha/slides] pronto para
download, com [formato], para [público].
"""

RES_CHECKLIST = """# Checklist de governança de IA (seguros)

Ponto de partida para a conversa de board sobre uso responsável de IA na seguradora.

## Dados e LGPD
- [ ] Há lista clara do que pode e do que não pode ser inserido em ferramentas de IA?
- [ ] Dados de segurados, tomadores e pessoas só entram em ferramentas aprovadas e com base legal?
- [ ] Há minimização de dados (usar o mínimo necessário) e controle de retenção?

## Regulação e decisão
- [ ] Decisões de subscrição e sinistro têm rastreabilidade e revisão humana?
- [ ] Negativas de cobertura jamais são automatizadas sem responsável nomeado?
- [ ] Números, cláusulas e fontes geradas por IA são verificados antes de uso externo?
- [ ] Questões jurídicas e atuariais permanecem com profissionais habilitados?

## Conectores e MCP
- [ ] Conectamos apenas fontes aprovadas, com escopo mínimo (de preferência leitura)?
- [ ] Há processo para um Owner provisionar conectores e revogar acessos quando necessário?
- [ ] Conectores personalizados (MCP de terceiros) passam por avaliação de segurança antes do uso?

## Capacidade e valor
- [ ] Cada função sabe o que pode delegar e como revisar?
- [ ] Há pipeline de casos de uso com dono e métrica (e não "teatro de IA")?
- [ ] O valor (tempo, qualidade, risco) é medido a cada trimestre?
"""

RES_SOBRE = """# sobre-mim.md — template

Quatro a seis linhas bastam. Deixe na pasta onde você trabalha (ou nas Instruções globais).

- **Nome / papel:** Maria Silva, diretora de subscrição de uma seguradora de seguro garantia.
- **O que faço:** decido sobre garantias de execução, leio editais e balanços, levo pareceres ao comitê.
- **O que estou resolvendo agora:** acelerar a análise de risco sem perder rigor.
- **Como gosto de pensar:** começo pela recomendação, depois os porquês; foco no que decide.
- **Como gosto de ser tratada:** em português, direto ao ponto, sem jargão; sempre liste o que eu devo verificar.
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


def build_referencia():
    b = ['<h1>Referência</h1>'
         '<p class="lede">Os apêndices do programa: o caso Bastião, os modelos do Claude, '
         "personalização, Skills, governança e onde confirmar o que está vigente.</p>"]

    # Apêndice B — case bible
    bible = (P("Seguradora, tomadores, apólices e números são <strong>fictícios</strong>, "
               "criados apenas para o treinamento.")
             + P("<strong>Quem é:</strong> seguradora brasileira de médio porte especializada "
                 "em " + g("Seguro garantia", "seguro garantia") + ". Prêmios emitidos ~R$ 1,8 "
                 "bi/ano. <strong>Ramos:</strong> Garantia de Execução de Contrato (carro-chefe), "
                 "Garantia Judicial, Fiança Locatícia e Riscos de Engenharia.")
             + P("<strong>Tensão central:</strong> a sinistralidade sobe, há forte "
                 "concentração em Construção Civil e no Sudeste, e a Construtora Pilar (maior "
                 "risco da casa) pede uma nova garantia grande.")
             + table(["Indicador", "1T24", "4T25", "Leitura"],
                     [["Sinistralidade", "~22%", "~42%", "Deterioração clara."],
                      ["Índice combinado", "~58%", "~79%", "Ainda lucrativo, mas piorando."],
                      ["Construtora Pilar", "Dívida/EBITDA ~4,8x; Liquidez 0,9", "—", "Crédito fraco; abaixo do exigido pelo edital."],
                      ["Pedido da Pilar", "+ R$ 60 mi", "—", "Empurra a exposição acima do limite aprovado (R$ 180 mi)."]]))
    b.append(details("Apêndice B — O caso Bastião Seguradora S.A.", bible, tag="Caso"))

    # Apêndice C — models
    models = (table(["Tier (referência)", "Pontos fortes", "Use para (em seguros)"],
                    [["Haiku 4.5", "Rápido, leve, econômico", "Triagem de avisos; resumos curtos; extração de campos."],
                     ["Sonnet 4.6", "Versátil; bom raciocínio, escrita, análise, visão", "A maioria do dia a dia: cartas, análises, comunicação, rascunhos."],
                     ["Opus 4.8", "Raciocínio profundo; documentos longos; alta precisão", "Parecer de subscrição a partir de edital + balanço; decisões de alto risco."]])
              + callout("Comece no Sonnet. Suba para o Opus quando a tarefa for difícil de "
                        "verdade ou o documento longo. Desça para o Haiku no volume simples. "
                        "Usar o Opus em tudo gasta o limite à toa. Cada nova versão é um novo "
                        "treino — vale retestar suas tarefas quando sai um modelo novo. "
                        "(Os nomes mudam com o tempo; confirme os atuais.)", label="Regras práticas", kind="gold"))
    b.append(details("Apêndice C — Modelos do Claude: qual usar e quando", models, tag="Modelos"))

    # Apêndice D — personalization
    pers = (P("Três níveis, do mais amplo ao mais específico. Onde configurar pode mudar na "
              "interface — procure em Configurações.")
            + H3("1) Preferências (valem para todas as conversas)")
            + prompt("Sou diretor(a) de subscrição em uma seguradora de seguro garantia.\n"
                     "Prefiro respostas em português, diretas e estruturadas, com a\n"
                     "RECOMENDAÇÃO primeiro e os porquês depois. Sempre liste o que eu\n"
                     "devo verificar. Não invente números; quando não souber, diga.",
                     label="Exemplo de preferências")
            + H3("2) Instruções de Projeto (valem só naquele Projeto)")
            + prompt("Este Projeto é da equipe de subscrição de Garantia de Execução.\n"
                     "Use sempre as condições gerais e a política de alçada anexadas.\n"
                     "Em pareceres, siga a estrutura: (1) resumo do risco; (2) tomador\n"
                     "(crédito); (3) edital/contrato (cláusulas-chave); (4) concentração\n"
                     "vs. limite; (5) recomendação e condições. Marque [VERIFICAR] em\n"
                     "todo número que dependa de fonte externa.",
                     label="Exemplo de instruções de Projeto")
            + H3("3) Estilos (o jeito de escrever)")
            + P("Ajustam a forma do texto e podem ser criados a partir de exemplos seus — "
                "por exemplo, um estilo “Parecer Bastião” treinado em pareceres antigos, "
                "para padronizar a escrita do time."))
    b.append(details("Apêndice D — Personalização do Claude", pers, tag="Personalizar"))

    # Apêndice F — skills
    skills = (P("Uma " + g("Skill", "Skill") + " é um pacote reutilizável de instruções que "
                "ensina o Claude a executar uma tarefa recorrente do seu jeito, com "
                "consistência. É como transformar um bom brief que você repete toda semana "
                "em um padrão da casa.")
              + P("<strong>Quando vale a pena:</strong> tarefas que se repetem e precisam "
                  "seguir um padrão (pareceres, súmulas de sinistro, respostas a clientes) e "
                  "quando a consistência de formato importa (governança, auditoria). "
                  "<strong>Quando ainda não vale:</strong> tarefas pontuais e exploratórias, "
                  "em que o brief muda toda vez.")
              + P("<strong>Prontas (da Anthropic):</strong> Word, Excel, PowerPoint e PDF. "
                  "Você já as usa quando o Claude gera um parecer, uma planilha ou um deck.")
              + callout("(1) Configurações › Capacidades: ligue “Execução de código e "
                        "criação de arquivos”. (2) Personalizar › Skills › “+ Criar skill”. "
                        "(3) Nome + descrição curta (até ~200 caracteres) — diz QUANDO usar. "
                        "(4) Escreva as instruções. (5) Teste com um caso real e ajuste a "
                        "descrição até a Skill “aparecer” sozinha.", label="Como construir a sua"))
    b.append(details("Apêndice F — Skills: o que são e onde entram", skills, tag="Skills"))

    # Apêndice F2 — biblioteca de skills por papel
    lib = (P("Oito Skills prontas para o time da seguradora. Crie cada uma em Personalizar "
             "› Skills; a <em>descrição</em> diz ao Claude quando usá-la. Baixe o pacote em "
             "<a href='recursos.html'>Recursos</a> (<code>biblioteca-de-skills.md</code>)."))
    for nome, papel, desc, instr in SKILLS:
        lib += render_skill(nome, papel, desc, instr)
    b.append(details("Apêndice F+ — Biblioteca de Skills por papel", lib, tag="Biblioteca"))

    # Apêndice G — governance checklist
    chk = (P("Ponto de partida para a conversa de board sobre uso responsável de IA. "
             "Baixe a versão em markdown na página Recursos.")
           + H3("Dados e LGPD")
           + P("Há lista clara do que pode/não pode entrar? Dados de pessoas só em "
               "ferramentas aprovadas e com base legal? Há minimização e controle de retenção?")
           + H3("Regulação e decisão")
           + P("Decisões de subscrição/sinistro com rastreabilidade e revisão humana? "
               "Negativas nunca automatizadas sem responsável? Números e fontes verificados "
               "antes de uso externo? Jurídico e atuária com profissionais habilitados?")
           + H3("Conectores e MCP")
           + P("Só fontes aprovadas, escopo mínimo? Há quem provisione e revogue acessos? "
               "Conectores de terceiros passam por avaliação de segurança?")
           + H3("Capacidade e valor")
           + P("Cada função sabe o que delegar e como revisar? Há pipeline com dono e "
               "métrica? O valor (tempo, qualidade, risco) é medido por trimestre?"))
    b.append(details("Apêndice G — Checklist de governança de IA", chk, tag="Governança"))

    # Apêndice H — where to verify
    verify = (P("Importante: o Claude e seus produtos evoluem rapidamente. Modelos, planos, "
                "limites e políticas de dados mudam. Antes de aplicar este treinamento, "
                "confirme o que está vigente nas fontes oficiais.")
              + P("<strong>Onde verificar:</strong> a documentação oficial e a central de "
                  "ajuda do Claude (modelos, planos, Projetos, Skills, limites, políticas de "
                  "dados); os materiais de prompting da Anthropic; e a política interna de IA "
                  "e de LGPD da sua organização (ferramentas e dados aprovados)."))
    b.append(details("Apêndice H — Recursos atuais e próximos passos", verify, tag="Verificar"))

    return page("Referência", "".join(b), active="referencia", depth=0)


# ---------------------------------------------------------------------------
# Dicas — "Como falar com o Claude (para ele funcionar como você)"
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
    """Corpo da página de dicas. depth define os links para os módulos."""
    mp = ("modulos/" if depth == 0 else "")  # single-file usa âncoras (tratado à parte)
    b = ['<h1>Como falar com o Claude</h1>',
         '<p class="lede">Uma colinha para o Claude funcionar como <em>você</em>. Vale para '
         "qualquer módulo — volte aqui sempre que precisar.</p>",
         render_tips(),
         callout("Defina claramente a tarefa, forneça contexto, incentive a IA a fazer "
                 "perguntas, gere várias alternativas, refine o que funcionar e transforme os "
                 "melhores resultados em modelos reutilizáveis.", label="Resumo em uma frase", kind="gold"),
         H2("Onde isto aparece no curso"),
         P("Estas dicas não são teoria — cada uma vira prática em algum módulo:"),
         table(["Dica", "Onde praticar"],
               [["Comece pela tarefa · seja específico (1, 7)", "Módulo 03 — O brief executivo"],
                ["“Me faça perguntas” · faça a IA perguntar (2, 6)", "Módulo 08 — Cowork"],
                ["Seu arquivo “sobre mim” (8)", "Módulo 08 — arquivos de contexto"],
                ["3 versões · recomece · gere bastante · diga quando errar (4, 5, 9, 10)", "Módulo 07 — o loop ver→criticar→iterar"],
                ["Salve como template · faça o difícil uma vez (11, 13)", "Módulos 10 e 11 — Skills e automações"]])]
    return "".join(b)


def build_dicas():
    return page("Dicas", dicas_body(depth=1), active="dicas", depth=0)


def build_skills_md():
    out = ["# Biblioteca de Skills — seguro garantia\n",
           "Skills por papel para o time da seguradora. Cada uma tem um NOME, uma DESCRIÇÃO",
           "(que diz ao Claude QUANDO usá-la) e as INSTRUÇÕES. Crie em Personalizar › Skills",
           "› “+ Criar skill”. Todas carregam a disciplina do [VERIFICAR].\n"]
    for nome, papel, desc, instr in SKILLS:
        out.append("## " + nome + "  _(" + papel + ")_")
        out.append("**Descrição:** " + desc)
        out.append("**Instruções:** " + instr + "\n")
    return "\n".join(out) + "\n"


def write_resources():
    d = os.path.join(ROOT, "arquivos")
    os.makedirs(d, exist_ok=True)
    # copia os materiais originais (da pasta ../junto)
    copied = []
    for fname, _ in ORIG_FILES:
        src = os.path.join(SRC, fname)
        if os.path.exists(src):
            shutil.copyfile(src, os.path.join(d, fname))
            copied.append(fname)
        else:
            print("  AVISO: não encontrei", src)
    # gera materiais do programa
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
    # confere se os arquivos do data room (gerados por gen_dataroom.py) estão presentes
    missing = [f for f, _ in DATAROOM_FILES + FAC_FILES
               if not os.path.exists(os.path.join(d, f))]
    if missing:
        print("  AVISO: rode 'python3 gen_dataroom.py' — faltam:", ", ".join(missing))
    return copied + list(gen)


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
    print("Recursos:", ", ".join(res))
    print("Pronto. Sirva com:  python3 -m http.server 8090")


if __name__ == "__main__":
    main()
