from pathlib import Path
import re

p = Path('index.html')
s = p.read_text()


def rep(old, new, label):
    global s
    count = s.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected 1 occurrence, found {count}')
    s = s.replace(old, new, 1)


def rep_count(old, new, expected, label):
    global s
    count = s.count(old)
    if count != expected:
        raise SystemExit(f'{label}: expected {expected} occurrences, found {count}')
    s = s.replace(old, new)


# Progression-related copy only.
rep("Auto-battler fan-made • 25 etapas • raridades • 4★ especiais • bosses",
    "Auto-battler fan-made • 50 etapas • raridades • 4★ especiais • bosses",
    'header stage count')
rep('<b id="roundStat">1/25</b>', '<b id="roundStat">1/50</b>', 'initial round counter')
rep('As batalhas são automáticas e ficam mais difíceis até o confronto final da etapa 25.',
    'As batalhas são automáticas e ficam mais difíceis até o confronto final da etapa 50.',
    'start screen final round')
rep('Supere 25 etapas e os bosses das etapas 6, 12, 18 e 25. Economize ouro, compre XP, encontre 4★ a partir do nível 6 e fortaleça seu time com equipamentos.',
    'Supere 50 etapas e os bosses das etapas 6, 12, 18, 25, 32, 38, 44 e 50. Economize ouro, compre XP, encontre 4★ a partir do nível 6 e fortaleça seu time com equipamentos.',
    'start objective')
rep('Etapa 6: Onix • 12: 3 Tauros • 18: Raikou, Entei ou Suicune • 25: Mewtwo. Vitória rende 2 componentes; ao perder removendo pelo menos 50% do HP total do boss, você recebe 1.',
    'Etapa 6: Onix • 12: 3 Tauros • 18: Raikou, Entei ou Suicune • 25: Mewtwo • 32: Tyranitar • 38: Dragonite • 44: Articuno + Zapdos + Moltres • 50: Rayquaza. Vitória rende 2 componentes; ao perder removendo pelo menos 50% do HP total do boss, você recebe 1.',
    'rules boss list')
rep('Sobreviva às 25 etapas. Não existem fraquezas, resistências ou imunidades elementais de dano: as tipagens servem para formar sinergias.',
    'Sobreviva às 50 etapas e derrote Rayquaza na etapa final. Não existem fraquezas, resistências ou imunidades elementais de dano: as tipagens servem para formar sinergias.',
    'rules objective')
rep("Electric:{icon:'⚡',levels:[3,5],desc:['+20% velocidade de ação','+20% velocidade de ação; invoca Zapdos']}",
    "Electric:{icon:'⚡',levels:[3,5],desc:['+20% velocidade de ação','+20% velocidade de ação; invoca Electivire']}",
    'electric synergy description')

# Enemy equipment pool: completed items only. Player item mechanics are untouched.
rep("const COMPONENTS=Object.keys(ITEM_DEFS).filter(k=>ITEM_DEFS[k].component);",
    "const COMPONENTS=Object.keys(ITEM_DEFS).filter(k=>ITEM_DEFS[k].component);\n  const ENEMY_EQUIPMENT_KEYS=Object.keys(ITEM_DEFS).filter(k=>ITEM_DEFS[k].recipe);",
    'enemy equipment pool')

old_bosses = """  const BOSS_ROUNDS=[6,12,18,25];
  const BOSS_DEFS={
    onix:{name:'Onix',dex:95,types:['Rock','Ground'],role:'Boss',hp:360,atk:24,def:20,range:1,speed:68,ability:{name:'Deslizamento de Pedras',kind:'blast',power:1.45},count:1},
    tauros:{name:'Tauros',dex:128,types:['Normal'],role:'Boss',hp:285,atk:31,def:11,range:1,speed:108,ability:{name:'Investida',kind:'blast',power:1.48},count:3},
    raikou:{name:'Raikou',dex:243,types:['Electric'],role:'Boss Lendário',hp:820,atk:50,def:15,range:3,speed:126,ability:{name:'Trovão Lendário',kind:'multi',power:1.55},count:1},
    entei:{name:'Entei',dex:244,types:['Fire'],role:'Boss Lendário',hp:930,atk:54,def:18,range:2,speed:103,ability:{name:'Fogo Sagrado',kind:'blast',power:1.72},count:1},
    suicune:{name:'Suicune',dex:245,types:['Water'],role:'Boss Lendário',hp:1050,atk:44,def:23,range:2,speed:98,ability:{name:'Aurora',kind:'heal',power:.42},count:1},
    mewtwo:{name:'Mewtwo',dex:150,types:['Psychic'],role:'Boss Final',hp:1650,atk:66,def:25,range:3,speed:128,ability:{name:'Psíquico Supremo',kind:'multi',power:1.82},count:1}
  };"""
