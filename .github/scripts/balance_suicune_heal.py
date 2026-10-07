from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
old = "suicune:{name:'Suicune',dex:245,types:['Water'],role:'Boss Lendário',hp:1050,atk:44,def:23,range:2,speed:98,ability:{name:'Aurora',kind:'heal',power:.42},count:1}"
new = "suicune:{name:'Suicune',dex:245,types:['Water'],role:'Boss Lendário',hp:1050,atk:44,def:23,range:2,speed:98,ability:{name:'Aurora',kind:'heal',power:.18},count:1}"
if old not in text:
    raise SystemExit('Suicune definition anchor not found or already changed')
if text.count(old) != 1:
    raise SystemExit(f'Expected exactly one Suicune definition, found {text.count(old)}')
text = text.replace(old, new, 1)
path.write_text(text, encoding='utf-8')
