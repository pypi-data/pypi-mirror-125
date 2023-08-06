import logging
AXNqj=True
AXNqp=False
AXNqS=None
AXNqn=Exception
AXNqP=open
AXNqJ=bool
AXNqY=str
AXNqO=int
AXNqQ=dict
AXNqy=list
AXNqf=isinstance
AXNqB=super
import os
import sys
from typing import Any,Callable,Dict,List
import click
from localstack.cli import LocalstackCli,LocalstackCliPlugin,console
class ProCliPlugin(LocalstackCliPlugin):
 name="pro"
 def should_load(self):
  e=os.getenv("LOCALSTACK_API_KEY")
  return AXNqj if e else AXNqp
 def is_active(self):
  return self.should_load()
 def attach(self,cli:LocalstackCli)->AXNqS:
  group:click.Group=cli.group
  group.add_command(cmd_login)
  group.add_command(cmd_logout)
  group.add_command(daemons)
  group.add_command(pod)
  group.add_command(dns)
  group.add_command(cpvcs)
@click.group(name="daemons",help="Manage local daemon processes")
def daemons():
 pass
@click.command(name="login",help="Log in with your account credentials")
@click.option("--username",help="Username for login")
@click.option("--provider",default="internal",help="OAuth provider (default: localstack internal login)")
def cmd_login(username,provider):
 from localstack_ext.bootstrap import auth
 try:
  auth.login(provider,username)
  console.print("successfully logged in")
 except AXNqn as e:
  console.print("authentication error: %s"%e)
@click.command(name="logout",help="Log out and delete any session tokens")
def cmd_logout():
 from localstack_ext.bootstrap import auth
 try:
  auth.logout()
  console.print("successfully logged out")
 except AXNqn as e:
  console.print("logout error: %s"%e)
@daemons.command(name="start",help="Start local daemon processes")
def cmd_daemons_start():
 from localstack_ext.bootstrap import local_daemon
 console.log("Starting local daemons processes ...")
 local_daemon.start_in_background()
@daemons.command(name="stop",help="Stop local daemon processes")
def cmd_daemons_stop():
 from localstack_ext.bootstrap import local_daemon
 console.log("Stopping local daemons processes ...")
 local_daemon.kill_servers()
@daemons.command(name="log",help="Show log of daemon process")
def cmd_daemons_log():
 from localstack_ext.bootstrap import local_daemon
 file_path=local_daemon.get_log_file_path()
 if not os.path.isfile(file_path):
  console.print("no log found")
 else:
  with AXNqP(file_path,"r")as fd:
   for line in fd:
    sys.stdout.write(line)
    sys.stdout.flush()
@click.group(name="dns",help="Manage DNS settings of your host")
def dns():
 pass
@dns.command(name="systemd-resolved",help="Manage DNS settings of systemd-resolved (Ubuntu, Debian etc.)")
@click.option("--revert",is_flag=AXNqj,help="Revert systemd-resolved settings for the docker interface")
def cmd_dns_systemd(revert:AXNqJ):
 import localstack_ext.services.dns_server
 from localstack_ext.bootstrap.dns_utils import configure_systemd
 console.print("Configuring systemd-resolved...")
 logger_name=localstack_ext.services.dns_server.LOG.name
 localstack_ext.services.dns_server.LOG=ConsoleLogger(logger_name)
 configure_systemd(revert)
def _cpvcs_initialized(pod_name:AXNqY)->AXNqJ:
 from localstack_ext.bootstrap.cpvcs.utils.common import config_context
 config_context.set_pod_context(pod_name=pod_name)
 if not config_context.is_initialized():
  console.print("[red]Error:[/red] Could not find local CPVCS instance")
  return AXNqp
 return AXNqj
@click.group(name="cpvcs",help="Experimental Cloud Pods with elaborate versioning mechanism")
def cpvcs():
 pass
@cpvcs.command(name="init",help="Creates a new cloud pod with cpvcs enabled")
@click.option("-n","--name",help="Name of the cloud pod",required=AXNqj)
def cmd_cpvcs_init(name:AXNqY):
 from localstack_ext.bootstrap import pods_client
 from localstack_ext.bootstrap.cpvcs.utils.common import config_context
 if config_context.is_initialized():
  console.print(f"[red]Error:[/red] CPVCS already instanciated for pod {name}")
 else:
  pods_client.init_cpvcs(pod_name=name,pre_config={"backend":"cpvcs"})
  console.print("Successfully created local CPVCS instance!")
