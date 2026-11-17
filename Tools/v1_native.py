"""Native Blueprint patch helpers; never rebuild existing gameplay graphs."""
import unreal
B=unreal.BlueprintEditorLibrary;G=unreal.BlueprintGraphPinLibrary;E=unreal.EditorAssetLibrary
class Graph:
 def __init__(self,bp):self.bp=bp;self.ed=unreal.BlueprintGraphEditor.get_graph_editor_by_name(bp,'EventGraph')
 def ip(self,n,k):return B.find_input_pin(n,k)
 def op(self,n,k='ReturnValue'):return B.find_output_pin(n,k)
 def link(self,a,b):assert G.try_create_connection(a,b),(str(G.get_pin_name(a)),str(G.get_pin_name(b)))
 def arg(self,n,k,v):
  p=self.ip(n,k)
  if isinstance(v,(str,int,float,bool)):
   assert G.set_pin_value(p,str(v).lower() if isinstance(v,bool) else str(v)),(n.get_name(),k,v)
  else:self.link(v,p)
  return n
 def call(self,fn,/,**kw):
  n=self.ed.add_call_function_node('/Script/'+fn)
  for k,v in kw.items():self.arg(n,k,v)
  return n
 def flow(self,n,f):self.link(f,B.find_execute_pin(n));return B.find_then_pin(n)
 def invoke(self,f,fn,/,**kw):n=self.call(fn,**kw);return self.flow(n,f)
 def branch(self,f,test):
  n=self.ed.add_branch_node();self.link(test,self.ip(n,'Condition'));self.link(f,B.find_execute_pin(n));return self.op(n,'then'),self.op(n,'else')
 def tag(self,tag,obj=None):
  kw={'Tag':tag}
  if obj is not None:kw['self']=obj
  return self.op(self.call('Engine.Actor:ActorHasTag',**kw))
 def get(self,k):return self.op(self.ed.add_get_member_variable_node(k),k)
 def put(self,f,k,v):n=self.ed.add_set_member_variable_node(k);self.arg(n,k,v);return self.flow(n,f)
 def math(self,fn,a,b=None):
  n=self.call('Engine.KismetMathLibrary:'+fn)
  values=[('A',a)]+([('B',b)] if b is not None else [])
  for k,v in sorted(values,key=lambda kv:isinstance(kv[1],(str,int,float,bool))):self.arg(n,k,v)
  return self.op(n)
 def each(self,f,tag):
  actors=self.call('Engine.GameplayStatics:GetAllActorsWithTag',Tag=tag);f=self.flow(actors,f)
  n=self.ed.add_macro_node('/Engine/EditorBlueprintResources/StandardMacros.StandardMacros:ForEachLoop');self.link(self.op(actors,'OutActors'),self.ip(n,'Array'));self.link(f,self.ip(n,'Exec'));return self.op(n,'LoopBody'),self.op(n,'Array Element'),self.op(n,'Completed')
 def comp(self,a,cls):return self.op(self.call('Engine.Actor:GetComponentByClass',self=a,ComponentClass='/Script/Engine.'+cls))
 def finish(self):
  B.compile_blueprint(self.bp);errors=self.ed.list_nodes_with_errors();assert not errors,[n.get_name() for n in errors];E.save_loaded_asset(self.bp)

