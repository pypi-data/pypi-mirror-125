import json
XDpzE=None
XDpzV=object
XDpzt=Exception
XDpzS=int
XDpzx=bool
XDpzv=str
XDpzl=set
XDpzn=property
XDpzf=classmethod
XDpzP=False
XDpzN=True
XDpzo=staticmethod
XDpzk=len
XDpzC=getattr
XDpzi=type
XDpzF=isinstance
XDpzQ=list
import logging
import os
import re
import traceback
from typing import Dict,List
from zipfile import ZipFile
import requests
import yaml
from dulwich import porcelain
from dulwich.client import get_transport_and_path_from_url
from dulwich.repo import Repo
from localstack import config,constants
from localstack.utils.common import(chmod_r,clone,cp_r,disk_usage,download,format_number,is_command_available,load_file,mkdir,new_tmp_dir,new_tmp_file,retry,rm_rf,run,safe_requests,save_file,to_bytes,to_str,unzip)
from localstack.utils.docker_utils import DOCKER_CLIENT
from localstack.utils.testutil import create_zip_file
from localstack_ext import config as ext_config
from localstack_ext.bootstrap.licensing import get_auth_headers
from localstack_ext.bootstrap.state_utils import api_states_traverse
from localstack_ext.constants import API_PATH_PODS,API_STATES_DIR
LOG=logging.getLogger(__name__)
PERSISTED_FOLDERS=["api_states","dynamodb","kinesis"]
class PodInfo:
 def __init__(self,name=XDpzE,pod_size=0):
  self.name=name
  self.pod_size=pod_size
  self.pod_size_compressed=0
  self.persisted_resource_names=[]
class CloudPodManager(XDpzV):
 BACKEND="_none_"
 def __init__(self,pod_name=XDpzE,config=XDpzE):
  self.pod_name=pod_name
  self._pod_config=config
 def init(self):
  raise XDpzt("Not implemented")
 def push(self,comment:XDpzv=XDpzE)->PodInfo:
  raise XDpzt("Not implemented")
 def pull(self):
  raise XDpzt("Not implemented")
 def commit(self,message:XDpzv=XDpzE):
  raise XDpzt("Not implemented")
 def inject(self,version:XDpzS,reset_state:XDpzx):
  raise XDpzt("Not implemented")
 def list_versions(self)->List[XDpzv]:
  raise XDpzt("Not implemented")
 def version_info(self,version:XDpzS):
  raise XDpzt("Not implemented")
 def set_version(self,version:XDpzS,inject_version_state:XDpzx,reset_state:XDpzx,commit_before:XDpzx):
  raise XDpzt("Not implemented")
 def list_version_commits(self,version:XDpzS)->List[XDpzv]:
  raise XDpzt("Not implemented")
 def get_commit_diff(self,version:XDpzS,commit:XDpzS)->XDpzv:
  pass
 def restart_container(self):
  LOG.info("Restarting LocalStack instance with updated persistence state - this may take some time ...")
  data={"action":"restart"}
  url="%s/health"%config.get_edge_url()
  try:
   requests.post(url,data=json.dumps(data))
  except requests.exceptions.ConnectionError:
   pass
  def check_status():
   LOG.info("Waiting for LocalStack instance to be fully initialized ...")
   response=requests.get(url)
   content=json.loads(to_str(response.content))
   statuses=[v for k,v in content["services"].items()]
   assert XDpzl(statuses)=={"running"}
  retry(check_status,sleep=3,retries=10)
 @XDpzn
 def pod_config(self):
  return self._pod_config or PodConfigManager.pod_config(self.pod_name)
 @XDpzf
 def get(cls,pod_name,pre_config=XDpzE):
  pod_config=pre_config if pre_config else PodConfigManager.pod_config(pod_name)
  backend=pod_config.get("backend")
  for clazz in cls.__subclasses__():
   if clazz.BACKEND==backend:
    return clazz(pod_name=pod_name,config=pod_config)
  raise XDpzt('Unable to find Cloud Pod manager implementation type "%s"'%backend)
 def deploy_pod_into_instance(self,pod_path):
  delete_pod_zip=XDpzP
  if os.path.isdir(pod_path):
   tmpdir=new_tmp_dir()
   for folder in PERSISTED_FOLDERS:
    src_folder=os.path.join(pod_path,folder)
    tgt_folder=os.path.join(tmpdir,folder)
    cp_r(src_folder,tgt_folder,rm_dest_on_conflict=XDpzN)
   pod_path=create_zip_file(tmpdir)
   rm_rf(tmpdir)
   delete_pod_zip=XDpzN
  zip_content=load_file(pod_path,mode="rb")
  url=get_pods_endpoint()
  result=requests.post(url,data=zip_content)
  if result.status_code>=400:
   raise XDpzt("Unable to restore pod state via local pods management API %s (code %s): %s"%(url,result.status_code,result.content))
  if delete_pod_zip:
   rm_rf(pod_path)
  else:
   return pod_path
 @XDpzo
 def get_state_zip_from_instance(get_content=XDpzP):
  url=f"{get_pods_endpoint()}/state"
  result=requests.get(url)
  if result.status_code>=400:
   raise XDpzt("Unable to get local pod state via management API %s (code %s): %s"%(url,result.status_code,result.content))
  if get_content:
   return result.content
  zip_file=f"{new_tmp_file()}.zip"
  save_file(zip_file,result.content)
  return zip_file
 def get_pod_info(self,pod_data_dir:XDpzv=XDpzE):
  result=PodInfo(self.pod_name)
  if pod_data_dir:
   result.pod_size=disk_usage(pod_data_dir)
   result.persisted_resource_names=get_persisted_resource_names(pod_data_dir)
  return result