@cpvcs.command(name="commit",help="Commits the current expansion point and creates a new (empty) revision")
@click.option("-m","--message",help="Add a comment describing the revision")
@click.option("-n","--name",help="Name of the cloud pod",required=AXNqj)
def cmd_cpvcs_commit(message:AXNqY,name:AXNqY):
 from localstack_ext.bootstrap import pods_client
 if _cpvcs_initialized(pod_name=name):
  pods_client.commit_state(pod_name=name,pre_config={"backend":"cpvcs"},message=message)
  console.print("Successfully commited the current state")
@cpvcs.command(name="push",help="Creates a new version by using the state files in the current expansion point (latest commit)")
@click.option("--squash",is_flag=AXNqj,help="Squashes commits together, so only the latest commit is stored in the revision graph")
@click.option("-m","--message",help="Add a comment describing the version")
@click.option("-n","--name",help="Name of the cloud pod",required=AXNqj)
def cmd_cpvcs_push(squash:AXNqJ,message:AXNqY,name:AXNqY):
 from localstack_ext.bootstrap import pods_client
 if _cpvcs_initialized(pod_name=name):
  pods_client.push_state(pod_name=name,pre_config={"backend":"cpvcs"},squash_commits=squash,comment=message)
  console.print("Successfully pushed the current state")
@cpvcs.command(name="inject",help="Injects the state from a version into the application runtime")
@click.option("--version",default="-1",type=AXNqO,help="Loads the state of the specified version - Most recent one by default")
@click.option("--reset",is_flag=AXNqj,default=AXNqp,help="Will reset the application state before injecting")
@click.option("-n","--name",help="Name of the cloud pod",required=AXNqj)
def cmd_cpvcs_inject(version:AXNqO,reset:AXNqJ,name:AXNqY):
 from localstack_ext.bootstrap import pods_client
 if _cpvcs_initialized(pod_name=name):
  pods_client.inject_state(pod_name=name,version=version,reset_state=reset,pre_config={"backend":"cpvcs"})
@cpvcs.command(name="versions",help="Lists all available version numbers")
@click.option("-n","--name",help="Name of the cloud pod",required=AXNqj)
def cmd_cpvcs_versions(name:AXNqY):
 if _cpvcs_initialized(pod_name=name):
  from localstack_ext.bootstrap import pods_client
  version_list=pods_client.list_versions(pod_name=name,pre_config={"backend":"cpvcs"})
  result="\n".join(version_list)
  console.print(result)
@cpvcs.command(name="version-info")
@click.option("--version",required=AXNqj,type=AXNqO)
@click.option("-n","--name",help="Name of the cloud pod",required=AXNqj)
def cmd_cpvcs_version_info(version:AXNqO,name:AXNqY):
 if _cpvcs_initialized(pod_name=name):
  from localstack_ext.bootstrap import pods_client
  info=pods_client.get_version_info(version=version,pod_name=name,pre_config={"backend":"cpvcs"})
  console.print(info)
@cpvcs.command(name="set-version",help="Set HEAD to a specific version")
@click.option("--version",required=AXNqj,type=AXNqO,help="The version the state should be set to")
@click.option("--inject",is_flag=AXNqj,help="Whether the state should be directly injected into the application runtime after changing version")
@click.option("--reset/--no-reset",default=AXNqj,help="Whether the current application state should be reset before changing version")
@click.option("--commit-before",is_flag=AXNqj,help="Whether the current application state should be commited to the currently selected version before changing version")
@click.option("-n","--name",help="Name of the cloud pod",required=AXNqj)
def cmd_cpvcs_set_version(version:AXNqO,inject:AXNqJ,reset:AXNqJ,commit_before:AXNqJ,name:AXNqY):
 if _cpvcs_initialized(pod_name=name):
  from localstack_ext.bootstrap import pods_client
  pods_client.set_version(version=version,inject_version_state=inject,reset_state=reset,commit_before=commit_before,pod_name=name,pre_config={"backend":"cpvcs"})
