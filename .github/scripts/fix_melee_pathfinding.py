from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

old = """  function moveToward(c,t){
    if(c.rootUntil>(state.combat?.elapsedMs||0)||!t)return;
    const opts=[];const dx=t.x-c.x,dy=t.y-c.y;if(dx)opts.push([c.x+Math.sign(dx),c.y]);if(dy)opts.push([c.x,c.y+Math.sign(dy)]);
    if(dy)opts.push([c.x+1,c.y],[c.x-1,c.y]);if(dx)opts.push([c.x,c.y+1],[c.x,c.y-1]);
    for(const [x,y] of opts){if(x>=0&&x<7&&y>=0&&y<6&&!occupied(x,y,c)){c.x=x;c.y=y;return}}
  }
"""

new = """  function moveToward(c,t){
    if(c.rootUntil>(state.combat?.elapsedMs||0)||!t)return;
    const range=combatRange(c);
    // Keep the existing simple movement for ranged units. The pathfinding below
    // is intentionally limited to melee so this fix cannot change ranged/support behavior.
    if(range>1){
      const opts=[];const dx=t.x-c.x,dy=t.y-c.y;if(dx)opts.push([c.x+Math.sign(dx),c.y]);if(dy)opts.push([c.x,c.y+Math.sign(dy)]);
      if(dy)opts.push([c.x+1,c.y],[c.x-1,c.y]);if(dx)opts.push([c.x,c.y+1],[c.x,c.y-1]);
      for(const [x,y] of opts){if(x>=0&&x<7&&y>=0&&y<6&&!occupied(x,y,c)){c.x=x;c.y=y;return}}
      return;
    }

    // Melee pathfinding on the 7x6 logical board. Search for the shortest path
    // to any free tile adjacent to the target while treating every living unit
    // as an obstacle. This prevents the old left/right oscillation behind allies.
    const start={x:c.x,y:c.y,first:null};
    const queue=[start],seen=new Set([c.x+','+c.y]);
    for(let qi=0;qi<queue.length;qi++){
      const cur=queue[qi];
      if(cur.first&&dist(cur,t)<=1){c.x=cur.first.x;c.y=cur.first.y;return}
      const dx=t.x-cur.x,dy=t.y-cur.y,dirs=[];
      if(dx)dirs.push([Math.sign(dx),0]);
      if(dy)dirs.push([0,Math.sign(dy)]);
      if(dx)dirs.push([-Math.sign(dx),0]);
      if(dy)dirs.push([0,-Math.sign(dy)]);
      if(!dx)dirs.push([1,0],[-1,0]);
      if(!dy)dirs.push([0,1],[0,-1]);
      const used=new Set();
      for(const [sx,sy] of dirs){
        const dk=sx+','+sy;if(used.has(dk))continue;used.add(dk);
        const x=cur.x+sx,y=cur.y+sy;
        if(x<0||x>=7||y<0||y>=6)continue;
        const key=x+','+y;if(seen.has(key)||occupied(x,y,c))continue;
        seen.add(key);queue.push({x,y,first:cur.first||{x,y}});
      }
    }
  }
"""

if old not in text:
    raise SystemExit('Expected moveToward block not found; no changes made.')
if text.count(old) != 1:
    raise SystemExit(f'Expected exactly one moveToward block, found {text.count(old)}')

text = text.replace(old, new, 1)

required = [
    'Melee pathfinding on the 7x6 logical board',
    'const queue=[start],seen=new Set',
    'if(range>1){',
    'if(cur.first&&dist(cur,t)<=1)'
]
for token in required:
    if token not in text:
        raise SystemExit(f'Missing validation token: {token}')

path.write_text(text, encoding='utf-8')