new_bosses = """  const BOSS_ROUNDS=[6,12,18,25,32,38,44,50];
  const BOSS_DEFS={
    onix:{name:'Onix',dex:95,types:['Rock','Ground'],role:'Boss',hp:360,atk:24,def:20,range:1,speed:68,ability:{name:'Deslizamento de Pedras',kind:'blast',power:1.45},count:1},
    tauros:{name:'Tauros',dex:128,types:['Normal'],role:'Boss',hp:285,atk:31,def:11,range:1,speed:108,ability:{name:'Investida',kind:'blast',power:1.48},count:3},
    raikou:{name:'Raikou',dex:243,types:['Electric'],role:'Boss Lendário',hp:820,atk:50,def:15,range:3,speed:126,ability:{name:'Trovão Lendário',kind:'multi',power:1.55},count:1},
    entei:{name:'Entei',dex:244,types:['Fire'],role:'Boss Lendário',hp:930,atk:54,def:18,range:2,speed:103,ability:{name:'Fogo Sagrado',kind:'blast',power:1.72},count:1},
    suicune:{name:'Suicune',dex:245,types:['Water'],role:'Boss Lendário',hp:1050,atk:44,def:23,range:2,speed:98,ability:{name:'Aurora',kind:'heal',power:.42},count:1},
    mewtwo:{name:'Mewtwo',dex:150,types:['Psychic'],role:'Boss',hp:1650,atk:66,def:25,range:3,speed:128,ability:{name:'Psíquico Supremo',kind:'multi',power:1.82},count:1},
    tyranitar:{name:'Tyranitar',dex:248,types:['Rock','Dark'],role:'Boss',hp:2200,atk:72,def:32,range:1,speed:90,ability:{name:'Triturar Sísmico',kind:'blast',power:1.90},count:1},
    dragonite:{name:'Dragonite',dex:149,types:['Dragon','Flying'],role:'Boss',hp:2600,atk:82,def:28,range:2,speed:112,ability:{name:'Fúria do Dragão',kind:'multi',power:1.95},count:1},
    birdtrio:{name:'Articuno + Zapdos + Moltres',dex:145,types:['Flying'],role:'Boss Triplo',count:3},
    rayquaza:{name:'Rayquaza',dex:384,types:['Dragon','Flying'],role:'Boss Final',hp:4200,atk:96,def:34,range:2,speed:128,ability:{name:'Ascensão Celeste',kind:'multi',power:2.05},count:1}
  };
  const BIRD_TRIO=[
    {name:'Articuno',dex:144,types:['Ice','Flying'],role:'Boss Lendário',hp:1350,atk:55,def:30,range:3,speed:96,ability:{name:'Nevasca',kind:'blizzard',power:1.30,chill:.25,duration:3000}},
    {name:'Zapdos',dex:145,types:['Electric','Flying'],role:'Boss Lendário',hp:1250,atk:72,def:22,range:3,speed:124,ability:{name:'Trovão',kind:'multi',power:1.70}},
    {name:'Moltres',dex:146,types:['Fire','Flying'],role:'Boss Lendário',hp:1300,atk:78,def:22,range:3,speed:110,ability:{name:'Fogo Celeste',kind:'blast',power:1.85}}
  ];"""
rep(old_bosses, new_bosses, 'boss definitions')

