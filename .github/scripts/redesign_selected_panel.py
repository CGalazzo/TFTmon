from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

marker = '/* ===== TFTMON SELECTED PANEL REDESIGN ===== */'
if marker not in text:
    css = r'''

    /* ===== TFTMON SELECTED PANEL REDESIGN ===== */
    /* Visual-only refinement for the selected Pokemon card. */
    #gameApp .side-right .selected-box{
      grid-column:1/-1;
      min-height:0!important;
      padding:9px!important;
      border:1px solid rgba(37,220,255,.48)!important;
      border-radius:14px!important;
      background:linear-gradient(180deg,rgba(5,27,43,.98),rgba(4,18,31,.98))!important;
      box-shadow:0 10px 28px rgba(0,0,0,.34),inset 0 1px rgba(255,255,255,.045)!important;
      backdrop-filter:none!important;
      -webkit-backdrop-filter:none!important;
      overflow:hidden!important;
      color:#eefaff;
    }
    #gameApp .selected-card-head{
      text-align:right;
      margin-bottom:7px;
      min-width:0;
    }
    #gameApp .selected-card-name{
      display:block;
      font-size:17px;
      line-height:1.05;
      font-weight:1000;
      color:#fff;
      letter-spacing:-.02em;
      white-space:nowrap;
      overflow:hidden;
      text-overflow:ellipsis;
    }
    #gameApp .selected-card-meta{
      display:block;
      margin-top:3px;
      font-size:9.5px;
      line-height:1.15;
      color:#9ec7de!important;
      white-space:normal;
    }
    #gameApp .selected-hero{
      display:grid;
      grid-template-columns:minmax(0,1fr) 58px;
      gap:6px;
      align-items:center;
      padding:7px 6px;
      border:1px solid #1c536f;
      border-radius:11px;
      background:radial-gradient(circle at 38% 45%,rgba(32,136,182,.15),transparent 48%),#061724;
      box-shadow:inset 0 1px rgba(255,255,255,.035);
    }
    #gameApp .selected-sprite-wrap{
      min-width:0;
      min-height:78px;
      display:grid;
      place-items:center;
    }
    #gameApp .selected-box img.selected-sprite{
      width:78px!important;
      height:78px!important;
      max-width:100%!important;
      object-fit:contain!important;
      image-rendering:pixelated;
      filter:drop-shadow(0 7px 6px rgba(0,0,0,.62))!important;
    }
    #gameApp .selected-stats{
      display:grid;
      gap:4px;
    }
    #gameApp .selected-stat{
      min-height:25px;
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:3px;
      padding:3px 5px;
      border:1px solid #246184;
      border-radius:8px;
      background:#0a2032;
      box-shadow:inset 0 1px rgba(255,255,255,.04);
      font-size:8px;
      line-height:1;
      color:#9bc8df;
      white-space:nowrap;
    }
    #gameApp .selected-stat b{
      display:inline!important;
      font-size:10px;
      color:#fff;
      line-height:1;
    }
    #gameApp .selected-info-grid{
      display:grid;
      grid-template-columns:repeat(2,minmax(0,1fr));
      gap:5px;
      margin-top:6px;
    }
    #gameApp .selected-info-card{
      min-width:0;
      padding:6px;
      border:1px solid #1e506c;
      border-radius:9px;
      background:#071a29;
      box-shadow:inset 0 1px rgba(255,255,255,.03);
    }
    #gameApp .selected-info-card small{
      display:block;
      margin-bottom:3px;
      color:#8ebbd2!important;
      font-size:8px;
      line-height:1;
      font-weight:900;
    }
    #gameApp .selected-info-card b{
      display:block!important;
      color:#f4fbff;
      font-size:9.5px;
      line-height:1.18;
      word-break:normal;
      overflow-wrap:break-word;
    }
    #gameApp .selected-ability,
    #gameApp .selected-passive,
    #gameApp .selected-equipment{
      margin-top:6px;
      padding:7px;
      border:1px solid #1d506c;
      border-radius:10px;
      background:#061724;
      box-shadow:inset 0 1px rgba(255,255,255,.03);
    }
    #gameApp .selected-section-title{
      display:block!important;
      margin-bottom:4px;
      color:#f4fbff;
      font-size:10px;
      line-height:1.15;
      font-weight:1000;
    }
    #gameApp .selected-section-copy{
      display:block;
      color:#d5e7f0;
      font-size:9.5px;
      line-height:1.35;
      font-weight:700;
    }
    #gameApp .selected-equipment-head{
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:5px;
      margin-bottom:6px;
    }
    #gameApp .selected-equipment-head b{
      display:block!important;
      color:#f4fbff;
      font-size:10px;
      line-height:1.1;
    }
    #gameApp .selected-equipment-slots{
      display:grid;
      grid-template-columns:repeat(3,minmax(0,1fr));
      gap:5px;
    }
    #gameApp .selected-equip-slot{
      min-width:0;
      aspect-ratio:1/1;
      display:grid;
      place-items:center;
      border:1px solid #285d7c;
      border-radius:9px;
      background:#0a1d2c;
      color:#396d8d;
      overflow:hidden;
    }
    #gameApp .selected-equip-slot.empty{
      font-size:22px;
      font-weight:500;
      line-height:1;
    }
    #gameApp .selected-equip-slot.filled{
      padding:3px;
    }
    #gameApp .selected-equip-slot .equipment-chip{
      display:grid!important;
      place-items:center;
      width:100%;
      min-width:0;
      padding:0!important;
      background:transparent!important;
      border:0!important;
    }
    #gameApp .selected-equip-slot .equipment-chip span{
      display:none!important;
    }
    #gameApp .selected-equip-slot img,
    #gameApp .selected-equip-slot .item-sprite{
      width:28px!important;
      height:28px!important;
      object-fit:contain!important;
      filter:none!important;
    }
    @media(max-width:1050px){
      #gameApp .side-right .selected-box{max-width:310px;width:100%;justify-self:start}
      #gameApp .selected-card-name{font-size:18px}
      #gameApp .selected-card-meta{font-size:10px}
    }
'''
    text = text.replace('</style>', css + '\n</style>', 1)

