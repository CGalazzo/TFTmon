from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
replacements = [
    ("litwick:{cost:2,role:'Atacante'", "litwick:{cost:2,role:'Mago'"),
    ("cyndaquil:{cost:2,role:'Mago'", "cyndaquil:{cost:2,role:'Atacante'")
]
for old, new in replacements:
    if text.count(old) != 1:
        raise SystemExit(f'Expected exactly one occurrence of {old!r}, found {text.count(old)}')
    text = text.replace(old, new, 1)
path.write_text(text, encoding='utf-8')
