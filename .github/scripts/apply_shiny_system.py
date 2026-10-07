from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
marker = '/* ===== TFTMON SHINY SYSTEM ===== */'
if marker in text:
    raise SystemExit('Shiny system already applied')

def replace_once(old, new, label):
    global text
    if old not in text:
        raise SystemExit(f'{label} anchor not found')
    if text.count(old) != 1:
        raise SystemExit(f'{label} expected once, found {text.count(old)}')
    text = text.replace(old, new, 1)

# 1) Shiny sprite endpoint while keeping every old SPRITE call valid.
replace_once(
"  const SPRITE = d => 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/' + d + '.png';",
"  const SPRITE = (d,shiny=false) => 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/' + (shiny?'shiny/':'') + d + '.png';",
'SPRITE helper')

# 2) Shiny state, chances and role-based passive definitions.
replace_once(
"    return {name,dex,cost:l.cost,role:l.role,types:l.types[st]||l.types[l.types.length-1],special:!!l.special,passive,\n      hp:Math.round(l.base[0]*mult),atk:Math.round(l.base[1]*(1+st*.56)),def:Math.round(l.base[2]*(1+st*.52)),\n      range:l.base[3],speed:Math.round(l.base[4]*(1+st*.08)),ability,final:st===l.stages.length-1};",
"    return {name,dex,cost:l.cost,role:l.role,types:l.types[st]||l.types[l.types.length-1],special:!!l.special,shiny:!!u.shiny,passive,\n      hp:Math.round(l.base[0]*mult),atk:Math.round(l.base[1]*(1+st*.56)),def:Math.round(l.base[2]*(1+st*.52)),\n      range:l.base[3],speed:Math.round(l.base[4]*(1+st*.08)),ability,final:st===l.stages.length-1};",
'stageData shiny flag')

replace_once(
"  function unit(line,stage=0){return {id:state.uid++,line,stage,items:[]};}\n  function newItem(key){return {id:state.itemUid++,key}}",
"  function unit(line,stage=0,shiny=false){return {id:state.uid++,line,stage,shiny:!!shiny,items:[]};}\n  const SHINY_CHANCE=.01,SHINY_SPECIAL_CHANCE=.005;\n  function shinyChanceForLine(line){return LINES[line]?.special?SHINY_SPECIAL_CHANCE:SHINY_CHANCE}\n  function shinyRoleKind(subject){\n    const role=String(subject?.role||LINES[subject?.line]?.role||''),roles=role.split('/').map(x=>x.trim());\n    if(roles.includes('Assassino'))return 'assassin';\n    if(roles.includes('Tanque'))return 'tank';\n    if(roles.includes('Suporte'))return 'support';\n    if(roles.includes('Bruiser')||roles.includes('Lutador'))return 'bruiser';\n    if(roles.includes('Mago'))return 'mage';\n    if(roles.includes('Atacante')||roles.includes('Carry'))return 'attacker';\n    return 'attacker';\n  }\n  function shinyPassiveDescription(subject){\n    const kind=shinyRoleKind(subject);\n    if(kind==='assassin')return 'Após o Salto Sombrio, recebe +15% de velocidade de ação adicional por 3s.';\n    if(kind==='tank')return 'Ao cair abaixo de 50% do HP pela primeira vez, recebe um escudo de 15% do HP máximo.';\n    if(kind==='support')return 'Curas e escudos gerados por este Pokémon são 15% mais fortes.';\n    if(kind==='bruiser')return 'Recebe +8% de HP máximo e +8% de ATK.';\n    if(kind==='mage')return 'Começa cada batalha com +20 de mana.';\n    return 'Recebe +10% de ATK.';\n  }\n  function applyShinyPreviewStats(p,u){\n    if(!u?.shiny)return p;const kind=shinyRoleKind(p);\n    if(kind==='attacker')p.atk=Math.round(p.atk*1.10);\n    else if(kind==='bruiser'){p.hp=Math.round(p.hp*1.08);p.atk=Math.round(p.atk*1.08)}\n    return p;\n  }\n  function newItem(key){return {id:state.itemUid++,key}}",
'unit and shiny helpers')

