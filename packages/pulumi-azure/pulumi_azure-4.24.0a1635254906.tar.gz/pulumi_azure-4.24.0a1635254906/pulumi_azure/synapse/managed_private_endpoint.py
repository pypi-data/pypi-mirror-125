# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ManagedPrivateEndpointArgs', 'ManagedPrivateEndpoint']

@pulumi.input_type
class ManagedPrivateEndpointArgs:
    def __init__(__self__, *,
                 subresource_name: pulumi.Input[str],
                 synapse_workspace_id: pulumi.Input[str],
                 target_resource_id: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ManagedPrivateEndpoint resource.
        :param pulumi.Input[str] subresource_name: Specifies the sub resource name which the Synapse Private Endpoint is able to connect to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] synapse_workspace_id: The ID of the Synapse Workspace on which to create the Managed Private Endpoint. Changing this forces a new resource to be created.
        :param pulumi.Input[str] target_resource_id: The ID of the Private Link Enabled Remote Resource which this Synapse Private Endpoint should be connected to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name which should be used for this Managed Private Endpoint. Changing this forces a new resource to be created.
        """
        pulumi.set(__self__, "subresource_name", subresource_name)
        pulumi.set(__self__, "synapse_workspace_id", synapse_workspace_id)
        pulumi.set(__self__, "target_resource_id", target_resource_id)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="subresourceName")
    def subresource_name(self) -> pulumi.Input[str]:
        """
        Specifies the sub resource name which the Synapse Private Endpoint is able to connect to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "subresource_name")

    @subresource_name.setter
    def subresource_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "subresource_name", value)

    @property
    @pulumi.getter(name="synapseWorkspaceId")
    def synapse_workspace_id(self) -> pulumi.Input[str]:
        """
        The ID of the Synapse Workspace on which to create the Managed Private Endpoint. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "synapse_workspace_id")

    @synapse_workspace_id.setter
    def synapse_workspace_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "synapse_workspace_id", value)

    @property
    @pulumi.getter(name="targetResourceId")
    def target_resource_id(self) -> pulumi.Input[str]:
        """
        The ID of the Private Link Enabled Remote Resource which this Synapse Private Endpoint should be connected to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "target_resource_id")

    @target_resource_id.setter
    def target_resource_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "target_resource_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name which should be used for this Managed Private Endpoint. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _ManagedPrivateEndpointState:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 subresource_name: Optional[pulumi.Input[str]] = None,
                 synapse_workspace_id: Optional[pulumi.Input[str]] = None,
                 target_resource_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ManagedPrivateEndpoint resources.
        :param pulumi.Input[str] name: Specifies the name which should be used for this Managed Private Endpoint. Changing this forces a new resource to be created.
        :param pulumi.Input[str] subresource_name: Specifies the sub resource name which the Synapse Private Endpoint is able to connect to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] synapse_workspace_id: The ID of the Synapse Workspace on which to create the Managed Private Endpoint. Changing this forces a new resource to be created.
        :param pulumi.Input[str] target_resource_id: The ID of the Private Link Enabled Remote Resource which this Synapse Private Endpoint should be connected to. Changing this forces a new resource to be created.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if subresource_name is not None:
            pulumi.set(__self__, "subresource_name", subresource_name)
        if synapse_workspace_id is not None:
            pulumi.set(__self__, "synapse_workspace_id", synapse_workspace_id)
        if target_resource_id is not None:
            pulumi.set(__self__, "target_resource_id", target_resource_id)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name which should be used for this Managed Private Endpoint. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="subresourceName")
    def subresource_name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the sub resource name which the Synapse Private Endpoint is able to connect to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "subresource_name")

    @subresource_name.setter
    def subresource_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subresource_name", value)

    @property
    @pulumi.getter(name="synapseWorkspaceId")
    def synapse_workspace_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Synapse Workspace on which to create the Managed Private Endpoint. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "synapse_workspace_id")

    @synapse_workspace_id.setter
    def synapse_workspace_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "synapse_workspace_id", value)

    @property
    @pulumi.getter(name="targetResourceId")
    def target_resource_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Private Link Enabled Remote Resource which this Synapse Private Endpoint should be connected to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "target_resource_id")

    @target_resource_id.setter
    def target_resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target_resource_id", value)


