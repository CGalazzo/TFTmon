from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

replacements = [
    ("const SHINY_CHANCE=.01,SHINY_SPECIAL_CHANCE=.005;", "const SHINY_CHANCE=.002,SHINY_SPECIAL_CHANCE=.0005;"),
    ("Cada oferta normal da loja tem 1% de chance de ser Shiny; Pokémon 4★ têm 0,5%.", "Cada oferta normal da loja tem 0,2% de chance de ser Shiny; Pokémon 4★ têm 0,05%."),
    ("Pokémon normais têm 1% de chance de aparecer Shiny em cada oferta; Pokémon 4★ têm 0,5%.", "Pokémon normais têm 0,2% de chance de aparecer Shiny em cada oferta; Pokémon 4★ têm 0,05%.")
]

for old, new in replacements:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'Expected exactly one occurrence of {old!r}, found {count}')
    text = text.replace(old, new, 1)

path.write_text(text, encoding='utf-8')
