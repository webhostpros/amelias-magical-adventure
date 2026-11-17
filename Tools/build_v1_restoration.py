"""Author curse-lifting scenery and a small persistent, tag-driven restoration actor."""
import unreal,math,random,json,sys
from pathlib import Path
P=Path(__file__).parent;sys.path.insert(0,str(P));from v1_native import Graph,B,G,E
if '-AllowSceneReauthoring' not in unreal.SystemLibrary.get_command_line():raise RuntimeError('One-time authoring reference. The release already contains the authored scene. Back up your project before deliberate reauthoring.')
R='/Game/AmeliasAdventure';T=unreal.AssetToolsHelpers.get_asset_tools();M=unreal.MaterialEditingLibrary;W=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);L=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem);L.load_level(R+'/Lvl_AmeliasAdventure');A={a.get_actor_label():a for a in W.get_all_level_actors()}
def material(name,col,glow=0):
 m=unreal.load_asset(R+'/Materials/'+name) or T.create_asset(name,R+'/Materials',unreal.Material,unreal.MaterialFactoryNew());M.delete_all_material_expressions(m);c=M.create_material_expression(m,unreal.MaterialExpressionConstant3Vector);c.set_editor_property('constant',unreal.LinearColor(*col,1));M.connect_material_property(c,'',unreal.MaterialProperty.MP_BASE_COLOR)
 if glow:
  n=M.create_material_expression(m,unreal.MaterialExpressionMultiply);n.set_editor_property('const_b',glow);M.connect_material_expressions(c,'',n,'A');M.connect_material_property(n,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR)
 M.recompile_material(m);E.save_loaded_asset(m);return m
palette=[(1,.12,.48),(.15,.65,1),(.65,.21,1),(.2,1,.65),(1,.72,.2)]
mats=[material('M_RestorationColor'+str(i),c,.3) for i,c in enumerate(palette)]
firemats=[material('M_FireworkGlow'+str(i),c,16) for i,c in enumerate(palette)]
stemmat=material('M_RestorationStem',(.7,.75,.5));wingmats=[material('M_Butterfly'+str(i),c,.6) for i,c in enumerate(palette)]
# Reuse the short-lived radial burst animation, with luminous particles for fireworks.
fb=unreal.load_asset(R+'/Blueprints/BP_SkyFirework') or E.duplicate_asset(R+'/Blueprints/BP_MagicCelebration',R+'/Blueprints/BP_SkyFirework')
sub=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);lib=unreal.SubobjectDataBlueprintFunctionLibrary
for h in sub.k2_gather_subobject_data_for_blueprint(fb):
 c=lib.get_object(lib.get_data(h))
 if isinstance(c,unreal.StaticMeshComponent):c.set_material(0,firemats[int(c.get_name().split('_')[0].removeprefix('Fleck'))%5]);c.set_cast_shadow(False)
B.compile_blueprint(fb);E.save_loaded_asset(fb)
def tag(a,value):a.tags=list(set(a.tags+[unreal.Name(value)]))
def hidden(a):a.set_actor_hidden_in_game(True);a.set_is_temporarily_hidden_in_editor(False)
def static(name,p,mesh,scale,mat=None,group='RestoredIsland'):
 a=A.get(name) or W.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(*p));a.modify();a.set_actor_label(name);A[name]=a;c=a.static_mesh_component;c.modify();c.set_mobility(unreal.ComponentMobility.MOVABLE);c.set_static_mesh(unreal.load_asset(mesh));c.set_collision_profile_name('NoCollision');c.set_cast_shadow(False)
 if mat:c.set_material(0,mat)
 a.set_actor_location(unreal.Vector(*p),False,True);a.set_actor_scale3d(unreal.Vector(*scale));tag(a,group);hidden(a);return a
# Keep all new foliage away from castle walls, shore rocks and obstacle landing surfaces.
exclude=[]
for n,a in A.items():
 if any(k in n.lower() for k in ['step','hop','shore_rock','edgerock','sign','dock']):
  b,e=a.get_actor_bounds(False)
  if e.x<1500 and e.y<1500:exclude.append((b.x,b.y,e.x+105,e.y+105))
