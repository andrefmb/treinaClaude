#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Construtor do site local "Curso .md" (pt-BR).
Gera as páginas HTML estáticas a partir do conteúdo definido abaixo.
Rode:  python3 build.py   (a partir da pasta do projeto)
Sirva: python3 -m http.server 8080  -> abra http://localhost:8080
"""
import html as _html
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# GLOSSÁRIO  (definições autorais em pt-BR)
# ---------------------------------------------------------------------------
GLOSSARY = {
    "Sessão": "Uma única conversa contínua com o Claude Code. Cada mensagem, cada arquivo lido e cada resultado de ferramenta vivem dentro de uma sessão — guardada localmente na sua máquina.",
    "Vercel": "Um serviço de hospedagem. Você entrega uma pasta de código; ele devolve uma URL pública que qualquer pessoa pode abrir — transforma seu jogo da cobrinha em um link em segundos.",
    "GitHub": "O site onde a maioria das pessoas hospeda repositórios git. Git é a ferramenta; o GitHub é um dos lugares populares que armazenam o resultado. É da Microsoft e gratuito para projetos públicos.",
    "HTML": "A linguagem de marcação das páginas web — define a estrutura: títulos, parágrafos, botões, imagens. O CSS aplica estilo; o JavaScript adiciona interatividade.",
    "Python": "Uma linguagem de programação — a língua franca de ciência de dados, machine learning e automações. Tem seu próprio interpretador e instalador de pacotes (pip).",
    "Contexto": "Tudo o que o Claude consegue enxergar agora — a conversa até aqui, os arquivos que leu, os resultados de ferramentas e as instruções de sistema. Um grande buffer de texto que o modelo lê de ponta a ponta antes de cada resposta.",
    "Skill": "Um pacote reutilizável de conhecimento que o Claude carrega sob demanda. Vive como uma pasta de markdown na sua máquina e entra em ação quando a conversa combina com aquilo para que a skill serve.",
    "Conector": "Pequenas pontes que permitem ao Claude acessar seus outros aplicativos — Gmail, Agenda, Drive, Slack — com a sua permissão explícita.",
    "Comando de barra": "Um atalho que você digita como /alguma-coisa para disparar um fluxo que o Claude já conhece. Digite /check-mail e ele faz a rotina inteira sem você reescrever o prompt.",
    "Loop": "O que torna o Claude um agente, e não um chatbot. Em vez de um único pergunta-e-responde, um loop roda o Claude repetidamente: agir, observar o que mudou, decidir o próximo passo, repetir.",
    "AutoResearch": "Um loop que transforma o Claude em um pesquisador de ML incansável. Você dá um conjunto de dados e uma métrica a superar; ele tenta uma abordagem, mede a pontuação, registra o que aprendeu e segue adiante.",
    "FLAML": "Fast and Lightweight AutoML — uma biblioteca Python de código aberto da Microsoft Research. Dê a ela um dataset e uma métrica; ela testa tipos de modelo e hiperparâmetros e devolve o melhor dentro de um orçamento de tempo fixo.",
    "Baseline": "A pontuação que uma abordagem simples-porém-honesta atinge no seu problema. É a barra que você precisa superar para afirmar que sua abordagem sofisticada realmente faz alguma diferença.",
    "AUC": "Area Under the (ROC) Curve — um número entre 0,5 (chute aleatório) e 1,0 (perfeito) que mede quão bem um classificador separa os exemplos “sim” dos “não”. Quanto maior, melhor.",
    "CPU vs GPU": "A CPU é o cérebro de uso geral do computador — poucos núcleos rápidos e flexíveis. A GPU tem milhares de núcleos mais lentos que fazem contas simples em paralelo — ideal para treinar ML.",
    "Repositório": "Uma pasta que o git acompanha — parece normal, mas dentro dela há um diretório oculto .git/ com todo o histórico: cada arquivo, cada mudança, cada commit, cada branch.",
    "Commit": "Um instantâneo do seu projeto em um momento, com uma mensagem descrevendo o que mudou. Cada commit sabe qual veio antes dele — é assim que o git reconstrói o histórico.",
    "Clonar": "git clone faz uma cópia local completa de um repositório — arquivos e histórico inteiro. Depois de clonar você pode lê-lo offline, editá-lo e fazer seus próprios commits.",
    "PATH": "Uma lista de pastas que o seu terminal percorre quando você digita um comando. Digite 'git' e o shell procura por um programa chamado git em cada pasta do PATH, em ordem.",
    "Pasta Downloads": "Onde o navegador salva os arquivos quando você clica em um link de download — o local exato depende do sistema operacional.",
}


def g(term, label=None):
    """Renderiza um termo de glossário com tooltip."""
    label = label or term
    definition = GLOSSARY[term]
    return ('<span class="term">' + _html.escape(label)
            + '<span class="tip"><strong>' + _html.escape(term) + '</strong>'
            + _html.escape(definition) + '</span></span>')


# ---------------------------------------------------------------------------
# Helpers de bloco
# ---------------------------------------------------------------------------
def H2(t): return "<h2>" + t + "</h2>"
def H3(t): return "<h3>" + t + "</h3>"
def P(t):  return "<p>" + t + "</p>"


def ic(t):
    """código inline"""
    return '<code class="inline">' + _html.escape(t) + "</code>"


def codeblock(text):
    return ('<div class="codeblock"><pre>'
            + _html.escape(text.strip("\n")) + "</pre></div>")


def prompt(code, label="Prompt", note=None):
    out = '<div class="prompt-label">' + _html.escape(label)
    if note:
        out += ' <span style="color:var(--accent)">· ' + _html.escape(note) + "</span>"
    out += "</div>" + codeblock(code)
    return out


def helpline(step):
    return ('<p class="helpline"><a href="../ajuda.html">Preciso de ajuda com '
            + step + " →</a></p>")


def details(summary, body, tag=None, reflect=False):
    cls = "box reflect" if reflect else "box"
    tag_html = '<span class="tag">' + _html.escape(tag) + "</span>" if tag else ""
    return ('<details class="' + cls + '"><summary>' + tag_html + " "
            + summary + '</summary><div class="box-body">' + body + "</div></details>")


def callout(body, label="Nota", kind=""):
    cls = "callout " + kind if kind else "callout"
    return ('<div class="' + cls + '"><span class="label">'
            + _html.escape(label) + "</span>" + body + "</div>")


def faq(items):
    out = ""
    for q, a in items:
        out += '<p class="faq-q">' + q + '</p><p class="faq-a">' + a + "</p>"
    return out


# ---------------------------------------------------------------------------
# Shell da página (cabeçalho, navegação, rodapé)
# ---------------------------------------------------------------------------
DISCLAIMER = (
    "Use ambientes de testes (sandbox) ou não-produtivos. Não envie dados "
    "confidenciais, de clientes ou não aprovados. Siga as orientações internas "
    "de TI/segurança. As saídas podem conter imprecisões."
)
DISCLAIMER2 = (
    "Certos exemplos e discussões neste material descrevem fluxos de IA "
    "exploratórios, casos de uso conceituais ou ideias voltadas ao futuro. Não "
    "devem ser interpretados como compromissos operacionais nem como roteiro de "
    "produtos. Material educacional — recriação local em português."
)


def nav(active, depth=0):
    """active: '', 'exercicios', 'ajuda', 'arquivos'. depth: 0 raiz, 1 subpasta."""
    up = "../" if depth else ""
    def cls(name): return ' class="active"' if active == name else ""
    return (
        '<header class="topbar">'
        '<a class="brand" href="' + up + 'index.html">.<span class="dot">md</span></a>'
        '<nav class="topnav">'
        '<a href="' + up + 'exercicios/index.html"' + cls("exercicios") + '>Exercícios</a>'
        '<a href="' + up + 'ajuda.html"' + cls("ajuda") + '>Pedir ajuda</a>'
        '<a href="' + up + 'arquivos.html"' + cls("arquivos") + '>Arquivos</a>'
        "</nav></header>"
    )


def footer(depth=0):
    up = "../" if depth else ""
    return (
        '<footer><div class="wrap">'
        '<p class="disclaimer">' + DISCLAIMER + "</p>"
        '<p class="disclaimer">' + DISCLAIMER2 + "</p>"
        '<div class="flinks">'
        '<a href="' + up + 'index.html">.md</a>'
        '<a href="' + up + 'exercicios/index.html">Exercícios</a>'
        '<a href="' + up + 'ajuda.html">Pedir ajuda</a>'
        '<a href="' + up + 'arquivos.html">Arquivos</a>'
        "</div>"
        '<p style="color:var(--muted-2);font-size:0.8rem">Recriação local em '
        "português · conteúdo instrucional original · feito para fins educacionais.</p>"
        "</div></footer>"
    )


def page(title, body, active="", depth=0, wide=False):
    up = "../" if depth else ""
    wrapcls = "wrap-wide" if wide else "wrap"
    return (
        "<!DOCTYPE html>\n"
        '<html lang="pt-BR"><head>'
        '<meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        "<title>" + _html.escape(title) + " · Curso .md</title>"
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?'
        "family=Bricolage+Grotesque:opsz,wght@12..96,400..800&"
        "family=Geist:wght@300..700&"
        'family=JetBrains+Mono:wght@400..700&display=swap" rel="stylesheet">'
        '<link rel="stylesheet" href="' + up + 'assets/styles.css">'
        "</head><body>"
        + nav(active, depth)
        + '<main><div class="' + wrapcls + '">' + body + "</div></main>"
        + footer(depth)
        + '<script src="' + up + 'assets/app.js"></script>'
        "</body></html>"
    )


print("templates definidos.")

# ---------------------------------------------------------------------------
# Conteúdo dos exercícios (texto autoral em pt-BR; prompts funcionais)
# ---------------------------------------------------------------------------
SESSION_STEP = (
    "<p><strong>Inicie uma nova " + g("Sessão", "sessão do Claude Code")
    + ".</strong> Toda vez que dissermos “inicie uma nova sessão”, é este o botão "
    "que você aperta: abra o Claude Code e comece uma conversa do zero.</p>"
)


def ex_1_1():
    b = []
    b.append(P("Esta é a sua primeira execução com um agente. Mantenha o prompt "
               "ridiculamente simples. Repare no que um bom agente faz com quase nada."))
    b.append(H2("Antes de começar — duas coisas em todo exercício"))
    b.append("<p><strong>1. Inicie uma nova " + g("Sessão", "sessão do Claude Code")
             + ".</strong> Abra o Claude Code e comece uma conversa nova. É este o "
               "botão que você aperta sempre que pedirmos uma nova sessão.</p>")
    b.append("<p><strong>2. Crie uma pasta nova</strong> e aponte o Claude Code para ela. "
             "Primeiro crie uma pasta vazia (no Finder ou no Explorador de Arquivos, em um "
             "lugar fácil como a Área de Trabalho; chame-a de " + ic("snake")
             + "). Depois, no seletor de pastas do Claude Code, escolha essa pasta vazia. "
               "A pasta que você escolher é tudo o que o Claude consegue ver — ele lê, "
               "escreve e roda comandos só dentro dela. Exercício novo → pasta nova.</p>")
    b.append(callout(
        "Está no painel do prompt, logo acima de onde você digita. Se o Claude Code "
        "abriu direto na sua pasta pessoal (você verá Documentos, Downloads etc. ao "
        "listar arquivos), feche e reabra; escolha a pasta vazia quando ele perguntar.",
        label="Não vê o seletor de pastas?"))
    b.append(P("<strong>Confirme que está no lugar certo.</strong>"))
    b.append(prompt("Quais arquivos existem nesta pasta?"))
    b.append("<p>O Claude deve responder que a pasta está vazia — é o esperado. Se ele "
             "listar suas pastas do " + g("GitHub") + " ou documentos aleatórios, você "
             "abriu a pasta errada; feche e reabra com a pasta vazia que acabou de criar.</p>")
    b.append(H2("Etapa 1 — O prompt simples"))
    b.append(helpline("a etapa 1"))
    b.append(P("Digite isto. Nada mais."))
    b.append(prompt("Crie um jogo da cobrinha usando HTML simples\n"
                    "Faça o deploy na Vercel e me dê a URL pública\n"
                    "(Use o Vercel CLI, que já está instalado; eu tenho uma conta na Vercel)"))
    b.append(P("Aperte enter. Veja ele construir."))
    b.append(callout("Pode ser que ele peça para você confirmar a " + g("Vercel")
                     + " no navegador.", label="Atenção"))
    b.append(details(
        "Travou? Debrief — o que deveria ter acontecido",
        P("O Claude escreveu um único " + ic("index.html") + " com um jogo da cobrinha "
          "funcionando. Ele rodou o " + ic("vercel") + " pela linha de comando, talvez "
          "abrindo o navegador para autenticar, e imprimiu uma URL pública.")
        + P("O jogo funciona. E quase certamente é genérico — cobra verde, maçã vermelha, "
            "sem menu, sem tema, sem surpresa. Esse é justamente o ponto: você deu quase "
            "nada ao agente e ele preencheu as lacunas com a média do que sabe. Essa "
            "distância é o que o Exercício 1.2 fecha.")
        + callout("O fluxo de autenticação da Vercel pode travar na primeira vez — confira a "
                  "aba do navegador. Se a construção de um jogo da cobrinha passar de três "
                  "minutos, o agente pode estar exagerando: inicie uma nova sessão e peça "
                  "para ele ser rápido.", label="Problemas comuns", kind="warn"),
        tag="Debrief"))
    b.append(details(
        "Travou? Perguntas frequentes deste exercício",
        faq([
            ("Faz mais de três minutos que está rodando e nada foi publicado. Por quê?",
             "Pode ser instabilidade do lado do Claude por excesso de uso. Também pode ser "
             "que adicionar coisas como telas de onboarding exija um frontend em camadas — "
             "em vez de um arquivo de 50 linhas, vêm ~1.000 linhas, o que demora mais. "
             "Confira o uso em Configurações → Uso, ou inicie uma nova sessão e peça rapidez."),
            ("Seria bom ver o " + ic("HTML") + " criado e onde ele fica localmente.",
             "A beleza é que você não precisa ver o código. Se voltar à pasta onde criou o "
             "jogo e fizer perguntas ali, o Claude enxerga o jogo naquela pasta. Você nunca "
             "precisa saber onde o código vive — só use sempre a mesma pasta para continuar."),
            ("Como abro o arquivo depois de criado?",
             "É só pedir ao Claude — “me dê o link do arquivo” ou “abra com o Finder” — e "
             "ele entrega ou abre diretamente."),
        ]),
        tag="FAQ"))
    b.append(details(
        "Opcional · Vá mais fundo",
        P("Mesmo formato de prompt, outro jogo genérico. Inicie uma nova sessão, pasta "
          "vazia nova:")
        + prompt("Crie um Tetris simples usando HTML\n"
                 "Faça o deploy na Vercel e me dê a URL pública")
        + P("Repare que o resultado é tão genérico quanto a cobrinha — blocos verdes, fonte "
            "padrão, sem tema. Especificações vazias colapsam para a média, não importa o "
            "tema. O conserto não é trocar de jogo; é um briefing mais rico."),
        tag="Vá mais fundo"))
    return "".join(b)


def ex_1_2():
    b = []
    b.append(P("O Exercício 1.1 deu o UAU a partir de uma ficha de especificação vazia. O "
               "agente preencheu as lacunas de memória. Serve como gancho; não é assim que "
               "se faz trabalho de verdade."))
    b.append(P("Agora adicionamos o que é uma ficha de verdade: um tema, um público, uma "
               "vibe, restrições. Ainda é uma única pergunta — mas com saída diferente."))
    b.append(H2("Etapa 1 — Nova sessão e o mesmo prompt, agora com a especificação"))
    b.append(helpline("a etapa 1"))
    b.append(prompt("Crie um jogo da cobrinha em HTML com os seguintes recursos:\n"
                    "- Pelo menos três fases\n"
                    "- Um fluxo de onboarding\n"
                    "- Garanta uma música-tema no menu principal\n"
                    "Faça o deploy na Vercel e me dê a URL pública\n"
                    "(Use o Vercel CLI, que já está instalado; eu tenho uma conta na Vercel)"))
    b.append(P("Mesmo modelo. Mesmo formato de prompt. A única coisa que mudou foi a "
               "especificação ao lado. Compare com o que o 1.1 produziu — repare o quanto "
               "mais de você existe no resultado."))
    b.append(details(
        "Travou? Debrief — o que deveria ter acontecido",
        P("Três fases, uma tela de onboarding, uma música-tema. Um resultado mais "
          "interessante não porque o modelo ficou mais esperto, mas porque o briefing ficou "
          "mais rico.")
        + P("A promoção a guardar: ficar mexendo no prompt é jogada de amador. Editar "
            + g("Contexto", "contexto") + " é a jogada profissional. Toda vez que você se "
            "pegar reescrevendo o mesmo prompt de três jeitos, pergunte: o que eu colocaria "
            "num arquivo " + ic(".md") + " que tornaria o próximo prompt desnecessário?"),
        tag="Debrief"))
    b.append(details(
        "Travou? Perguntas frequentes deste exercício",
        faq([
            ("Onde deve viver a especificação? Escrevo como arquivo?",
             "Tanto faz — colocar no prompt ou em um arquivo separado é equivalente. Se "
             "escolher o arquivo, basta apontar o agente para ele."),
            ("Por que a primeira versão foi tão genérica?",
             "Porque você não deu nada para o agente ancorar. Sem contexto, ele recorre à "
             "média do que “jogo da cobrinha” significa nos dados de treino. Com uma "
             "especificação, ele recorre à sua especificação."),
        ]),
        tag="FAQ"))
    b.append(details(
        "Opcional · Vá mais fundo",
        P("Agora faça um jogo que ensine algo. Mesmo setup, mesmo modelo — mude só o briefing.")
        + prompt("Crie um jogo em HTML que ensine a tabuada do 7 para crianças de 7 anos\n"
                 "- Fluxo de onboarding que explica as regras\n"
                 "- Pontuação, três vidas e uma tela de “muito bem”\n"
                 "- Paleta aconchegante, tom encorajador\n"
                 "Faça o deploy na Vercel e me dê a URL pública")
        + P("(Ou escolha seu tema: vocabulário de comida em espanhol, capitais, list "
            "comprehensions em " + g("Python") + ".) O jogo agora tem um propósito que não "
            "tinha um minuto atrás — e a única coisa que mudou foi o briefing ao lado."),
        tag="Vá mais fundo"))
    b.append(details(
        "Reflexão · Interlúdio A — O que acabou de acontecer",
        P("Você acabou de rodar um experimento controlado em si mesmo. Mesmo modelo, mesmo "
          "prompt, dois resultados completamente diferentes. A variável foi um arquivo.")
        + P("Um arquivo markdown é a unidade de trabalho mais barata e poderosa que você "
            "tem. Todo exercício seguinte — " + g("Skill", "skills") + ", person.md, "
            "voice.md, program.md — é uma variação deste tema. O agente faz o que você pede, "
            "mas faz no estilo dos arquivos ao redor.")
        + P("A mudança de hábito a instalar: toda vez que você responder uma pergunta, "
            "escreva a resposta em um arquivo. Aí todo agente — o seu e o dos outros — passa "
            "a saber. Menos perguntas, mais produtividade. Documentação deixa de ser tarefa "
            "chata: vira combustível."),
        reflect=True, tag="Reflexão"))
    return "".join(b)


def ex_2_1():
    b = []
    b.append(P("Ensine algo novo ao seu agente. Vamos pegar um documento, transformar em "
               "apresentação e — o pulo do gato — destilar tudo isso em uma " + g("Skill")
               + " reutilizável."))
    b.append(SESSION_STEP)
    b.append(P("<strong>Primeiro:</strong> baixe o arquivo " + ic("prosus_management_overview.md")
               + " (veja a página <a href='../arquivos.html'>Arquivos</a>), abra a sua "
               + g("Pasta Downloads", "pasta Downloads") + " e arraste-o para a janela de chat "
               "do Claude Code."))
    b.append(prompt("Crie uma apresentação sobre o prosus_management_overview.md (apenas 4 slides)\n"
                    "use pptxgenjs para criar os slides"))
    b.append(prompt("Adicione o logo no canto superior direito:\n"
                    "https://www.prosus.com/~/media/Images/P/prosus-corp-v2/logo/logo.png\n"
                    "Aplique um estilo como:\n"
                    "https://www.prosus.com/stylesheets/global.css\n"
                    "Assuma as cores, fontes e a vibe.",
                    label="Prompt de continuação", note="Mesma conversa!"))
    b.append(prompt("Transforme tudo o que você aprendeu em uma skill chamada:\n"
                    "\"create-prosus-presentation\"\n"
                    "Garanta que essa skill seja sempre chamada ao criar uma apresentação,\n"
                    "para termos uma marca uniforme da empresa.",
                    label="Prompt de continuação #2", note="Mesma conversa!"))
    b.append(P("Agora dá para reexecutar o primeiro prompt (depois de remover a apresentação "
               "anterior da pasta) e ver que a apresentação sai “de primeira” no estilo "
               "desejado. Você acabou de ensinar algo novo ao Claude."))
    b.append(callout(
        "Uma skill foi criada em " + ic("~/.claude/skills/create-prosus-presentation/")
        + " — agora ela aparece na lista de skills disponíveis. Estrutura típica: "
        + ic("SKILL.md") + " (descrição que dispara em qualquer tarefa de slides/pptx, com "
        "regras de marca embutidas), " + ic("assets/template.js") + " (starter pronto de "
        "pptxgenjs com helpers como addTitleBar, addFooter, addLogo, addCard e slides de "
        "exemplo), " + ic("assets/logo.png") + " e " + ic("references/brand.md") + " (paleta "
        "estendida, escala tipográfica, motivos, coisas a evitar).",
        label="Saída esperada", kind="tip"))
    b.append(details(
        "Travou? Debrief — o que deveria ter acontecido",
        P("Uma skill em " + ic("~/.claude/skills/create-prosus-presentation/") + " com "
          "aquela estrutura. O recado: mesmo modelo, saída radicalmente diferente — a partir "
          "de um arquivo markdown que você mesmo escreveu.")
        + callout("Se a skill não aparecer em " + ic("/skills") + ", reinicie o Claude Code "
                  "por completo (não só feche a janela). Skills só atualizam ao reiniciar.",
                  label="Dica", kind="warn"),
        tag="Debrief"))
    b.append(details(
        "Travou? Perguntas frequentes deste exercício",
        faq([
            ("Se eu criar uma skill, qual é o escopo dela?",
             "Há três escopos. <strong>Projeto</strong>: disponível só naquela pasta "
             "(recomendado para começar a experimentar). <strong>Global</strong>: disponível "
             "em toda " + g("Sessão", "sessão") + " (bom para “sempre faça apresentações "
             "assim”). <strong>Plugin</strong>: liga/desliga por conversa e pode ser "
             "distribuído. É importante dizer na descrição <em>quando</em> a skill deve ser "
             "usada — isso ajuda o Claude a guardá-la certo e a decidir quando chamá-la."),
            ("Como o Claude sabe quando usar uma skill?",
             "Digite " + ic("/context") + " no Claude — você verá uma parte do "
             + g("Contexto", "contexto") + " reservada às skills. O nome e a descrição de "
             "toda skill ficam sempre carregados. Ao receber um pedido, o Claude varre essas "
             "descrições; se uma combina, ele carrega o resto da skill e a segue. Por isso "
             "uma descrição clara é crucial."),
            ("Então skills são sempre arquivos .md com uma descrição de como funcionam?",
             "Sim. O " + ic("SKILL.md") + " tem nome e descrição sempre carregados; se o "
             "pedido combina com a descrição, o Claude carrega o corpo da skill e o usa. "
             "Skills podem fazer de “escrever uma apresentação no estilo da empresa” a "
             "tarefas bem mais amplas."),
        ]),
        tag="FAQ"))
    b.append(details(
        "Opcional · Vá mais fundo",
        P("Rode a mesma receita em outro domínio — e-mails. Cole um e-mail seu em "
          + ic("email_sample.md") + " e:")
        + prompt("Leia email_sample.md. Espelhe o tom — tamanho das frases, saudação,\n"
                 "despedida, o jeito como eu abro e fecho.\n"
                 "Agora transforme o que aprendeu em uma skill chamada create-prosus-email\n"
                 "que dispare sempre que eu pedir um rascunho, resposta ou follow-up de e-mail.")
        + P("Confirme em uma sessão nova: peça um rascunho sobre qualquer coisa. Slides "
            "(do 2.1) e e-mails agora saem no estilo certo por padrão — mesma receita, duas "
            "skills, zero re-explicação."),
        tag="Vá mais fundo"))
    return "".join(b)


def ex_2_2():
    b = []
    b.append(P("Sinta como é fácil aprender algo novo. Aprender deixou de ser sobre o "
               "material — passou a ser sobre saber o que você precisa aprender."))
    b.append(SESSION_STEP)
    b.append(prompt("Explique para mim o conceito \"skill.md\", visualize, eu sou de\n"
                    "negócios e não de tecnologia, use palavras simples."))
    b.append(prompt("Agora explique também o conceito de skills em geral, além do .md",
                    label="Prompt de continuação"))
    b.append(H2("Agora use o Person.md"))
    b.append(P("Primeiro, faça o seu próprio " + ic("person.md") + " — um arquivo de cinco "
               "linhas que diz ao Claude quem você é, o que está resolvendo e como gosta de "
               "ser tratado. Salve ao lado de onde você está trabalhando."))
    b.append(SESSION_STEP)
    b.append(prompt("Leia person.md, explique para mim o skill.md e visualize."))
    b.append(details(
        "Travou? Debrief — o que deveria ter acontecido",
        P("Duas visualizações do mesmo conceito (uma " + g("Skill", "skill") + "): uma "
          "genérica e uma personalizada. A genérica está ok. A personalizada é o momento em "
          "que a lição entra.")
        + P("O ponto: você consegue ensinar quase qualquer coisa a si mesmo com um prompt de "
            "uma linha e um " + ic("person.md") + " de cinco linhas. Aprender deixa de ser "
            "sobre o material e passa a ser sobre saber o que perguntar."),
        tag="Debrief"))
    b.append(details(
        "Travou? Perguntas frequentes deste exercício",
        faq([
            ("Recebi “não existe skills.md” — eu deveria ter baixado um arquivo?",
             "“Skill” é um conceito, não um arquivo que você precisa ter. Ajuste o prompt "
             "para “explique o conceito skill.md” ou “isto é um conceito, não um arquivo "
             "real” e o Claude explicará em vez de procurar um arquivo."),
            ("Onde o person.md deve ficar?",
             "Salve na pasta de onde você está rodando o Claude Code, com o nome exato "
             + ic("person.md") + " — é o caminho que o prompt acima espera. Se guardou em "
             "outro lugar, mova-o ou atualize o prompt para o caminho real."),
            ("O que vai dentro de um person.md?",
             "Cinco linhas bastam: seu papel, o que você está resolvendo, como gosta de "
             "pensar e como gosta de ser tratado."),
        ]),
        tag="FAQ"))
    b.append(details(
        "Opcional · Vá mais fundo",
        P("Escolha algo que você realmente não sabe fazer — Remotion, " + g("FLAML")
          + ", Whisper, pptxgenjs — e peça ao Claude para ensinar com um exemplo executável:")
        + prompt("Me ensine Remotion. Faça um vídeo de cinco segundos que eu possa\n"
                 "renderizar agora, explique cada linha e me diga o que quebrar primeiro\n"
                 "para aprender.")
        + P("O prompt que pede ensino devolve código, explicação e um ponto de partida — "
            "tudo junto. O agente é o seu tutor mais rápido; o gargalo é só saber o que pedir."),
        tag="Vá mais fundo"))
    b.append(details(
        "Reflexão · Interlúdio B — Skills como memória durável",
        P("Você já usou " + g("Contexto", "contexto") + " de dois jeitos. <strong>Arquivos "
          "soltos</strong> (" + ic("person.md") + "): largados ao lado de um prompt, no "
          "escopo daquela " + g("Sessão", "sessão") + ". <strong>Skills</strong> "
          "(create-prosus-presentation): registradas com o Claude, com escopo de projeto / "
          "conta / plugin, acionadas automaticamente quando a descrição combina.")
        + P("O modelo mental: um arquivo solto é um post-it na mesa de um colega. Uma skill "
            "é uma seção do manual da empresa. Os dois ajudam. O manual acumula. Regra "
            "prática: toda vez que você responder a mesma pergunta duas vezes, escreva uma "
            "skill. A terceira vez sai de graça."),
        reflect=True, tag="Reflexão"))
    return "".join(b)


def ex_2_3():
    b = []
    b.append(P("Sinta como é fácil aprender algo novo — usando um VÍDEO!"))
    b.append(SESSION_STEP)
    b.append(prompt("Crie um vídeo apresentando o <nome>.md usando Remotion\n"
                    "Mantenha no máximo 4 cenas"))
    b.append(P("Troque <nome> pelo seu nome (você já deve ter o " + ic("<nome>.md")
               + " do Exercício 2.2). O agente usa Remotion para renderizar o vídeo. Veja "
               "uma introdução de 4 cenas sobre você surgir com um único prompt."))
    b.append(details(
        "Travou? Debrief — o que deveria ter acontecido",
        P("Um vídeo de quatro cenas, temático sobre a pessoa, renderizado em disco e "
          "provavelmente reproduzível direto da pasta. Se o agente pediu para adicionar "
          "legendas, ele provavelmente instalou o Whisper sozinho para transcrever.")
        + P("A lição: o limite do que seu agente faz por você é, em boa parte, o limite das "
            "palavras que você conhece. Acrescentar “Remotion” ao seu vocabulário destravou "
            "uma capacidade hoje. O mesmo vale para “" + g("FLAML", "FLAML") + "”, "
            "“pptxgenjs”, “" + g("Vercel", "Vercel") + "”, “Whisper” e dezenas de outras. O "
            "Claude conhece as ferramentas. Você só precisa saber os nomes."),
        tag="Debrief"))
    b.append(details(
        "Travou? Perguntas frequentes deste exercício",
        faq([
            ("A saída em vídeo é incrível — tem limite de duração? Dá para fazer séries?",
             "Não há limite que você alcance facilmente — vídeos de 6 minutos são viáveis; "
             "dá para transcrever sua própria voz e sincronizar cenas. Funciona porque o "
             "Claude Code planeja tarefas longas e as quebra em passos pequenos. Combine com "
             "uma API de texto-para-voz realista e praticamente não há limite."),
            ("De onde o arquivo .md tira as informações?",
             "Em geral, esses arquivos de pessoa são montados com a ajuda do Claude — "
             "reunindo aparições públicas (podcasts, vídeos, entrevistas) e consolidando num "
             "[nome].md. Se há conteúdo em outro idioma nas aparições, o arquivo pode "
             "“saber” escrever naquele idioma."),
        ]),
        tag="FAQ"))
    b.append(details(
        "Opcional · Vá mais fundo",
        P("Re-renderize a mesma composição para celular — 9:16, pronto para stories.")
        + prompt("Renderize o vídeo de novo em 1080×1920 (9:16, retrato), com cenas mais curtas.")
        + P("Mesmo conteúdo, otimizado para o vertical. O mesmo truque vale para quadrado "
            "(1:1) ou 16:9. Uma mudança de configuração, distribuição completamente diferente."),
        tag="Vá mais fundo"))
    return "".join(b)


def ex_2_4():
    b = []
    b.append(P("Todo mundo conhece a sensação: “isto parece coisa de IA”. Dá para encarar "
               "como defeito ou consertar dando ao agente a sua própria voz. Essa voz vive "
               "no seu " + ic("<nome>.md") + "."))
    b.append(SESSION_STEP)
    b.append(prompt("Rascunhe um e-mail no meu tom de voz usando o <nome>.md\n"
                    "A mensagem que quero transmitir é:\n"
                    "A forma como as empresas se organizam está prestes a mudar para sempre.\n"
                    "Não de forma incremental. Fundamentalmente.\n"
                    "Estamos saindo de organogramas hierárquicos — divididos por departamentos,\n"
                    "cheios de gargalos de aprovação — rumo a algo diferente: organizações\n"
                    "inteligentes e orientadas a processos, onde fluxos agênticos rodam loops\n"
                    "limitados entre checkpoints humanos.\n"
                    "Isto não é um ganho de produtividade. É um repensar de toda a estrutura.\n"
                    "Me devolva diretamente para eu conferir aqui; não crie um rascunho de verdade"))
    b.append(P("Depois pergunte a si mesmo: <em>este é um e-mail que você escreveria?</em>"))
    b.append(details(
        "Travou? Debrief — o que deveria ter acontecido",
        P("Um rascunho que soa plausivelmente como <em>você</em>, não genérico. Repare na "
          "trava deliberada do prompt: <em>me devolva diretamente; não crie um rascunho de "
          "verdade</em>.")
        + callout("Nunca deixe um agente enviar algo em seu nome sem você ler antes. Injeção "
                  "de prompt vinda de conteúdo de terceiros (o e-mail que você responde, o "
                  "documento que resume) é uma superfície de ataque real. Confira antes de "
                  "enviar.", label="Segurança", kind="warn"),
        tag="Debrief"))
    b.append(details(
        "Travou? Perguntas frequentes deste exercício",
        faq([
            ("Isso generaliza bem? Mensagem de Slack, memorando, post no LinkedIn?",
             "Sim — mesmo padrão. O " + ic("<nome>.md") + " é a voz; o prompt é a mensagem. "
             "O truque é manter o arquivo de voz rico (3–5 parágrafos de como você realmente "
             "escreve)."),
            ("Há preocupação de confidencialidade se o Claude ler meus e-mails?",
             "Em contas corporativas, o provedor não guarda os dados nem os usa para treino — "
             "mesmo nível de confiança de um serviço de e-mail ou armazenamento em nuvem. "
             "Sempre siga as políticas internas de segurança."),
        ]),
        tag="FAQ"))
    b.append(details(
        "Opcional · Vá mais fundo",
        P("Inverta o exercício. Pegue o " + ic("person.md") + " de um colega e:")
        + prompt("Leia <colega>.md. Rascunhe um e-mail DELE PARA MIM, na voz dele,\n"
                 "resumindo o que ele mais gostaria que eu soubesse sobre a semana dele.\n"
                 "Me devolva diretamente; não crie um rascunho de verdade.")
        + P("A mesma engrenagem em espelho — a voz flui do arquivo nos dois sentidos. Útil "
            "para se preparar para um 1:1 e imaginar como o outro lado soa antes de falar."),
        tag="Vá mais fundo"))
    return "".join(b)


def ex_2_5():
    b = []
    b.append(P("Transforme um fluxo de trabalho repetitivo em um comando reutilizável."))
    b.append(callout(
        "Conecte o Google Agenda e/ou e-mail. São " + g("Conector", "conectores")
        + " — pequenas pontes que permitem ao Claude Code ler sua agenda ou caixa de entrada "
        "em seu nome. Em Configurações → Conectores, entre na sua conta e conceda só os "
        "escopos com que você se sente confortável. Você pode revogar a qualquer momento. "
        "Prefira permissão somente-leitura.", label="Setup"))
    b.append(SESSION_STEP)
    b.append(prompt("Verifique as últimas 24h do meu e-mail"))
    b.append(P("<strong>Em seguida</strong>, torne o fluxo seu: ajuste como quer os "
               "resultados, defina o que é importante e o que não é. Quando estiver "
               "satisfeito com o resumo, aplique a mágica do Claude Code:"))
    b.append(prompt("Transforme o fluxo acima em um único comando do Claude: /check-mail\n"
                    "Salve em ~/.claude/commands/\n"
                    "Ele precisa instruir a fazer a verificação do e-mail de uma só vez,\n"
                    "como descrevi acima"))
    b.append(details(
        "Travou? Debrief — o que deveria ter acontecido",
        P("Um " + g("Comando de barra", "comando de barra") + " " + ic("/check-mail")
          + " funcionando em " + ic("~/.claude/commands/check-mail.md") + ", que ao ser "
          "chamado resume as últimas 24h da sua caixa segundo as suas regras. O arquivo é só "
          "markdown. Leia. Edite. Amanhã você refina as regras sem tocar em código."),
        tag="Debrief"))
    b.append(details(
        "Travou? Perguntas frequentes deste exercício",
        faq([
            ("Quais conectores são necessários?",
             "Um basta — o e-mail é um bom padrão por ser usado diariamente. O exercício é "
             "mais sobre o fluxo do que sobre o conector específico."),
            ("Devo conceder todas as permissões que aparecem, inclusive “apagar tudo”?",
             "O e-mail somente-leitura é o mais seguro — ele só lê, não envia. Usamos para "
             "resumir e-mails, então conecte com permissão de leitura. Evite conceder "
             "escrita/envio/exclusão a menos que realmente precise."),
            ("O comando de barra nunca apareceu. Como faço o " + ic("/check-mail")
             + " funcionar?",
             "Duas coisas: reinicie o Claude Code por completo (não só feche a janela) — "
             "comandos só atualizam ao reiniciar; e, para comandos de projeto, você precisa "
             "estar dentro da pasta do projeto. Para comandos globais, coloque o arquivo em "
             + ic("~/.claude/commands/") + "."),
        ]),
        tag="FAQ"))
    b.append(details(
        "Opcional · Vá mais fundo",
        P("Componha um segundo comando — " + ic("/morning-brief") + " — a partir das peças "
          "que você já tem. Inicie uma nova sessão:")
        + prompt("Crie um comando /morning-brief em ~/.claude/commands/morning-brief.md.\n"
                 "Ele deve:\n"
                 "- rodar a mesma lógica do /check-mail (últimas 24h, minhas regras)\n"
                 "- adicionar a agenda de hoje (próximas 8 horas, só título + horário + quem)\n"
                 "- adicionar os PRs abertos atribuídos a mim (use a CLI gh)\n"
                 "- produzir uma tela combinada que eu leia em 60 segundos")
        + P("Reinicie o Claude Code e digite " + ic("/morning-brief") + ". Você compôs três "
            "fluxos em um atalho — sem escrever uma linha de código fora do arquivo "
            + ic(".md") + ". Reutilize, não reescreva."),
        tag="Vá mais fundo"))
    return "".join(b)


def ex_3_1():
    b = []
    b.append(P("O 1.1 deu o UAU. O 1.2 mostrou que o " + g("Contexto", "contexto")
               + " vence o prompt. Agora subimos um nível: deixe o agente <em>ver</em> o que "
               "construiu, criticar a própria saída e iterar. É a jogada que separa o uso "
               "amador do profissional."))
    b.append(H2("Escolha UM artefato para iterar"))
    b.append(P("<strong>A)</strong> Seu jogo — crie um jogo que simule algo do seu negócio. "
               "<strong>B)</strong> Um dashboard do seu domínio — dataset real ou fictício, "
               "gráficos, filtros, interatividade. Algo que plausivelmente viveria dentro da "
               "sua empresa na segunda-feira."))
    b.append(callout(
        "Na página <a href='../arquivos.html'>Arquivos</a> há um dataset de e-commerce de "
        "exemplo para dashboards e um " + ic("snake-example.html") + " caso você tenha "
        "pulado os exercícios 1.1/1.2. O maior acervo de datasets fica em huggingface.co/"
        "datasets (não baixe 100 GB!).", label="Recursos extras"))
    b.append(H2("Comece"))
    b.append(prompt("Leia <nome>.md, eu quero fazer .......... usando .....\n"
                    "Me faça algumas perguntas para construirmos isto juntos.\n"
                    "O objetivo é fazer algo que mostre o poder da IA\n"
                    "e que eu possa compartilhar com meus colegas via Vercel.\n"
                    "A reação deles tem que ser \"Uau, foi você que fez isso?\""))
    b.append(H2("Em repetição"))
    b.append(prompt("Abra e examine. Depois reflita sobre a sua própria\n"
                    "criação e proponha três melhorias concretas."))
    b.append(prompt("Olha esse botão, está pequeno demais para clicar", label="Prompt (exemplo)"))
    b.append(P("O agente vê o artefato (screenshots, DOM, console), critica e propõe "
               "mudanças. Você concorda com algumas, rejeita outras. Reexecuta. Veja. Itere. "
               "<strong>Faça isto pelo menos duas vezes.</strong> Repare como você digita "
               "menos e muda mais."))
    b.append(H2("Publique"))
    b.append(prompt("Faça o deploy na Vercel e me dê a URL pública"))
    b.append(callout(
        "Por que fazemos isto: iteração é como o trabalho de verdade acontece. One-shots são "
        "demos. O loop profissional é ver → criticar → atualizar contexto → reexecutar. "
        "Você não está revisando o código — está revisando se o agente fez o que você quis dizer.",
        label="O ponto do capítulo"))
    b.append(details(
        "Travou? Debrief — o que deveria ter acontecido",
        P("Uma URL publicada que parece bem melhor que a versão 1. E, principalmente, você "
          "mal digitou. O trabalho aconteceu no " + g("Loop", "loop") + " entre agente e "
          "artefato. Você saiu do metrônomo do pergunta-e-responde."),
        tag="Debrief"))
    b.append(details(
        "Travou? Perguntas frequentes deste exercício",
        faq([
            ("Como atingir aquele nível de qualidade de design?",
             "Peça ao Claude Code para fazer perguntas, buscar referências em outros sites, "
             "agir como um designer minimalista e simplificar o máximo possível. Depois "
             "adicione alguns toques, como um botão de modo escuro."),
            ("Posso mandar uma pasta de arquivos e pedir um resumo de cada um?",
             "Sim. Abra uma " + g("Sessão", "sessão") + " naquela pasta e peça: “explore "
             "todos os arquivos desta pasta e gere um resumo executivo”. Ele lê e produz o .md."),
        ]),
        tag="FAQ"))
    b.append(details(
        "Opcional · Vá mais fundo",
        P("Mini-hackathon — escolha UMA trilha. O loop é o mesmo; muda o artefato. Rode "
          "ver → criticar → iterar de ponta a ponta:")
        + "<p><strong>Trilha A — Slide.</strong> Gere um slide no estilo da empresa sobre um "
          "tema que importa. Screenshot. Peça crítica contra a marca. Itere até passar numa "
          "revisão executiva.</p>"
        + "<p><strong>Trilha B — E-mail.</strong> Rascunhe um e-mail com checagem de tom "
          "usando seu " + ic("voice.md") + ". Renderize em PDF. Peça crítica contra o arquivo "
          "de voz. Itere até soar como você.</p>"
        + "<p><strong>Trilha C — Dashboard.</strong> Construa um dashboard de métricas de uma "
          "página (dados fictícios servem). Screenshot. Peça crítica contra um painel que "
          "você usa de verdade. Itere até parecer plausível na wiki do seu time.</p>"
        + P("Qualquer que seja: a lição é o loop, não o artefato — ver → criticar → "
            "atualizar contexto → reexecutar. O formato é acessório."),
        tag="Vá mais fundo"))
    return "".join(b)


def ex_4():
    b = []
    b.append(P("Todo mundo adora deep research — vamos pegar a ideia de pesquisa profunda e "
               "deixar a IA fazer um " + g("Loop", "loop") + " sobre ela."))
    b.append(H2("Antes"))
    b.append(prompt("Pesquise na web sobre AutoResearch aplicado a negócios"))
    b.append(P("Rode isto para ver o “antes”."))
    b.append(H2("Depois"))
    b.append(prompt("Pesquise na web sobre \"AutoResearch aplicado a negócios\". Mantenha UM\n"
                    "relatório em AR-applications.md — edite e reorganize conforme aprende,\n"
                    "não apenas anexe. A cada passagem, pense em novos termos de busca para\n"
                    "preencher lacunas e achar novas direções, e itere. Repita 5 vezes.\n"
                    "(não use a ferramenta /loop)"))
    b.append(P("O loop roda 5 iterações e para sozinho."))
    b.append(H2("Plugin permanente"))
    b.append(prompt("Clone: https://github.com/fjfok/Humboldt\n"
                    "Coloque em ~/Documents/github/\n"
                    "Instale este plugin usando /plugin"))
    b.append(P("Depois: pergunte ao Claude como usá-lo e experimente."))
    b.append(details(
        "Travou? Debrief — o que deveria ter acontecido",
        P("Um arquivo " + ic("AR-applications.md") + " na sua pasta, bem mais longo e útil do "
          "que uma única busca produziria. Repare que o agente gera novos ângulos de busca "
          "que você não teria pensado — não é mágica, é persistência aplicada à pergunta “o "
          "que está faltando aqui?”.")
        + P("Você também aprendeu algo sobre o seu próprio trabalho: onde, no seu dia, você "
            "faz buscas de um tiro só e para no primeiro resultado razoável? Isso é "
            "candidato a virar loop. Iteração vence inteligência."),
        tag="Debrief"))
    b.append(details(
        "Travou? Perguntas frequentes deste exercício",
        faq([
            ("Dá um caso real onde essa distribuição de conhecimento via arquivo .md "
             "funcionaria?",
             "Imagine refinar as perguntas sugeridas de um assistente conversacional, "
             "analisando o histórico para promover exploração de recursos. Depois de algumas "
             "iterações, você teria um .md resumindo aprendizados — transferível para outros "
             "padrões de assistente."),
            ("Para um problema de ranqueamento, dá para usar AutoResearch?",
             "Em princípio sim — se você tem um benchmark e uma métrica clara, não há motivo "
             "para o padrão não se aplicar. Padrão: pequenos experimentos → escolher os "
             "melhores → escalar → testar A/B em produção."),
        ]),
        tag="FAQ"))
    b.append(details(
        "Opcional · Vá mais fundo",
        P("Reexecute o loop com uma restrição invertida — mesmo tema, formato diferente.")
        + prompt("Continue o loop no AR-applications.md, mas desta vez:\n"
                 "- só aceite achados embasados por uma fonte primária (artigo, relatório de\n"
                 "  empresa, ≥2024)\n"
                 "- ignore posts de blog e listicles\n"
                 "- quando achar uma contradição com o que já está no arquivo, marque-a\n"
                 "  explicitamente")
        + P("Veja os termos de busca que o agente inventa mudarem. Uma restrição diferente "
            "remodela o caminho pelo mesmo problema — essa é a lição, não o tema."),
        tag="Vá mais fundo"))
    return "".join(b)


def ex_5():
    b = []
    b.append(P("O Exercício 4 repetia a mesma tarefa N vezes. Este é diferente: o "
               + g("Loop", "loop") + " <em>mede</em>, <em>muda uma variável</em> e roda de "
               "novo, tentando superar a própria pontuação anterior. É o " + g("AutoResearch")
               + " mínimo viável."))
    b.append(P("Usamos uma tarefa de machine learning pequena e amigável à " + g("CPU vs GPU", "CPU")
               + " para o loop convergir na hora. Sem GPU, sem nuvem, sem espera."))
    b.append(callout(
        "O " + g("Baseline", "baseline") + " é " + ic("StandardScaler → LogisticRegression(C=1.0)")
        + ". Ele pontuou: " + ic("val_auc = 0.8896") + " e " + ic("test_auc = 0.8690") + ". A "
        + g("AUC") + " vai de 0,5 (chute) a 1,0 (perfeito). O trabalho do loop é empurrar "
        "esses números para cima.", label="O baseline"))
    b.append(H2("A tarefa"))
    b.append(prompt("Clone este repositório: https://github.com/fjfok/autoresearch-edu\n"
                    "Coloque em ~/Documents/github/\n"
                    "Vá para a pasta recém-criada."))
    b.append(callout(
        "Inicie uma nova sessão do Claude Code. Quando ele perguntar qual pasta abrir, dê "
        "dois cliques na pasta " + ic("autoresearch-edu") + " para abri-la como projeto.",
        label="Isto precisa ser feito manualmente", kind="warn"))
    b.append(P("<strong>Confirme que está no lugar certo.</strong>"))
    b.append(prompt("Quais arquivos existem nesta pasta?"))
    b.append(P("Você deve ver, mais ou menos: " + ic(".claude/") + ", " + ic("README.md")
               + ", " + ic("prepare.py") + ", " + ic("program.md") + ", " + ic("train.py")
               + ". O sinal-chave é que " + ic("train.py") + ", " + ic("program.md") + " e "
               + ic(".claude/") + " estão presentes."))
    b.append(prompt("Verifique se você tem tudo instalado para rodar o código deste repositório"))
    b.append(P("Este repositório inclui um " + g("Comando de barra", "comando de barra")
               + " custom em " + ic(".claude/commands/autoresearch.md") + ". Dispare o loop "
               "do chat:"))
    b.append(prompt("/autoresearch"))
    b.append(details(
        "Não vê o comando /autoresearch?",
        P("Dois planos B: (1) reinicie a aplicação do Claude por completo — comandos de "
          "projeto só atualizam num reinício total; (2) se ainda não aparecer, cole este "
          "prompt:")
        + prompt("Leia .claude/commands/autoresearch.md e siga aquelas instruções"),
        tag="Travou?"))
    b.append(P("O comando carrega o dataset, estabelece um baseline, roda o " + g("FLAML")
               + ", executa N iterações de catraca (ratchet) e gera as visualizações finais."))
    b.append(details(
        "Debrief — o que deveria ter acontecido",
        P("Uma nova pontuação " + ic("test_auc") + " que supera " + ic("0.8690") + ". Uma "
          "visualização mostrando a catraca — a pontuação subindo em degraus, às vezes "
          "revertendo quando uma mudança piorou, e subindo de novo. Um registro de aprendizados.")
        + P("É o menor loop de AutoResearch de nível produção. Internalize o formato: "
            "<strong>Fixo</strong> (interface de dados, scorer, split de avaliação); "
            "<strong>Livre</strong> (o que o agente edita: modelo, escala, hiperparâmetros, "
            "subconjunto de features); <strong>Catraca</strong> (mantém a mudança se superar "
            "o melhor até agora, reverte caso contrário); <strong>Parar</strong> (N iterações "
            "ou K rodadas sem melhora)."),
        tag="Debrief"))
    b.append(details(
        "Perguntas frequentes deste exercício",
        faq([
            ("Recebi erros — uv não instalado, Python 3.9 vs 3.10, sem venv. O que faço?",
             "Se o seu ambiente permitir e você seguir as orientações internas de TI, peça ao "
             "Claude Code para te guiar pela instalação. Em máquinas corporativas, prefira "
             "fluxos de instalação aprovados ou consulte o suporte."),
            ("Estou permitindo 99% das coisas. O que vocês recomendam?",
             "Para o curso, liberar os pacotes listados está ok. Fora do curso, consulte a "
             "TI para qualquer coisa nova. Hábito de segurança: a qualquer momento, pergunte "
             "ao Claude “olhe tudo que fiz até agora e me diga se criei alguma vulnerabilidade”."),
            ("Como isto é melhor que um sweep, Monte Carlo ou otimização Bayesiana?",
             "Agentes de raciocínio usam o conhecimento de mundo do modelo para gerar "
             "hipóteses sobre o que tentar a seguir, em vez de amostrar aleatoriamente. Menos "
             "passos até o ótimo — e isso torna viável otimizar processos reais de negócio."),
            ("Qual é o escopo de mudanças que o AutoResearch pode fazer?",
             "O " + ic("program.md") + " define o que está no escopo (ex.: só o "
             + ic("train.py") + ") e o que está fora. Há também um orçamento de tempo fixo "
             "por iteração para manter a eficiência."),
        ]),
        tag="FAQ"))
    b.append(details(
        "Opcional · Vá mais fundo",
        P("Aponte o mesmo loop para outro alvo no mesmo dataset.")
        + prompt("Rode o /autoresearch de novo com a coluna-alvo trocada de conversão para LTV\n"
                 "(ou churn, ou receita por sessão — escolha uma).\n"
                 "Mantenha todo o resto idêntico: mesmo split treino/validação/teste, mesmo\n"
                 "formato do scorer, mesmo orçamento. Escreva em um results.tsv separado.")
        + P("Quando terminar, compare os dois " + ic("learnings.md") + ". Mesmos dados, duas "
            "perguntas — as features descobertas se sobrepõem, ou cada alvo quer um modelo "
            "diferente?"),
        tag="Vá mais fundo"))
    return "".join(b)


def ex_6():
    b = []
    b.append(P("No Exercício 5 o " + g("Loop", "loop") + " já vinha montado — você rodou "
               + ic("/autoresearch") + " e assistiu. Desta vez você o constrói. Mesmo "
               "formato, domínio diferente: um simulador de restaurante em vez de um modelo "
               "de propensão."))
    b.append(H2("O que você está otimizando"))
    b.append(P("Você administra <strong>The Rotterdam Table</strong> — um bistrô europeu "
               "casual em Roterdã — por 30 dias. Sua única alça sobre o mundo é "
               + ic("python -m rest_sim <comando>") + ": ler estado, decidir, avançar, repetir."))
    b.append('<div class="spec-grid">'
             + spec_cell("Local", "Bistrô europeu", "22 mesas · 78 lugares")
             + spec_cell("Duração", "30 dias", "um turno / dia")
             + spec_cell("Caixa inicial", "€10.000", "moeda: €")
             + spec_cell("Seed", "20260423", "RNG determinístico")
             + "</div>")
    b.append(P("O loop diário: <code class='inline'>status</code> (ler estado) → "
               "<code class='inline'>decide</code> (0–N ações — o único passo do LLM) → "
               "<code class='inline'>advance</code> (+1 dia) → repete 30×. O “cérebro” que "
               "vive dentro do " + ic("decide") + " é " + ic(".claude/agents/restaurant-manager.md")
               + " — esse é o arquivo que o seu loop vai modificar."))
    b.append(H3("As alavancas que você controla"))
    b.append(P("INVENTÁRIO, MENU, EQUIPE, RESERVAS, MARKETING, LAYOUT — comandos como "
               + ic("restock") + ", " + ic("set-price") + ", " + ic("add-item") + ", "
               + ic("set-staff") + ", " + ic("set-cap") + ", " + ic("promo") + ", "
               + ic("convert-table") + ", além de visões somente-leitura (" + ic("status")
               + ", " + ic("kpis") + ", " + ic("pnl") + ", " + ic("heatmap") + ", "
               + ic("news") + "). O trabalho do agente é escolher quais disparar em cada dia."))
    b.append(H3("Como você é pontuado"))
    b.append('<div class="scorebar">'
             '<div class="row"><span class="pos">+ lucro líquido total</span><span>sempre</span></div>'
             '<div class="row"><span class="neg">− 200k × Δsat²</span><span>se sat &lt; 0,78</span></div>'
             '<div class="row"><span class="neg">− 80k × Δrep²</span><span>se rep &lt; 4,10</span></div>'
             '<div class="row"><span class="neg">− 8 × walkouts</span><span>por desistência</span></div>'
             "</div>")
    b.append(callout(
        "Se o caixa cair abaixo de −€5.000, a execução para e a pontuação trava em −€150.000. "
        "Onde você está no dia 30: não fazer nada ≈ −€5.577; Haiku padrão ≈ +€24.129 (← o "
        "piso a superar); Opus reportado ≈ €100k. <strong>Meta: superar +€24.129 de lucro "
        "líquido mantendo reputação ≥ 4,0 e satisfação ≥ 0,75.</strong>", label="Placar"))
    b.append(H2("Setup"))
    b.append(P("<strong>1. Clone o " + g("Repositório", "repositório") + ".</strong> Na sua "
               "sessão atual do Claude Code:"))
    b.append(prompt("Clone este repositório: https://github.com/fjfok/REST-bench\n"
                    "Coloque em ~/Documents/github/"))
    b.append(P("<strong>2. Abra essa pasta numa sessão nova — manualmente.</strong> O Claude "
               "Code não troca o próprio diretório no meio da sessão: feche-o (ou abra uma "
               "janela nova), inicie uma sessão e dê dois cliques na pasta " + ic("REST-bench") + "."))
    b.append(P("<strong>Confirme que está no lugar certo.</strong>"))
    b.append(prompt("Quais arquivos existem nesta pasta?"))
    b.append(P("Você deve ver " + ic("rest_sim/") + " e " + ic(".claude/") + " presentes."))
    b.append(P("<strong>3. Confira a instalação.</strong>"))
    b.append(prompt("Verifique se você tem tudo instalado para rodar o código deste repositório"))
    b.append(details(
        "Dois erros possíveis nesta etapa",
        "<p><strong>1) Python não instalado (Windows).</strong> Acesse python.org/downloads, "
        "baixe o instalador do Python 3 e, na primeira tela, marque “Add python.exe to "
        + g("PATH", "PATH") + "” antes de instalar. Depois confira num novo Prompt de Comando:</p>"
        + prompt("python --version\npip --version")
        + "<p><strong>2) numpy ausente.</strong> Peça ao Claude para instalar, ou rode:</p>"
        + prompt("python3 -m pip install --user numpy"),
        tag="Instalação"))
    b.append(H2("Reproduza o baseline (3 min)"))
    b.append(P("Antes de otimizar, rode o " + g("Baseline", "baseline") + " você mesmo para "
               "ter o ground truth."))
    b.append(prompt("/play-month 30 20260423"))
    b.append(P("Mesmos argumentos do baseline (" + ic("30") + " = dias, " + ic("20260423")
               + " = seed). Sua execução deve cair perto de +€24.129 — o piso que seu loop "
               "precisa superar. Enquanto o " + ic("/play-month") + " roda, o REST-bench "
               "serve um dashboard ao vivo em http://localhost:8765. Se a porta 8765 estiver "
               "ocupada:"))
    b.append(prompt("python -m rest_sim dashboard --port 8766"))
    b.append(H2("A tarefa: converter isto em AutoResearch"))
    b.append(P("Baixe o primer de AutoResearch (página <a href='../arquivos.html'>Arquivos</a>: "
               + ic("autoresearch-build-your-own.md") + ") e arraste-o para o Claude Code."))
    b.append(prompt("Leia o \"autoresearch-build-your-own.md\" anexado.\n"
                    ".claude/agents/restaurant-manager.md é o único arquivo que o loop pode\n"
                    "editar (como o train.py)\n"
                    "Nosso objetivo é maximizar o lucro líquido do fim do mês mantendo a\n"
                    "reputação saudável (>= 4.0) e a satisfação >= 0.75.\n"
                    "Crie um comando (.claude/commands/auto-research) que: edite o\n"
                    "restaurant-manager.md; rode o /play-month; escreva os resultados;\n"
                    "aprenda; repita dentro dos limites!\n"
                    "Escreva os resultados em .tsv"))
    b.append(details(
        "Travou? Debrief — o que deveria ter acontecido",
        P("Um " + ic(".claude/commands/auto-research.md") + " funcionando que você escreveu "
          "com o agente; um arquivo " + ic(".tsv") + " com uma linha por iteração (mutações "
          "tentadas, métricas, mantido-ou-revertido); e uma nova pontuação que supera o baseline.")
        + P("Repare no mapeamento a partir do Exercício 5: " + ic("train.py") + " → "
            + ic("restaurant-manager.md") + " (o único arquivo que o loop edita); "
            + ic("prepare.py") + " → " + ic("/play-month") + " (o scorer, travado); "
            + ic("program.md") + " → seu novo comando " + ic("auto-research") + " (a lógica "
            "do loop). Esse mapeamento é a " + g("Skill", "skill") + "."),
        tag="Debrief"))
    b.append(details(
        "Travou? Perguntas frequentes deste exercício",
        faq([
            ("Dá para explicar o problema antes de começar?",
             "Veja “O que você está otimizando” no topo desta página — local, loop diário, o "
             "que é modelado, alavancas e placar. Em resumo: simulamos um bistrô em Roterdã "
             "com mesas, menu, equipe e estoque. As probabilidades vêm de dados reais do "
             "setor de serviços. Não modelamos clima nem sazonalidade."),
            ("O que o seed faz?",
             "Uma semente pseudoaleatória — garante os mesmos números “aleatórios” a cada "
             "execução, deixando o experimento reprodutível. Por isso o baseline fixa "
             + ic("--seed 20260423") + ": para seus números baterem com os nossos."),
            ("Então o manager é o equivalente do train.py?",
             "Sim — o " + ic("program.md") + " é o comando de AutoResearch (o loop). O "
             + ic("train.py") + " decide como treinar o modelo no exemplo anterior; o "
             + ic("restaurant-manager.md") + " decide como tocar o negócio aqui."),
            ("Como vejo em que dia a simulação está?",
             "O REST-bench traz um dashboard ao vivo em http://localhost:8765 e transmite "
             "cada avanço e decisão. Se preferir acompanhar por arquivos, abra o "
             + ic("results.tsv") + "."),
        ]),
        tag="FAQ"))
    b.append(details(
        "Opcional · Vá mais fundo",
        P("Tente outro benchmark — o YC-bench. Mesmo arcabouço de loop, domínio totalmente "
          "diferente.")
        + prompt("Clone https://github.com/FlorisFok/AutoResearchYC (construído sobre o\n"
                 "dataset yc-bench: https://huggingface.co/datasets/collinear-ai/yc-bench).\n"
                 "Mapeie os três papéis do REST-bench:\n"
                 "- restaurant-manager.md -> o arquivo de agente editável (o que ele vira aqui?)\n"
                 "- /play-month -> o scorer travado (qual o equivalente no yc-bench?)\n"
                 "- comando auto-research -> o mesmo formato, apontado para o novo harness.\n"
                 "Supere o baseline publicado.")
        + P("Compare as trajetórias lado a lado. Se o AutoResearch acha padrões análogos em "
            "dois domínios sem relação, você sentiu a generalidade do loop. Se ele empaca, a "
            "lacuna te diz exatamente o que torna um domínio “loop-ável”."),
        tag="Vá mais fundo"))
    return "".join(b)


def spec_cell(k, v, x=""):
    out = '<div class="spec-cell"><div class="sk">' + _html.escape(k) + '</div>'
    out += '<div class="sv">' + _html.escape(v) + "</div>"
    if x:
        out += '<div class="sx">' + _html.escape(x) + "</div>"
    return out + "</div>"


print("conteúdo dos exercícios definido.")

# ---------------------------------------------------------------------------
# Metadados + ordem
# ---------------------------------------------------------------------------
EXERCISES = [
    ("1.1", "I",  "1 de 11",  "10 min", "Cobrinha, cru",
     "Crie um jogo — sinta o UAU", ex_1_1),
    ("1.2", "I",  "2 de 11",  "15 min", "Cobrinha, com contexto",
     "O mesmo prompt — agora com contexto", ex_1_2),
    ("2.1", "I",  "3 de 11",  "30 min", "Ensine o agente",
     "Ensine algo novo ao seu agente!", ex_2_1),
    ("2.2", "I",  "4 de 11",  "25 min", "Explique a skill de volta",
     "Aprenda algo novo, do jeito fácil", ex_2_2),
    ("2.3", "I",  "5 de 11",  "30 min", "Vídeo de introdução com Remotion",
     "Aprenda algo novo, com um vídeo", ex_2_3),
    ("2.4", "I",  "6 de 11",  "20 min", "E-mail no seu tom de voz",
     "Escreva no seu próprio tom de voz", ex_2_4),
    ("2.5", "I",  "7 de 11",  "25 min", "Comando /check-mail",
     "Crie um comando a partir do seu fluxo", ex_2_5),
    ("3.1", "I",  "8 de 11",  "45 min", "Veja, critique, itere, publique",
     "Itere enxergando — o loop profissional", ex_3_1),
    ("4",   "II", "9 de 11",  "30 min", "Seu primeiro loop de pesquisa",
     "Crie seu primeiro loop", ex_4),
    ("5",   "II", "10 de 11", "60 min", "AutoResearch em um modelo de propensão",
     "Seu primeiro loop de aprendizado", ex_5),
    ("6",   "II", "11 de 11", "75 min", "AutoResearch no REST-bench",
     "Agora você constrói o loop", ex_6),
]
ACT_NAME = {"I": "Ato I — Sinta o poder", "II": "Ato II — Construa o loop"}


def slug(eid):
    return "exercise-" + eid


def build_exercise(i):
    eid, act, idx, mins, title, subtitle, fn = EXERCISES[i]
    prev = EXERCISES[i - 1] if i > 0 else None
    nxt = EXERCISES[i + 1] if i < len(EXERCISES) - 1 else None

    head = (
        '<a class="breadcrumb" href="index.html">← Todos os exercícios</a>'
        '<div class="meta-pill">Ato ' + act + " · " + idx + " · " + mins + "</div>"
        '<div class="step-head"><span class="ex-number">' + eid + "</span></div>"
        "<h1>" + _html.escape(title) + "</h1>"
        '<p class="subtitle">' + _html.escape(subtitle) + "</p>"
    )

    body = head + fn()

    # barra concluído
    if nxt:
        next_label = nxt[0] + " " + nxt[4]
        next_href = slug(nxt[0]) + ".html"
    else:
        next_label = "Finalizar — voltar a todos os exercícios"
        next_href = "index.html"
    done = (
        '<div class="done-bar" data-done-bar data-ex="' + eid + '" data-next-label="'
        + _html.escape(next_label) + '" data-next-href="' + next_href + '">'
        '<span class="grow">Terminou? Marque para acompanhar seu progresso.</span>'
        '<button class="btn" data-done-btn type="button">Marcar como concluído</button>'
        "</div>"
    )

    # prev / next
    pn = '<div class="prevnext">'
    if prev:
        pn += ('<a href="' + slug(prev[0]) + '.html"><div class="dir">← Anterior</div>'
               + '<div>' + prev[0] + " " + _html.escape(prev[4]) + "</div></a>")
    else:
        pn += "<span></span>"
    if nxt:
        pn += ('<a class="nx" href="' + slug(nxt[0]) + '.html"><div class="dir">Próximo →</div>'
               + '<div>' + nxt[0] + " " + _html.escape(nxt[4]) + "</div></a>")
    else:
        pn += ('<a class="nx" href="index.html"><div class="dir">Fim →</div>'
               + "<div>Todos os exercícios</div></a>")
    pn += "</div>"

    return page(eid + " " + title, body + done + pn, active="exercicios", depth=1)


def build_list():
    body = ['<h1>Currículo</h1>'
            '<p class="lede">Onze exercícios. Dois atos. Cerca de seis horas de ponta a '
            'ponta, menos se você pular os aprofundamentos. Cada exercício é '
            'autocontido — comece no 1.1, pule para o que importa, ou retome de onde parou.</p>']
    body.append('<div class="progress-bar"><span data-progress-fill></span></div>'
                '<p class="progress-text" data-progress-text>0 de 11 exercícios concluídos</p>')
    body.append('<div data-ex-list>')
    last_act = None
    for eid, act, idx, mins, title, subtitle, fn in EXERCISES:
        if act != last_act:
            if last_act is not None:
                body.append("</ul>")           # fecha a lista do ato anterior
            sub = ("um prompt, um app funcionando" if act == "I"
                   else "fluxos agênticos com revisão humana")
            body.append('<div class="act-head"><h2>' + ACT_NAME[act] + "</h2>"
                        '<div class="act-sub">' + sub + "</div></div>")
            body.append('<ul class="ex-list">')
            last_act = act
        body.append(
            '<a class="ex-row" data-ex-row="' + eid + '" href="' + slug(eid) + '.html">'
            '<span class="check">✓</span>'
            '<span class="num">' + eid + "</span>"
            '<span class="title">' + _html.escape(title) + "</span>"
            '<span class="dur">' + mins + "</span></a>"
        )
    body.append("</ul></div>")
    return page("Exercícios", "".join(body), active="exercicios", depth=1)


def build_home():
    body = (
        '<div class="hero">'
        "<h1>Reimagine <span class='accent'>o seu trabalho</span>.</h1>"
        '<p class="lede" style="max-width:620px;margin:0.6em auto 1.6em">'
        "Um curso prático de IA para líderes e equipes. ~6 horas de ponta a ponta, 2–3 se "
        "você for rápido. O objetivo é <em>sentir</em> — e não só ouvir falar — o que dá "
        "para fazer hoje com agentes de código como o Claude Code. Comece por aqui.</p>"
        '<a class="btn" href="exercicios/index.html">Estou pronto →</a>'
        "</div>"
        + callout(
            "Este curso é um ambiente educacional para experimentar ferramentas e fluxos de "
            "IA modernos. Exemplos, simulações e exercícios são ilustrativos e rodam em "
            "ambientes controlados. Implantação em produção, uso de dados de clientes, "
            "revisões de segurança e implementações operacionais permanecem sujeitos às "
            "políticas de governança, jurídico, privacidade e cibersegurança da sua "
            "organização.", label="Antes de começar")
    )
    return page("Início", body, active="", depth=0)


def build_help():
    body = [
        '<a class="breadcrumb" href="index.html">← Voltar ao início</a>',
        "<h1>Pedir ajuda</h1>",
        '<p class="lede">Escolha onde você travou. Cada caminho indica o que pedir ao seu '
        "assistente para destravar rápido.</p>",
        '<div class="card-grid">',
        '<a class="card" href="exercicios/exercise-1.1.html"><span class="k">Setup</span>'
        "<h3>Estou configurando minha máquina</h3>"
        "<p>Abra o Claude Code, crie uma pasta vazia e confirme com “Quais arquivos existem "
        "nesta pasta?”. Comece pelo Exercício 1.1.</p></a>",
        '<a class="card" href="exercicios/index.html"><span class="k">Exercícios</span>'
        "<h3>Estou travado em um exercício</h3>"
        "<p>Cada exercício tem blocos “Travou?” com Debrief e FAQ. Abra-os para o passo a "
        "passo do que deveria ter acontecido.</p></a>",
        '<a class="card" href="arquivos.html"><span class="k">Geral</span>'
        "<h3>Preciso de um arquivo do curso</h3>"
        "<p>Os arquivos referenciados nos exercícios (templates, exemplos, datasets) estão "
        "na página Arquivos, prontos para baixar.</p></a>",
        "</div>",
        callout(
            "Dica universal: a qualquer momento você pode colar o erro no chat e pedir “explique "
            "este erro em palavras simples e me dê o próximo passo”. O agente é o seu suporte "
            "de primeira linha.", label="Atalho"),
    ]
    return page("Pedir ajuda", "".join(body), active="ajuda", depth=0)


FILES = [
    ("person-template.md", "Template de person.md — quem você é, em 5 linhas (Ex. 2.2)"),
    ("prosus_management_overview.md", "Visão geral de exemplo de uma empresa fictícia (Ex. 2.1)"),
    ("autoresearch-build-your-own.md", "Primer de AutoResearch — como funciona e como construir o seu (Ex. 6)"),
    ("snake-example.html", "Cobrinha inicial, caso você tenha pulado o 1.1 / 1.2 (Ex. 3.1)"),
    ("ecommerce_sample.csv", "Dataset sintético de e-commerce para dashboards (Ex. 3.1)"),
]


def build_files():
    body = ['<a class="breadcrumb" href="index.html">← Voltar ao início</a>',
            "<h1>Arquivos</h1>",
            '<p class="lede">Arquivos referenciados nos exercícios. Clique para baixar e '
            "arraste para o chat do Claude Code quando o exercício pedir.</p>"]
    for fname, desc in FILES:
        body.append(
            '<div class="file-row"><span class="fname">' + _html.escape(fname) + "</span>"
            '<span class="fdesc">' + _html.escape(desc) + "</span>"
            '<a class="btn ghost dl" href="arquivos/' + fname + '" download>Baixar ↓</a></div>')
    body.append(callout(
        "Estes recursos foram preparados para esta versão local em português e são exemplos/"
        "templates ilustrativos — substitua pelos seus próprios dados quando for aplicar no "
        "seu contexto.", label="Sobre os arquivos"))
    return page("Arquivos", "".join(body), active="arquivos", depth=0)


# ---------------------------------------------------------------------------
# Recursos para download (autorais)
# ---------------------------------------------------------------------------
RES_PERSON = """# person.md — template