# 3) Shop odds/info, roll chance and visual card.
replace_once(
"    $('#shopInfoContent').innerHTML='<table class=\"shop-table\"><thead><tr><th>Nível</th><th>1$</th><th>2$</th><th>3$</th><th>4★</th><th>Normal B/2ª/3ª</th><th>4★ B/2ª/3ª</th></tr></thead><tbody>'+rows.join('')+'</tbody></table><p class=\"item-note\"><b>3º estágio não aparece na loja.</b> Ele só pode ser obtido evoluindo 3 cópias do 2º estágio. As chances removidas do 3º estágio foram transferidas para o 2º estágio.</p>';",
"    $('#shopInfoContent').innerHTML='<table class=\"shop-table\"><thead><tr><th>Nível</th><th>1$</th><th>2$</th><th>3$</th><th>4★</th><th>Normal B/2ª/3ª</th><th>4★ B/2ª/3ª</th></tr></thead><tbody>'+rows.join('')+'</tbody></table><p class=\"item-note\"><b>3º estágio não aparece na loja.</b> Ele só pode ser obtido evoluindo 3 cópias do 2º estágio. As chances removidas do 3º estágio foram transferidas para o 2º estágio.</p><p class=\"item-note\"><b>✨ Shiny:</b> Pokémon normais têm 1% de chance de aparecer Shiny em cada oferta; Pokémon 4★ têm 0,5%. O preço é o mesmo da versão normal.</p>';",
'shop info shiny note')

replace_once(
"      return {line,stage:rollStage(line)};",
"      return {line,stage:rollStage(line),shiny:Math.random()<shinyChanceForLine(line)};",
'shop shiny roll')

replace_once(
"    for(const offer of state.shop){if(offer&&LINES[offer.line].special&&!state.runStats.specialSeen.includes(offer.line))state.runStats.specialSeen.push(offer.line)}\n    render();",
"    for(const offer of state.shop){\n      if(offer&&LINES[offer.line].special&&!state.runStats.specialSeen.includes(offer.line))state.runStats.specialSeen.push(offer.line);\n      if(offer?.shiny){const p=stageData({line:offer.line,stage:offer.stage,shiny:true});log('✨ SHINY! Um Shiny '+p.name+' apareceu na loja!','win')}\n    }\n    render();",
'shop shiny log')

replace_once(
"      const offer=normalizeOffer(entry),l=LINES[offer.line],u={line:offer.line,stage:offer.stage},p=stageData(u),price=unitPrice(offer.line,offer.stage),d=document.createElement('div');\n      d.className='card rarity-'+l.cost;\n      const rarity=l.special?'★★★★ Especial':l.cost+'$ • '+(['Comum','Incomum','Raro'][l.cost-1]||'Especial');\n      const evo=p.final&&offer.stage>0?'Forma final':offer.stage>0?'Forma '+(offer.stage+1):'Forma base';\n      d.innerHTML='<div class=\"cost\">'+price+'</div><div class=\"rarity-label\">'+rarity+'</div><img src=\"'+SPRITE(p.dex)+'\"><div class=\"name\">'+p.name+'</div><div class=\"meta\">'+p.types.join(' / ')+' • '+p.role+'<br>'+evo+' • '+p.ability.name+'</div><button class=\"btn buy\">Comprar</button>';",
"      const offer=normalizeOffer(entry),l=LINES[offer.line],u={line:offer.line,stage:offer.stage,shiny:!!offer.shiny},p=stageData(u),price=unitPrice(offer.line,offer.stage),d=document.createElement('div');\n      d.className='card rarity-'+l.cost+(offer.shiny?' shiny-card':'');\n      const rarity=(offer.shiny?'✨ SHINY • ':'')+(l.special?'★★★★ Especial':l.cost+'$ • '+(['Comum','Incomum','Raro'][l.cost-1]||'Especial'));\n      const evo=p.final&&offer.stage>0?'Forma final':offer.stage>0?'Forma '+(offer.stage+1):'Forma base';\n      d.innerHTML='<div class=\"cost\">'+price+'</div><div class=\"rarity-label\">'+rarity+'</div><img src=\"'+SPRITE(p.dex,offer.shiny)+'\"><div class=\"name\">'+(offer.shiny?'✨ Shiny ':'')+p.name+'</div><div class=\"meta\">'+p.types.join(' / ')+' • '+p.role+'<br>'+evo+' • '+p.ability.name+'</div><button class=\"btn buy\">Comprar</button>';\n      if(offer.shiny)d.title='Passiva Shiny: '+shinyPassiveDescription(u);",
'render shop shiny card')

