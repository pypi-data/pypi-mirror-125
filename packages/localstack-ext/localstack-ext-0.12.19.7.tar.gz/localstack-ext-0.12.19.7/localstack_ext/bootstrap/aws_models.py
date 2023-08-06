from localstack.utils.aws import aws_models
OmDVz=super
OmDVk=None
OmDVQ=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  OmDVz(LambdaLayer,self).__init__(arn)
  self.cwd=OmDVk
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.OmDVQ.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,OmDVQ,env=OmDVk):
  OmDVz(RDSDatabase,self).__init__(OmDVQ,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,OmDVQ,env=OmDVk):
  OmDVz(RDSCluster,self).__init__(OmDVQ,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,OmDVQ,env=OmDVk):
  OmDVz(AppSyncAPI,self).__init__(OmDVQ,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,OmDVQ,env=OmDVk):
  OmDVz(AmplifyApp,self).__init__(OmDVQ,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,OmDVQ,env=OmDVk):
  OmDVz(ElastiCacheCluster,self).__init__(OmDVQ,env=env)
class TransferServer(BaseComponent):
 def __init__(self,OmDVQ,env=OmDVk):
  OmDVz(TransferServer,self).__init__(OmDVQ,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,OmDVQ,env=OmDVk):
  OmDVz(CloudFrontDistribution,self).__init__(OmDVQ,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,OmDVQ,env=OmDVk):
  OmDVz(CodeCommitRepository,self).__init__(OmDVQ,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