Cinco linhas bastam. Edite e salve ao lado de onde você roda o Claude Code.

- **Nome:** Maria Silva
- **Papel:** Diretora de operações em uma empresa de tecnologia.
- **O que estou resolvendo:** quero acelerar análises e protótipos sem depender de TI para cada experimento.
- **Como gosto de pensar:** começo pelo problema do cliente, prefiro exemplos concretos a teoria.
- **Como gosto de ser tratada:** direto ao ponto, em português, sem jargão; me mostre o resultado primeiro.
"""

RES_MGMT = """# Visão geral da empresa (EXEMPLO FICTÍCIO)

> Documento de exemplo criado para o curso. Não representa nenhuma empresa real.
> Use-o no Exercício 2.1 ou substitua pelo seu próprio material.

## Quem somos
A **Acme Digital** é um grupo de tecnologia que opera marketplaces e serviços
financeiros em mercados emergentes. Missão: usar tecnologia para melhorar a vida
de bilhões de pessoas.

## Segmentos
- **Marketplaces:** classificados, comércio e entrega de comida.
- **Pagamentos & Fintech:** carteira digital, crédito e remessas.
- **Edtech:** plataformas de aprendizagem.

## Números do ano (ilustrativos)
- Receita: € 6,2 bi (+18% a/a)
- Usuários ativos: 320 milhões
- Colaboradores: 24.000 em 30 países

