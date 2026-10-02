# Kanto Tactics v0.2

Protótipo fan-made de auto-battler inspirado em TFT, usando exclusivamente Pokémon da primeira geração.

## O que já existe

- Tabuleiro 7x6.
- Loja com 5 opções.
- Ouro, juros, reroll e compra/venda.
- XP e nível do treinador.
- Limite de Pokémon no campo igual ao nível.
- Banco com 9 espaços.
- 20 linhas-base de Kanto na loja.
- Evolução automática ao juntar 3 cópias iguais.
- Sem itens e sem itens de evolução.
- 8 sinergias ativas na v0.2: Fire, Water, Electric, Grass, Psychic, Flying, Poison e Ground.
- Funções de unidade: tanque, atacante, mago, suporte e assassino.
- Habilidades automáticas e mana.
- Combate automático com movimentação no tabuleiro.
- IA com progressão por 15 rodadas.
- Rival final fortalecido na rodada 15.
- Layout responsivo para desktop e celular.

## Evolução

A loja vende somente formas iniciais. Três cópias da mesma forma evoluem automaticamente para a próxima forma da linha.

Exemplo:

Charmander + Charmander + Charmander -> Charmeleon

Charmeleon + Charmeleon + Charmeleon -> Charizard

Nenhuma pedra ou item de evolução é usado nesta versão.

## Deploy

O projeto é um site estático e o arquivo `index.html` fica na raiz do repositório. Pode ser importado diretamente no Vercel sem build command.

## Observação

Protótipo não comercial criado para testes de mecânica e balanceamento.


## Alterações da v0.2

- Combate ignora ações sem alvo vivo e impede ações após morte por veneno.
- Para devolver um Pokémon ao banco, selecione-o no campo e clique em um espaço vazio do banco.
- Sequência de vitórias ou derrotas: 3 consecutivas dão +1 ouro; 4 dão +2; 5 ou mais dão +3 por rodada.
- Trocar de vitória para derrota ou vice-versa inicia uma nova sequência em 1. Reiniciar a partida zera a sequência.
- O bônus é pago a partir do terceiro resultado consecutivo, somado ao ouro base e aos juros existentes. O registro detalha cada parcela.