rng=random.Random(417);patches=[]
for i in range(1000):
 x=rng.uniform(-2300,8300);y=rng.uniform(-3900,3600)
 if 2100<x<7550 and -2850<y<1550:continue
 if any(abs(x-bx)<ex and abs(y-by)<ey for bx,by,ex,ey in exclude):continue
 if any((x-px)**2+(y-py)**2<200**2 for px,py in patches):continue
 patches.append((x,y))
 if len(patches)>=105:break
for i,(x,y) in enumerate(patches):
 # Mixed small and exotic flower clusters, with three mushrooms per meadow patch.
 for j in range(4):
  scale=(.9+(i%4)*.4)*(2.3 if j==0 and i%7==0 else 1);a=static('Restoration_Flower%03d_%d'%(i,j),(x+rng.uniform(-55,55),y+rng.uniform(-55,55),4),'/Game/Medieval_Castle/meshes/plants/SM_flower_0'+str(1+(i+j)%8),(scale,scale,scale));a.set_actor_rotation(unreal.Rotator(yaw=rng.uniform(0,360)),False)
 if i%2==0:
  for j in range(3):
   px=x+70+j*27;py=y+40;h=18+(i+j)%4*8
   static('Restoration_MushroomStem%d_%d'%(i,j),(px,py,4+h/2),'/Engine/BasicShapes/Cylinder',(.075,.075,h/100),stemmat)
   static('Restoration_MushroomCap%d_%d'%(i,j),(px,py,4+h),'/Engine/BasicShapes/Sphere',(.28,.28,.1),mats[(i+j)%5])
# Imported animals use their matching pack animation skeletons.
animals=[('Kitty',(-1250,500,4),.85),('Kitty',(1300,1900,4),.95),('Horse',(3400,2700,4),1),('Horse',(4700,-3500,4),.93),('Chicken',(700,700,4),1),('Chicken',(770,735,4),1),('Deer',(7400,2400,4),1),('Deer',(200,-2100,4),.8)]
for i,(species,p,size) in enumerate(animals):
 name='Restoration_Animal'+str(i);a=A.get(name) or W.spawn_actor_from_class(unreal.SkeletalMeshActor,unreal.Vector(*p));a.modify();a.set_actor_label(name);A[name]=a;c=a.skeletal_mesh_component;c.modify();c.set_skeletal_mesh_asset(unreal.load_asset('/Game/Animals_Free/Animals/Meshes/SKM_'+species+'_001'));c.set_collision_profile_name('NoCollision');c.set_animation_mode(unreal.AnimationMode.ANIMATION_SINGLE_NODE);clip='ANIM_Chicken_001_Anim_Chicken_001_idle' if species=='Chicken' else 'ANIM_'+species+'_001_Anim_'+species+'_001_'+('eat' if species=='Horse' else 'idle');c.set_animation(unreal.load_asset('/Game/Animals_Free/Animals/Animations/'+clip));c.play(True);a.set_actor_scale3d(unreal.Vector(size,size,size));a.set_actor_rotation(unreal.Rotator(yaw=i*51),False);tag(a,'RestoredIsland');hidden(a)
# Butterflies have two asymmetric wings. Controller animates their figure-eight flight.
for i,(x,y) in enumerate(patches[::4]):
 for side in [-1,1]:
  a=static('Restoration_Butterfly%d_%d'%(i,side),(x,y,80),'/Engine/BasicShapes/Sphere',(.07,.13,.012),wingmats[i%5],'RestoredIsland');tag(a,'RestorationButterfly');tag(a,'Butterfly'+str(i));tag(a,'ButterflyLeft' if side<0 else 'ButterflyRight')