## Prioridades estratégicas
1. Crescimento dos marketplaces com unit economics saudáveis.
2. Expansão responsável de crédito.
3. Adoção de IA em toda a operação — do atendimento à engenharia.

## Valores
Foco no cliente · Coragem · Simplicidade · Responsabilidade.
"""

RES_AUTORESEARCH = """# AutoResearch — como funciona e como construir o seu

> Primer escrito para esta versão local do curso (texto original em pt-BR).

## A ideia em uma frase
AutoResearch é um **loop** que transforma o agente em um pesquisador incansável:
ele tenta uma abordagem, **mede** o resultado contra uma métrica, **registra** o
que aprendeu e **decide** se mantém ou reverte a mudança — repetindo até um
critério de parada.

## As quatro peças
1. **Fixo** — o que nunca muda: a interface dos dados, o *scorer* (como a pontuação
   é calculada) e o split de avaliação (treino / validação / teste). Travar isso
   é o que impede o agente de "trapacear".
2. **Livre** — o que o agente pode editar: o modelo, o pré-processamento, os
   hiperparâmetros, o subconjunto de features. No Exercício 5 isso é o `train.py`;
   no Exercício 6 é o `restaurant-manager.md`.
3. **Catraca (ratchet)** — a regra de decisão: mantenha a mudança se ela superar a
   melhor pontuação até agora; reverta caso contrário. A pontuação só sobe.
