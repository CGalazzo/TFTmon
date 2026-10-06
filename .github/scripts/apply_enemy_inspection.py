from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
marker = '// ===== TFTMON ENEMY INSPECTION ====='
if marker in text:
    raise SystemExit('Enemy inspection already applied')

# 1) Track read-only enemy inspection separately from the player's selected unit.
old_state = "bench:Array(9).fill(null),board:Array(42).fill(null),shop:[],selected:null,uid:1,combat:null,enemyPreview:null,inventory:[]"
new_state = "bench:Array(9).fill(null),board:Array(42).fill(null),shop:[],selected:null,enemySelected:null,uid:1,combat:null,enemyPreview:null,inventory:[]"
if text.count(old_state) < 2:
    raise SystemExit('state/reset anchors not found twice')
text = text.replace(old_state, new_state)

# 2) Selecting/moving one of the player's Pokemon clears enemy inspection.
old_drag = "draggingUnitId=u.id;state.selected={id:u.id,location,index};d.classList.add('dragging');els.board.classList.add('dragging-active');"
new_drag = "draggingUnitId=u.id;state.enemySelected=null;state.selected={id:u.id,location,index};d.classList.add('dragging');els.board.classList.add('dragging-active');"
if old_drag not in text:
    raise SystemExit('drag select anchor not found')
text = text.replace(old_drag, new_drag, 1)

old_click = "d.onclick=e=>{e.stopPropagation();if(state.battle)return;state.selected={id:u.id,location,index};render()};"
new_click = "d.onclick=e=>{e.stopPropagation();if(state.battle)return;state.enemySelected=null;state.selected={id:u.id,location,index};render()};"
if old_click not in text:
    raise SystemExit('player click anchor not found')
text = text.replace(old_click, new_click, 1)

old_move = "state.selected={id:source.u.id,location:destination,index};render();return true;"
new_move = "state.enemySelected=null;state.selected={id:source.u.id,location:destination,index};render();return true;"
if old_move not in text:
    raise SystemExit('move select anchor not found')
text = text.replace(old_move, new_move, 1)

# 3) Preserve enemy equipment names in combatants for inspection only.
old_items = "effects:{},rootUntil:0,hasCast:false,nextRegenAt:3000,summoned:false,dead:false,itemBonus:itemBonuses(u),intangibleUntil:0"
new_items = "effects:{},rootUntil:0,hasCast:false,nextRegenAt:3000,summoned:false,dead:false,items:(u.items||[]).map(i=>({id:i.id,key:i.key})),itemBonus:itemBonuses(u),intangibleUntil:0"
if old_items not in text:
    raise SystemExit('makeCombatant item anchor not found')
text = text.replace(old_items, new_items, 1)

# 4) Add enemy-inspection helpers and a read-only detail renderer using the approved Selected panel styling.
insert_before = "  function selectedBox(){"
if insert_before not in text:
    raise SystemExit('selectedBox anchor not found')
