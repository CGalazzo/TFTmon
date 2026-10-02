# Kanto Tactics v0.6

Protótipo fan-made de auto-battler com base em Pokémon de Kanto e unidades especiais selecionadas de Johto e Hoenn. Site estático: `index.html` na raiz, sem build obrigatório para o Vercel.

## Base preservada

- Tabuleiro 7×6, banco com 9 espaços e loja com 5 opções.
- A loja pode oferecer formas base e evoluídas; três cópias do mesmo estágio continuam evoluindo automaticamente. Formas finais não fundem.
- Equipamentos combináveis; evoluções continuam sem itens de evolução.
- Ouro, juros, reroll, compra/venda, XP e nível do treinador; limite de campo igual ao nível (máximo 9).
- Juros na vitória e na derrota: +1 ouro por cada 10 guardados antes da recompensa, até +5 com 50 ou mais. Somam à recompensa base e ao bônus de sequência; gastar ouro reduz os juros da próxima rodada.
- XP visível abaixo do nível, com experiência atual/necessária e barra de progresso. Atualiza ao comprar XP, concluir rodada, subir de nível e reiniciar; nível 9 mostra nível máximo.
- Sequências de vitórias ou derrotas: 3 dão +1 ouro; 4 dão +2; 5 ou mais dão +3 por rodada. Resultado diferente reinicia a sequência em 1; nova partida zera.
- Mana, habilidades automáticas, movimentação e combate automático; jornada ampliada para 25 etapas, com quatro encontros de boss.
- Selecione um Pokémon no campo e clique em um espaço vazio do banco para retirá-lo.
- Correções da v0.2 mantidas: sem ação contra alvo inexistente e sem ação após morte por dano periódico.


## Progressão e bosses — preservados da v0.5

- A jornada agora possui 25 etapas.
- As etapas 1, 2 e 3 são propositalmente leves, com poucos inimigos, sem evoluções e atributos reduzidos.
- A dificuldade sobe gradualmente em quantidade, atributos e chance de formas evoluídas.
- A partir da parte intermediária da partida, as composições da IA passam a ser montadas para ativar conjuntos de 3 linhas; nos trechos avançados, passam a buscar conjuntos de 5 linhas.
- Boss da etapa 6: **Onix**.
- Boss da etapa 12: **3 Tauros**.
- Boss da etapa 18: **Raikou, Entei ou Suicune**, sorteado uma vez por partida.
- Boss da etapa 25: **Mewtwo**.
- Os lendários de boss não entram na loja, no banco nem no elenco permanente.
- Em batalhas de boss, sobreviver ao limite de tempo sem derrotar o boss conta como derrota.
- Recompensa de boss: vitória = 2 componentes; derrota com pelo menos 50% do HP total removido = 1 componente; derrota abaixo de 50% = 0.


## Loja e raridades — v0.6

Cada espaço da loja sorteia primeiro a raridade, depois a linha e por fim o estágio evolutivo. Pokémon especiais 4★ só entram no pool a partir do nível 6.

| Nível | 1$ | 2$ | 3$ | 4★ especial |
|---:|---:|---:|---:|---:|
| 2 | 70% | 30% | 0% | 0% |
| 3 | 55% | 35% | 10% | 0% |
| 4 | 40% | 35% | 25% | 0% |
| 5 | 28% | 37% | 35% | 0% |
| 6 | 18% | 32% | 47% | 3% |
| 7 | 10% | 25% | 57% | 8% |
| 8 | 5% | 18% | 65% | 12% |
| 9 | 3% | 12% | 67% | 18% |

Formas normais também podem aparecer evoluídas:

| Nível | Base | 2ª forma | Final |
|---:|---:|---:|---:|
| 2 | 100% | 0% | 0% |
| 3 | 98% | 2% | 0% |
| 4 | 92% | 8% | 0% |
| 5 | 82% | 16% | 2% |
| 6 | 70% | 25% | 5% |
| 7 | 58% | 32% | 10% |
| 8 | 48% | 35% | 17% |
| 9 | 40% | 37% | 23% |

Para os especiais 4★: nível 6 = 94/5/1; nível 7 = 82/15/3; nível 8 = 72/21/7; nível 9 = 62/26/12 para forma base/2ª/final. Lapras sempre aparece como Lapras.

Preços normais seguem o valor equivalente do estágio: custo base × 3 por evolução. Nos 4★, os preços são 4 ouro na forma base, 9 na segunda forma e 16 na forma final. A própria interface mostra as probabilidades do nível atual.

