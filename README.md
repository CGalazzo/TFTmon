# Kanto Tactics v0.3

Protótipo fan-made de auto-battler com Pokémon de Kanto e Johto. Site estático: `index.html` na raiz, sem build obrigatório para o Vercel.

## Base preservada

- Tabuleiro 7×6, banco com 9 espaços e loja com 5 opções.
- Loja vende formas iniciais; três cópias da mesma forma evoluem automaticamente. Formas finais não fundem.
- Sem equipamentos ou itens de evolução.
- Ouro, juros, reroll, compra/venda, XP e nível do treinador; limite de campo igual ao nível (máximo 7).
- Sequências de vitórias ou derrotas: 3 dão +1 ouro; 4 dão +2; 5 ou mais dão +3 por rodada. Resultado diferente reinicia a sequência em 1; nova partida zera.
- Mana, habilidades automáticas, movimentação e combate automático; 15 rodadas e rival final fortalecido.
- Selecione um Pokémon no campo e clique em um espaço vazio do banco para retirá-lo.
- Correções da v0.2 mantidas: sem ação contra alvo inexistente e sem ação após morte por dano periódico.

## Elenco: 33 linhas

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

## Validação

Execute com Node.js:

```sh
node --test tests/game.test.cjs
```

Os testes executam o JavaScript real do jogo em um DOM simulado, cobrindo conjuntos, efeitos, invocação, evoluções, economia, ações de posicionamento e combates completos das oito composições nas 15 rodadas. Não substituem a avaliação visual em navegador nem os testes de balanceamento com jogadores.

Protótipo não comercial criado para testes de mecânica e balanceamento.