class CloudPodManagerCPVCS(CloudPodManager):
 BACKEND="cpvcs"
 @XDpzo
 def _add_state_files_func(**kwargs):
  from localstack_ext.bootstrap.cpvcs import cpvcs_api
  dir_name=kwargs.get("dir_name")
  file_name=kwargs.get("fname")
  region=kwargs.get("region")
  service_name=kwargs.get("service_name")
  cpvcs_api.create_state_file_from_fs(path=dir_name,file_name=file_name,service=service_name,region=region)
 def _add_state_to_cpvs_store(self):
  from localstack_ext.bootstrap.cpvcs.utils.common import config_context
  if not config_context.is_initialized():
   LOG.debug("No CPVCS instance detected - Could not push")
   return
  zip_file=self.get_state_zip_from_instance()
  tmp_dir=new_tmp_dir()
  with ZipFile(zip_file,"r")as state_zip:
   state_zip.extractall(tmp_dir)
   api_states_path=os.path.join(tmp_dir,API_STATES_DIR)
   api_states_traverse(api_states_path=api_states_path,side_effect=CloudPodManagerCPVCS._add_state_files_func,mutables=XDpzE)
  rm_rf(zip_file)
  rm_rf(tmp_dir)
 def init(self):
  from localstack_ext.bootstrap.cpvcs import cpvcs_api
  cpvcs_api.init(pod_name=self.pod_name)
 def push(self,comment:XDpzv=XDpzE)->PodInfo:
  from localstack_ext.bootstrap.cpvcs import cpvcs_api
  cpvcs_api.set_pod(self.pod_name)
  self._add_state_to_cpvs_store()
  created_version=cpvcs_api.push(comment=comment)
  LOG.debug(f"Created new version: {created_version}")
  return PodInfo()
 def pull(self):
  LOG.debug("Attempted to pull from Local CPVCS - Not available")
 def commit(self,message:XDpzv=XDpzE):
  from localstack_ext.bootstrap.cpvcs import cpvcs_api
  cpvcs_api.set_pod(self.pod_name)
  self._add_state_to_cpvs_store()
  finalized_revision=cpvcs_api.commit(message=message)
  LOG.debug(f"Finalized revision: {finalized_revision}")
 def inject(self,version:XDpzS,reset_state:XDpzx):
  from localstack_ext.bootstrap.cpvcs import cpvcs_api
  cpvcs_api.set_pod(self.pod_name)
  if version==-1:
   version=cpvcs_api.get_head().version_number
  tmp_pod_path=cpvcs_api.get_version_state_pod(version)
  if not tmp_pod_path:
   LOG.warning(f"Could not find state for pod with version {version}")
   return
  if reset_state:
   reset_local_state(reset_data_dir=XDpzN)
  self.deploy_pod_into_instance(tmp_pod_path)
 def list_versions(self)->List[XDpzv]:
  from localstack_ext.bootstrap.cpvcs import cpvcs_api
  cpvcs_api.set_pod(self.pod_name)
  version_list=cpvcs_api.list_versions()
  return version_list
 def version_info(self,version:XDpzS):
  from localstack_ext.bootstrap.cpvcs import cpvcs_api
  cpvcs_api.set_pod(self.pod_name)
  if version==-1:
   version=cpvcs_api.get_max_version_no()
  version_info=cpvcs_api.get_version_info(version)
  return "\n".join(version_info)
 def set_version(self,version:XDpzS,inject_version_state:XDpzx,reset_state:XDpzx,commit_before:XDpzx):
  from localstack_ext.bootstrap.cpvcs import cpvcs_api
  cpvcs_api.set_pod(self.pod_name)
  version_exists=cpvcs_api.set_active_version(version_no=version,commit_before=commit_before)
  if not version_exists:
   LOG.warning(f"Could not find version {version}")
  if inject_version_state:
   self.inject(version=version,reset_state=reset_state)
 def list_version_commits(self,version:XDpzS)->List[XDpzv]:
  from localstack_ext.bootstrap.cpvcs import cpvcs_api
  cpvcs_api.set_pod(self.pod_name)
  commits=cpvcs_api.list_version_commits(version_no=version)
  return commits
 def get_commit_diff(self,version:XDpzS,commit:XDpzS)->XDpzv:
  from localstack_ext.bootstrap.cpvcs import cpvcs_api
  cpvcs_api.set_pod(self.pod_name)
  commit_diff=cpvcs_api.get_commit_diff(version_no=version,commit_no=commit)
  return commit_diff