start = text.index('  function selectedBox(){')
end = text.index('  function renderStats(){', start)
new_func = r'''  function selectedBox(){
    const f=state.selected?findUnit(state.selected.id):null;$('#sellBtn').disabled=!f||state.battle;
    if(!f){els.selected.innerHTML='<small>Nenhum Pokémon selecionado.</small>';return}
    const p=stageData(f.u),val=unitPrice(f.u.line,f.u.stage),ib=itemBonuses(f.u),items=(f.u.items||[]);
    p.hp=Math.round(p.hp*(1+ib.hp));p.atk=Math.round(p.atk*(1+ib.atk));p.def=Math.round(p.def*(1+ib.def));
    const stageLabel=f.u.stage===0?'Forma base':p.final?'Forma final':'Evolução '+(f.u.stage+1);
    const equipSlots=Array.from({length:3},(_,i)=>{
      const item=items[i];
      if(!item)return '<span class="selected-equip-slot empty" aria-label="Espaço de equipamento vazio">+</span>';
      return '<span class="selected-equip-slot filled" title="'+ITEM_DEFS[item.key].name+'"><span class="equipment-chip">'+itemSpriteHTML(item.key,'compact')+'<span>'+ITEM_DEFS[item.key].name+'</span></span></span>';
    }).join('');
    els.selected.innerHTML=
      '<div class="selected-card-head"><span class="selected-card-name">'+(p.special?'★★★★ ':'')+p.name+'</span><small class="selected-card-meta">'+p.types.join(' / ')+' • '+p.role+'</small></div>'+
      '<div class="selected-hero"><div class="selected-sprite-wrap"><img class="selected-sprite" src="'+SPRITE(p.dex)+'" alt="'+p.name+'"></div><div class="selected-stats">'+
        '<div class="selected-stat"><span>HP</span><b>'+p.hp+'</b></div><div class="selected-stat"><span>ATK</span><b>'+p.atk+'</b></div><div class="selected-stat"><span>DEF</span><b>'+p.def+'</b></div></div></div>'+
      '<div class="selected-info-grid">'+
        '<div class="selected-info-card"><small>Raridade</small><b>'+rarityName(f.u)+'</b></div>'+
        '<div class="selected-info-card"><small>Estágio</small><b>'+stageLabel+'</b></div>'+
        '<div class="selected-info-card"><small>Habilidade</small><b>'+p.ability.name+'</b></div>'+
        '<div class="selected-info-card"><small>Venda</small><b>'+val+' ouro</b></div></div>'+
      '<div class="selected-ability"><b class="selected-section-title">O que a habilidade faz</b><span class="selected-section-copy">'+abilityDescription(p)+'</span></div>'+
      (p.passive?'<div class="selected-passive"><b class="selected-section-title">Passiva especial</b><span class="selected-section-copy">'+passiveDescription(p)+'</span></div>':'')+
      '<div class="selected-equipment"><div class="selected-equipment-head"><b>Equipamentos ('+items.length+'/3)</b></div><div class="selected-equipment-slots">'+equipSlots+'</div></div>';
  }
'''
text = text[:start] + new_func + text[end:]

# Lightweight guardrails: only the expected visual function/classes were added.
required = [
    'TFTMON SELECTED PANEL REDESIGN',
    'class="selected-sprite"',
    'class="selected-info-grid"',
    'class="selected-equipment-slots"',
    'function renderStats(){'
]
for token in required:
    if token not in text:
        raise SystemExit(f'Missing expected token: {token}')

path.write_text(text, encoding='utf-8')