# 4) Purchase and automatic evolution inheritance.
replace_once(
"    state.gold-=cost;const u=unit(offer.line,offer.stage);if(open>=0)state.bench[open]=u;",
"    state.gold-=cost;const u=unit(offer.line,offer.stage,!!offer.shiny);if(open>=0)state.bench[open]=u;if(u.shiny)log('✨ Você comprou Shiny '+stageData(u).name+'!','win');",
'buy shiny unit')

replace_once(
"    const copies=allPlayerUnits().filter(u=>u.line===line&&u.stage===stage);if(extraUnit)copies.push(extraUnit);\n    if(copies.length<3)return;\n    const picked=copies.slice(0,3).map(u=>u===extraUnit?{u,location:'purchase',index:-1}:removeById(u.id));\n    const boardDest=picked.find(x=>x&&x.location==='board');\n    const evolved=unit(line,stage+1);inheritItems(evolved,picked,boardDest);",
"    const copies=allPlayerUnits().filter(u=>u.line===line&&u.stage===stage);if(extraUnit)copies.push(extraUnit);\n    if(copies.length<3)return;\n    const mergeCopies=copies.slice(0,3),shinyCopy=copies.find(u=>u.shiny);if(shinyCopy&&!mergeCopies.includes(shinyCopy))mergeCopies[2]=shinyCopy;\n    const picked=mergeCopies.map(u=>u===extraUnit?{u,location:'purchase',index:-1}:removeById(u.id));\n    const boardDest=picked.find(x=>x&&x.location==='board');\n    const evolved=unit(line,stage+1,picked.some(x=>x?.u?.shiny));inheritItems(evolved,picked,boardDest);",
'tryMerge shiny inheritance')

replace_once(
"    const p=stageData(evolved);toast('<span class=\"evo\">EVOLUÇÃO!</span> '+p.name+' entrou no time.');log('✨ Evolução: '+p.name,'win');\n    if(state.selected&&copies.some(x=>x.id===state.selected.id))state.selected={id:evolved.id,location:boardDest?'board':'bench',index:boardDest?boardDest.index:state.bench.findIndex(x=>x&&x.id===evolved.id)};",
"    const p=stageData(evolved);toast('<span class=\"evo\">EVOLUÇÃO!</span> '+(evolved.shiny?'✨ Shiny ':'')+p.name+' entrou no time.');log('✨ Evolução: '+(evolved.shiny?'Shiny ':'')+p.name,'win');\n    if(state.selected&&mergeCopies.some(x=>x.id===state.selected.id))state.selected={id:evolved.id,location:boardDest?'board':'bench',index:boardDest?boardDest.index:state.bench.findIndex(x=>x&&x.id===evolved.id)};",
'tryMerge shiny messaging')

