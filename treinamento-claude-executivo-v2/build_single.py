#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera UM único arquivo HTML autossuficiente com TODO o treinamento:
- todo o conteúdo (início + 13 módulos + recursos + referência) numa só página
- CSS e JS embutidos (funciona offline, sem servidor)
- arquivos do data room embutidos em base64 (download funciona a partir do .html)
- barra lateral de navegação, progresso (localStorage), copiar, tooltips e colapsáveis

Pré-requisito: rode antes `python3 gen_dataroom.py` e `python3 build.py` (para os
arquivos existirem em /arquivos). Depois: `python3 build_single.py`.
Saída: treinamento-completo.html
"""
import base64
import html as _html
import os
import build  # reaproveita conteúdo, glossário, módulos, etc.

ROOT = os.path.dirname(os.path.abspath(__file__))
ARQ = os.path.join(ROOT, "arquivos")

MIME = {
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".md": "text/markdown", ".html": "text/html", ".csv": "text/csv", ".pdf": "application/pdf",
}


def data_uri(fname):
    path = os.path.join(ARQ, fname)
    with open(path, "rb") as f:
        raw = f.read()
    ext = os.path.splitext(fname)[1].lower()
    mime = MIME.get(ext, "application/octet-stream")
    return "data:" + mime + ";base64," + base64.b64encode(raw).decode("ascii")


def file_rows(files):
    # usa data-file (baixa do mapa embutido) para não duplicar o base64
    out = ""
    for fname, desc in files:
        if not os.path.exists(os.path.join(ARQ, fname)):
            continue
        out += ('<div class="file-row"><span class="fname">' + _html.escape(fname) + "</span>"
                '<span class="fdesc">' + _html.escape(desc) + "</span>"
                '<a class="btn ghost dl" data-file="' + fname + '" href="#" download="' + fname
                + '">Baixar ↓</a></div>')
    return out


def files_map(facilitator):
    """{nome: data-uri} dos arquivos a embutir (gabarito só na versão do facilitador)."""
    names = []
    for group in (build.DATAROOM_FILES, build.GEN_FILES):
        names += [f for f, _ in group]
    if facilitator:
        names += [f for f, _ in build.FAC_FILES]
    seen, parts = set(), []
    for fname in names:
        if fname in seen or not os.path.exists(os.path.join(ARQ, fname)):
            continue
        seen.add(fname)
        parts.append('"' + fname + '":"' + data_uri(fname) + '"')
    return "{" + ",".join(parts) + "}"


# ---------------------------------------------------------------------------
# Conteúdo SÓ do facilitador
# ---------------------------------------------------------------------------
def facnote(body):
    return ('<div class="facnote"><span class="label">Nota do facilitador</span>'
            + body + "</div>")


# Notas por módulo (id -> html), exibidas apenas na versão do facilitador
FAC_NOTES = {
    "00": build.P("Abra com a pergunta: “Quanto do tempo do seu time é gasto lendo e "
                  "resumindo documentos antes de decidir?”. Instale o modelo da delegação "
                  "(contexto + tarefa + materiais + revisão) e apresente a Aurora e a regra "
                  "do dado fictício.")
           + build.P("<strong>Números-chave do caso (para conferir):</strong> receita "
                     "~R$ 4,1 bi (crescimento desacelerou para negativo); margem bruta "
                     "~34% → ~30,5%; e-commerce ~24% da receita, +20%; MercadoVivo cresce "
                     "~22% e ganha share; decisão em pauta: acelerar o digital."),
    "02": build.P("<strong>Exercício — poder e limite.</strong> Depois, um breve debrief: “O "
                  "que o Claude fez bem?” e “Onde você teve de verificar?”. Pedir as próprias "
                  "incertezas já instala a postura crítica."),
    "03": build.P("<strong>Exercício — uma linha vs. um brief.</strong> Rode as duas versões "
                  "na sala e compare lado a lado. O atalho que deve ficar: diga o público e o "
                  "formato."),
    "04": build.P("<strong>Respostas esperadas + verificação.</strong> O resumo deve pegar a "
                  "desaceleração da receita, a queda de margem e o avanço do digital. Ao "
                  "cruzar com a planilha, surgem os <strong>erros plantados</strong> "
                  "(crescimento do 2T25 em branco, margem EBITDA do 3T25 que não bate, "
                  "balanço que não fecha por R$ 50 mi). Gabarito completo em "
                  "<code>Aurora_Gabarito_Facilitador.md</code> (Recursos). Não revele antes."),
    "06": build.P("O objetivo aqui <strong>não é a resposta</strong>, e sim treinar boas "
                  "perguntas. Faça-os rodar o advogado do diabo e o pre-mortem e perceber que "
                  "o Claude é um sparring. Lembre: verificar os fatos que ele trouxer."),
    "13": build.P("O exercício do Excel (“sinalize células que não batem”) e o cruzamento do "
                  "Módulo 04 são onde os <strong>erros plantados</strong> aparecem. Gabarito "
                  "completo em <code>Aurora_Gabarito_Facilitador.md</code>."),
    "15": build.P("Faça a <strong>demonstração de alucinação ao vivo</strong>: peça um dado "
                  "obscuro e específico e mostre como pode vir plausível e errado. Conecte à "
                  "verificação dos módulos 04 e 13."),
    "16": build.P("Cada participante escreve três compromissos (semana / mês / trimestre). "
                  "Entregue a biblioteca de prompts e skills e o checklist de governança "
                  "(Recursos). Reforce a regra dos dados."),
}


def section_facil_guide():
    b = ['<h1>Guia do facilitador</h1>',
         build.P("Esta versão é o roteiro de condução. Os blocos "
                 "<strong>Nota do facilitador</strong> aparecem ao longo dos módulos com "
                 "ênfases e respostas esperadas — e o gabarito do exercício de verificação "
                 "está nas notas dos módulos 04 e 13 e em Recursos."),
         build.callout("Use dados públicos ou fictícios. Reforce a regra na abertura e de "
                       "novo na governança: nunca colar dados pessoais (LGPD) ou "
                       "confidenciais em ferramentas não aprovadas.",
                       label="Regra de ouro do dia", kind="warn"),
         build.H2("Antes de começar (setup)"),
         build.P("Garanta que cada participante tenha: acesso ao Claude num notebook (login "
                 "feito); os arquivos do caso Aurora baixados; e um Projeto criado com os "
                 "arquivos carregados. Tenha projetor e os arquivos compartilhados com a turma."),
         build.H2("Princípios de facilitação"),
         build.table(["Situação", "Como conduzir"],
                     [["O cético", "Mostre cedo uma alucinação real e o tema de governança. Cético calibrado vira o melhor governante."],
                      ["O entusiasta", "Desafie com uma tarefa que exige verificação (um número do relatório, um dado de mercado). Mostre onde o julgamento humano é insubstituível."],
                      ["Fluências distintas", "Trabalhe em pares e circule pela sala."],
                      ["O ritual do debrief", "Após cada exercício: “O que o Claude fez bem?” e “Onde você teve de verificar ou corrigir?”."]]),
         build.H2("Sequência sugerida (núcleo)"),
         build.P("Setup · Abertura · Conhecendo o Claude · Fundamentos · Brief executivo · "
                 "Ler relatórios · Do relatório ao deck · Concorrência (poder das perguntas) · "
                 "Construir · Personalização e Skills · Conectores · Governança · Plano. Os "
                 "aprofundamentos (Análise de mercado, Cowork, Projetos, Automações, Nível 4) "
                 "ficam melhores como sessões à parte. Priorize a mão na massa."),
         build.callout("Os documentos de apoio, a biblioteca de prompts/skills, o checklist "
                       "de governança e o gabarito estão na seção Recursos.", label="Materiais")]
    return '<section id="guia-facilitador" class="doc-section">' + "".join(b) + "</section>"


# ---------------------------------------------------------------------------
# Seções
# ---------------------------------------------------------------------------
def section_home():
    M = build.MODULES
    agenda = '<ul class="agenda">'
    for mid, act, title, subtitle, fn, deep in M:
        tag = (' <span style="font-family:var(--font-mono);font-size:.6rem;text-transform:'
               'uppercase;letter-spacing:.05em;color:var(--gold)">· aprof.</span>') if deep else ''
        agenda += ('<li><span class="ag-num">' + mid + '</span><span class="ag-t">'
                   '<a href="#modulo-' + mid + '" style="text-decoration:none;color:inherit">'
                   + _html.escape(title) + "</a>" + tag + "</span></li>")
    agenda += "</ul>"
    body = (
        '<div class="kicker">Programa Executivo</div>'
        "<h1>Dominando o <span style='color:var(--gold);font-style:italic'>Claude</span></h1>"
        '<p class="lede">A versão executiva: usar o Claude no trabalho de liderança — ler '
        "relatórios, montar apresentações, analisar concorrência e mercado, fazer perguntas "
        "melhores e conectar e-mail e agenda. O ponto não é virar técnico: é virar um usuário "
        "fluente e um bom governante do uso de IA. Fio condutor: o caso fictício "
        "<strong>Aurora S.A.</strong> Documento único — navegue pela barra lateral; seu "
        "progresso fica salvo neste navegador.</p>"
        '<a class="btn" href="#modulo-00">Começar pelo Módulo 00 →</a> '
        '<a class="btn ghost" href="#dicas">Ver as dicas</a>'
        + build.callout("Use dados públicos ou fictícios. Nunca cole dados pessoais (LGPD) ou "
                        "confidenciais em ferramentas que a empresa ainda não aprovou. A "
                        "disciplina começa agora e volta no módulo de governança.",
                        label="A regra de hoje", kind="warn")
        + build.H2("O que você será capaz de fazer")
        + build.table(["Ao final, cada participante consegue…", ""],
                      [["Ler relatórios e extrair o que importa", "resumo executivo + o que verificar."],
                       ["Produzir apresentações", "do relatório ao deck para o board (.pptx)."],
                       ["Analisar concorrência e mercado", "com olhar crítico e perguntas melhores."],
                       ["Usar o Claude como parceiro de pensamento", "advogado do diabo, pre-mortem."],
                       ["Conectar e-mail e agenda", "brief do dia, preparo de reunião — com governança."],
                       ["Governar o uso de IA", "com cuidado de LGPD, sigilo e verificação."]])
        + build.H2("A jornada")
        + agenda
        + build.P("<span style='color:var(--muted)'>O núcleo (módulos sem o selo "
                  "<em>aprofundamento</em>) é a espinha dorsal; os aprofundamentos estendem o "
                  "programa e funcionam como sessões separadas ou consulta.</span>")
    )
    return '<section id="inicio" class="doc-section hero-section">' + body + "</section>"


def section_module(i, facilitator=False):
    mid, act, title, subtitle, fn, deep = build.MODULES[i]
    deep_pill = " · Aprofundamento" if deep else ""
    head = (
        '<div class="meta-pill">' + build.ACT_NAME[act].split(" —")[0] + " · Módulo " + mid
        + deep_pill + "</div>"
        '<div class="mod-number">' + mid + "</div>"
        "<h1>" + _html.escape(title) + "</h1>"
        '<p class="subtitle">' + _html.escape(subtitle) + "</p>"
    )
    note = facnote(FAC_NOTES[mid]) if (facilitator and mid in FAC_NOTES) else ""
    done = ('<div class="done-bar" data-done-bar><span class="grow">Terminou este módulo? '
            'Marque para acompanhar seu progresso.</span>'
            '<button class="btn" data-done-btn data-mod="' + mid
            + '" type="button">Marcar como concluído</button></div>')
    return ('<section id="modulo-' + mid + '" class="doc-section">' + head + fn() + note
            + done + "</section>")


def extract_body(full_html):
    """Extrai o conteúdo interno gerado por build.page()."""
    body = full_html.split('<main><div class="wrap">', 1)[1]
    body = body.rsplit("</div></main>", 1)[0]
    return body


def section_recursos(facilitator=False):
    b = ['<h1>Recursos para levar</h1>'
         '<p class="lede">Os arquivos do caso Aurora e os materiais do programa — '
         "embutidos neste documento. Clique para baixar e arraste para o seu Projeto no Claude.</p>"]
    b.append(build.H2("Caso Aurora (dados e relatórios)"))
    b.append(file_rows(build.DATAROOM_FILES))
    b.append(build.H2("Materiais do programa"))
    b.append(file_rows(build.GEN_FILES))
    if facilitator:
        b.append(build.H2("Só para o facilitador"))
        b.append(build.callout("Contém as respostas dos erros plantados no data room. Não "
                               "distribua aos participantes antes do exercício de verificação.",
                               label="Confidencial", kind="warn"))
        b.append(file_rows(build.FAC_FILES))
    return '<section id="recursos" class="doc-section">' + "".join(b) + "</section>"


def section_dicas():
    return '<section id="dicas" class="doc-section">' + build.dicas_body(depth=0) + "</section>"


def section_referencia():
    body = extract_body(build.build_referencia())
    return '<section id="referencia" class="doc-section">' + body + "</section>"


# ---------------------------------------------------------------------------
# Barra lateral (TOC)
# ---------------------------------------------------------------------------
def sidebar(facilitator=False):
    badge = ('<span class="side-badge">Facilitador</span>' if facilitator
             else '<span class="side-badge aluno">Participante</span>')
    s = ['<aside class="sidebar"><div class="side-inner">'
         '<a class="brand" href="#inicio"><span class="mark">Dominando o Claude</span></a>'
         + badge
         + '<div class="progress-bar"><span data-progress-fill></span></div>'
         '<p class="progress-text" data-progress-text>0 de 17 módulos</p>'
         '<nav class="toc">'
         '<a class="toc-link" href="#inicio">Início</a>']
    if facilitator:
        s.append('<a class="toc-link" href="#guia-facilitador">Guia do facilitador</a>')
    last = None
    for mid, act, title, subtitle, fn, deep in build.MODULES:
        if act != last:
            s.append('<div class="toc-act">' + build.ACT_NAME[act] + "</div>")
            last = act
        s.append('<a class="toc-link toc-mod" data-toc="' + mid + '" href="#modulo-' + mid + '">'
                 '<span class="toc-check">✓</span><span class="toc-num">' + mid + "</span>"
                 + _html.escape(title) + "</a>")
    s.append('<div class="toc-act">Apoio</div>')
    s.append('<a class="toc-link" href="#dicas">Dicas</a>')
    s.append('<a class="toc-link" href="#recursos">Recursos</a>')
    s.append('<a class="toc-link" href="#referencia">Referência</a>')
    s.append("</nav></div></aside>")
    return "".join(s)


# ---------------------------------------------------------------------------
# CSS e JS específicos do arquivo único
# ---------------------------------------------------------------------------
EXTRA_CSS = """
/* ---- layout de arquivo único ---- */
.app { display: grid; grid-template-columns: 300px minmax(0,1fr); align-items: start; }
.sidebar { position: sticky; top: 0; height: 100vh; overflow-y: auto;
  border-right: 1px solid var(--line); background: color-mix(in srgb,var(--paper) 70%,#fff); }
.side-inner { padding: 22px 18px 40px; }
.sidebar .brand { display: block; margin-bottom: 14px; }
.sidebar .brand .mark { font-family: var(--font-display); font-weight: 600; font-size: 1.1rem; color: var(--navy); }
.toc { display: flex; flex-direction: column; gap: 1px; margin-top: 10px; }
.toc-act { font-family: var(--font-mono); font-size: .64rem; text-transform: uppercase;
  letter-spacing: .08em; color: var(--gold); font-weight: 700; margin: 14px 0 4px; }
.toc-link { text-decoration: none; color: var(--muted); font-size: .9rem; padding: 5px 8px;
  border-radius: 8px; transition: background .12s, color .12s; }
.toc-link:hover { background: var(--navy-soft); color: var(--navy); }
.toc-link.active { background: var(--navy); color: #fff; }
.toc-mod { display: flex; align-items: center; gap: 7px; }
.toc-num { font-family: var(--font-mono); font-weight: 700; color: var(--gold); font-size: .8rem; }
.toc-link.active .toc-num { color: #fff; }
.toc-check { width: 15px; height: 15px; border-radius: 999px; border: 1.5px solid var(--line);
  display: inline-grid; place-items: center; font-size: .6rem; color: transparent; flex-shrink: 0; }
.toc-mod.done .toc-check { background: var(--ok); border-color: var(--ok); color: #fff; }
.toc-mod.done { color: var(--muted-2); }
.content { padding: 0 clamp(18px,5vw,64px); max-width: 860px; }
.doc-section { padding: 46px 0 30px; border-bottom: 1px solid var(--line-soft); scroll-margin-top: 18px; }
.doc-section:last-child { border-bottom: 0; }
.hero-section h1 { font-size: clamp(2.4rem,6vw,3.6rem); }
.topbar-single { display: none; }
@media (max-width: 900px) {
  .app { grid-template-columns: 1fr; }
  .sidebar { position: static; height: auto; border-right: 0; border-bottom: 1px solid var(--line); }
  .side-inner { padding: 16px clamp(16px,5vw,40px); }
  .toc { display: grid; grid-template-columns: 1fr 1fr; }
  .toc-act { grid-column: 1 / -1; }
}
@media print {
  .sidebar { display: none; }
  .app { display: block; }
  .doc-section { page-break-inside: avoid; }
  details.box { border: 1px solid #ccc; } details.box .box-body { display: block !important; }
}
/* ---- selo de público + nota do facilitador ---- */
.side-badge { display: inline-block; font-family: var(--font-mono); font-size: .62rem;
  text-transform: uppercase; letter-spacing: .08em; font-weight: 700; padding: 2px 9px;
  border-radius: 999px; margin-bottom: 14px; background: var(--gold); color: #fff; }
.side-badge.aluno { background: var(--navy); }
.facnote { border: 1px solid var(--navy); border-left: 4px solid var(--navy);
  background: var(--navy-soft); border-radius: 0 var(--radius) var(--radius) 0;
  padding: 14px 18px; margin: 1.4em 0; color: var(--ink-soft); }
.facnote .label { font-family: var(--font-mono); font-size: .68rem; text-transform: uppercase;
  letter-spacing: .08em; color: var(--navy); display: block; margin-bottom: 5px; font-weight: 700; }
.facnote ol { margin: .4em 0; }
@media print { .facnote { border-color: #888; background: #f0f0f0; } }
"""

SINGLE_JS = """
(function(){
  "use strict";
  var KEY="treino-claude-executivo-v2-progresso";
  var ORDER=["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16"];
  function load(){try{return JSON.parse(localStorage.getItem(KEY))||{}}catch(e){return {}}}
  function save(p){try{localStorage.setItem(KEY,JSON.stringify(p))}catch(e){}}

  function initCopy(){
    document.querySelectorAll(".codeblock").forEach(function(block){
      if(block.querySelector(".copy-btn"))return;
      var pre=block.querySelector("pre"); if(!pre)return;
      var btn=document.createElement("button");
      btn.className="copy-btn"; btn.type="button"; btn.textContent="Copiar";
      btn.addEventListener("click",function(){
        var t=pre.innerText;
        function ok(){btn.textContent="Copiado!";btn.classList.add("copied");
          setTimeout(function(){btn.textContent="Copiar";btn.classList.remove("copied")},1600);}
        if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(ok,fb)}else{fb()}
        function fb(){var ta=document.createElement("textarea");ta.value=t;ta.style.position="fixed";
          ta.style.opacity="0";document.body.appendChild(ta);ta.select();
          try{document.execCommand("copy");ok()}catch(e){}document.body.removeChild(ta);}
      });
      block.appendChild(btn);
    });
  }
  function positionTip(t){
    var tip=t.querySelector(".tip"); if(!tip)return;
    var r=t.getBoundingClientRect(), w=tip.offsetWidth, center=r.left+r.width/2;
    var left=center-w/2, m=10, shift=0;
    if(left<m)shift=m-left;
    else if(left+w>window.innerWidth-m)shift=(window.innerWidth-m)-(left+w);
    shift=Math.round(shift);
    tip.style.transform="translateX(calc(-50% + "+shift+"px)) translateY(-2px)";
    tip.style.setProperty("--arrow-shift",(-shift)+"px");
  }
  function initTooltips(){
    var terms=document.querySelectorAll(".term");
    terms.forEach(function(t){t.setAttribute("tabindex","0");
      t.addEventListener("mouseenter",function(){positionTip(t)});
      t.addEventListener("focus",function(){positionTip(t)});
      t.addEventListener("click",function(e){e.stopPropagation();
        var was=t.classList.contains("open");
        terms.forEach(function(o){o.classList.remove("open")});
        if(!was){t.classList.add("open");positionTip(t)}});});
    document.addEventListener("click",function(){terms.forEach(function(o){o.classList.remove("open")})});
  }
  function refresh(){
    var p=load(),done=0;
    ORDER.forEach(function(id){
      var on=!!p[id]; if(on)done++;
      var toc=document.querySelector('[data-toc="'+id+'"]'); if(toc)toc.classList.toggle("done",on);
      var sec=document.getElementById("modulo-"+id);
      if(sec){var bar=sec.querySelector("[data-done-bar]");
        if(bar)bar.classList.toggle("is-done",on);
        var btn=sec.querySelector("[data-done-btn]");
        if(btn)btn.textContent=on?"✓ Concluído":"Marcar como concluído";}
    });
    var pct=Math.round(done/ORDER.length*100);
    var fill=document.querySelector("[data-progress-fill]"); if(fill)fill.style.width=pct+"%";
    var txt=document.querySelector("[data-progress-text]"); if(txt)txt.textContent=done+" de "+ORDER.length+" módulos ("+pct+"%)";
  }
  function initDone(){
    document.addEventListener("click",function(e){
      var b=e.target.closest("[data-done-btn]"); if(!b)return;
      var id=b.getAttribute("data-mod"); var p=load();
      if(p[id])delete p[id]; else p[id]=true; save(p); refresh();
    });
  }
  function initSpy(){
    var links={}; document.querySelectorAll(".toc-link").forEach(function(a){
      links[a.getAttribute("href").slice(1)]=a;});
    var obs=new IntersectionObserver(function(es){
      es.forEach(function(en){ if(en.isIntersecting){
        var id=en.target.id;
        Object.values(links).forEach(function(a){a.classList.remove("active")});
        if(links[id])links[id].classList.add("active");
      }});
    },{rootMargin:"-20% 0px -70% 0px"});
    document.querySelectorAll(".doc-section").forEach(function(s){obs.observe(s)});
  }
  function initDownloads(){
    document.addEventListener("click",function(e){
      var c=e.target.closest("[data-file]"); if(!c)return;
      e.preventDefault();
      var uri=(window.TRAINING_FILES||{})[c.getAttribute("data-file")]; if(!uri)return;
      var a=document.createElement("a"); a.href=uri; a.download=c.getAttribute("data-file");
      document.body.appendChild(a); a.click(); a.remove();
    });
  }
  document.addEventListener("DOMContentLoaded",function(){
    initCopy(); initTooltips(); initDone(); initDownloads(); refresh();
    try{initSpy()}catch(e){}
  });
})();
"""


def build_html(css, facilitator):
    sections = [section_home()]
    if facilitator:
        sections.append(section_facil_guide())
    for i in range(len(build.MODULES)):
        sections.append(section_module(i, facilitator))
    sections.append(section_dicas())
    sections.append(section_recursos(facilitator))
    sections.append(section_referencia())
    content = "".join(sections)

    # ajusta links internos (de páginas para âncoras)
    repl = [
        ('href="../recursos.html"', 'href="#recursos"'),
        ("href='../recursos.html'", "href='#recursos'"),
        ('href="../referencia.html"', 'href="#referencia"'),
        ("href='../referencia.html'", "href='#referencia'"),
        ('href="recursos.html"', 'href="#recursos"'),
        ("href='recursos.html'", "href='#recursos'"),
        ('href="referencia.html"', 'href="#referencia"'),
        ("href='referencia.html'", "href='#referencia'"),
        ('href="../arquivos.html"', 'href="#recursos"'),
        ("href='../arquivos.html'", "href='#recursos'"),
        ('href="../modulos/index.html"', 'href="#inicio"'),
        ('href="index.html"', 'href="#inicio"'),
    ]
    for a, bb in repl:
        content = content.replace(a, bb)

    footer = (
        '<footer><div class="wrap">'
        "<p>" + build.DISCLAIMER + "</p><p>" + build.DISCLAIMER2 + "</p>"
        '<p style="font-size:.8rem">Documento único · programa hands-on · '
        "todos os dados do caso são fictícios.</p></div></footer>"
    )

    title = ("Dominando o Claude — guia do facilitador" if facilitator
             else "Dominando o Claude — caderno do participante")
    htmlout = (
        "<!DOCTYPE html>\n"
        '<html lang="pt-BR"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        "<title>" + title + "</title>"
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?'
        "family=Fraunces:ital,opsz,wght@0,9..144,400..700;1,9..144,400..600&"
        "family=Inter:wght@300..700&family=JetBrains+Mono:wght@400..700&display=swap"
        '" rel="stylesheet">'
        "<style>" + css + EXTRA_CSS + "</style>"
        "</head><body>"
        '<div class="app">' + sidebar(facilitator)
        + '<div class="content">' + content + footer + "</div></div>"
        "<script>window.TRAINING_FILES=" + files_map(facilitator) + ";</script>"
        "<script>" + SINGLE_JS + "</script>"
        "</body></html>"
    )
    return htmlout, len(sections)


def main():
    with open(os.path.join(ROOT, "assets", "styles.css"), encoding="utf-8") as f:
        css = f.read()
    targets = [
        ("treinamento-aluno.html", False),
        ("treinamento-facilitador.html", True),
    ]
    for fname, fac in targets:
        htmlout, n = build_html(css, fac)
        out = os.path.join(ROOT, fname)
        with open(out, "w", encoding="utf-8") as f:
            f.write(htmlout)
        print("Gerado: %-32s (%.0f KB, %d seções)"
              % (fname, os.path.getsize(out) / 1024, n))


if __name__ == "__main__":
    main()