4. **Parada** — N iterações, ou K rodadas seguidas sem melhora, ou um orçamento de
   tempo esgotado.

## O ciclo de cada iteração (≈ 9 passos)
1. Ler o estado atual (melhor pontuação, histórico).
2. Formular uma hipótese do que tentar a seguir.
3. Editar o arquivo "livre".
4. Rodar / pontuar.
5. Extrair métricas (pontuação, tempo, status).
6. Se quebrou, consertar.
7. Registrar resultado + hipótese em um log (`.tsv` ou `learnings.md`).
8. Decisão de catraca: ficou melhor? mantém; senão reverte.
9. Repetir até a parada.

## Como construir o seu
Você precisa de três arquivos/papéis:
- **O editável** — o único arquivo que o loop muta.
- **O scorer travado** — um comando que devolve uma pontuação reprodutível (use um
  *seed* fixo).
- **O comando do loop** — a lógica acima, escrita como um comando de barra
  (`.claude/commands/auto-research.md`).

## Quando um problema é "loop-ável"?
Três condições: (1) você consegue **medir** o resultado de forma automática e
reprodutível; (2) existe um **espaço de mudanças** que o agente pode editar; e
(3) cada iteração é **barata** o suficiente para rodar muitas vezes. Se as três
valem, o padrão se aplica — seja num modelo de ML, num simulador de negócio ou em
qualquer processo com uma métrica clara.
"""

RES_SNAKE = """<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cobrinha — exemplo inicial</title>
<style>
  body{margin:0;background:#0a0a0a;color:#ededed;font-family:system-ui,sans-serif;
       display:flex;flex-direction:column;align-items:center;justify-content:center;
       height:100vh;gap:14px}
  h1{font-size:1.2rem;color:#d90276;letter-spacing:.04em}
  canvas{background:#111;border:2px solid #d90276;border-radius:10px;touch-action:none}
  #score{font-family:ui-monospace,monospace}
  small{color:#737373}
</style></head>
<body>
  <h1>COBRINHA</h1>
  <div id="score">Pontos: 0</div>
  <canvas id="c" width="360" height="360"></canvas>
  <small>Use as setas (ou WASD). Exemplo inicial — peça ao Claude para melhorar.</small>
<script>
const cv=document.getElementById('c'),ctx=cv.getContext('2d'),G=18,N=cv.width/G;
let snake,dir,food,score,alive,timer;
function reset(){snake=[{x:9,y:9}];dir={x:1,y:0};score=0;alive=true;place();
  document.getElementById('score').textContent='Pontos: 0';
  clearInterval(timer);timer=setInterval(tick,110);}
function place(){food={x:(Math.random()*N)|0,y:(Math.random()*N)|0};}
function tick(){
  const h={x:(snake[0].x+dir.x+N)%N,y:(snake[0].y+dir.y+N)%N};
  if(snake.some(s=>s.x===h.x&&s.y===h.y)){alive=false;clearInterval(timer);draw();return;}
  snake.unshift(h);
  if(h.x===food.x&&h.y===food.y){score++;document.getElementById('score').textContent='Pontos: '+score;place();}
  else snake.pop();
  draw();
}
function draw(){
  ctx.fillStyle='#111';ctx.fillRect(0,0,cv.width,cv.height);
  ctx.fillStyle='#ff4da6';ctx.fillRect(food.x*G+2,food.y*G+2,G-4,G-4);
  ctx.fillStyle='#d90276';snake.forEach(s=>ctx.fillRect(s.x*G+1,s.y*G+1,G-2,G-2));
  if(!alive){ctx.fillStyle='rgba(0,0,0,.6)';ctx.fillRect(0,0,cv.width,cv.height);
    ctx.fillStyle='#fff';ctx.font='20px system-ui';ctx.textAlign='center';
    ctx.fillText('Fim de jogo — espaço para reiniciar',cv.width/2,cv.height/2);}
}
addEventListener('keydown',e=>{
  const k=e.key.toLowerCase();
  if((k==='arrowup'||k==='w')&&dir.y===0)dir={x:0,y:-1};
  else if((k==='arrowdown'||k==='s')&&dir.y===0)dir={x:0,y:1};
  else if((k==='arrowleft'||k==='a')&&dir.x===0)dir={x:-1,y:0};
  else if((k==='arrowright'||k==='d')&&dir.x===0)dir={x:1,y:0};
  else if(k===' '&&!alive)reset();
});
reset();
</script>
</body></html>
"""


def make_ecommerce_csv():
    import random
    rnd = random.Random(20260423)
    cats = ["Eletrônicos", "Moda", "Casa", "Beleza", "Esportes", "Livros", "Brinquedos", "Mercado"]
    regions = ["Sudeste", "Sul", "Nordeste", "Norte", "Centro-Oeste"]
    channels = ["Web", "App", "Marketplace"]
    rows = ["order_id,data,categoria,regiao,canal,qtd,preco_unit,receita,custo,margem,devolvido"]
    for i in range(1, 401):
        cat = rnd.choice(cats)
        reg = rnd.choice(regions)
        ch = rnd.choice(channels)
        qtd = rnd.randint(1, 5)
        preco = round(rnd.uniform(19.9, 899.0), 2)
        receita = round(preco * qtd, 2)
        custo = round(receita * rnd.uniform(0.45, 0.8), 2)
        margem = round(receita - custo, 2)
        dev = rnd.random() < 0.07
        m = rnd.randint(1, 12)
        d = rnd.randint(1, 28)
        data = "2026-%02d-%02d" % (m, d)
        rows.append("%d,%s,%s,%s,%s,%d,%.2f,%.2f,%.2f,%.2f,%s" %
                     (1000 + i, data, cat, reg, ch, qtd, preco, receita, custo, margem,
                      "sim" if dev else "nao"))
    return "\n".join(rows) + "\n"


def write_resources():
    d = os.path.join(ROOT, "arquivos")
    os.makedirs(d, exist_ok=True)
    files = {
        "person-template.md": RES_PERSON,
        "prosus_management_overview.md": RES_MGMT,
        "autoresearch-build-your-own.md": RES_AUTORESEARCH,
        "snake-example.html": RES_SNAKE,
        "ecommerce_sample.csv": make_ecommerce_csv(),
    }
    for name, content in files.items():
        with open(os.path.join(d, name), "w", encoding="utf-8") as f:
            f.write(content)
    return list(files)


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
    write("ajuda.html", build_help())
    write("arquivos.html", build_files())
    write("exercicios/index.html", build_list())
    for i in range(len(EXERCISES)):
        write("exercicios/" + slug(EXERCISES[i][0]) + ".html", build_exercise(i))
    res = write_resources()
    print("Recursos gerados:", ", ".join(res))
    print("Pronto. Sirva com:  python3 -m http.server 8080")


if __name__ == "__main__":
    main()
