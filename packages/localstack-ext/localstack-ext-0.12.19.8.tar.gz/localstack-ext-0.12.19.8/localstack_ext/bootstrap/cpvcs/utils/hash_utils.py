import hashlib
pQLBf=str
pQLBh=hex
pQLBT=open
pQLBx=Exception
pQLBk=map
pQLBP=isinstance
import logging
import os
import random
from localstack_ext.bootstrap.cpvcs.models import CPVCSNode,Revision,Version
from localstack_ext.bootstrap.cpvcs.utils.common import config_context
LOG=logging.getLogger(__name__)
def random_hash()->pQLBf:
 return pQLBh(random.getrandbits(160))
def compute_file_hash(file_path:pQLBf)->pQLBf:
 try:
  with pQLBT(file_path,"rb")as fp:
   return hashlib.sha1(fp.read()).hexdigest()
 except pQLBx as e:
  LOG.warning(f"Failed to open file and compute hash for file at {file_path}: {e}")
def compute_node_hash(cpvcs_node:CPVCSNode)->pQLBf:
 if not cpvcs_node.state_files:
  return random_hash()
 state_file_keys=pQLBk(lambda state_file:state_file.hash_ref,cpvcs_node.state_files)
 m=hashlib.sha1()
 for key in state_file_keys:
  try:
   with pQLBT(os.path.join(config_context.get_obj_store_path(),key),"rb")as fp:
    m.update(fp.read())
  except pQLBx as e:
   LOG.warning(f"Failed to open file and compute hash for {key}: {e}")
 if pQLBP(cpvcs_node,Revision):
  m.update(cpvcs_node.rid.encode("utf-8"))
  m.update(pQLBf(cpvcs_node.revision_number).encode("utf-8"))
 elif pQLBP(cpvcs_node,Version):
  m.update(pQLBf(cpvcs_node.version_number).encode("utf-8"))
 return m.hexdigest()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
