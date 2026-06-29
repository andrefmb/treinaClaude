# Curso .md — versão local em português (pt-BR)

Recriação local e interativa do currículo de exercícios (11 exercícios, 2 atos),
com o **mesmo mecanismo de interatividade**: blocos de prompt com botão **Copiar**,
seções colapsáveis (Debrief / FAQ / Vá mais fundo / Reflexão), **tooltips de
glossário** inline, navegação entre exercícios e **acompanhamento de progresso**
(salvo no navegador via `localStorage`).

O texto instrucional foi escrito originalmente em português, seguindo a mesma
estrutura pedagógica. Os prompts a digitar no agente foram localizados para pt-BR,
mantendo tokens técnicos (nomes de arquivo, URLs, comandos de CLI).

## Como rodar

```bash
cd prosus-curso-ptbr
python3 -m http.server 8080
# abra http://localhost:8080
```

> Use um servidor local (acima) em vez de abrir os arquivos com `file://` —
> assim os downloads e os caminhos relativos funcionam corretamente.

## Estrutura

```
prosus-curso-ptbr/
├── index.html              # página inicial
├── ajuda.html              # "Pedir ajuda"
├── arquivos.html           # downloads dos recursos
├── exercicios/
│   ├── index.html          # lista dos 11 exercícios + barra de progresso
│   └── exercise-*.html      # 1.1, 1.2, 2.1…2.5, 3.1, 4, 5, 6
├── arquivos/               # recursos para download (templates/exemplos)
├── assets/
│   ├── styles.css          # tema (acento magenta, 3 fontes)
│   └── app.js              # copiar, tooltips, progresso
└── build.py                # gera todas as páginas a partir do conteúdo
```

## Regenerar / editar

Todo o conteúdo vive em `build.py` (glossário, exercícios, páginas). Edite lá e
rode `python3 build.py` para regenerar o site. As fontes (Bricolage Grotesque,
Geist, JetBrains Mono) vêm do Google Fonts e exigem internet na primeira carga;
o resto é 100% local.