old_key = """  function bossKeyForRound(round,legendary){
    if(round===6)return 'onix';if(round===12)return 'tauros';if(round===18)return legendary||'raikou';if(round===25)return 'mewtwo';return null;
  }"""
new_key = """  function bossKeyForRound(round,legendary){
    if(round===6)return 'onix';if(round===12)return 'tauros';if(round===18)return legendary||'raikou';if(round===25)return 'mewtwo';
    if(round===32)return 'tyranitar';if(round===38)return 'dragonite';if(round===44)return 'birdtrio';if(round===50)return 'rayquaza';return null;
  }"""
rep(old_key, new_key, 'boss round mapping')

old_diff = """  function difficultyProfile(round){
    if(round<=1)return {count:1,scale:.70,stage1:0,stage2:0,synergy:0};
    if(round===2)return {count:1,scale:.76,stage1:0,stage2:0,synergy:0};
    if(round===3)return {count:2,scale:.80,stage1:0,stage2:0,synergy:0};
    if(round<=5)return {count:round===4?2:3,scale:round===4?.86:.92,stage1:0,stage2:0,synergy:0};
    if(round<=8)return {count:3,scale:.96,stage1:.15,stage2:0,synergy:3};
    if(round<=11)return {count:4,scale:1.00,stage1:.28,stage2:0,synergy:3};
    if(round<=14)return {count:5,scale:1.06,stage1:.44,stage2:0,synergy:3};
    if(round<=17)return {count:5,scale:1.11,stage1:.62,stage2:0,synergy:5};
    if(round<=21)return {count:6,scale:1.16,stage1:.76,stage2:0,synergy:5};
    return {count:7,scale:1.23,stage1:.88,stage2:0,synergy:5};
  }"""
new_diff = """  function difficultyProfile(round){
    if(round<=1)return {count:1,scale:.70,stage1:0,stage2:0,synergy:0};
    if(round===2)return {count:1,scale:.76,stage1:0,stage2:0,synergy:0};
    if(round===3)return {count:2,scale:.80,stage1:0,stage2:0,synergy:0};
    if(round<=5)return {count:round===4?2:3,scale:round===4?.86:.92,stage1:0,stage2:0,synergy:0};
    if(round<=8)return {count:3,scale:.96,stage1:.15,stage2:0,synergy:3};
    if(round<=11)return {count:4,scale:1.00,stage1:.28,stage2:0,synergy:3};
    if(round<=14)return {count:5,scale:1.06,stage1:.44,stage2:0,synergy:3};
    if(round<=17)return {count:5,scale:1.11,stage1:.62,stage2:0,synergy:5};
    if(round<=21)return {count:6,scale:1.16,stage1:.76,stage2:0,synergy:5};
    if(round<=25)return {count:7,scale:1.23,stage1:.88,stage2:0,synergy:5};
    if(round<=28)return {count:8,scale:1.28,stage1:.92,stage2:0,synergy:5,items:1};
    if(round<=31)return {count:8,scale:1.33,stage1:.96,stage2:0,synergy:5,items:2};
    if(round<=35)return {count:9,scale:1.36,stage1:.97,stage2:0,synergy:5,items:2};
    if(round<=37)return {count:9,scale:1.41,stage1:.98,stage2:0,synergy:5,items:3};
    if(round<=40)return {count:10,scale:1.45,stage1:.98,stage2:0,synergy:5,items:3};
    if(round<=43)return {count:10,scale:1.52,stage1:.99,stage2:0,synergy:5,items:4};
    if(round<=46)return {count:11,scale:1.57,stage1:1,stage2:0,synergy:5,items:4};
    return {count:11,scale:1.65,stage1:1,stage2:0,synergy:5,items:6};
  }"""
rep(old_diff, new_diff, 'difficulty progression')

# State and reset both carry maxRounds.
rep_count('maxRounds:25', 'maxRounds:50', 2, 'max rounds state/reset')

# Harder XP curve, still capped at player level 9.
rep('function xpNeed(){return state.level>=9?999:state.level*4;}',
    "const XP_NEEDS={2:8,3:12,4:16,5:24,6:36,7:56,8:80};\n  function xpNeed(){return state.level>=9?999:(XP_NEEDS[state.level]||state.level*4);}",
    'xp curve')