class CloudPodManagerFilesystem(CloudPodManager):
 BACKEND="file"
 def push(self,comment:XDpzv=XDpzE)->PodInfo:
  local_folder=self.target_folder()
  print('Pushing state of cloud pod "%s" to local folder: %s'%(self.pod_name,local_folder))
  mkdir(local_folder)
  zip_file=self.get_state_zip_from_instance()
  unzip(zip_file,local_folder)
  chmod_r(local_folder,0o777)
  result=self.get_pod_info(local_folder)
  print("Done.")
  return result
 def pull(self):
  local_folder=self.target_folder()
  if not os.path.exists(local_folder):
   print('WARN: Local path of cloud pod "%s" does not exist: %s'%(self.pod_name,local_folder))
   return
  print('Pulling state of cloud pod "%s" from local folder: %s'%(self.pod_name,local_folder))
  self.deploy_pod_into_instance(local_folder)
 def target_folder(self):
  local_folder=re.sub(r"^file://","",self.pod_config.get("url",""))
  return local_folder
class CloudPodManagerManaged(CloudPodManager):
 BACKEND="managed"
 def push(self,comment:XDpzv=XDpzE)->PodInfo:
  zip_data_content=self.get_state_zip_from_instance(get_content=XDpzN)
  print('Pushing state of cloud pod "%s" to backend server (%s KB)'%(self.pod_name,format_number(XDpzk(zip_data_content)/1000.0)))
  self.push_content(self.pod_name,zip_data_content)
  print("Done.")
  result=self.get_pod_info()
  result.pod_size_compressed=XDpzk(zip_data_content)
  return result
 def pull(self):
  presigned_url=self.presigned_url(self.pod_name,"pull")
  print('Pulling state of cloud pod "%s" from managed storage'%self.pod_name)
  zip_path=new_tmp_file()
  download(presigned_url,zip_path)
  self.deploy_pod_into_instance(zip_path)
  rm_rf(zip_path)
 @XDpzo
 def presigned_url(pod_name:XDpzv,mode:XDpzv)->XDpzv:
  data={"pod_name":pod_name,"mode":mode}
  data=json.dumps(data)
  auth_headers=get_auth_headers()
  url="%s/cloudpods/data"%constants.API_ENDPOINT
  if ext_config.SYNC_POD_VERSION:
   url=f"{url}?version={ext_config.SYNC_POD_VERSION}"
  response=safe_requests.post(url,data,headers=auth_headers)
  content=response.content
  if response.status_code>=400:
   raise XDpzt("Unable to get cloud pod presigned URL (code %s): %s"%(response.status_code,content))
  content=json.loads(to_str(content))
  return content["presignedURL"]
 @XDpzf
 def push_content(cls,pod_name,zip_data_content):
  presigned_url=cls.presigned_url(pod_name,"push")
  res=safe_requests.put(presigned_url,data=zip_data_content)
  if res.status_code>=400:
   raise XDpzt("Unable to push pod state to API (code %s): %s"%(res.status_code,res.content))
  return res
