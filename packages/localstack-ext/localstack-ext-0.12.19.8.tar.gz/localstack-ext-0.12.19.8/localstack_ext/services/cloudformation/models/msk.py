from localstack.services.cloudformation.service_models import GenericBaseModel
CmSiw=staticmethod
CmSia=None
CmSiY=classmethod
from localstack.utils.aws import aws_stack
class KafkaCluster(GenericBaseModel):
 @CmSiw
 def cloudformation_type():
  return "AWS::MSK::Cluster"
 def get_physical_resource_id(self,attribute=CmSia,**kwargs):
  return self.props.get("ClusterArn")
 def fetch_state(self,stack_name,resources):
  client=aws_stack.connect_to_service("kafka")
  cluster_name=self.resolve_refs_recursively(stack_name,self.props["ClusterName"],resources)
  clusters=client.list_clusters()["ClusterInfoList"]
  clusters=[c for c in clusters if c["ClusterName"]==cluster_name]
  return(clusters or[CmSia])[0]
 @CmSiY
 def get_deploy_templates(cls):
  def _create_params(params,resource_id,resources,**kwargs):
   resource=cls(resources[resource_id])
   props=resource.props
   storage_info=props.get("BrokerNodeGroupInfo",{}).get("StorageInfo",{})
   if "EBSStorageInfo" in storage_info:
    storage_info["EbsStorageInfo"]=storage_info.pop("EBSStorageInfo")
   return{"ClusterArn":resource.props.get("ClusterArn")}
  def _delete_params(params,resource_id,resources,**kwargs):
   resource=cls(resources[resource_id])
   return{"ClusterArn":resource.props.get("ClusterArn")}
  return{"create":{"function":"create_cluster","parameters":_create_params},"delete":{"function":"delete_cluster","parameters":_delete_params}}
# Created by pyminifier (https://github.com/liftoff/pyminifier)