# Late-game enemy equipment distribution only.
rep('const profile=difficultyProfile(state.round),arr=[],positions=[];',
    'const profile=difficultyProfile(state.round),arr=[],positions=[],enemyLoadouts=Array.from({length:profile.count},()=>[]);',
    'enemy loadout init')
rep("while(positions.length<profile.count){const p=Math.floor(Math.random()*21);if(!positions.includes(p))positions.push(p)}",
    """while(positions.length<profile.count){const p=Math.floor(Math.random()*21);if(!positions.includes(p))positions.push(p)}
    for(let i=0;i<(profile.items||0);i++){
      const target=(i*2+state.round)%profile.count,current=enemyLoadouts[target],pool=ENEMY_EQUIPMENT_KEYS.filter(k=>!current.some(item=>item.key===k));
      const key=pool[Math.floor(Math.random()*pool.length)];if(key)current.push({id:'enemy-'+state.round+'-'+i,key});
    }""",
    'enemy equipment distribution')
rep("const pos=positions[n],combatant=makeCombatant({id:8000+n,line:key,stage},'enemy',pos%7,Math.floor(pos/7));",
    "const pos=positions[n],combatant=makeCombatant({id:8000+n,line:key,stage,items:enemyLoadouts[n]},'enemy',pos%7,Math.floor(pos/7));",
    'enemy equipment application')

# Support a three-species boss encounter without changing combat movement/targeting.
old_makeboss = """  function makeBossCombatant(key,index=0){
    const d=BOSS_DEFS[key],positions=d.count===3?[{x:1,y:1},{x:3,y:1},{x:5,y:1}]:[{x:3,y:1}],p=positions[index]||positions[0];
    return {cid:'enemy-boss-'+key+'-'+index,side:'enemy',line:'boss-'+key,stage:0,name:d.name,dex:d.dex,types:d.types,role:d.role,
      maxHp:d.hp,hp:d.hp,atk:d.atk,def:d.def,range:d.range,speed:d.speed,ability:d.ability,mana:0,shield:0,x:p.x,y:p.y,meter:0,stun:0,
      effects:{},rootUntil:0,hasCast:false,nextRegenAt:3000,summoned:false,boss:true,bossKey:key,dead:false,itemBonus:{atk:0,hp:0,def:0,speed:0,power:0,regen:0,shield:0,basicLeech:0,abilityLeech:0,manaOnAttack:0}};
  }"""
new_makeboss = """  function makeBossCombatant(key,index=0){
    const meta=BOSS_DEFS[key],d=key==='birdtrio'?(BIRD_TRIO[index]||BIRD_TRIO[0]):meta,positions=meta.count===3?[{x:1,y:1},{x:3,y:1},{x:5,y:1}]:[{x:3,y:1}],p=positions[index]||positions[0];
    return {cid:'enemy-boss-'+key+'-'+index,side:'enemy',line:'boss-'+key,stage:0,name:d.name,dex:d.dex,types:d.types,role:d.role,
      maxHp:d.hp,hp:d.hp,atk:d.atk,def:d.def,range:d.range,speed:d.speed,ability:d.ability,mana:0,shield:0,x:p.x,y:p.y,meter:0,stun:0,
      effects:{},rootUntil:0,hasCast:false,nextRegenAt:3000,summoned:false,boss:true,bossKey:key,dead:false,itemBonus:{atk:0,hp:0,def:0,speed:0,power:0,regen:0,shield:0,basicLeech:0,abilityLeech:0,manaOnAttack:0}};
  }"""
rep(old_makeboss, new_makeboss, 'multi-species boss support')

rep("const factor={onix:2,tauros:1,raikou:1.4,entei:1.4,suicune:1.4,mewtwo:1.6}[c.bossKey]||1.25;",
    "const factor={onix:2,tauros:1,raikou:1.4,entei:1.4,suicune:1.4,mewtwo:1.6,tyranitar:1.6,dragonite:1.55,birdtrio:1.35,rayquaza:1.8}[c.bossKey]||1.25;",
    'new boss sprite scale')

