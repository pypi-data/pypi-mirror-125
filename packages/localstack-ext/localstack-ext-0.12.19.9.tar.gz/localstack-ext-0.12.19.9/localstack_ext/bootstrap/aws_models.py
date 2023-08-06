from localstack.utils.aws import aws_models
HtKzp=super
HtKzY=None
HtKzq=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  HtKzp(LambdaLayer,self).__init__(arn)
  self.cwd=HtKzY
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.HtKzq.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,HtKzq,env=HtKzY):
  HtKzp(RDSDatabase,self).__init__(HtKzq,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,HtKzq,env=HtKzY):
  HtKzp(RDSCluster,self).__init__(HtKzq,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,HtKzq,env=HtKzY):
  HtKzp(AppSyncAPI,self).__init__(HtKzq,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,HtKzq,env=HtKzY):
  HtKzp(AmplifyApp,self).__init__(HtKzq,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,HtKzq,env=HtKzY):
  HtKzp(ElastiCacheCluster,self).__init__(HtKzq,env=env)
class TransferServer(BaseComponent):
 def __init__(self,HtKzq,env=HtKzY):
  HtKzp(TransferServer,self).__init__(HtKzq,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,HtKzq,env=HtKzY):
  HtKzp(CloudFrontDistribution,self).__init__(HtKzq,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,HtKzq,env=HtKzY):
  HtKzp(CodeCommitRepository,self).__init__(HtKzq,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