# 5) Field/bench visuals.
replace_once(
"    const p=stageData(u),d=document.createElement('div');d.className='token'+(p.special?' special-token':'')+(state.selected&&state.selected.id===u.id?' selected':'');",
"    const p=stageData(u),d=document.createElement('div');d.className='token'+(p.special?' special-token':'')+(u.shiny?' shiny-token':'')+(state.selected&&state.selected.id===u.id?' selected':'');",
'createToken shiny class')

replace_once(
"    d.innerHTML='<img src=\"'+SPRITE(p.dex)+'\" alt=\"'+p.name+'\"><div class=\"mini\">'+(p.special?'<span class=\"special-stars\">★★★★</span> ':'')+p.name+(u.stage?' • E'+(u.stage+1):'')+'</div>';",
"    d.innerHTML='<img src=\"'+SPRITE(p.dex,u.shiny)+'\" alt=\"'+(u.shiny?'Shiny ':'')+p.name+'\"><div class=\"mini\">'+(p.special?'<span class=\"special-stars\">★★★★</span> ':'')+(u.shiny?'<span class=\"shiny-name\">✨ Shiny</span> ':'')+p.name+(u.stage?' • E'+(u.stage+1):'')+'</div>';",
'createToken shiny sprite')

# 6) Selected panel and rarity.
replace_once(
"  function rarityName(u){\n    const l=LINES[u.line];return l.special?'★★★★ Especial':l.cost===1?'1$ • Comum':l.cost===2?'2$ • Incomum':'3$ • Raro';\n  }",
"  function rarityName(u){\n    const l=LINES[u.line],base=l.special?'★★★★ Especial':l.cost===1?'1$ • Comum':l.cost===2?'2$ • Incomum':'3$ • Raro';return (u.shiny?'✨ Shiny • ':'')+base;\n  }",
'rarity shiny label')

replace_once(
"    const p=stageData(f.u),val=unitPrice(f.u.line,f.u.stage),ib=itemBonuses(f.u),items=(f.u.items||[]);\n    p.hp=Math.round(p.hp*(1+ib.hp));p.atk=Math.round(p.atk*(1+ib.atk));p.def=Math.round(p.def*(1+ib.def));",
"    const p=stageData(f.u),val=unitPrice(f.u.line,f.u.stage),ib=itemBonuses(f.u),items=(f.u.items||[]);\n    p.hp=Math.round(p.hp*(1+ib.hp));p.atk=Math.round(p.atk*(1+ib.atk));p.def=Math.round(p.def*(1+ib.def));applyShinyPreviewStats(p,f.u);",
'selected shiny stat preview')

replace_once(
"      '<div class=\"selected-card-head\"><span class=\"selected-card-name\">'+(p.special?'★★★★ ':'')+p.name+'</span><small class=\"selected-card-meta\">'+p.types.join(' / ')+' • '+p.role+'</small></div>'+\n      '<div class=\"selected-hero\"><div class=\"selected-sprite-wrap\"><img class=\"selected-sprite\" src=\"'+SPRITE(p.dex)+'\" alt=\"'+p.name+'\"></div><div class=\"selected-stats\">'+",
"      '<div class=\"selected-card-head\"><span class=\"selected-card-name\">'+(p.special?'★★★★ ':'')+(f.u.shiny?'✨ Shiny ':'')+p.name+'</span><small class=\"selected-card-meta\">'+p.types.join(' / ')+' • '+p.role+'</small></div>'+\n      '<div class=\"selected-hero\"><div class=\"selected-sprite-wrap\"><img class=\"selected-sprite'+(f.u.shiny?' shiny-selected-sprite':'')+'\" src=\"'+SPRITE(p.dex,f.u.shiny)+'\" alt=\"'+(f.u.shiny?'Shiny ':'')+p.name+'\"></div><div class=\"selected-stats\">'+",
'selected shiny identity')

