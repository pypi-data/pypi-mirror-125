# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['SnapshotArgs', 'Snapshot']

@pulumi.input_type
class SnapshotArgs:
    def __init__(__self__, *,
                 account_name: pulumi.Input[str],
                 pool_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 volume_name: pulumi.Input[str],
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Snapshot resource.
        :param pulumi.Input[str] account_name: The name of the NetApp account in which the NetApp Pool should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] pool_name: The name of the NetApp pool in which the NetApp Volume should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group where the NetApp Snapshot should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] volume_name: The name of the NetApp volume in which the NetApp Snapshot should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name of the NetApp Snapshot. Changing this forces a new resource to be created.
        """
        pulumi.set(__self__, "account_name", account_name)
        pulumi.set(__self__, "pool_name", pool_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "volume_name", volume_name)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            warnings.warn("""This property as been deprecated as the API no longer supports tags and will be removed in version 3.0 of the provider.""", DeprecationWarning)
            pulumi.log.warn("""tags is deprecated: This property as been deprecated as the API no longer supports tags and will be removed in version 3.0 of the provider.""")
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> pulumi.Input[str]:
        """
        The name of the NetApp account in which the NetApp Pool should be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "account_name")

    @account_name.setter
    def account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "account_name", value)

    @property
    @pulumi.getter(name="poolName")
    def pool_name(self) -> pulumi.Input[str]:
        """
        The name of the NetApp pool in which the NetApp Volume should be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "pool_name")

    @pool_name.setter
    def pool_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "pool_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group where the NetApp Snapshot should be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="volumeName")
    def volume_name(self) -> pulumi.Input[str]:
        """
        The name of the NetApp volume in which the NetApp Snapshot should be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "volume_name")

    @volume_name.setter
    def volume_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "volume_name", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the NetApp Snapshot. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _SnapshotState:
    def __init__(__self__, *,
                 account_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 pool_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 volume_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Snapshot resources.
        :param pulumi.Input[str] account_name: The name of the NetApp account in which the NetApp Pool should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name of the NetApp Snapshot. Changing this forces a new resource to be created.
        :param pulumi.Input[str] pool_name: The name of the NetApp pool in which the NetApp Volume should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group where the NetApp Snapshot should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] volume_name: The name of the NetApp volume in which the NetApp Snapshot should be created. Changing this forces a new resource to be created.
        """
        if account_name is not None:
            pulumi.set(__self__, "account_name", account_name)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if pool_name is not None:
            pulumi.set(__self__, "pool_name", pool_name)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if tags is not None:
            warnings.warn("""This property as been deprecated as the API no longer supports tags and will be removed in version 3.0 of the provider.""", DeprecationWarning)
            pulumi.log.warn("""tags is deprecated: This property as been deprecated as the API no longer supports tags and will be removed in version 3.0 of the provider.""")
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if volume_name is not None:
            pulumi.set(__self__, "volume_name", volume_name)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the NetApp account in which the NetApp Pool should be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "account_name")

    @account_name.setter
    def account_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_name", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the NetApp Snapshot. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="poolName")
    def pool_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the NetApp pool in which the NetApp Volume should be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "pool_name")

    @pool_name.setter
    def pool_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pool_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource group where the NetApp Snapshot should be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="volumeName")
    def volume_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the NetApp volume in which the NetApp Snapshot should be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "volume_name")

    @volume_name.setter
    def volume_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "volume_name", value)


class Snapshot(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 pool_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 volume_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a NetApp Snapshot.

        ## NetApp Snapshot Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_virtual_network = azure.network.VirtualNetwork("exampleVirtualNetwork",
            address_spaces=["10.0.0.0/16"],
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name)
        example_subnet = azure.network.Subnet("exampleSubnet",
            resource_group_name=example_resource_group.name,
            virtual_network_name=example_virtual_network.name,
            address_prefixes=["10.0.2.0/24"],
            delegations=[azure.network.SubnetDelegationArgs(
                name="netapp",
                service_delegation=azure.network.SubnetDelegationServiceDelegationArgs(
                    name="Microsoft.Netapp/volumes",
                    actions=[
                        "Microsoft.Network/networkinterfaces/*",
                        "Microsoft.Network/virtualNetworks/subnets/join/action",
                    ],
                ),
            )])
        example_account = azure.netapp.Account("exampleAccount",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name)
        example_pool = azure.netapp.Pool("examplePool",
            account_name=example_account.name,
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            service_level="Premium",
            size_in_tb=4)
        example_volume = azure.netapp.Volume("exampleVolume",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            account_name=example_account.name,
            pool_name=example_pool.name,
            volume_path="my-unique-file-path",
            service_level="Premium",
            subnet_id=azurerm_subnet["test"]["id"],
            storage_quota_in_gb=100)
        example_snapshot = azure.netapp.Snapshot("exampleSnapshot",
            account_name=example_account.name,
            pool_name=example_pool.name,
            volume_name=example_volume.name,
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name)
        ```

        ## Import

        NetApp Snapshot can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:netapp/snapshot:Snapshot example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.NetApp/netAppAccounts/account1/capacityPools/pool1/volumes/volume1/snapshots/snapshot1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The name of the NetApp account in which the NetApp Pool should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name of the NetApp Snapshot. Changing this forces a new resource to be created.
        :param pulumi.Input[str] pool_name: The name of the NetApp pool in which the NetApp Volume should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group where the NetApp Snapshot should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] volume_name: The name of the NetApp volume in which the NetApp Snapshot should be created. Changing this forces a new resource to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SnapshotArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a NetApp Snapshot.

        ## NetApp Snapshot Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_virtual_network = azure.network.VirtualNetwork("exampleVirtualNetwork",
            address_spaces=["10.0.0.0/16"],
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name)
        example_subnet = azure.network.Subnet("exampleSubnet",
            resource_group_name=example_resource_group.name,
            virtual_network_name=example_virtual_network.name,
            address_prefixes=["10.0.2.0/24"],
            delegations=[azure.network.SubnetDelegationArgs(
                name="netapp",
                service_delegation=azure.network.SubnetDelegationServiceDelegationArgs(
                    name="Microsoft.Netapp/volumes",
                    actions=[
                        "Microsoft.Network/networkinterfaces/*",
                        "Microsoft.Network/virtualNetworks/subnets/join/action",
                    ],
                ),
            )])
        example_account = azure.netapp.Account("exampleAccount",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name)
        example_pool = azure.netapp.Pool("examplePool",
            account_name=example_account.name,
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            service_level="Premium",
            size_in_tb=4)
        example_volume = azure.netapp.Volume("exampleVolume",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            account_name=example_account.name,
            pool_name=example_pool.name,
            volume_path="my-unique-file-path",
            service_level="Premium",
            subnet_id=azurerm_subnet["test"]["id"],
            storage_quota_in_gb=100)
        example_snapshot = azure.netapp.Snapshot("exampleSnapshot",
            account_name=example_account.name,
            pool_name=example_pool.name,
            volume_name=example_volume.name,
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name)
        ```

        ## Import

        NetApp Snapshot can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:netapp/snapshot:Snapshot example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.NetApp/netAppAccounts/account1/capacityPools/pool1/volumes/volume1/snapshots/snapshot1
        ```

        :param str resource_name: The name of the resource.
        :param SnapshotArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SnapshotArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 pool_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 volume_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SnapshotArgs.__new__(SnapshotArgs)

            if account_name is None and not opts.urn:
                raise TypeError("Missing required property 'account_name'")
            __props__.__dict__["account_name"] = account_name
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            if pool_name is None and not opts.urn:
                raise TypeError("Missing required property 'pool_name'")
            __props__.__dict__["pool_name"] = pool_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if tags is not None and not opts.urn:
                warnings.warn("""This property as been deprecated as the API no longer supports tags and will be removed in version 3.0 of the provider.""", DeprecationWarning)
                pulumi.log.warn("""tags is deprecated: This property as been deprecated as the API no longer supports tags and will be removed in version 3.0 of the provider.""")
            __props__.__dict__["tags"] = tags
            if volume_name is None and not opts.urn:
                raise TypeError("Missing required property 'volume_name'")
            __props__.__dict__["volume_name"] = volume_name
        super(Snapshot, __self__).__init__(
            'azure:netapp/snapshot:Snapshot',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            account_name: Optional[pulumi.Input[str]] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            pool_name: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            volume_name: Optional[pulumi.Input[str]] = None) -> 'Snapshot':
        """
        Get an existing Snapshot resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The name of the NetApp account in which the NetApp Pool should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name of the NetApp Snapshot. Changing this forces a new resource to be created.
        :param pulumi.Input[str] pool_name: The name of the NetApp pool in which the NetApp Volume should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group where the NetApp Snapshot should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] volume_name: The name of the NetApp volume in which the NetApp Snapshot should be created. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SnapshotState.__new__(_SnapshotState)

        __props__.__dict__["account_name"] = account_name
        __props__.__dict__["location"] = location
        __props__.__dict__["name"] = name
        __props__.__dict__["pool_name"] = pool_name
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["tags"] = tags
        __props__.__dict__["volume_name"] = volume_name
        return Snapshot(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> pulumi.Output[str]:
        """
        The name of the NetApp account in which the NetApp Pool should be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "account_name")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the NetApp Snapshot. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="poolName")
    def pool_name(self) -> pulumi.Output[str]:
        """
        The name of the NetApp pool in which the NetApp Volume should be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "pool_name")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the resource group where the NetApp Snapshot should be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="volumeName")
    def volume_name(self) -> pulumi.Output[str]:
        """
        The name of the NetApp volume in which the NetApp Snapshot should be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "volume_name")

