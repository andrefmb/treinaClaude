# Gabarito do facilitador — erros e lacunas plantados

> CONFIDENCIAL — só para o facilitador. Não distribua aos participantes.
> Estes itens existem para treinar a disciplina de verificação (Módulo de governança).

O `Bastiao_DataRoom.xlsx` contém inconsistências propositais. No exercício de
verificação, peça ao Claude para auditar a qualidade dos dados — ele deve achar:

1. Resumo da Carteira / 2T25: Índice Combinado em branco. Claude deve calcular Sinistralidade + Despesas (= 78%).
2. Resumo da Carteira / 3T25: Sinistralidade exibida 36,0% não bate com Sinistros Pagos ÷ Prêmio Emitido (real ≈ 41%). Pedir ao Claude recalcular a partir das colunas.
3. Tomadores / Planalto Construtora: Exposição (118% do limite) está marcada como 'Dentro do limite' — deveria ser 'Acima do limite'.
4. Tomadores / Litoral Engenharia: Rating em branco — exige due diligence antes de decidir.
5. Apólices: ~4 prêmios não batem com IS × Taxa (linhas plantadas); 3 taxas em branco; 1 IS negativo (typo, AP com IS < 0); e 3 regiões grafadas em CAIXA ALTA (sujeira). Bom para pedir uma 'auditoria de qualidade'.
6. Sinistros / SIN-2010: Reserva preenchida como texto 'n/d' — quebra somas. Claude deve sinalizar e tratar.
7. Sinistros / SIN-2022: Data de aviso em formato dd/mm/aaaa (as demais em aaaa-mm-dd) — inconsistência de formato.
8. Sinistros: o id SIN-2001 aparece DUPLICADO (duas linhas). Claude deve detectar a duplicidade ao agregar.

## Respostas esperadas (números do caso)
- Sinistralidade real do 3T25 ≈ 41% (não 36%).
- Índice Combinado do 2T25 = 40 + 38 = 78%.
- Construtora Pilar: antes da nova garantia, exposição R$ 150 mi / limite R$ 180 mi (83%).
  Com a nova garantia de R$ 60 mi → R$ 210 mi → ESTOURA o limite de R$ 180 mi.
- Planalto Construtora está, de fato, acima do limite (≈118%).
- Pedir sempre as premissas na precificação; tratar como direcional.