helpers = r'''  // ===== TFTMON ENEMY INSPECTION =====
  function selectedEnemyCombatant(){
    const ref=state.enemySelected;if(!ref)return null;
    const pools=[];
    if(state.combat?.units)pools.push(state.combat.units);
    if(state.enemyPreview?.units)pools.push(state.enemyPreview.units);
    for(const pool of pools){const c=pool.find(x=>x&&x.side==='enemy'&&x.cid===ref.cid);if(c)return c}
    state.enemySelected=null;return null;
  }
  function inspectEnemy(c){
    if(!c||c.side!=='enemy')return;
    state.enemySelected={cid:c.cid};state.selected=null;selectedBox();
  }
  function enemyInspectionStats(c){
    if(state.battle&&state.combat?.units?.includes(c))return c;
    const copy={...c,itemBonus:{...(c.itemBonus||{})},effects:{...(c.effects||{})},bonus:c.bonus?{...c.bonus}:undefined};
    const preview=state.enemyPreview||ensureEnemyPreview();
    applyBonus(copy,synergyBonuses(preview?.units||[c]));
    if(copy.passive?.kind==='sandstorm')copy.def=Math.round(copy.def*(1+(copy.passive.defBoost||0)));
    return copy;
  }
  function enemyCategoryLabel(c){
    if(c.boss)return 'Boss';if(c.summoned)return 'Invocação';
    const l=LINES[c.line];if(!l)return 'Especial';
    return l.special?'★★★★ Especial':l.cost===1?'1$ • Comum':l.cost===2?'2$ • Incomum':'3$ • Raro';
  }
  function enemyStageLabel(c){
    if(c.boss)return 'Boss';if(c.summoned)return 'Invocação';
    const l=LINES[c.line],stage=Math.max(0,c.stage||0);if(!l)return 'Especial';
    if(stage===0)return 'Forma base';return stage>=l.stages.length-1?'Forma final':'Evolução '+(stage+1);
  }
  function enemyDamageSummary(c){
    const a=c.ability||{},power=c.bonus?.power||1,atk=Math.max(0,c.atk||0),hp=Math.max(0,c.maxHp||0),raw=n=>Math.max(0,Math.round(n));
    const low=raw(atk*.90),high=raw(atk*1.10),main=raw(atk*(a.power||0)*power);
    let skill='Efeito especial.';
    if(a.kind==='blast')skill='Habilidade: '+main+' de dano principal; dano em área reduzido.';
    else if(a.kind==='multi')skill='Habilidade: '+main+' no primeiro alvo e cerca de '+raw(main*.68)+' nos demais.';
    else if(a.kind==='stun')skill='Habilidade: '+main+' de dano + atordoamento.';
    else if(a.kind==='heal')skill='Habilidade: cura cerca de '+raw(hp*(a.power||0)*power)+' e causa cerca de '+raw(atk*.7*power)+' de dano.';
    else if(a.kind==='shield')skill='Habilidade: gera cerca de '+raw(hp*(a.power||0)*power)+' de escudo e causa cerca de '+raw(atk*.8*power)+' de dano.';
    else if(a.kind==='dragonRush')skill='Habilidade: '+main+' no alvo e cerca de '+raw(main*.40)+' nos inimigos próximos.';
    else if(a.kind==='quake')skill='Habilidade: '+main+' de dano em área + controle.';
    else if(a.kind==='shadowBall')skill='Habilidade: '+main+' de dano; recupera mana ao finalizar.';
    else if(a.kind==='blizzard')skill='Habilidade: cerca de '+main+' em até 4 alvos + redução de velocidade.';
    else if(a.kind==='meteorMash')skill='Habilidade: cerca de '+main+' por alvo atingido + geração de escudo.';
    else if(a.power)skill='Habilidade: cerca de '+main+' de dano.';
    return 'Ataque básico: '+low+'–'+high+' antes da DEF. '+skill+' Valores são antes da DEF e de escudos do alvo.';
  }
  function renderEnemySelectedBox(c){
    const s=enemyInspectionStats(c),items=(c.items||[]),hpNow=state.battle?Math.max(0,Math.ceil(c.hp||0)):s.maxHp;
    const equipSlots=Array.from({length:3},(_,i)=>{
      const item=items[i],def=item&&ITEM_DEFS[item.key];
      if(!item||!def)return '<span class="selected-equip-slot empty" aria-label="Espaço de equipamento vazio">+</span>';
      return '<span class="selected-equip-slot filled" title="'+def.name+'"><span class="equipment-chip">'+itemSpriteHTML(item.key,'compact')+'<span>'+def.name+'</span></span></span>';
    }).join('');
    els.selected.innerHTML=
      '<div class="selected-card-head"><span class="selected-card-name">'+(s.special?'★★★★ ':'')+s.name+'</span><small class="selected-card-meta">OPONENTE • '+(s.types||[]).join(' / ')+' • '+s.role+'</small></div>'+
      '<div class="selected-hero"><div class="selected-sprite-wrap"><img class="selected-sprite" src="'+SPRITE(s.dex)+'" alt="'+s.name+'"></div><div class="selected-stats">'+
        '<div class="selected-stat"><span>HP</span><b>'+s.maxHp+'</b></div><div class="selected-stat"><span>ATK</span><b>'+Math.round(s.atk)+'</b></div><div class="selected-stat"><span>DEF</span><b>'+Math.round(s.def)+'</b></div></div></div>'+
      '<div class="selected-info-grid">'+
        '<div class="selected-info-card"><small>Categoria</small><b>'+enemyCategoryLabel(c)+'</b></div>'+
        '<div class="selected-info-card"><small>Estágio</small><b>'+enemyStageLabel(c)+'</b></div>'+
        '<div class="selected-info-card"><small>Alcance</small><b>'+combatRange(s)+' casa'+(combatRange(s)===1?'':'s')+'</b></div>'+
        '<div class="selected-info-card"><small>Velocidade</small><b>'+Math.round(s.speed)+'</b></div>'+
        '<div class="selected-info-card"><small>HP atual</small><b>'+hpNow+' / '+s.maxHp+'</b></div>'+
        '<div class="selected-info-card"><small>Estado</small><b>'+(c.dead?'Derrotado':'Ativo')+'</b></div></div>'+
      '<div class="selected-ability"><b class="selected-section-title">Habilidade • '+(s.ability?.name||'Nenhuma')+'</b><span class="selected-section-copy">'+abilityDescription(s)+'</span></div>'+
      '<div class="selected-passive"><b class="selected-section-title">Dano estimado</b><span class="selected-section-copy">'+enemyDamageSummary(s)+'</span></div>'+
      (s.passive?'<div class="selected-passive"><b class="selected-section-title">Passiva especial</b><span class="selected-section-copy">'+passiveDescription(s)+'</span></div>':'')+
      '<div class="selected-equipment"><div class="selected-equipment-head"><b>Equipamentos ('+items.length+'/3)</b></div><div class="selected-equipment-slots">'+equipSlots+'</div></div>';
  }
'''
text = text.replace(insert_before, helpers + '\n' + insert_before, 1)