## Pokémon especiais 4★ — v0.6

- **Dratini → Dragonair → Dragonite**: Multiescala reduz dano acima de 70% do HP em 15% / 25% / 35%. Fúria do Dragão fica mais forte e concede velocidade temporária crescente.
- **Larvitar → Pupitar → Tyranitar**: Tempestade de Areia reduz a velocidade inimiga em 8% / 12% / 18% e aumenta a própria defesa em 10% / 20% / 30%. Terremoto ganha alcance, dano e controle.
- **Gastly → Haunter → Gengar**: Sombra concede intangibilidade inicial por 0,4s / 0,7s / 1,0s. Bola Sombria aumenta o dano e devolve 20 / 35 / 50 de mana ao finalizar um alvo.
- **Lapras**: Canção Protetora concede escudo inicial de 12% do HP máximo aos aliados. Blizzard causa dano em área e reduz velocidade.
- **Beldum → Metang → Metagross**: Corpo Metálico reduz o primeiro controle recebido em 50% / 75% / 100%. Meteor Mash aumenta dano e escudo por inimigo atingido.

Os especiais mantêm seus tipos normais e só contribuem para conjuntos já existentes. Dragon e Dark, por exemplo, ainda não possuem conjunto próprio. Os 4★ não foram adicionados ao gerador de composições normais da IA da v0.5 e não substituem os lendários de boss.

## Elenco: 33 linhas padrão + 5 linhas especiais 4★

As 20 linhas existentes foram mantidas. Novas linhas disponíveis na loja:

| Forma inicial | Evoluções no jogo | Tipos |
|---|---|---|
| Growlithe | Arcanine | Fire |
| Cyndaquil | Quilava → Typhlosion | Fire |
| Voltorb | Electrode | Electric |
| Mareep | Flaaffy → Ampharos | Electric |
| Chinchou | Lanturn | Water / Electric |
| Slowpoke | Slowbro | Water / Psychic |
| Wooper | Quagsire | Water / Ground |
| Drowzee | Hypno | Psychic |
| Natu | Xatu | Psychic / Flying |
| Hoppip | Skiploom → Jumpluff | Grass / Flying |
| Spearow | Fearow | Normal / Flying |
| Geodude | Graveler → Golem | Rock / Ground |
| Phanpy | Donphan | Ground |

Utilizam-se as formas tradicionais, sem variantes regionais. Evoluções alternativas ficam para versões posteriores. Os atributos e custos iniciais dos novos Pokémon são valores de teste; as 20 linhas anteriores mantêm seus atributos base.

## Conjuntos de tipos

- Contam apenas linhas evolutivas diferentes no campo. Banco e invocações não contam.
- Repetidos e formas diferentes da mesma linha contam uma vez por tipo. Por exemplo, Pikachu + Raichu = 1 Electric.
- Tipos duplos contribuem para ambos os conjuntos. O tipo da forma atual é considerado (Charizard adiciona Flying; Charmander não).
- Os bônus são definidos no início de cada combate e continuam até o fim, mesmo após derrotas de membros do time.
- Bônus só afetam unidades do tipo correspondente. O nível de 5 substitui o de 3.
- A mesma regra vale para o jogador e o rival.
- Tipos sem conjunto ativo, como Normal, Bug, Steel e Rock, são apenas identificados.
- **Sem fraquezas, resistências ou imunidades por tipo.** O dano depende dos atributos, habilidades, defesa, escudos e conjuntos; Água não tem vantagem de dano sobre Fogo.

| Tipo | 3 linhas | 5 linhas |
|---|---|---|
| Fire | +15% ATK | +30% ATK; dano de habilidades aplica queimadura de 2% HP máximo/s durante 3s |
| Water | +20% HP máximo | +35% HP máximo; cura 2% HP máximo a cada 3s |
| Electric | +20% velocidade de ação | Mantém +20% e invoca Zapdos uma vez no início do combate |
| Grass | Cura 2% HP máximo a cada 3s | Cura 4% HP máximo a cada 3s; primeira habilidade de cada unidade enraíza o alvo por 1,5s |
| Psychic | +25 mana inicial | +40 mana inicial; +20% potência de dano, cura e escudo das habilidades |
| Flying | 10% esquiva contra ataques básicos | 20% esquiva básica; +15% velocidade de ação |
| Poison | Ataques básicos aplicam veneno de 1% HP máximo/s durante 3s | Veneno de 2% HP máximo/s; alvo recebe 30% menos cura enquanto envenenado |
| Ground | +20% DEF | +40% DEF; escudo inicial de 15% HP máximo |

