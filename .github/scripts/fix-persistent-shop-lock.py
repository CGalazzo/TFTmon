from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="if(free&&state.shopLocked&&state.shop.length){render();return}"
new="if(free&&state.shopLocked){render();return}"
if old not in s:
    raise SystemExit('target shop lock condition not found')
if s.count(old)!=1:
    raise SystemExit(f'unexpected match count: {s.count(old)}')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