class ManagedPrivateEndpoint(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 subresource_name: Optional[pulumi.Input[str]] = None,
                 synapse_workspace_id: Optional[pulumi.Input[str]] = None,
                 target_resource_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Allows you to Manages a Synapse Managed Private Endpoint.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_account = azure.storage.Account("exampleAccount",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            account_tier="Standard",
            account_replication_type="LRS",
            account_kind="StorageV2",
            is_hns_enabled=True)
        example_data_lake_gen2_filesystem = azure.storage.DataLakeGen2Filesystem("exampleDataLakeGen2Filesystem", storage_account_id=example_account.id)
        example_workspace = azure.synapse.Workspace("exampleWorkspace",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            storage_data_lake_gen2_filesystem_id=example_data_lake_gen2_filesystem.id,
            sql_administrator_login="sqladminuser",
            sql_administrator_login_password="H@Sh1CoR3!",
            managed_virtual_network_enabled=True)
        example_firewall_rule = azure.synapse.FirewallRule("exampleFirewallRule",
            synapse_workspace_id=azurerm_synapse_workspace["test"]["id"],
            start_ip_address="0.0.0.0",
            end_ip_address="255.255.255.255")
        example_connect = azure.storage.Account("exampleConnect",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            account_tier="Standard",
            account_replication_type="LRS",
            account_kind="BlobStorage")
        example_managed_private_endpoint = azure.synapse.ManagedPrivateEndpoint("exampleManagedPrivateEndpoint",
            synapse_workspace_id=example_workspace.id,
            target_resource_id=example_connect.id,
            subresource_name="blob",
            opts=pulumi.ResourceOptions(depends_on=[example_firewall_rule]))
        ```

        ## Import

        Synapse Managed Private Endpoint can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:synapse/managedPrivateEndpoint:ManagedPrivateEndpoint example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Synapse/workspaces/workspace1/managedVirtualNetworks/default/managedPrivateEndpoints/endpoint1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: Specifies the name which should be used for this Managed Private Endpoint. Changing this forces a new resource to be created.
        :param pulumi.Input[str] subresource_name: Specifies the sub resource name which the Synapse Private Endpoint is able to connect to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] synapse_workspace_id: The ID of the Synapse Workspace on which to create the Managed Private Endpoint. Changing this forces a new resource to be created.
        :param pulumi.Input[str] target_resource_id: The ID of the Private Link Enabled Remote Resource which this Synapse Private Endpoint should be connected to. Changing this forces a new resource to be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ManagedPrivateEndpointArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Allows you to Manages a Synapse Managed Private Endpoint.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_account = azure.storage.Account("exampleAccount",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            account_tier="Standard",
            account_replication_type="LRS",
            account_kind="StorageV2",
            is_hns_enabled=True)
        example_data_lake_gen2_filesystem = azure.storage.DataLakeGen2Filesystem("exampleDataLakeGen2Filesystem", storage_account_id=example_account.id)
        example_workspace = azure.synapse.Workspace("exampleWorkspace",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            storage_data_lake_gen2_filesystem_id=example_data_lake_gen2_filesystem.id,
            sql_administrator_login="sqladminuser",
            sql_administrator_login_password="H@Sh1CoR3!",
            managed_virtual_network_enabled=True)
        example_firewall_rule = azure.synapse.FirewallRule("exampleFirewallRule",
            synapse_workspace_id=azurerm_synapse_workspace["test"]["id"],
            start_ip_address="0.0.0.0",
            end_ip_address="255.255.255.255")
        example_connect = azure.storage.Account("exampleConnect",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            account_tier="Standard",
            account_replication_type="LRS",
            account_kind="BlobStorage")
        example_managed_private_endpoint = azure.synapse.ManagedPrivateEndpoint("exampleManagedPrivateEndpoint",
            synapse_workspace_id=example_workspace.id,
            target_resource_id=example_connect.id,
            subresource_name="blob",
            opts=pulumi.ResourceOptions(depends_on=[example_firewall_rule]))
        ```

        ## Import

        Synapse Managed Private Endpoint can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:synapse/managedPrivateEndpoint:ManagedPrivateEndpoint example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Synapse/workspaces/workspace1/managedVirtualNetworks/default/managedPrivateEndpoints/endpoint1
        ```

        :param str resource_name: The name of the resource.
        :param ManagedPrivateEndpointArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ManagedPrivateEndpointArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 subresource_name: Optional[pulumi.Input[str]] = None,
                 synapse_workspace_id: Optional[pulumi.Input[str]] = None,
                 target_resource_id: Optional[pulumi.Input[str]] = None,
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
            __props__ = ManagedPrivateEndpointArgs.__new__(ManagedPrivateEndpointArgs)

            __props__.__dict__["name"] = name
            if subresource_name is None and not opts.urn:
                raise TypeError("Missing required property 'subresource_name'")
            __props__.__dict__["subresource_name"] = subresource_name
            if synapse_workspace_id is None and not opts.urn:
                raise TypeError("Missing required property 'synapse_workspace_id'")
            __props__.__dict__["synapse_workspace_id"] = synapse_workspace_id
            if target_resource_id is None and not opts.urn:
                raise TypeError("Missing required property 'target_resource_id'")
            __props__.__dict__["target_resource_id"] = target_resource_id
        super(ManagedPrivateEndpoint, __self__).__init__(
            'azure:synapse/managedPrivateEndpoint:ManagedPrivateEndpoint',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            name: Optional[pulumi.Input[str]] = None,
            subresource_name: Optional[pulumi.Input[str]] = None,
            synapse_workspace_id: Optional[pulumi.Input[str]] = None,
            target_resource_id: Optional[pulumi.Input[str]] = None) -> 'ManagedPrivateEndpoint':
        """
        Get an existing ManagedPrivateEndpoint resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: Specifies the name which should be used for this Managed Private Endpoint. Changing this forces a new resource to be created.
        :param pulumi.Input[str] subresource_name: Specifies the sub resource name which the Synapse Private Endpoint is able to connect to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] synapse_workspace_id: The ID of the Synapse Workspace on which to create the Managed Private Endpoint. Changing this forces a new resource to be created.
        :param pulumi.Input[str] target_resource_id: The ID of the Private Link Enabled Remote Resource which this Synapse Private Endpoint should be connected to. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ManagedPrivateEndpointState.__new__(_ManagedPrivateEndpointState)

        __props__.__dict__["name"] = name
        __props__.__dict__["subresource_name"] = subresource_name
        __props__.__dict__["synapse_workspace_id"] = synapse_workspace_id
        __props__.__dict__["target_resource_id"] = target_resource_id
        return ManagedPrivateEndpoint(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the name which should be used for this Managed Private Endpoint. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="subresourceName")
    def subresource_name(self) -> pulumi.Output[str]:
        """
        Specifies the sub resource name which the Synapse Private Endpoint is able to connect to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "subresource_name")

    @property
    @pulumi.getter(name="synapseWorkspaceId")
    def synapse_workspace_id(self) -> pulumi.Output[str]:
        """
        The ID of the Synapse Workspace on which to create the Managed Private Endpoint. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "synapse_workspace_id")

    @property
    @pulumi.getter(name="targetResourceId")
    def target_resource_id(self) -> pulumi.Output[str]:
        """
        The ID of the Private Link Enabled Remote Resource which this Synapse Private Endpoint should be connected to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "target_resource_id")

