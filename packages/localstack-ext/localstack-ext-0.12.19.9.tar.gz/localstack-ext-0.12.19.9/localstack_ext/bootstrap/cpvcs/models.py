from datetime import datetime
tiBXn=str
tiBXo=int
tiBXC=super
tiBXH=False
tiBXz=isinstance
tiBXU=hash
tiBXc=True
tiBXQ=list
tiBXY=map
tiBXg=None
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:tiBXn):
  self.hash_ref:tiBXn=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:tiBXn,rel_path:tiBXn,file_name:tiBXn,size:tiBXo,service:tiBXn,region:tiBXn):
  tiBXC().__init__(hash_ref)
  self.rel_path:tiBXn=rel_path
  self.file_name:tiBXn=file_name
  self.size:tiBXo=size
  self.service:tiBXn=service
  self.region:tiBXn=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,tiBXU=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return tiBXH
  if not tiBXz(other,StateFileRef):
   return tiBXH
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return tiBXU((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other):
  if not other:
   return tiBXH
  if not tiBXz(other,StateFileRef):
   return tiBXH
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others):
  for other in others:
   if self.congruent(other):
    return tiBXc
  return tiBXH
 def metadata(self)->tiBXn:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:tiBXn,state_files:Set[StateFileRef],parent_ptr:tiBXn):
  tiBXC().__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:tiBXn=parent_ptr
 def state_files_info(self)->tiBXn:
  return "\n".join(tiBXQ(tiBXY(lambda state_file:tiBXn(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:tiBXn,head_ptr:tiBXn,message:tiBXn,timestamp:tiBXn=tiBXn(datetime.now().timestamp()),delta_log_ptr:tiBXn=tiBXg):
  self.tail_ptr:tiBXn=tail_ptr
  self.head_ptr:tiBXn=head_ptr
  self.message:tiBXn=message
  self.timestamp:tiBXn=timestamp
  self.delta_log_ptr:tiBXn=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:tiBXn,to_node:tiBXn)->tiBXn:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:tiBXn,state_files:Set[StateFileRef],parent_ptr:tiBXn,creator:tiBXn,rid:tiBXn,revision_number:tiBXo,assoc_commit:Commit=tiBXg):
  tiBXC().__init__(hash_ref,state_files,parent_ptr)
  self.creator:tiBXn=creator
  self.rid:tiBXn=rid
  self.revision_number:tiBXo=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(tiBXU=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(tiBXY(lambda state_file:tiBXn(state_file),self.state_files))if self.state_files else "",assoc_commit=tiBXn(self.assoc_commit))
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:tiBXn,state_files:Set[StateFileRef],parent_ptr:tiBXn,creator:tiBXn,comment:tiBXn,active_revision_ptr:tiBXn,outgoing_revision_ptrs:Set[tiBXn],incoming_revision_ptr:tiBXn,version_number:tiBXo):
  tiBXC().__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(tiBXU=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(tiBXY(lambda stat_file:tiBXn(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