# A huge readable sky celebration above the castle; appears during the painting.
a=A.get('Restoration_Hurray') or W.spawn_actor_from_class(unreal.TextRenderActor,unreal.Vector(5800,1800,1900));a.modify();a.set_actor_label('Restoration_Hurray');a.text_render.set_text('HURRAY!');a.text_render.set_world_size(240);a.text_render.set_horizontal_alignment(unreal.HorizTextAligment.EHTA_CENTER);a.text_render.set_text_render_color(unreal.Color(255,180,235,255));a.set_actor_rotation(unreal.Rotator(yaw=180),False);tag(a,'RestorationHurray');hidden(a)
# Sunny white light throughout every room, independent of the carried lantern.
for i,(x,y,z) in enumerate([(2800,0,390),(3500,650,390),(3500,-650,390),(4300,550,390),(5000,300,390),(5700,-400,390),(4300,-1750,430),(5200,-1750,430),(6100,-1750,430),(6700,-1750,430)]):
 name='Restoration_DayFill'+str(i);a=A.get(name) or W.spawn_actor_from_class(unreal.PointLight,unreal.Vector(x,y,z));a.modify();a.set_actor_label(name);c=a.point_light_component;c.modify();c.set_mobility(unreal.ComponentMobility.MOVABLE);c.set_intensity(550);c.set_light_color(unreal.LinearColor(1,.97,.93,1));c.set_attenuation_radius(1150);c.set_cast_shadows(False);tag(a,'VictoryDayLight');hidden(a)
name='Restoration_DaylightExposure';a=A.get(name) or W.spawn_actor_from_class(unreal.PostProcessVolume,unreal.Vector());a.modify();a.set_actor_label(name);a.set_editor_property('unbound',True);a.priority=250;a.blend_weight=0;s=unreal.PostProcessSettings();s.override_auto_exposure_bias=True;s.auto_exposure_bias=.7;s.override_scene_color_tint=True;s.scene_color_tint=unreal.LinearColor(1,1,1,1);s.override_color_saturation=True;s.color_saturation=unreal.Vector4(1.12,1.1,1.1,1);a.settings=s;tag(a,'VictoryExposure')
# Tiny restoration controller keeps all state in the existing save's HUD tags.
bp=unreal.load_asset(R+'/Blueprints/BP_IslandRestoration');g=Graph(bp)
for k,t in [('GardenShown','bool'),('DaylightShown','bool'),('LastFirework','real')]:
 try:unreal.get_default_object(bp.generated_class()).get_editor_property(k)
 except:B.add_member_variable(bp,k,B.get_basic_type_by_name(t))
B.compile_blueprint(bp)
tick=g.ed.find_event_node('ReceiveTick');assert tick
f=B.find_then_pin(tick);pc=g.call('Engine.GameplayStatics:GetPlayerController',PlayerIndex=0);hud=g.op(g.call('Engine.PlayerController:GetHUD',self=g.op(pc)));time=g.op(g.call('Engine.GameplayStatics:GetTimeSeconds'))
def reveal(f,group):
 body,a,done=g.each(f,group);g.invoke(body,'Engine.Actor:SetActorHiddenInGame',self=a,bNewHidden=False);return done