# Electric 5-line summon: Zapdos -> Electivire. Existing summon rules remain the same.
pattern = r"  function summonZapdos\(side\)\{.*?\n  \}\n(?=  function dist\()"
match = re.search(pattern, s, re.S)
if not match:
    raise SystemExit('summonZapdos block not found')
new_summon = """  function summonElectivire(side){
    if(!state.combat||state.combat.units.some(c=>c.side===side&&c.summoned))return;
    const allies=state.combat.units.filter(c=>c.side===side&&!c.dead&&!c.summoned);
    if(!allies.length)return;
    const free=[];
    for(let y=side==='player'?3:0;y<(side==='player'?6:3);y++)for(let x=0;x<7;x++)if(!occupied(x,y))free.push({x,y});
    free.sort((a,b)=>Math.min(...allies.map(c=>dist(a,c)))-Math.min(...allies.map(c=>dist(b,c)))||(side==='player'?b.y-a.y:a.y-b.y)||a.x-b.x);
    if(!free.length)return;
    const c={cid:side+'-electivire',side,line:'electivire',stage:0,name:'Electivire',dex:466,types:['Electric'],role:'Lutador / Invocação',
      maxHp:230,hp:230,atk:28,def:10,range:1,speed:110,ability:{name:'Soco Trovão',kind:'blast',power:1.35},
      mana:0,shield:0,...free[0],meter:0,stun:0,effects:{},rootUntil:0,hasCast:false,nextRegenAt:3000,summoned:true,dead:false};
    applyBonus(c,{});state.combat.units.push(c);
    log('⚡ '+(side==='player'?'Seu time':'O rival')+' invocou Electivire com 5 linhas Elétricas!');
  }
"""
s = s[:match.start()] + new_summon + s[match.end():]
rep("if(pb.Electric===2)summonZapdos('player');", "if(pb.Electric===2)summonElectivire('player');", 'player electric summon')
rep("if(!bossKey&&eb.Electric===2)summonZapdos('enemy');", "if(!bossKey&&eb.Electric===2)summonElectivire('enemy');", 'enemy electric summon')

# New boss rounds hit harder on a loss; existing rounds stay identical.
rep("const bossDamage={6:8,12:12,18:16,25:20}[state.round]||0,",
    "const bossDamage={6:8,12:12,18:16,25:20,32:24,38:28,44:32,50:36}[state.round]||0,",
    'boss player damage progression')

# Avoid the awkward label "3x Articuno + Zapdos + Moltres".
rep("el.innerHTML='<b>👑 Etapa '+state.round+' • '+(d.count>1?d.count+'× ':'')+d.name+'</b>';",
    "el.innerHTML='<b>👑 Etapa '+state.round+' • '+(bossKey==='birdtrio'?d.name:(d.count>1?d.count+'× ':'')+d.name)+'</b>';",
    'bird trio preview')

# Safety checks: progression changes only.
checks = [
    'Auto-battler fan-made • 50 etapas',
    '<b id="roundStat">1/50</b>',
    'maxRounds:50',
    'const BOSS_ROUNDS=[6,12,18,25,32,38,44,50];',
    "if(round===50)return 'rayquaza'",
    'const XP_NEEDS={2:8,3:12,4:16,5:24,6:36,7:56,8:80};',
    "name:'Electivire',dex:466",
    "birdtrio:{name:'Articuno + Zapdos + Moltres'",
    "rayquaza:{name:'Rayquaza',dex:384",
    'items:6',
    'count:11,scale:1.65'
]
for needle in checks:
    if needle not in s:
        raise SystemExit('validation missing: ' + needle)
if s.count('maxRounds:50') != 2:
    raise SystemExit('expected two maxRounds:50 entries')
if 'summonZapdos' in s:
    raise SystemExit('old Zapdos summon reference still present')
if 'maxRounds:25' in s:
    raise SystemExit('old maxRounds still present')

p.write_text(s)
print('50-round progression patch validated successfully')
