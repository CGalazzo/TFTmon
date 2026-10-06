from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
marker = '/* ===== TFTMON INVISIBLE BOARD CELLS ===== */'
if marker in text:
    raise SystemExit('Marker already present')
css = r'''

    /* ===== TFTMON INVISIBLE BOARD CELLS ===== */
    /* Keep all 42 functional hitboxes, but hide their resting visual overlay. */
    #gameApp .board .cell{
      border-color:transparent!important;
      background:transparent!important;
      box-shadow:none!important;
      outline:none!important;
    }
    #gameApp .board .cell::before,
    #gameApp .board .cell::after{
      border-color:transparent!important;
      background:transparent!important;
      box-shadow:none!important;
      opacity:0!important;
    }
    #gameApp .board .cell:hover{
      border-color:transparent!important;
      background:transparent!important;
      box-shadow:none!important;
      outline:none!important;
    }
    /* Only show the actual destination while dragging a Pokemon. */
    #gameApp .board.dragging-active .cell.drag-over{
      outline:2px solid rgba(245,197,66,.88)!important;
      background:rgba(245,197,66,.08)!important;
      box-shadow:inset 0 0 14px rgba(245,197,66,.16),0 0 12px rgba(245,197,66,.22)!important;
    }
'''
idx = text.rfind('</style>')
if idx < 0:
    raise SystemExit('No closing style tag found')
text = text[:idx] + css + '\n' + text[idx:]
path.write_text(text, encoding='utf-8')
