#!/usr/bin/env bash
set -euo pipefail

cat assets/arena-v3-part0{1..8}.b64 assets/arena-v3-part09{a,b,c,d}.b64 | tr -d '\n\r ' | base64 -d > assets/tftmon-arena-game.webp

python3 - <<'PY'
from pathlib import Path
import hashlib, struct

img=Path('assets/tftmon-arena-game.webp').read_bytes()
if len(img)!=76722: raise SystemExit(f'arena size mismatch: {len(img)}')
if hashlib.sha256(img).hexdigest()!='476d86d45e257de1f012fbe46e3015d2cd68445ef5ed0d7176bf395be01a7457': raise SystemExit('arena sha256 mismatch')
if img[:4]!=b'RIFF' or img[8:12]!=b'WEBP': raise SystemExit('arena is not WEBP')
if struct.unpack('<I',img[4:8])[0]+8!=len(img): raise SystemExit('arena RIFF length mismatch')

p=Path('index.html'); s=p.read_text(encoding='utf-8')
marker='/* ===== TFTMON EXACT APPROVED FLOATING ARENA — 2026-10-05 ===== */'
start=s.find(marker); end=s.find('</style>',start)
if start<0 or end<0: raise SystemExit('arena style marker not found')
W,H=2078,757
red_y=[118,179,239,300]; red_top=[531,687,829,973,1117,1261,1403,1548]; red_bot=[476,648,801,965,1128,1289,1446,1602]
blue_y=[339,404,474,551]; blue_top=[459,622,787,957,1128,1294,1455,1612]; blue_bot=[402,590,777,956,1141,1322,1493,1650]
def row(y0,y1,top,bot,ya,yb):
 m=(y0+y1)/2; t=(m-ya)/(yb-ya); b=[top[i]+(bot[i]-top[i])*t for i in range(8)]; out=[]
 for c in range(7):
  x0=b[c]+3; x1=b[c+1]-3
  out.append((x0/W*100,(y0+3)/H*100,(x1-x0)/W*100,(y1-y0-6)/H*100))
 return out
cells=[]
for r in range(3): cells+=row(red_y[r],red_y[r+1],red_top,red_bot,red_y[0],red_y[-1])
for r in range(3): cells+=row(blue_y[r],blue_y[r+1],blue_top,blue_bot,blue_y[0],blue_y[-1])
css='''/* ===== TFTMON EXACT APPROVED FLOATING ARENA — 2026-10-05 ===== */
/* The artwork owns the visible 7x6 grid. Gameplay cells are transparent hitboxes aligned to it. */
#gameApp .arena-decor{display:none!important}
#gameApp .board,#gameApp .battle-preview[data-boss] + .board{position:relative!important;isolation:isolate!important;display:block!important;width:min(100%,1100px)!important;max-width:1100px!important;aspect-ratio:1100/401!important;height:auto!important;margin:4px auto 26px!important;padding:0!important;overflow:visible!important;border:0!important;border-radius:0!important;background-color:transparent!important;background-image:url('assets/tftmon-arena-game.webp')!important;background-size:100% 100%!important;background-position:center!important;background-repeat:no-repeat!important;box-shadow:none!important}
#gameApp .board::before,#gameApp .board::after{display:none!important}
#gameApp .cell{position:absolute!important;z-index:2!important;min-width:0!important;min-height:0!important;overflow:visible!important;border:0!important;background:transparent!important;box-shadow:none!important;border-radius:8px!important;outline:none!important}
#gameApp .cell::before{content:""!important;position:absolute!important;inset:2px!important;border-radius:8px!important;background:transparent!important;box-shadow:none!important;pointer-events:none!important;transition:.14s ease!important}
#gameApp .cell::after{display:none!important}
#gameApp .cell:hover::before{background:rgba(255,255,255,.05)!important}
#gameApp .board.dragging-active .player-zone::before{background:rgba(56,198,255,.08)!important;box-shadow:inset 0 0 0 1px rgba(132,235,255,.45)!important}
#gameApp .board.dragging-active .enemy-zone::before{background:rgba(255,99,72,.025)!important}
#gameApp .cell.drag-over::before{background:rgba(255,226,91,.14)!important;box-shadow:inset 0 0 0 2px rgba(255,230,112,.82),0 0 12px rgba(255,219,80,.38)!important}
#gameApp .battle-layer,#gameApp .fx-layer{inset:0!important;top:0!important;right:0!important;bottom:0!important;left:0!important;overflow:visible!important;pointer-events:none!important}
#gameApp .battle-layer{z-index:40!important}#gameApp .fx-layer{z-index:25!important}
#gameApp .fighter{width:9.5%!important;height:28%!important;transform-origin:center bottom!important;scale:var(--arena-depth,1);overflow:visible!important}
#gameApp .fighter-sprite,#gameApp .fighter-sprite img{overflow:visible!important}
'''
for i,(x,y,w,h) in enumerate(cells,1): css+=f'#gameApp .cell:nth-child({i}){{left:{x:.4f}%!important;top:{y:.4f}%!important;width:{w:.4f}%!important;height:{h:.4f}%!important}}\n'
css+='''#gameApp .cell:nth-child(-n+7) .token{scale:.82;transform-origin:center bottom}
#gameApp .cell:nth-child(n+8):nth-child(-n+14) .token{scale:.88;transform-origin:center bottom}
#gameApp .cell:nth-child(n+15):nth-child(-n+21) .token{scale:.94;transform-origin:center bottom}
#gameApp .cell:nth-child(n+22):nth-child(-n+28) .token{scale:.94;transform-origin:center bottom}
#gameApp .cell:nth-child(n+29):nth-child(-n+35) .token{scale:1;transform-origin:center bottom}
#gameApp .cell:nth-child(n+36):nth-child(-n+42) .token{scale:1.06;transform-origin:center bottom}
@media(max-width:820px){#gameApp .board,#gameApp .battle-preview[data-boss] + .board{width:min(calc(100vw - 6px),1100px)!important;max-width:calc(100vw - 6px)!important;aspect-ratio:1100/401!important;margin:2px auto 22px!important}#gameApp .fighter{width:10%!important;height:29%!important}#gameApp .cell::before{inset:1px!important;border-radius:5px!important}}
'''
s=s[:start]+css+'\n'+s[end:]
if 'const boardCell=cells[Math.max(0,Math.min(41,c.y*7+c.x))];' not in s: raise SystemExit('cell-centered combat positioning missing')
p.write_text(s,encoding='utf-8')
PY

git diff --check
git config user.name 'github-actions[bot]'
git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
git rm -f assets/arena-v3-part0{1..8}.b64 assets/arena-v3-part09{a,b,c,d}.b64 .github/workflows/apply-arena-v3.yml scripts/apply-arena-v3.sh
git add index.html assets/tftmon-arena-game.webp
git commit -m 'Apply clean aligned 7x6 arena artwork'
git push origin HEAD:main
