from localstack.utils.aws import aws_models
UPTHI=super
UPTHF=None
UPTHS=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  UPTHI(LambdaLayer,self).__init__(arn)
  self.cwd=UPTHF
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.UPTHS.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,UPTHS,env=UPTHF):
  UPTHI(RDSDatabase,self).__init__(UPTHS,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,UPTHS,env=UPTHF):
  UPTHI(RDSCluster,self).__init__(UPTHS,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,UPTHS,env=UPTHF):
  UPTHI(AppSyncAPI,self).__init__(UPTHS,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,UPTHS,env=UPTHF):
  UPTHI(AmplifyApp,self).__init__(UPTHS,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,UPTHS,env=UPTHF):
  UPTHI(ElastiCacheCluster,self).__init__(UPTHS,env=env)
class TransferServer(BaseComponent):
 def __init__(self,UPTHS,env=UPTHF):
  UPTHI(TransferServer,self).__init__(UPTHS,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,UPTHS,env=UPTHF):
  UPTHI(CloudFrontDistribution,self).__init__(UPTHS,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,UPTHS,env=UPTHF):
  UPTHI(CodeCommitRepository,self).__init__(UPTHS,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
