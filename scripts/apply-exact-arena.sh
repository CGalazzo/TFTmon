#!/usr/bin/env bash
set -euo pipefail

cat \
  assets/tftmon-arena-exact-1.b64 \
  assets/tftmon-arena-exact-2.b64 \
  assets/tftmon-arena-exact-3.b64 \
  assets/tftmon-arena-exact-4.b64 \
  assets/tftmon-arena-exact-5.b64 \
  assets/tftmon-arena-exact-6.b64 \
  | tr -d '\n\r ' \
  | base64 -d > assets/tftmon-arena-approved.webp

python3 - <<'PY'
from pathlib import Path
import struct

image = Path('assets/tftmon-arena-approved.webp')
raw = image.read_bytes()
if raw[:4] != b'RIFF' or raw[8:12] != b'WEBP':
    raise SystemExit('Exact arena is not a valid WEBP RIFF container')
declared = struct.unpack('<I', raw[4:8])[0] + 8
if len(raw) != declared:
    raise SystemExit(f'Exact arena is truncated: actual={len(raw)} declared={declared}')
if len(raw) != 87912:
    raise SystemExit(f'Unexpected exact arena byte size: {len(raw)}')
sig = raw.find(b'\x9d\x01\x2a')
if sig < 0 or sig + 7 > len(raw):
    raise SystemExit('Could not read exact arena VP8 dimensions')
width = struct.unpack('<H', raw[sig+3:sig+5])[0] & 0x3fff
height = struct.unpack('<H', raw[sig+5:sig+7])[0] & 0x3fff
if (width, height) != (1160, 390):
    raise SystemExit(f'Unexpected exact arena dimensions: {width}x{height}')
print(f'VALID EXACT ARENA: {len(raw)} bytes, {width}x{height}')

path = Path('index.html')
text = path.read_text(encoding='utf-8')
marker = '/* ===== TFTMON EXACT APPROVED FLOATING ARENA — 2026-10-05 ===== */'
start = text.find(marker)
if start < 0:
    raise SystemExit('Approved arena CSS marker not found')
end = text.find('</style>', start)
if end < 0:
    raise SystemExit('Approved arena style block end not found')
block = text[start:end]

replacements = [
    ('width:min(100%,950px)!important;', 'width:min(100%,1160px)!important;', 1),
    ('max-width:950px!important;', 'max-width:1160px!important;', 1),
    ('aspect-ratio:950/590!important;', 'aspect-ratio:1160/390!important;', 2),
    ('padding:9.7% 10.5% 23.6%!important;', 'padding:8% 17% 21% 19.5%!important;', 2),
    ("background-image:url('assets/tftmon-arena-live.webp')!important;", "background-image:url('assets/tftmon-arena-approved.webp')!important;", 1),
    ('width:11.2%!important;', 'width:8.5%!important;', 1),
    ('height:14.2%!important;', 'height:24%!important;', 1),
    ('#gameApp .fighter{width:11.8%!important;height:14.8%!important}', '#gameApp .fighter{width:9%!important;height:25%!important}', 1),
]
for old, new, expected in replacements:
    count = block.count(old)
    if count != expected:
        raise SystemExit(f'Expected {expected} occurrence(s) of {old!r}, found {count}')
    block = block.replace(old, new)
text = text[:start] + block + text[end:]

old_coords = """      const arenaTy=(c.y+.5)/6;
      const arenaLeftPct=24.2+(11.8-24.2)*arenaTy,arenaRightPct=75.8+(88.2-75.8)*arenaTy;
      const arenaXPct=arenaLeftPct+(arenaRightPct-arenaLeftPct)*((c.x+.5)/7);
      const arenaYPct=17.1+(76.4-17.1)*arenaTy;
      d.style.left=(layer.clientWidth*arenaXPct/100-layer.clientWidth*.056)+'px';
      d.style.top=(layer.clientHeight*arenaYPct/100-layer.clientHeight*.071)+'px';
      d.style.setProperty('--arena-depth',(0.80+arenaTy*.27).toFixed(3));"""
new_coords = """      const arenaTy=(c.y+.5)/6;
      const arenaLeftPct=23.8+(19.5-23.8)*arenaTy,arenaRightPct=79.2+(83.0-79.2)*arenaTy;
      const arenaXPct=arenaLeftPct+(arenaRightPct-arenaLeftPct)*((c.x+.5)/7);
      const arenaYPct=c.y<3?(12.7+c.y*10.0):(45.5+(c.y-3)*12.7);
      d.style.left=(layer.clientWidth*arenaXPct/100-layer.clientWidth*.0425)+'px';
      d.style.top=(layer.clientHeight*arenaYPct/100-layer.clientHeight*.12)+'px';
      d.style.setProperty('--arena-depth',(0.82+arenaTy*.26).toFixed(3));"""
if text.count(old_coords) != 1:
    raise SystemExit(f'Expected exact old combat coordinate block once, found {text.count(old_coords)}')
text = text.replace(old_coords, new_coords, 1)

style_after = text[start:text.find('</style>', start)]
if "assets/tftmon-arena-live.webp" in style_after:
    raise SystemExit('Old corrupted arena reference still present in approved CSS')
if "assets/tftmon-arena-approved.webp" not in text:
    raise SystemExit('Exact approved arena reference missing after patch')

path.write_text(text, encoding='utf-8')
PY

git diff --check

git config user.name 'github-actions[bot]'
git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
git rm -f \
  assets/tftmon-arena-exact-1.b64 \
  assets/tftmon-arena-exact-2.b64 \
  assets/tftmon-arena-exact-3.b64 \
  assets/tftmon-arena-exact-4.b64 \
  assets/tftmon-arena-exact-5.b64 \
  assets/tftmon-arena-exact-6.b64
git rm -f assets/tftmon-arena-live.webp || true
git add index.html assets/tftmon-arena-approved.webp
git commit -m 'Apply exact approved TFTmon arena from approved mockup'
git push origin HEAD:main