Enraizamento impede movimento, mas permite ataques e habilidades. Dano periódico usa o HP máximo do alvo, consome escudos e não recebe modificadores de tipo ou esquiva. Veneno e queimadura podem coexistir, mas aplicações do mesmo efeito apenas renovam a duração, sem acumular intensidade. Os tempos seguem o relógio de combate (atualizado a cada 260ms), não a frequência das ações de cada unidade.

Foram corrigidos os tipos do Beedrill (Bug/Poison, sem Flying) e completadas as identificações de Bug, Normal e Steel em linhas antigas, sem criar novos conjuntos.

## Zapdos

- Invocação temporária por 5 linhas Electric; não aparece na loja, no banco ou na equipe persistente.
- Uma invocação por lado por combate, numa casa livre próxima dos aliados, na metade do tabuleiro desse lado.
- Não ocupa o limite do treinador, não conta para conjuntos e não recebe bônus de conjunto.
- Atributos iniciais de teste: 180 HP, 24 ATK, 8 DEF, alcance 3, velocidade 105; habilidade Tempestade Elétrica atinge até três alvos.
- Pode atacar, usar habilidade, receber cura, sofrer efeitos e ser derrotado. Não reaparece no mesmo combate.
- Desaparece ao fim da batalha. Invocações sobreviventes não acrescentam dano ao HP do treinador.
- Nenhum lendário foi adicionado à loja.


## Acabamento de gameplay antes da fase gráfica

- **Detalhes completos do Pokémon selecionado:** raridade, estágio evolutivo, tipos, função, HP/ATK/DEF, habilidade, explicação do efeito, passiva dos 4★, valor de venda e equipamentos.
- **Travar loja:** a loja pode ser bloqueada para permanecer igual ao avançar de etapa. Reroll manual continua funcionando e não remove o bloqueio.
- **Preview da próxima batalha:** mostra etapa, quantidade de inimigos e nível de composição; em bosses mostra nome, quantidade e regra de recompensa.
- **Painel de chances da loja:** tabela completa dos níveis 2–9, chances 1$/2$/3$/4★ e chances de forma base/2ª/final para Pokémon normais e especiais.
- **Resumo pós-batalha:** mostra vitória/derrota, dano causado, ouro recebido, juros, bônus de sequência, HP perdido e, em boss, percentual de HP removido e recompensa.
- **Resumo final da partida:** etapa alcançada, vitórias/derrotas, bosses vencidos, time final e histórico de 4★ vistos/comprados.
- **Progressão até o nível 9 validada sem alterar a economia:** são 140 XP totais do nível 2 ao 9; as 25 batalhas entregam 50 XP passivos, restando 90 XP, equivalentes a 23 compras de 4 XP (92 ouro).
- **Sanidade de balanceamento:** bosses e 4★ continuam com os atributos e habilidades já aprovados; foram adicionadas validações para garantir valores finitos e progressão das evoluções sem rebalanceamento automático.

Este pacote não altera as regras aprovadas de itens, sinergias, bosses, raridades, recompensas, dano por tipo ou habilidades especiais.


## Tela inicial e limpeza de interface

- A partida agora abre com uma **tela inicial** que resume o objetivo e o ciclo principal: loja, evolução, combate automático e sinergias.
- As **regras completas** ficam em uma janela própria, acessível tanto na tela inicial quanto durante a partida.
- A tela principal foi simplificada: o bloco permanente de regras rápidas foi removido.
- **Mochila/equipamentos** deixaram de ocupar uma seção longa da página e agora abrem em modal pelo botão `🎒 Mochila`.
- O **registro da partida** deixou a lateral fixa e agora abre pelo botão `📜 Histórico`.
- As chances completas da loja continuam disponíveis pelo botão `Chances da loja`; na tela principal aparece apenas o nível da loja e a chance atual de 4★.
- O preview da próxima luta foi encurtado para etapa, quantidade de inimigos/sinergia ou nome do boss.
- A lateral direita fica focada apenas no Pokémon selecionado.
- Foram criados slots independentes para futura identidade visual: `--start-bg-image`, `--game-bg-image`, `--logo-image`, `--hero-image`, além de `data-art-slot="logo"` e `data-art-slot="hero"`. Isso permite trocar logo, fundos e arte principal depois sem mexer nas regras do jogo.
- Nenhuma regra de combate, economia, boss, raridade, item, evolução, sinergia ou progressão foi alterada nesta etapa.

