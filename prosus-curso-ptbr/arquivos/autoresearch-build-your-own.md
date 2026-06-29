# AutoResearch — como funciona e como construir o seu

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