class CloudPodManagerGit(CloudPodManager):
 BACKEND="git"
 def push(self,comment:XDpzv=XDpzE):
  repo=self.local_repo()
  branch=to_bytes(self.pod_config.get("branch"))
  remote_location=self.pod_config.get("url")
  try:
   porcelain.pull(repo,remote_location,refspecs=branch)
  except XDpzt as e:
   if self.has_git_cli():
    run("cd %s; git checkout %s; git pull"%(to_str(branch),self.clone_dir))
   else:
    LOG.info("Unable to pull repo: %s %s",e,traceback.format_exc())
  zip_file=self.get_state_zip_from_instance()
  tmp_data_dir=new_tmp_dir()
  unzip(zip_file,tmp_data_dir)
  is_empty_repo=b"HEAD" not in repo or repo.refs.allkeys()=={b"HEAD"}
  if is_empty_repo:
   LOG.debug("Initializing empty repository %s"%self.clone_dir)
   init_file=os.path.join(self.clone_dir,".init")
   save_file(init_file,"")
   porcelain.add(repo,init_file)
   porcelain.commit(repo,message="Initial commit")
  if branch not in repo:
   porcelain.branch_create(repo,branch,force=XDpzN)
  self.switch_branch(branch)
  for folder in PERSISTED_FOLDERS:
   LOG.info("Copying persistence folder %s to local git repo %s"%(folder,self.clone_dir))
   src_folder=os.path.join(tmp_data_dir,folder)
   tgt_folder=os.path.join(self.clone_dir,folder)
   cp_r(src_folder,tgt_folder)
   files=tgt_folder
   if os.path.isdir(files):
    files=[os.path.join(root,f)for root,_,files in os.walk(tgt_folder)for f in files]
   if files:
    porcelain.add(repo,files)
  porcelain.commit(repo,message="Update cloud pod state")
  try:
   porcelain.push(repo,remote_location,branch)
  except XDpzt:
   if not self.has_git_cli():
    raise
   run("cd %s; git push origin %s"%(self.clone_dir,to_str(branch)))
  result=self.get_pod_info(tmp_data_dir)
  return result
 def pull(self):
  repo=self.local_repo()
  client,path=self.client()
  remote_refs=client.fetch(path,repo)
  branch=self.pod_config.get("branch")
  remote_ref=b"refs/heads/%s"%to_bytes(branch)
  if remote_ref not in remote_refs:
   raise XDpzt('Unable to find branch "%s" in remote git repo'%branch)
  remote_location=self.pod_config.get("url")
  self.switch_branch(branch)
  branch_ref=b"refs/heads/%s"%to_bytes(branch)
  from dulwich.errors import HangupException
  try:
   porcelain.pull(repo,remote_location,branch_ref)
  except HangupException:
   pass
  self.deploy_pod_into_instance(self.clone_dir)
 def client(self):
  client,path=get_transport_and_path_from_url(self.pod_config.get("url"))
  return client,path
 def local_repo(self):
  self.clone_dir=XDpzC(self,"clone_dir",XDpzE)
  if not self.clone_dir:
   pod_dir_name=re.sub(r"(\s|/)+","",self.pod_name)
   self.clone_dir=os.path.join(config.TMP_FOLDER,"pods",pod_dir_name,"repo")
   mkdir(self.clone_dir)
   if not os.path.exists(os.path.join(self.clone_dir,".git")):
    porcelain.clone(self.pod_config.get("url"),self.clone_dir)
    self.switch_branch(self.pod_config.get("branch"))
  return Repo(self.clone_dir)
 def switch_branch(self,branch):
  repo=self.local_repo()
  if self.has_git_cli():
   return run("cd %s; git checkout %s"%(self.clone_dir,to_str(branch)))
  branch_ref=b"refs/heads/%s"%to_bytes(branch)
  if branch_ref not in repo.refs:
   branch_ref=b"refs/remotes/origin/%s"%to_bytes(branch)
  repo.reset_index(repo[branch_ref].tree)
  repo.refs.set_symbolic_ref(b"HEAD",branch_ref)
 def has_git_cli(self):
  return is_command_available("git")