# Day lighting is idempotent and restored when loading any previous victory save.
win,_=g.branch(f,g.tag('SpellLifted',hud));once,new=g.branch(win,g.get('DaylightShown'));new=reveal(new,'VictoryDayLight');actors=g.call('Engine.GameplayStatics:GetAllActorsOfClass',ActorClass='/Script/Engine.PostProcessVolume');new=g.flow(actors,new);loop=g.ed.add_macro_node('/Engine/EditorBlueprintResources/StandardMacros.StandardMacros:ForEachLoop');g.link(g.op(actors,'OutActors'),g.ip(loop,'Array'));g.link(new,g.ip(loop,'Exec'));a=g.op(loop,'Array Element');body,_=g.branch(g.op(loop,'LoopBody'),g.tag('VictoryExposure',a));setter=g.ed.add_set_member_variable_node('BlendWeight','/Script/Engine.PostProcessVolume');g.arg(setter,'self',a);g.arg(setter,'BlendWeight',1);g.flow(setter,body);new=g.put(g.op(loop,'Completed'),'DaylightShown',True)
# Independent chains all execute each Tick using a shared continuation.
# Multiple inputs to an impure node are legal and act as a join.
join=g.call('Engine.KismetSystemLibrary:PrintString',InString='',bPrintToScreen=False,bPrintToLog=False);g.flow(join,once);g.flow(join,new);f=B.find_then_pin(join)
shown,unshown=g.branch(f,g.get('GardenShown'));can,wait=g.branch(unshown,g.tag('PinkCastleOwned',hud));can=reveal(can,'RestoredIsland');can=g.put(can,'GardenShown',True)
j=g.call('Engine.KismetSystemLibrary:PrintString',InString='',bPrintToScreen=False,bPrintToLog=False)
for q in [shown,can,wait]:g.flow(j,q)
f=B.find_then_pin(j)
painting,quiet=g.branch(f,g.tag('PinkPainting',hud));painting=reveal(painting,'RestorationHurray');elapsed=g.math('Subtract_DoubleDouble',time,g.get('LastFirework'));go,waiting=g.branch(painting,g.math('Greater_DoubleDouble',elapsed,.55));go=g.put(go,'LastFirework',time)
# Alternate each burst over the island and above the castle. Existing confetti continues beneath.
x=g.math('Add_DoubleDouble',4400,g.math('Multiply_DoubleDouble',g.math('Sin',g.math('Multiply_DoubleDouble',time,1.7)),2800));y=g.math('Multiply_DoubleDouble',g.math('Sin',g.math('Multiply_DoubleDouble',time,2.3)),2600);z=g.math('Add_DoubleDouble',1500,g.math('Multiply_DoubleDouble',g.math('Sin',time),500));v=g.op(g.call('Engine.KismetMathLibrary:MakeVector',X=x,Y=y,Z=z));tr=g.op(g.call('Engine.KismetMathLibrary:MakeTransform',Location=v,Scale='4,4,4'));spawn=g.call('Engine.GameplayStatics:BeginDeferredActorSpawnFromClass',ActorClass=fb.generated_class().get_path_name(),SpawnTransform=tr,CollisionHandlingOverride='AlwaysSpawn');go=g.flow(spawn,go);go=g.invoke(go,'Engine.GameplayStatics:FinishSpawningActor',Actor=g.op(spawn),SpawnTransform=tr)
j=g.call('Engine.KismetSystemLibrary:PrintString',InString='',bPrintToScreen=False,bPrintToLog=False)
for q in [quiet,waiting,go]:g.flow(j,q)
f=B.find_then_pin(j)
# Butterflies orbit their fixed meadow homes, with rapid wing beats.
visible,_=g.branch(f,g.get('GardenShown'));body,butterfly,done=g.each(visible,'RestorationButterfly')
for i,(px,py) in enumerate(patches[::4]):
 yes,body=g.branch(body,g.tag('Butterfly'+str(i),butterfly));phase=g.math('Add_DoubleDouble',time,i*1.7);bx=g.math('Add_DoubleDouble',px,g.math('Multiply_DoubleDouble',g.math('Sin',phase),70));by=g.math('Add_DoubleDouble',py,g.math('Multiply_DoubleDouble',g.math('Sin',g.math('Multiply_DoubleDouble',phase,1.6)),45));bz=g.math('Add_DoubleDouble',90,g.math('Multiply_DoubleDouble',g.math('Sin',g.math('Multiply_DoubleDouble',phase,2)),25));left=g.tag('ButterflyLeft',butterfly);sel=g.call('Engine.KismetMathLibrary:SelectFloat',A=-8,B=8,bPickA=left);by=g.math('Add_DoubleDouble',by,g.op(sel));v=g.op(g.call('Engine.KismetMathLibrary:MakeVector',X=bx,Y=by,Z=bz));yes=g.invoke(yes,'Engine.Actor:K2_SetActorLocation',self=butterfly,NewLocation=v,bSweep=False,bTeleport=True);roll=g.math('Multiply_DoubleDouble',g.math('Sin',g.math('Multiply_DoubleDouble',phase,24)),55);rot=g.op(g.call('Engine.KismetMathLibrary:MakeRotator',Roll=roll,Yaw=g.math('Multiply_DoubleDouble',phase,25)));g.invoke(yes,'Engine.Actor:K2_SetActorRotation',self=butterfly,NewRotation=rot)
g.finish();a=A.get('Restoration_Controller') or W.spawn_actor_from_class(bp.generated_class(),unreal.Vector());a.modify();a.set_actor_label('Restoration_Controller');a.set_actor_tick_interval(.1)
L.save_current_level();unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True,True);(P/'v1_restoration_result.json').write_text(json.dumps({'flower_patches':len(patches),'flowers':len(patches)*4,'mushrooms':len(patches[::2])*3,'butterflies':len(patches[::4]),'animals':len(animals),'controller_nodes':len(g.ed.list_all_nodes())},indent=2));unreal.log('V1_RESTORATION_COMPLETE')