replace_once(
"      (p.passive?'<div class=\"selected-passive\"><b class=\"selected-section-title\">Passiva especial</b><span class=\"selected-section-copy\">'+passiveDescription(p)+'</span></div>':'')+\n      '<div class=\"selected-equipment\">",
"      (p.passive?'<div class=\"selected-passive\"><b class=\"selected-section-title\">Passiva especial</b><span class=\"selected-section-copy\">'+passiveDescription(p)+'</span></div>':'')+\n      (f.u.shiny?'<div class=\"selected-passive shiny-passive-box\"><b class=\"selected-section-title\">✨ Passiva Shiny</b><span class=\"selected-section-copy\">'+shinyPassiveDescription(f.u)+'</span></div>':'')+\n      '<div class=\"selected-equipment\">",
'selected shiny passive')

# 7) Combatant carries shiny state and role-based bonuses.
replace_once(
"    const p=stageData(u);return {cid:side+'-'+u.id+'-'+Math.random(),side,line:u.line,stage:u.stage,name:p.name,dex:p.dex,types:p.types,role:p.role,\n      maxHp:p.hp,hp:p.hp,atk:p.atk,def:p.def,range:p.range,speed:p.speed,ability:p.ability,passive:p.passive,special:p.special,mana:0,shield:0,x,y,meter:Math.random()*35,stun:0,",
"    const p=stageData(u);return {cid:side+'-'+u.id+'-'+Math.random(),side,line:u.line,stage:u.stage,name:p.name,dex:p.dex,types:p.types,role:p.role,\n      maxHp:p.hp,hp:p.hp,atk:p.atk,def:p.def,range:p.range,speed:p.speed,ability:p.ability,passive:p.passive,special:p.special,shiny:!!u.shiny,shinyKind:u.shiny?shinyRoleKind(p):null,mana:0,shield:0,x,y,meter:Math.random()*35,stun:0,",
'makeCombatant shiny fields')

replace_once(
"    c.maxHp=Math.round(c.maxHp*(1+ib.hp)*b.hp);c.hp=c.maxHp;c.atk=Math.round(c.atk*(1+ib.atk)*b.atk);c.def=Math.round(c.def*(1+ib.def)*b.def);\n    c.speed=c.speed*(1+ib.speed)*b.speed;c.mana=b.mana;c.shield=Math.round(c.maxHp*(b.shield+ib.shield));",
"    c.maxHp=Math.round(c.maxHp*(1+ib.hp)*b.hp);c.atk=Math.round(c.atk*(1+ib.atk)*b.atk);c.def=Math.round(c.def*(1+ib.def)*b.def);\n    if(c.shinyKind==='attacker')c.atk=Math.round(c.atk*1.10);\n    else if(c.shinyKind==='bruiser'){c.maxHp=Math.round(c.maxHp*1.08);c.atk=Math.round(c.atk*1.08)}\n    c.hp=c.maxHp;c.speed=c.speed*(1+ib.speed)*b.speed;c.mana=b.mana+(c.shinyKind==='mage'?20:0);c.shield=Math.round(c.maxHp*(b.shield+ib.shield));\n    c.shinySupportBoost=c.shinyKind==='support'?.15:0;c.shinyTankShieldUsed=false;c.shinyAssassinBoostUntil=0;",
'apply shiny combat bonuses')

# 8) Assassin Shiny gets a separate +15% action-speed boost for 3s after the opening jump.
replace_once(
"      c.speedBoost=Math.max(c.speedBoost||0,.25);\n      c.speedBoostUntil=Math.max(c.speedBoostUntil||0,now+2000);",
"      c.speedBoost=Math.max(c.speedBoost||0,.25);\n      c.speedBoostUntil=Math.max(c.speedBoostUntil||0,now+2000);\n      if(c.shiny&&c.shinyKind==='assassin')c.shinyAssassinBoostUntil=Math.max(c.shinyAssassinBoostUntil||0,now+3000);",
'shiny assassin jump bonus')