class PodConfigManagerMeta(XDpzi):
 def __getattr__(cls,attr):
  def _call(*args,**kwargs):
   result=XDpzE
   for manager in cls.CHAIN:
    try:
     tmp=XDpzC(manager,attr)(*args,**kwargs)
     if tmp:
      if not result:
       result=tmp
      elif XDpzF(tmp,XDpzQ)and XDpzF(result,XDpzQ):
       result.extend(tmp)
    except XDpzt:
     if LOG.isEnabledFor(logging.DEBUG):
      LOG.exception("error during PodConfigManager call chain")
   if result is not XDpzE:
    return result
   raise XDpzt('Unable to run operation "%s" for local or remote configuration'%attr)
  return _call
class PodConfigManager(XDpzV,metaclass=PodConfigManagerMeta):
 CHAIN=[]
 @XDpzf
 def pod_config(cls,pod_name):
  pods=PodConfigManager.list_pods()
  pod_config=[pod for pod in pods if pod["pod_name"]==pod_name]
  if not pod_config:
   raise XDpzt('Unable to find config for pod named "%s"'%pod_name)
  return pod_config[0]
class PodConfigManagerLocal(XDpzV):
 CONFIG_FILE=".localstack.yml"
 def list_pods(self):
  local_pods=self._load_config(safe=XDpzN).get("pods",{})
  local_pods=[{"pod_name":k,"state":"Local Only",**v}for k,v in local_pods.items()]
  existing_names=XDpzl([pod["pod_name"]for pod in local_pods])
  result=[pod for pod in local_pods if pod["pod_name"]not in existing_names]
  return result
 def store_pod_metadata(self,pod_name,metadata):
  pass
 def _load_config(self,safe=XDpzP):
  try:
   return yaml.safe_load(to_str(load_file(self.CONFIG_FILE)))
  except XDpzt:
   if safe:
    return{}
   raise XDpzt('Unable to find and parse config file "%s"'%self.CONFIG_FILE)
class PodConfigManagerRemote(XDpzV):
 def list_pods(self):
  result=[]
  auth_headers=get_auth_headers()
  url="%s/cloudpods"%constants.API_ENDPOINT
  response=safe_requests.get(url,headers=auth_headers)
  content=response.content
  if response.status_code>=400:
   raise XDpzt("Unable to fetch list of pods from API (code %s): %s"%(response.status_code,content))
  remote_pods=json.loads(to_str(content)).get("cloudpods",[])
  remote_pods=[{"state":"Shared",**pod}for pod in remote_pods]
  result.extend(remote_pods)
  return result
 def store_pod_metadata(self,pod_name,metadata):
  auth_headers=get_auth_headers()
  metadata["pod_name"]=pod_name
  response=safe_requests.post("%s/cloudpods"%constants.API_ENDPOINT,json.dumps(metadata),headers=auth_headers)
  content=response.content
  if response.status_code>=400:
   raise XDpzt("Unable to store pod metadata in API (code %s): %s"%(response.status_code,content))
  return json.loads(to_str(content))
PodConfigManager.CHAIN.append(PodConfigManagerLocal())
PodConfigManager.CHAIN.append(PodConfigManagerRemote())
def init_cpvcs(pod_name:XDpzv,pre_config:Dict[XDpzv,XDpzv],**kwargs):
 backend=CloudPodManager.get(pod_name=pod_name,pre_config=pre_config)
 backend.init()
def commit_state(pod_name:XDpzv,pre_config:Dict[XDpzv,XDpzv],message:XDpzv=XDpzE,**kwargs):
 backend=CloudPodManager.get(pod_name=pod_name,pre_config=pre_config)
 backend.commit(message=message)
def inject_state(pod_name:XDpzv,version:XDpzS,reset_state:XDpzx,pre_config:Dict[XDpzv,XDpzv],**kwargs):
 backend=CloudPodManager.get(pod_name=pod_name,pre_config=pre_config)
 backend.inject(version=version,reset_state=reset_state)
def list_versions(pod_name:XDpzv,pre_config:Dict[XDpzv,XDpzv],**kwargs)->List[XDpzv]:
 backend=CloudPodManager.get(pod_name=pod_name,pre_config=pre_config)
 versions=backend.list_versions()
 return versions