## Validação

Execute com Node.js:

```sh
node --test tests/game.test.cjs
```

Os testes executam o JavaScript real do jogo em um DOM simulado, cobrindo conjuntos, efeitos, invocação, evoluções, economia, loja por raridade, formas evoluídas, nível 9, habilidades especiais 4★, ações de posicionamento, curva de dificuldade, bosses e combates completos das oito composições nas 25 etapas. Não substituem a avaliação visual em navegador nem os testes de balanceamento com jogadores.

Protótipo não comercial criado para testes de mecânica e balanceamento.


## Itens — preservados na v0.6

- 5 componentes (Garra, Pena, Cristal, Casco, Semente) e 15 receitas, consultáveis na mochila.
- Selecione um Pokémon, clique em um item da mochila e em Equipar. Até 3 itens por Pokémon, incluindo componentes.
- Para combinar, selecione dois componentes, na mochila ou equipados, e confirme a prévia. Os componentes são consumidos e o equipamento ocupa uma vaga. Não há desmontagem.
- A combinação prioriza o Pokémon que carregava o primeiro componente equipado; se ele já possui o equipamento resultante, o resultado vai para a mochila.
- Um equipamento completo de cada tipo por Pokémon. Componentes repetidos são permitidos.
- Remoção gratuita durante a preparação. Nenhuma alteração de equipamento é permitida em combate ou após o fim da partida.
- A evolução preserva os itens: prioriza equipamentos completos, começando pelos da unidade que estava no campo. Excedentes e equipamentos completos duplicados voltam à mochila. Componentes não são combinados automaticamente na evolução.
- Venda devolve todos os itens à mochila, sem alterar o valor de venda do Pokémon. A mochila não tem limite de capacidade.
- A partida começa com 2 componentes aleatórios.
- Não existem mais pacotes automáticos nas etapas 4, 7, 10 e 13.
- Os novos componentes são conquistados nos bosses das etapas 6, 12, 18 e 25: derrotar o boss concede 2 componentes; perder após remover pelo menos 50% do HP total do encontro concede 1; abaixo de 50% não concede componente.
- No encontro de 3 Tauros, o percentual usa a soma do HP inicial dos três. Reiniciar limpa recompensas anteriores e sorteia novamente os 2 componentes iniciais.
- Bônus percentuais dos itens no mesmo atributo se somam; esse total é multiplicado pelo bônus do conjunto. O equipamento substitui os bônus dos componentes consumidos. Escudos e regeneração de itens somam aos dos conjuntos.
- Cura por dano considera apenas HP efetivamente retirado por dano direto, sem escudos, excesso além do HP restante, veneno ou queimadura. A redução de cura por veneno também afeta essa cura.
- Itens não concedem tipos nem modificam a eficácia elemental. Zapdos não recebe equipamentos. A IA mantém o comportamento anterior, sem receber equipamentos extras nesta versão.

| Componentes | Equipamento | Efeito total |
|---|---|---|
| Garra + Garra | Faixa Muscular | +25% ATK |
| Pena + Pena | Lenço Veloz | +25% velocidade |
| Cristal + Cristal | Óculos Sábios | +25% potência |
| Casco + Casco | Revestimento Metálico | +35% DEF |
| Semente + Semente | Restos | +20% HP; regenera 2% HP/3s |
| Garra + Pena | Garra Rápida | +15% ATK e velocidade |
| Garra + Cristal | Orbe de Poder | +20% ATK e potência |
| Garra + Casco | Faixa de Combate | +15% ATK; +25% DEF |
| Garra + Semente | Presa Vital | +15% ATK; cura 15% do dano direto dos ataques básicos |
| Pena + Cristal | Amuleto Energético | +15% velocidade; +10 mana por ataque básico |
| Pena + Casco | Manto Ágil | +15% velocidade; +20% DEF |
| Pena + Semente | Faixa de Vigor | +15% velocidade; +20% HP |
| Cristal + Casco | Barreira Mística | +15% potência; escudo inicial de 20% HP |
| Cristal + Semente | Sino Restaurador | +15% potência; cura 15% do dano direto das habilidades |
| Casco + Semente | Colete Protetor | +25% DEF e HP |

Componentes isolados: Garra +10% ATK; Pena +10% velocidade; Cristal +10% potência; Casco +15% DEF; Semente +10% HP. Potência se aplica a dano, cura e escudo das habilidades.