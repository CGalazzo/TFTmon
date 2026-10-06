from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
marker = '// ===== TFTMON ASSASSIN SHADOW JUMP ====='
if marker in text:
    raise SystemExit('Assassin shadow jump already applied')

# 1) Add the safe one-time assassin jump helpers before the combat FX helpers.
insert_before = "  function fxTypeFor(c,kind=''){"
if insert_before not in text:
    raise SystemExit('fxTypeFor anchor not found')
helpers = r'''  // ===== TFTMON ASSASSIN SHADOW JUMP =====
  // One safe opening jump for Assassins. It never overlaps another living unit.
  function assassinShadowDestination(c,t){
    if(!c||!t||!state.combat)return null;
    const behind=t.side==='enemy'?-1:1;
    const preferred=[
      {x:t.x,y:t.y+behind},
      {x:t.x-1,y:t.y+behind},{x:t.x+1,y:t.y+behind},
      {x:t.x-1,y:t.y},{x:t.x+1,y:t.y},
      {x:t.x,y:t.y-behind}
    ];
    const seen=new Set();
    const valid=p=>p.x>=0&&p.x<7&&p.y>=0&&p.y<6&&!(p.x===c.x&&p.y===c.y)&&!occupied(p.x,p.y,c);
    for(const p of preferred){
      const key=p.x+','+p.y;if(seen.has(key))continue;seen.add(key);
      if(valid(p))return {x:p.x,y:p.y};
    }
    const radius=[];
    for(let y=0;y<6;y++)for(let x=0;x<7;x++){
      const p={x,y};if(dist(p,t)>2||!valid(p))continue;
      radius.push(p);
    }
    radius.sort((a,b)=>dist(a,t)-dist(b,t)||(t.side==='enemy'?a.y-b.y:b.y-a.y)||dist(a,c)-dist(b,c)||a.x-b.x);
    return radius[0]||null;
  }
  function performAssassinShadowJumps(){
    const combat=state.combat;if(!combat)return;
    const assassins=combat.units.filter(c=>!c.dead&&c.assassinJumpPending&&roleHas(c,'Assassino'));
    for(const c of assassins){
      c.assassinJumpPending=false;
      const foes=combat.units.filter(x=>x.side!==c.side&&!x.dead);if(!foes.length)continue;
      const t=targetForRole(c,foes);if(!t)continue;
      const dest=assassinShadowDestination(c,t);
      // Revalidate immediately before moving so multiple Assassins can never share a tile.
      if(!dest||occupied(dest.x,dest.y,c))continue;
      fxRing(c,'ghost');
      c.x=dest.x;c.y=dest.y;c.shadowJumped=true;
      const now=combat.elapsedMs||0;
      c.speedBoost=Math.max(c.speedBoost||0,.25);
      c.speedBoostUntil=Math.max(c.speedBoostUntil||0,now+2000);
      setTimeout(()=>{if(state.combat===combat&&!c.dead){fxRing(c,'ghost');flash(c.cid,'cast')}},35);
    }
    renderCombat();
  }
'''
text = text.replace(insert_before, helpers + '\n' + insert_before, 1)

# 2) Mark Assassins as waiting for the opening jump and keep a timer handle on combat state.
old_combat = "state.combat={units:[...player,...enemy],ticks:0,elapsedMs:0,timer:null,timeoutId:null,startedAt:battleStart,deadline:battleStart+COMBAT_LIMIT_MS,bossKey,bossInitialHp:enemy.filter(c=>c.boss).reduce((s,c)=>s+c.maxHp,0),enemyInitialHp:enemy.reduce((s,c)=>s+c.maxHp,0)};"
new_combat = "state.combat={units:[...player,...enemy],ticks:0,elapsedMs:0,timer:null,timeoutId:null,assassinJumpTimer:null,startedAt:battleStart,deadline:battleStart+COMBAT_LIMIT_MS,bossKey,bossInitialHp:enemy.filter(c=>c.boss).reduce((s,c)=>s+c.maxHp,0),enemyInitialHp:enemy.reduce((s,c)=>s+c.maxHp,0)};\n    state.combat.units.forEach(c=>{if(roleHas(c,'Assassino'))c.assassinJumpPending=true});"
if old_combat not in text:
    raise SystemExit('combat state anchor not found')
text = text.replace(old_combat, new_combat, 1)

# 3) Schedule the jump 400ms after battle start. Assassins wait in place until then.
old_timer = "    const combat=state.combat;\n    combat.timer=setInterval(combatTick,COMBAT_TICK_MS);"
new_timer = "    const combat=state.combat;\n    combat.assassinJumpTimer=setTimeout(()=>{\n      if(!state.battle||state.combat!==combat)return;\n      combat.elapsedMs=Math.min(COMBAT_LIMIT_MS,Date.now()-combat.startedAt);\n      performAssassinShadowJumps();\n    },400);\n    combat.timer=setInterval(combatTick,COMBAT_TICK_MS);"
if old_timer not in text:
    raise SystemExit('combat timer anchor not found')
text = text.replace(old_timer, new_timer, 1)

# 4) While waiting for the opening jump, Assassins do not walk or attack.
old_tick = "      if(c.stun>0){c.stun--;continue}\n      let actionSpeed=c.speed*(1-(c.sandSlow||0));"
new_tick = "      if(c.stun>0){c.stun--;continue}\n      if(c.assassinJumpPending)continue;\n      let actionSpeed=c.speed*(1-(c.sandSlow||0));"
if old_tick not in text:
    raise SystemExit('combat tick anchor not found')
text = text.replace(old_tick, new_tick, 1)

# 5) Clean up the jump timer if combat ends before it fires.
old_finish = "    clearInterval(state.combat.timer);clearTimeout(state.combat.timeoutId);"
new_finish = "    clearInterval(state.combat.timer);clearTimeout(state.combat.timeoutId);clearTimeout(state.combat.assassinJumpTimer);"
if old_finish not in text:
    raise SystemExit('finishBattle timer anchor not found')
text = text.replace(old_finish, new_finish, 1)

path.write_text(text, encoding='utf-8')
