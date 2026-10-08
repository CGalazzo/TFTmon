from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="    if(free&&state.shopLocked&&state.shop.length){render();return}\n"
new="    if(free&&state.shopLocked){state.shopLocked=false;if(state.shop.length){render();return}}\n"
if old not in s:
    raise SystemExit('Target shop lock condition not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