# 5) Let selectedBox show an inspected opponent while keeping player controls read-only for enemies.
old_selected_head = "  function selectedBox(){\n    const f=state.selected?findUnit(state.selected.id):null;$('#sellBtn').disabled=!f||state.battle;\n    if(!f){els.selected.innerHTML='<small>Nenhum Pokémon selecionado.</small>';return}"
new_selected_head = "  function selectedBox(){\n    const f=state.selected?findUnit(state.selected.id):null,enemy=!f?selectedEnemyCombatant():null;$('#sellBtn').disabled=!f||state.battle;\n    if(enemy){renderEnemySelectedBox(enemy);return}\n    if(!f){els.selected.innerHTML='<small>Nenhum Pokémon selecionado.</small>';return}"
if old_selected_head not in text:
    raise SystemExit('selectedBox header anchor not found')
text = text.replace(old_selected_head, new_selected_head, 1)

# 6) Enemy preview tokens become clickable only inside their own cell-sized wrapper.
old_preview_end = "    d.innerHTML='<img src=\"'+SPRITE(c.dex)+'\" alt=\"'+c.name+'\"><div class=\"enemy-preview-name\">'+c.name+'</div>';\n    d.title=c.name;return d;"
new_preview_end = "    d.innerHTML='<img src=\"'+SPRITE(c.dex)+'\" alt=\"'+c.name+'\"><div class=\"enemy-preview-name\">'+c.name+'</div>';\n    d.title=c.name+' • Clique para ver atributos';d.tabIndex=0;d.setAttribute('role','button');\n    d.onclick=e=>{e.stopPropagation();inspectEnemy(c)};d.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();inspectEnemy(c)}};return d;"
if old_preview_end not in text:
    raise SystemExit('enemy preview token anchor not found')
text = text.replace(old_preview_end, new_preview_end, 1)

# 7) Enemy fighters are clickable during battle and the panel stays live as HP changes.
old_fighter_toggle = "      d.classList.toggle('player',c.side==='player');d.classList.toggle('enemy',c.side==='enemy');\n      d.style.setProperty('--sprite-scale',String(spriteScaleForCombat(c)));"
new_fighter_toggle = "      d.classList.toggle('player',c.side==='player');d.classList.toggle('enemy',c.side==='enemy');\n      if(c.side==='enemy'){d.tabIndex=0;d.setAttribute('role','button');d.onclick=e=>{e.stopPropagation();inspectEnemy(c)};d.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();inspectEnemy(c)}}}else{d.removeAttribute('tabindex');d.removeAttribute('role');d.onclick=null;d.onkeydown=null}\n      d.style.setProperty('--sprite-scale',String(spriteScaleForCombat(c)));"
if old_fighter_toggle not in text:
    raise SystemExit('fighter click anchor not found')
text = text.replace(old_fighter_toggle, new_fighter_toggle, 1)

old_render_end = "    layer.querySelectorAll('.fighter').forEach(d=>{if(!known.has(d.dataset.cid))d.remove()});\n  }"
new_render_end = "    layer.querySelectorAll('.fighter').forEach(d=>{if(!known.has(d.dataset.cid))d.remove()});\n    if(state.enemySelected)selectedBox();\n  }"
if old_render_end not in text:
    raise SystemExit('renderCombat end anchor not found')
text = text.replace(old_render_end, new_render_end, 1)

# 8) Clear inspected enemy at battle end so the next round starts cleanly.
old_finish = "state.battle=false;state.combat=null;const interest="
new_finish = "state.enemySelected=null;state.battle=false;state.combat=null;const interest="
if old_finish not in text:
    raise SystemExit('finishBattle clear anchor not found')
text = text.replace(old_finish, new_finish, 1)

# 9) Override pointer-events at the very end of CSS without changing any hitbox dimensions.
css = r'''

    /* ===== TFTMON ENEMY INSPECTION ===== */
    /* Click area stays inside the logical enemy cell; oversized sprites remain visual only. */
    #gameApp .board:not(.in-battle) .enemy-preview-token{
      pointer-events:auto!important;
      cursor:pointer!important;
    }
    #gameApp .board:not(.in-battle) .enemy-preview-token *{
      pointer-events:none!important;
    }
    #gameApp .battle-layer .fighter.enemy{
      pointer-events:auto!important;
      cursor:pointer!important;
    }
    #gameApp .battle-layer .fighter.player{
      pointer-events:none!important;
    }
    #gameApp .battle-layer .fighter.enemy:hover .fighter-sprite{
      filter:brightness(1.10);
    }
'''
idx = text.rfind('</style>')
if idx < 0:
    raise SystemExit('closing style tag not found')
text = text[:idx] + css + '\n' + text[idx:]

path.write_text(text, encoding='utf-8')