replace_once(
"      let actionSpeed=c.speed*(1-(c.sandSlow||0));if(c.chillUntil>state.combat.elapsedMs)actionSpeed*=1-(c.chill||0);if(c.speedBoostUntil>state.combat.elapsedMs)actionSpeed*=1+(c.speedBoost||0);",
"      let actionSpeed=c.speed*(1-(c.sandSlow||0));if(c.chillUntil>state.combat.elapsedMs)actionSpeed*=1-(c.chill||0);if(c.speedBoostUntil>state.combat.elapsedMs)actionSpeed*=1+(c.speedBoost||0);if(c.shinyAssassinBoostUntil>state.combat.elapsedMs)actionSpeed*=1.15;",
'combat tick shiny assassin speed')

# 9) Shiny Tank emergency shield.
replace_once(
"    t.hp=Math.max(0,t.hp-raw);const dealt=before-t.hp;\n    if(t.hp===0)t.dead=true;\n    else if(t.dragonAscension&&!t.dragonResurgenceUsed&&t.maxHp&&t.hp/t.maxHp<.40){\n      t.dragonResurgenceUsed=true;heal(t,t.maxHp*.25);t.speedBoost=Math.max(t.speedBoost||0,.30);t.speedBoostUntil=Math.max(t.speedBoostUntil||0,now+4000);t.dragonResurgenceUntil=now+4000;\n    }",
"    t.hp=Math.max(0,t.hp-raw);const dealt=before-t.hp;\n    if(t.hp===0)t.dead=true;\n    else{\n      if(t.shiny&&t.shinyKind==='tank'&&!t.shinyTankShieldUsed&&t.maxHp&&t.hp/t.maxHp<.50){\n        t.shinyTankShieldUsed=true;const shinyShield=Math.round(t.maxHp*.15);t.shield+=shinyShield;fxFloat(t,'+'+shinyShield+' ESCUDO','shield');fxRing(t,'shield');\n      }\n      if(t.dragonAscension&&!t.dragonResurgenceUsed&&t.maxHp&&t.hp/t.maxHp<.40){\n        t.dragonResurgenceUsed=true;heal(t,t.maxHp*.25);t.speedBoost=Math.max(t.speedBoost||0,.30);t.speedBoostUntil=Math.max(t.speedBoostUntil||0,now+4000);t.dragonResurgenceUntil=now+4000;\n      }\n    }",
'shiny tank shield')

# 10) Support Shiny boosts only healing/shield output, not damage.
replace_once(
"      if(a1)heal(a1,c.maxHp*a.power*power);damage(c,t,c.atk*.7*power)",
"      if(a1)heal(a1,c.maxHp*a.power*power*(1+(c.shinySupportBoost||0)));damage(c,t,c.atk*.7*power)",
'shiny support heal')
replace_once(
"      const gain=Math.round(c.maxHp*a.power*power);fxAbility(c,t,a.kind,a.name);c.shield+=gain;fxFloat(c,'+'+gain+' ESCUDO','shield');damage(c,t,c.atk*.8*power)",
"      const gain=Math.round(c.maxHp*a.power*power*(1+(c.shinySupportBoost||0)));fxAbility(c,t,a.kind,a.name);c.shield+=gain;fxFloat(c,'+'+gain+' ESCUDO','shield');damage(c,t,c.atk*.8*power)",
'shiny support shield')