@cpvcs.command(name="commits",help="Shows the commit history of a version")
@click.option("--version","-v",default=-1)
@click.option("-n","--name",help="Name of the cloud pod",required=AXNqj)
def cmd_cpvcs_commits(version:AXNqO,name:AXNqY):
 if _cpvcs_initialized(pod_name=name):
  from localstack_ext.bootstrap import pods_client
  commits=pods_client.list_version_commits(version=version,pod_name=name,pre_config={"backend":"cpvcs"})
  result="\n".join(commits)
  console.print(result)
@cpvcs.command(name="commit-diff",help="Shows the changes made by a commit")
@click.option("--version","-v",required=AXNqj)
@click.option("--commit","-c",required=AXNqj)
@click.option("-n","--name",help="Name of the cloud pod",required=AXNqj)
def cmd_cpvcs_commit_diff(version:AXNqO,commit:AXNqO,name:AXNqY):
 if _cpvcs_initialized(pod_name=name):
  from localstack_ext.bootstrap import pods_client
  commit_diff=pods_client.get_commit_diff(version=version,commit=commit,pod_name=name,pre_config={"backend":"cpvcs"})
  if commit_diff:
   console.print_json(commit_diff)
  else:
   console.print(f"[red]Error:[/red] Commit {commit} not found for version {version}")
@click.group(name="pod",help="Manage state of local cloud pods")
def pod():
 from localstack_ext.bootstrap.licensing import is_logged_in
 if not is_logged_in():
  console.print("[red]Error:[/red] not logged in, please log in first")
  sys.exit(1)
@pod.command(name="list",help="Get a list of available local cloud pods")
def cmd_pod_list():
 status=console.status("Fetching list of pods from server ...")
 status.start()
 from localstack import config
 from localstack.utils.common import format_bytes
 from localstack_ext.bootstrap import pods_client
 try:
  result=pods_client.list_pods(AXNqS)
  status.stop()
  columns={"pod_name":"Name","backend":"Backend","url":"URL","size":"Size","state":"State"}
  print_table(columns,result,formatters={"size":format_bytes})
 except AXNqn as e:
  status.stop()
  if config.DEBUG:
   console.print_exception()
  else:
   console.print("[red]Error:[/red]",e)
@pod.command(name="create",help="Create a new local cloud pod")
def cmd_pod_create():
 msg="Please head over to https://app.localstack.cloud to create a new cloud pod. (CLI support is coming soon)"
 console.print(msg)
@pod.command(name="push",help="Push the state of the LocalStack instance to a cloud pod")
@click.argument("name")
def cmd_pod_push(name:AXNqY):
 from localstack_ext.bootstrap import pods_client
 pods_client.push_state(name)
@pod.command(name="pull",help="Pull the state of a cloud pod into the running LocalStack instance")
@click.argument("name")
def cmd_pod_pull(name:AXNqY):
 from localstack_ext.bootstrap import pods_client
 pods_client.pull_state(name)
@pod.command(name="reset",help="Reset the local state to get a fresh LocalStack instance")
def cmd_pod_reset():
 from localstack_ext.bootstrap import pods_client
 pods_client.reset_local_state()
def print_table(columns:Dict[AXNqY,AXNqY],rows:List[Dict[AXNqY,Any]],formatters:Dict[AXNqY,Callable[[Any],AXNqY]]=AXNqS):
 from rich.table import Table
 if formatters is AXNqS:
  formatters=AXNqQ()
 t=Table()
 for k,name in columns.items():
  t.add_column(name)
 for row in rows:
  cells=AXNqy()
  for c in columns.keys():
   cell=row.get(c)
   if c in formatters:
    cell=formatters[c](cell)
   if cell is AXNqS:
    cell=""
   if not AXNqf(cell,AXNqY):
    cell=AXNqY(cell)
   cells.append(cell)
  t.add_row(*cells)
 console.print(t)
class ConsoleLogger(logging.Logger):
 def __init__(self,name):
  AXNqB(ConsoleLogger,self).__init__(name)
 def info(self,msg:Any,*args:Any,**kwargs:Any)->AXNqS:
  console.print(msg%args)
 def warning(self,msg:Any,*args:Any,**kwargs:Any)->AXNqS:
  console.print("[red]Warning:[/red] ",msg%args)
 def error(self,msg:Any,*args:Any,**kwargs:Any)->AXNqS:
  console.print("[red]Error:[/red] ",msg%args)
 def exception(self,msg:Any,*args:Any,**kwargs:Any)->AXNqS:
  console.print("[red]Error:[/red] ",msg%args)
  console.print_exception()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
