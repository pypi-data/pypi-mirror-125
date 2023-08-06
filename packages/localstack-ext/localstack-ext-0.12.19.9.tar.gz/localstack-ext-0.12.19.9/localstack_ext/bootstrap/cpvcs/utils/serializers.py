import abc
YxQvb=str
YxQvh=staticmethod
YxQvL=set
YxQvg=list
YxQvm=map
YxQvK=int
YxQvu=open
import logging
import os
from typing import Dict,Optional,Set
from localstack_ext.bootstrap.cpvcs.models import(Commit,CPVCSNode,CPVCSObj,Revision,StateFileRef,Version)
from localstack_ext.bootstrap.cpvcs.utils.common import config_context
LOG=logging.getLogger(__name__)
class CPVCSSerializer(abc.ABC):
 def __init__(self):
  pass
 @abc.abstractmethod
 def store_obj(self,cpvcs_obj:CPVCSObj)->YxQvb:
  pass
 @abc.abstractmethod
 def retrieve_obj(self,key:YxQvb)->Optional[CPVCSObj]:
  pass
 @YxQvh
 def _deserialize_state_files(state_files_str:YxQvb)->Set[StateFileRef]:
  if not state_files_str:
   return YxQvL()
  state_files_attrs=state_files_str.split(";")
  state_files:Set[StateFileRef]=YxQvL()
  for state_file_attrs in state_files_attrs:
   instance_attrs=YxQvg(YxQvm(lambda x:x.split(":")[1],state_file_attrs.split(",")))
   state_files.add(StateFileRef(size=YxQvK(instance_attrs[0]),service=instance_attrs[1],region=instance_attrs[2],hash_ref=instance_attrs[3],file_name=instance_attrs[4],rel_path=instance_attrs[5]))
  return state_files
class VersionSerializerTxt(CPVCSSerializer):
 def store_obj(self,cpvcs_obj:CPVCSNode)->YxQvb:
  with YxQvu(os.path.join(config_context.get_ver_obj_store_path(),cpvcs_obj.hash_ref),"w")as fp:
   fp.write(YxQvb(cpvcs_obj))
  return cpvcs_obj.hash_ref
 def retrieve_obj(self,key:YxQvb)->Optional[Version]:
  file_path=os.path.join(config_context.get_ver_obj_store_path(),key)
  if not os.path.isfile(file_path):
   LOG.debug(f"No Version Obj file found in path {file_path}")
   return
  with YxQvu(os.path.join(config_context.get_ver_obj_store_path(),key),"r")as fp:
   lines=YxQvg(YxQvm(lambda line:line.rstrip(),fp.readlines()))
   version_attrs=YxQvg(YxQvm(lambda line:line.split("=")[1],lines))
   state_files=self._deserialize_state_files(version_attrs[8])
   return Version(parent_ptr=version_attrs[0],hash_ref=version_attrs[1],creator=version_attrs[2],comment=version_attrs[3],version_number=YxQvK(version_attrs[4]),active_revision_ptr=version_attrs[5],outgoing_revision_ptrs=YxQvL(version_attrs[6].split(";")),incoming_revision_ptr=version_attrs[7],state_files=state_files)
class RevisionSerializerTxt(CPVCSSerializer):
 def store_obj(self,cpvcs_obj:Revision)->YxQvb:
  with YxQvu(os.path.join(config_context.get_rev_obj_store_path(),cpvcs_obj.hash_ref),"w")as fp:
   fp.write(YxQvb(cpvcs_obj))
  return cpvcs_obj.hash_ref
 def retrieve_obj(self,key:YxQvb)->Optional[Revision]:
  file_path=os.path.join(config_context.get_rev_obj_store_path(),key)
  if not os.path.isfile(file_path):
   LOG.debug(f"No Revision Obj file found in path {file_path}")
   return
  def _deserialize_commit(commit_str:YxQvb)->Commit:
   if not commit_str or commit_str=="None":
    return
   commit_attrs=YxQvg(YxQvm(lambda commit_attr:commit_attr.split(":")[1],commit_str.split(",")))
   return Commit(tail_ptr=commit_attrs[0],head_ptr=commit_attrs[1],message=commit_attrs[2],timestamp=commit_attrs[3],delta_log_ptr=commit_attrs[4])
  with YxQvu(os.path.join(config_context.get_rev_obj_store_path(),key))as fp:
   lines=YxQvg(YxQvm(lambda line:line.rstrip(),fp.readlines()))
   revision_attrs=YxQvg(YxQvm(lambda line:line.split("=")[1],lines))
   state_files=self._deserialize_state_files(revision_attrs[5])
   return Revision(parent_ptr=revision_attrs[0],hash_ref=revision_attrs[1],creator=revision_attrs[2],rid=revision_attrs[3],revision_number=YxQvK(revision_attrs[4]),state_files=state_files,assoc_commit=_deserialize_commit(revision_attrs[6]))
version_serializer=VersionSerializerTxt()
revision_serializer=RevisionSerializerTxt()
txt_serializers:Dict[YxQvb,CPVCSSerializer]={"version":version_serializer,"revision":revision_serializer}
# Created by pyminifier (https://github.com/liftoff/pyminifier)
