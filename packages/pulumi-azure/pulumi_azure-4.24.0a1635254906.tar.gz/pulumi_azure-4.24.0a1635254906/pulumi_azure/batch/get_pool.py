# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = [
    'GetPoolResult',
    'AwaitableGetPoolResult',
    'get_pool',
    'get_pool_output',
]

@pulumi.output_type
class GetPoolResult:
    """
    A collection of values returned by getPool.
    """
    def __init__(__self__, account_name=None, auto_scales=None, certificates=None, container_configurations=None, display_name=None, fixed_scales=None, id=None, max_tasks_per_node=None, metadata=None, name=None, network_configuration=None, node_agent_sku_id=None, resource_group_name=None, start_task=None, storage_image_references=None, vm_size=None):
        if account_name and not isinstance(account_name, str):
            raise TypeError("Expected argument 'account_name' to be a str")
        pulumi.set(__self__, "account_name", account_name)
        if auto_scales and not isinstance(auto_scales, list):
            raise TypeError("Expected argument 'auto_scales' to be a list")
        pulumi.set(__self__, "auto_scales", auto_scales)
        if certificates and not isinstance(certificates, list):
            raise TypeError("Expected argument 'certificates' to be a list")
        pulumi.set(__self__, "certificates", certificates)
        if container_configurations and not isinstance(container_configurations, list):
            raise TypeError("Expected argument 'container_configurations' to be a list")
        pulumi.set(__self__, "container_configurations", container_configurations)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if fixed_scales and not isinstance(fixed_scales, list):
            raise TypeError("Expected argument 'fixed_scales' to be a list")
        pulumi.set(__self__, "fixed_scales", fixed_scales)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if max_tasks_per_node and not isinstance(max_tasks_per_node, int):
            raise TypeError("Expected argument 'max_tasks_per_node' to be a int")
        pulumi.set(__self__, "max_tasks_per_node", max_tasks_per_node)
        if metadata and not isinstance(metadata, dict):
            raise TypeError("Expected argument 'metadata' to be a dict")
        pulumi.set(__self__, "metadata", metadata)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if network_configuration and not isinstance(network_configuration, dict):
            raise TypeError("Expected argument 'network_configuration' to be a dict")
        pulumi.set(__self__, "network_configuration", network_configuration)
        if node_agent_sku_id and not isinstance(node_agent_sku_id, str):
            raise TypeError("Expected argument 'node_agent_sku_id' to be a str")
        pulumi.set(__self__, "node_agent_sku_id", node_agent_sku_id)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if start_task and not isinstance(start_task, dict):
            raise TypeError("Expected argument 'start_task' to be a dict")
        pulumi.set(__self__, "start_task", start_task)
        if storage_image_references and not isinstance(storage_image_references, list):
            raise TypeError("Expected argument 'storage_image_references' to be a list")
        pulumi.set(__self__, "storage_image_references", storage_image_references)
        if vm_size and not isinstance(vm_size, str):
            raise TypeError("Expected argument 'vm_size' to be a str")
        pulumi.set(__self__, "vm_size", vm_size)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> str:
        """
        The name of the Batch account.
        """
        return pulumi.get(self, "account_name")

    @property
    @pulumi.getter(name="autoScales")
    def auto_scales(self) -> Sequence['outputs.GetPoolAutoScaleResult']:
        """
        A `auto_scale` block that describes the scale settings when using auto scale.
        """
        return pulumi.get(self, "auto_scales")

    @property
    @pulumi.getter
    def certificates(self) -> Optional[Sequence['outputs.GetPoolCertificateResult']]:
        """
        One or more `certificate` blocks that describe the certificates installed on each compute node in the pool.
        """
        return pulumi.get(self, "certificates")

    @property
    @pulumi.getter(name="containerConfigurations")
    def container_configurations(self) -> Sequence['outputs.GetPoolContainerConfigurationResult']:
        """
        The container configuration used in the pool's VMs.
        """
        return pulumi.get(self, "container_configurations")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="fixedScales")
    def fixed_scales(self) -> Sequence['outputs.GetPoolFixedScaleResult']:
        """
        A `fixed_scale` block that describes the scale settings when using fixed scale.
        """
        return pulumi.get(self, "fixed_scales")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="maxTasksPerNode")
    def max_tasks_per_node(self) -> int:
        """
        The maximum number of tasks that can run concurrently on a single compute node in the pool.
        """
        return pulumi.get(self, "max_tasks_per_node")

    @property
    @pulumi.getter
    def metadata(self) -> Mapping[str, str]:
        return pulumi.get(self, "metadata")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the endpoint.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkConfiguration")
    def network_configuration(self) -> 'outputs.GetPoolNetworkConfigurationResult':
        return pulumi.get(self, "network_configuration")

    @property
    @pulumi.getter(name="nodeAgentSkuId")
    def node_agent_sku_id(self) -> str:
        """
        The Sku of the node agents in the Batch pool.
        """
        return pulumi.get(self, "node_agent_sku_id")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="startTask")
    def start_task(self) -> Optional['outputs.GetPoolStartTaskResult']:
        """
        A `start_task` block that describes the start task settings for the Batch pool.
        """
        return pulumi.get(self, "start_task")

    @property
    @pulumi.getter(name="storageImageReferences")
    def storage_image_references(self) -> Sequence['outputs.GetPoolStorageImageReferenceResult']:
        """
        The reference of the storage image used by the nodes in the Batch pool.
        """
        return pulumi.get(self, "storage_image_references")

    @property
    @pulumi.getter(name="vmSize")
    def vm_size(self) -> str:
        """
        The size of the VM created in the Batch pool.
        """
        return pulumi.get(self, "vm_size")


