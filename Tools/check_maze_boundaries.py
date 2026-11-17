import unreal,json
from pathlib import Path
from collections import deque
p=Path(__file__).parent;unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).load_level('/Game/AmeliasAdventure/Lvl_AmeliasAdventure');aa=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
w=[]
for a in aa:
 n=a.get_actor_label()
 if n.startswith(('MazeUnified','MazeBattleSeal','MazeOuterEastSeal')) and not a.get_editor_property('hidden'):
  b,e=a.get_actor_bounds(False);w.append((n,b.x-e.x,b.x+e.x,b.y-e.y,b.y+e.y))
def blocked(x,y):return any(lo-58<x<hi+58 and bot-58<y<top+58 for _,lo,hi,bot,top in w)
def reach(start):
 q=deque([start]);seen={start}
 while q:
  x,y=q.popleft()
  for dx,dy in [(20,0),(-20,0),(0,20),(0,-20)]:
   t=(x+dx,y+dy)
   if t not in seen and 4220<=t[0]<=5780 and -1140<=t[1]<=780 and not blocked(*t):seen.add(t);q.append(t)
 return seen
normal=reach((4300,-500));secret=reach((4300,700));checks={'ordinary_cannot_reach_wizard':not any(y<-1080 for x,y in normal),'secret_reaches_wizard':any(y<-1080 for x,y in secret),'components_separate':not bool(normal&secret)}
spans=[v for v in w if v[0].startswith('MazeUnified')];overlaps=[]
for i,a in enumerate(spans):
 for b in spans[i+1:]:
  if min(a[2],b[2])-max(a[1],b[1])>.01 and min(a[4],b[4])-max(a[3],b[3])>.01:overlaps.append([a[0],b[0]])
checks['no_overlapping_maze_cubes']=not overlaps
(p/'maze_boundary_checks.json').write_text(json.dumps({'checks':checks,'walls':w,'overlaps':overlaps,'normal_cells':len(normal),'secret_cells':len(secret)},indent=2));assert all(checks.values()),checks
