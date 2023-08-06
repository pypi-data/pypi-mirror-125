from datetime import datetime
iLKkM=str
iLKkx=int
iLKkj=super
iLKkW=False
iLKkV=isinstance
iLKku=hash
iLKkc=True
iLKke=list
iLKkr=map
iLKkq=None
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:iLKkM):
  self.hash_ref:iLKkM=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:iLKkM,rel_path:iLKkM,file_name:iLKkM,size:iLKkx,service:iLKkM,region:iLKkM):
  iLKkj().__init__(hash_ref)
  self.rel_path:iLKkM=rel_path
  self.file_name:iLKkM=file_name
  self.size:iLKkx=size
  self.service:iLKkM=service
  self.region:iLKkM=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,iLKku=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return iLKkW
  if not iLKkV(other,StateFileRef):
   return iLKkW
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return iLKku((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other):
  if not other:
   return iLKkW
  if not iLKkV(other,StateFileRef):
   return iLKkW
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others):
  for other in others:
   if self.congruent(other):
    return iLKkc
  return iLKkW
 def metadata(self)->iLKkM:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:iLKkM,state_files:Set[StateFileRef],parent_ptr:iLKkM):
  iLKkj().__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:iLKkM=parent_ptr
 def state_files_info(self)->iLKkM:
  return "\n".join(iLKke(iLKkr(lambda state_file:iLKkM(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:iLKkM,head_ptr:iLKkM,message:iLKkM,timestamp:iLKkM=iLKkM(datetime.now().timestamp()),delta_log_ptr:iLKkM=iLKkq):
  self.tail_ptr:iLKkM=tail_ptr
  self.head_ptr:iLKkM=head_ptr
  self.message:iLKkM=message
  self.timestamp:iLKkM=timestamp
  self.delta_log_ptr:iLKkM=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:iLKkM,to_node:iLKkM)->iLKkM:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:iLKkM,state_files:Set[StateFileRef],parent_ptr:iLKkM,creator:iLKkM,rid:iLKkM,revision_number:iLKkx,assoc_commit:Commit=iLKkq):
  iLKkj().__init__(hash_ref,state_files,parent_ptr)
  self.creator:iLKkM=creator
  self.rid:iLKkM=rid
  self.revision_number:iLKkx=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(iLKku=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(iLKkr(lambda state_file:iLKkM(state_file),self.state_files))if self.state_files else "",assoc_commit=iLKkM(self.assoc_commit))
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:iLKkM,state_files:Set[StateFileRef],parent_ptr:iLKkM,creator:iLKkM,comment:iLKkM,active_revision_ptr:iLKkM,outgoing_revision_ptrs:Set[iLKkM],incoming_revision_ptr:iLKkM,version_number:iLKkx):
  iLKkj().__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(iLKku=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(iLKkr(lambda stat_file:iLKkM(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
