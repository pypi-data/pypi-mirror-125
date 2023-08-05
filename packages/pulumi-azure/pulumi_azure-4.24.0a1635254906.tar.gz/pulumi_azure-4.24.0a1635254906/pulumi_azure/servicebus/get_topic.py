# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetTopicResult',
    'AwaitableGetTopicResult',
    'get_topic',
    'get_topic_output',
]

@pulumi.output_type
class GetTopicResult:
    """
    A collection of values returned by getTopic.
    """
    def __init__(__self__, auto_delete_on_idle=None, default_message_ttl=None, duplicate_detection_history_time_window=None, enable_batched_operations=None, enable_express=None, enable_partitioning=None, id=None, max_size_in_megabytes=None, name=None, namespace_name=None, requires_duplicate_detection=None, resource_group_name=None, status=None, support_ordering=None):
        if auto_delete_on_idle and not isinstance(auto_delete_on_idle, str):
            raise TypeError("Expected argument 'auto_delete_on_idle' to be a str")
        pulumi.set(__self__, "auto_delete_on_idle", auto_delete_on_idle)
        if default_message_ttl and not isinstance(default_message_ttl, str):
            raise TypeError("Expected argument 'default_message_ttl' to be a str")
        pulumi.set(__self__, "default_message_ttl", default_message_ttl)
        if duplicate_detection_history_time_window and not isinstance(duplicate_detection_history_time_window, str):
            raise TypeError("Expected argument 'duplicate_detection_history_time_window' to be a str")
        pulumi.set(__self__, "duplicate_detection_history_time_window", duplicate_detection_history_time_window)
        if enable_batched_operations and not isinstance(enable_batched_operations, bool):
            raise TypeError("Expected argument 'enable_batched_operations' to be a bool")
        pulumi.set(__self__, "enable_batched_operations", enable_batched_operations)
        if enable_express and not isinstance(enable_express, bool):
            raise TypeError("Expected argument 'enable_express' to be a bool")
        pulumi.set(__self__, "enable_express", enable_express)
        if enable_partitioning and not isinstance(enable_partitioning, bool):
            raise TypeError("Expected argument 'enable_partitioning' to be a bool")
        pulumi.set(__self__, "enable_partitioning", enable_partitioning)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if max_size_in_megabytes and not isinstance(max_size_in_megabytes, int):
            raise TypeError("Expected argument 'max_size_in_megabytes' to be a int")
        pulumi.set(__self__, "max_size_in_megabytes", max_size_in_megabytes)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if namespace_name and not isinstance(namespace_name, str):
            raise TypeError("Expected argument 'namespace_name' to be a str")
        pulumi.set(__self__, "namespace_name", namespace_name)
        if requires_duplicate_detection and not isinstance(requires_duplicate_detection, bool):
            raise TypeError("Expected argument 'requires_duplicate_detection' to be a bool")
        pulumi.set(__self__, "requires_duplicate_detection", requires_duplicate_detection)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if support_ordering and not isinstance(support_ordering, bool):
            raise TypeError("Expected argument 'support_ordering' to be a bool")
        pulumi.set(__self__, "support_ordering", support_ordering)

    @property
    @pulumi.getter(name="autoDeleteOnIdle")
    def auto_delete_on_idle(self) -> str:
        """
        The ISO 8601 timespan duration of the idle interval after which the Topic is automatically deleted, minimum of 5 minutes.
        """
        return pulumi.get(self, "auto_delete_on_idle")

    @property
    @pulumi.getter(name="defaultMessageTtl")
    def default_message_ttl(self) -> str:
        """
        The ISO 8601 timespan duration of TTL of messages sent to this topic if no TTL value is set on the message itself.
        """
        return pulumi.get(self, "default_message_ttl")

    @property
    @pulumi.getter(name="duplicateDetectionHistoryTimeWindow")
    def duplicate_detection_history_time_window(self) -> str:
        """
        The ISO 8601 timespan duration during which duplicates can be detected.
        """
        return pulumi.get(self, "duplicate_detection_history_time_window")

    @property
    @pulumi.getter(name="enableBatchedOperations")
    def enable_batched_operations(self) -> bool:
        """
        Boolean flag which controls if server-side batched operations are enabled.
        """
        return pulumi.get(self, "enable_batched_operations")

    @property
    @pulumi.getter(name="enableExpress")
    def enable_express(self) -> bool:
        """
        Boolean flag which controls whether Express Entities are enabled. An express topic holds a message in memory temporarily before writing it to persistent storage.
        """
        return pulumi.get(self, "enable_express")

    @property
    @pulumi.getter(name="enablePartitioning")
    def enable_partitioning(self) -> bool:
        """
        Boolean flag which controls whether to enable the topic to be partitioned across multiple message brokers.
        """
        return pulumi.get(self, "enable_partitioning")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="maxSizeInMegabytes")
    def max_size_in_megabytes(self) -> int:
        """
        Integer value which controls the size of memory allocated for the topic. For supported values see the "Queue/topic size" section of [this document](https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-quotas).
        """
        return pulumi.get(self, "max_size_in_megabytes")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="namespaceName")
    def namespace_name(self) -> str:
        return pulumi.get(self, "namespace_name")

    @property
    @pulumi.getter(name="requiresDuplicateDetection")
    def requires_duplicate_detection(self) -> bool:
        """
        Boolean flag which controls whether the Topic requires duplicate detection.
        """
        return pulumi.get(self, "requires_duplicate_detection")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        The Status of the Service Bus Topic. Acceptable values are Active or Disabled.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="supportOrdering")
    def support_ordering(self) -> bool:
        """
        Boolean flag which controls whether the Topic supports ordering.
        """
        return pulumi.get(self, "support_ordering")