# 11) Combat and final summary use shiny sprites/labels.
replace_once(
"      d.classList.toggle('boss-fighter',!!c.boss);",
"      d.classList.toggle('boss-fighter',!!c.boss);d.classList.toggle('shiny-fighter',!!c.shiny);",
'combat shiny class')
replace_once(
"      const img=d.querySelector('img');img.src=SPRITE(c.dex);\n      d.querySelector('.label').textContent=c.name+(c.summoned?' ⚡':'');",
"      const img=d.querySelector('img');img.src=SPRITE(c.dex,c.shiny);\n      d.querySelector('.label').textContent=(c.shiny?'✨ ':'')+c.name+(c.summoned?' ⚡':'');",
'combat shiny sprite')
replace_once(
"    const mons=team.length?team.map(u=>{const p=stageData(u);return '<div class=\"final-mon\"><img src=\"'+SPRITE(p.dex)+'\"><div>'+(p.special?'★★★★ ':'')+p.name+'</div><small>'+p.types.join(' / ')+'</small></div>'}).join(''):'<span class=\"subtitle\">Nenhum Pokémon restante.</span>';",
"    const mons=team.length?team.map(u=>{const p=stageData(u);return '<div class=\"final-mon\"><img src=\"'+SPRITE(p.dex,u.shiny)+'\"><div>'+(p.special?'★★★★ ':'')+(u.shiny?'✨ Shiny ':'')+p.name+'</div><small>'+p.types.join(' / ')+'</small></div>'}).join(''):'<span class=\"subtitle\">Nenhum Pokémon restante.</span>';",
'final summary shiny')

# 12) Rules explain the mechanic and clarify synergy behavior.
rules_anchor = "  <div class=\"modal-section\"><h3>★★★★ Pokémon especiais</h3><p>Dratini, Larvitar, Gastly, Gible e Beldum são 4★. Eles começam a aparecer no nível 6, podem vir evoluídos e possuem habilidades/passivas exclusivas.</p></div>"
rules_new = rules_anchor + "\n  <div class=\"modal-section\"><h3>✨ Pokémon Shiny</h3><p>Cada oferta normal da loja tem 1% de chance de ser Shiny; Pokémon 4★ têm 0,5%. Shiny custa o mesmo, usa sua coloração especial e recebe uma Passiva Shiny de acordo com a função. Se uma das 3 cópias usadas na evolução for Shiny, a evolução continua Shiny. Shiny e normal contam como a mesma linha para sinergias.</p></div>"
replace_once(rules_anchor, rules_new, 'rules shiny section')

# 13) Visual-only Shiny styling. No hitbox/layout changes.
css = r'''

    /* ===== TFTMON SHINY SYSTEM ===== */
    #gameApp .card.shiny-card{
      border-color:rgba(255,226,105,.92)!important;
      box-shadow:0 0 0 1px rgba(255,246,181,.34),0 0 18px rgba(255,215,72,.34),0 10px 24px rgba(0,0,0,.38)!important;
      background-image:radial-gradient(circle at 72% 18%,rgba(255,241,155,.12),transparent 34%)!important;
    }
    #gameApp .card.shiny-card .rarity-label,#gameApp .card.shiny-card .name,#gameApp .shiny-name{
      color:#fff0a6!important;text-shadow:0 0 8px rgba(255,220,72,.7);
    }
    #gameApp .card.shiny-card>img,
    #gameApp .token.shiny-token>img,
    #gameApp .fighter.shiny-fighter .fighter-sprite img,
    #gameApp .selected-sprite.shiny-selected-sprite{
      filter:drop-shadow(0 7px 5px rgba(0,0,0,.62)) drop-shadow(0 0 9px rgba(255,230,95,.88))!important;
    }
    #gameApp .token.shiny-token .mini,#gameApp .fighter.shiny-fighter .label{
      color:#fff0a6!important;text-shadow:0 0 7px rgba(255,220,72,.72),0 1px 3px #000!important;
    }
    #gameApp .shiny-passive-box{
      border-color:rgba(255,220,86,.55)!important;
      background:linear-gradient(180deg,rgba(60,45,8,.28),rgba(6,23,36,.96))!important;
      box-shadow:inset 0 1px rgba(255,246,180,.08),0 0 10px rgba(255,215,70,.08)!important;
    }
    #gameApp .shiny-passive-box .selected-section-title{color:#fff0a6!important}
'''
idx = text.rfind('</style>')
if idx < 0:
    raise SystemExit('closing style tag not found')
text = text[:idx] + css + '\n' + text[idx:]

path.write_text(text, encoding='utf-8')