def get_version_info(version:XDpzS,pod_name:XDpzv,pre_config:Dict[XDpzv,XDpzv],**kwargs):
 backend=CloudPodManager.get(pod_name=pod_name,pre_config=pre_config)
 info=backend.version_info(version=version)
 return info
def set_version(version:XDpzS,inject_version_state:XDpzx,reset_state:XDpzx,commit_before:XDpzx,pod_name:XDpzv,pre_config:Dict[XDpzv,XDpzv],**kwargs)->XDpzx:
 backend=CloudPodManager.get(pod_name=pod_name,pre_config=pre_config)
 success=backend.set_version(version=version,inject_version_state=inject_version_state,reset_state=reset_state,commit_before=commit_before)
 return success
def list_version_commits(version:XDpzS,pod_name:XDpzv,pre_config:Dict[XDpzv,XDpzv])->List[XDpzv]:
 backend=CloudPodManager.get(pod_name=pod_name,pre_config=pre_config)
 commits=backend.list_version_commits(version=version)
 return commits
def get_commit_diff(version:XDpzS,commit:XDpzS,pod_name:XDpzv,pre_config:Dict[XDpzv,XDpzv])->XDpzv:
 backend=CloudPodManager.get(pod_name=pod_name,pre_config=pre_config)
 commit_diff=backend.get_commit_diff(version=version,commit=commit)
 return commit_diff
def push_state(pod_name,pre_config=XDpzE,squash_commits=XDpzP,comment=XDpzE,**kwargs):
 backend=CloudPodManager.get(pod_name=pod_name,pre_config=pre_config)
 pod_config=clone(backend.pod_config)
 pod_info=backend.push(comment=comment)
 pod_config["size"]=pod_info.pod_size or pod_info.pod_size_compressed
 pod_config["available_resources"]=pod_info.persisted_resource_names
 return pod_config
def get_pods_endpoint():
 edge_url=config.get_edge_url()
 return f"{edge_url}{API_PATH_PODS}"
def pull_state(pod_name,**kwargs):
 pre_config=kwargs.get("pre_config",XDpzE)
 if not pod_name:
  raise XDpzt("Need to specify a pod name")
 backend=CloudPodManager.get(pod_name=pod_name,pre_config=pre_config)
 backend.pull()
 print("Done.")
def reset_local_state(reset_data_dir=XDpzP):
 url=f"{get_pods_endpoint()}/state"
 if reset_data_dir:
  url+="/datadir"
 print("Sending request to reset the service states in local instance ...")
 result=requests.delete(url)
 if result.status_code>=400:
  raise XDpzt("Unable to reset service state via local management API %s (code %s): %s"%(url,result.status_code,result.content))
 print("Done.")
def list_pods(args):
 return PodConfigManager.list_pods()
def get_data_dir_from_container()->XDpzv:
 try:
  details=DOCKER_CLIENT.inspect_container(config.MAIN_CONTAINER_NAME)
  mounts=details.get("Mounts")
  env=details.get("Config",{}).get("Env",[])
  data_dir_env=[e for e in env if e.startswith("DATA_DIR=")][0].partition("=")[2]
  try:
   data_dir_host=[m for m in mounts if m["Destination"]==data_dir_env][0]["Source"]
   data_dir_host=re.sub(r"^(/host_mnt)?",r"",data_dir_host)
   data_dir_env=data_dir_host
  except XDpzt:
   LOG.debug(f"No docker volume for data dir '{data_dir_env}' detected")
  return data_dir_env
 except XDpzt:
  LOG.warning('''Unable to determine DATA_DIR from LocalStack Docker container - please make sure $MAIN_CONTAINER_NAME is configured properly''')
def get_persisted_resource_names(data_dir)->List[XDpzv]:
 names=[]
 with os.scandir(data_dir)as entries:
  for entry in entries:
   if entry.is_dir()and entry.name!="api_states":
    names.append(entry.name)
 with os.scandir(os.path.join(data_dir,"api_states"))as entries:
  for entry in entries:
   if entry.is_dir()and XDpzk(os.listdir(entry.path))>0:
    names.append(entry.name)
 LOG.debug(f"Detected state files for the following APIs: {names}")
 return names
# Created by pyminifier (https://github.com/liftoff/pyminifier)