class AwaitableGetTopicResult(GetTopicResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTopicResult(
            auto_delete_on_idle=self.auto_delete_on_idle,
            default_message_ttl=self.default_message_ttl,
            duplicate_detection_history_time_window=self.duplicate_detection_history_time_window,
            enable_batched_operations=self.enable_batched_operations,
            enable_express=self.enable_express,
            enable_partitioning=self.enable_partitioning,
            id=self.id,
            max_size_in_megabytes=self.max_size_in_megabytes,
            name=self.name,
            namespace_name=self.namespace_name,
            requires_duplicate_detection=self.requires_duplicate_detection,
            resource_group_name=self.resource_group_name,
            status=self.status,
            support_ordering=self.support_ordering)


def get_topic(name: Optional[str] = None,
              namespace_name: Optional[str] = None,
              resource_group_name: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTopicResult:
    """
    Use this data source to access information about an existing Service Bus Topic.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.servicebus.get_topic(name="existing",
        resource_group_name="existing",
        namespace_name="existing")
    pulumi.export("id", example.id)
    ```


    :param str name: The name of this Service Bus Topic.
    :param str namespace_name: The name of the Service Bus Namespace.
    :param str resource_group_name: The name of the Resource Group where the Service Bus Topic exists.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['namespaceName'] = namespace_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:servicebus/getTopic:getTopic', __args__, opts=opts, typ=GetTopicResult).value

    return AwaitableGetTopicResult(
        auto_delete_on_idle=__ret__.auto_delete_on_idle,
        default_message_ttl=__ret__.default_message_ttl,
        duplicate_detection_history_time_window=__ret__.duplicate_detection_history_time_window,
        enable_batched_operations=__ret__.enable_batched_operations,
        enable_express=__ret__.enable_express,
        enable_partitioning=__ret__.enable_partitioning,
        id=__ret__.id,
        max_size_in_megabytes=__ret__.max_size_in_megabytes,
        name=__ret__.name,
        namespace_name=__ret__.namespace_name,
        requires_duplicate_detection=__ret__.requires_duplicate_detection,
        resource_group_name=__ret__.resource_group_name,
        status=__ret__.status,
        support_ordering=__ret__.support_ordering)


@_utilities.lift_output_func(get_topic)
def get_topic_output(name: Optional[pulumi.Input[str]] = None,
                     namespace_name: Optional[pulumi.Input[str]] = None,
                     resource_group_name: Optional[pulumi.Input[str]] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTopicResult]:
    """
    Use this data source to access information about an existing Service Bus Topic.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.servicebus.get_topic(name="existing",
        resource_group_name="existing",
        namespace_name="existing")
    pulumi.export("id", example.id)
    ```


    :param str name: The name of this Service Bus Topic.
    :param str namespace_name: The name of the Service Bus Namespace.
    :param str resource_group_name: The name of the Resource Group where the Service Bus Topic exists.
    """
    ...