class AwaitableGetPoolResult(GetPoolResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPoolResult(
            account_name=self.account_name,
            auto_scales=self.auto_scales,
            certificates=self.certificates,
            container_configurations=self.container_configurations,
            display_name=self.display_name,
            fixed_scales=self.fixed_scales,
            id=self.id,
            max_tasks_per_node=self.max_tasks_per_node,
            metadata=self.metadata,
            name=self.name,
            network_configuration=self.network_configuration,
            node_agent_sku_id=self.node_agent_sku_id,
            resource_group_name=self.resource_group_name,
            start_task=self.start_task,
            storage_image_references=self.storage_image_references,
            vm_size=self.vm_size)


def get_pool(account_name: Optional[str] = None,
             certificates: Optional[Sequence[pulumi.InputType['GetPoolCertificateArgs']]] = None,
             name: Optional[str] = None,
             resource_group_name: Optional[str] = None,
             start_task: Optional[pulumi.InputType['GetPoolStartTaskArgs']] = None,
             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPoolResult:
    """
    Use this data source to access information about an existing Batch pool

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.batch.get_pool(account_name="testbatchaccount",
        name="testbatchpool",
        resource_group_name="test")
    ```


    :param str account_name: The name of the Batch account.
    :param Sequence[pulumi.InputType['GetPoolCertificateArgs']] certificates: One or more `certificate` blocks that describe the certificates installed on each compute node in the pool.
    :param str name: The name of the endpoint.
    :param pulumi.InputType['GetPoolStartTaskArgs'] start_task: A `start_task` block that describes the start task settings for the Batch pool.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['certificates'] = certificates
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    __args__['startTask'] = start_task
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:batch/getPool:getPool', __args__, opts=opts, typ=GetPoolResult).value

    return AwaitableGetPoolResult(
        account_name=__ret__.account_name,
        auto_scales=__ret__.auto_scales,
        certificates=__ret__.certificates,
        container_configurations=__ret__.container_configurations,
        display_name=__ret__.display_name,
        fixed_scales=__ret__.fixed_scales,
        id=__ret__.id,
        max_tasks_per_node=__ret__.max_tasks_per_node,
        metadata=__ret__.metadata,
        name=__ret__.name,
        network_configuration=__ret__.network_configuration,
        node_agent_sku_id=__ret__.node_agent_sku_id,
        resource_group_name=__ret__.resource_group_name,
        start_task=__ret__.start_task,
        storage_image_references=__ret__.storage_image_references,
        vm_size=__ret__.vm_size)


@_utilities.lift_output_func(get_pool)
def get_pool_output(account_name: Optional[pulumi.Input[str]] = None,
                    certificates: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetPoolCertificateArgs']]]]] = None,
                    name: Optional[pulumi.Input[str]] = None,
                    resource_group_name: Optional[pulumi.Input[str]] = None,
                    start_task: Optional[pulumi.Input[Optional[pulumi.InputType['GetPoolStartTaskArgs']]]] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetPoolResult]:
    """
    Use this data source to access information about an existing Batch pool

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.batch.get_pool(account_name="testbatchaccount",
        name="testbatchpool",
        resource_group_name="test")
    ```


    :param str account_name: The name of the Batch account.
    :param Sequence[pulumi.InputType['GetPoolCertificateArgs']] certificates: One or more `certificate` blocks that describe the certificates installed on each compute node in the pool.
    :param str name: The name of the endpoint.
    :param pulumi.InputType['GetPoolStartTaskArgs'] start_task: A `start_task` block that describes the start task settings for the Batch pool.
    """
    ...
