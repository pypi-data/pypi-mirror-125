# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['FabricArgs', 'Fabric']

@pulumi.input_type
class FabricArgs:
    def __init__(__self__, *,
                 recovery_vault_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Fabric resource.
        :param pulumi.Input[str] recovery_vault_name: The name of the vault that should be updated.
        :param pulumi.Input[str] resource_group_name: Name of the resource group where the vault that should be updated is located.
        :param pulumi.Input[str] location: In what region should the fabric be located.
        :param pulumi.Input[str] name: The name of the network mapping.
        """
        pulumi.set(__self__, "recovery_vault_name", recovery_vault_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="recoveryVaultName")
    def recovery_vault_name(self) -> pulumi.Input[str]:
        """
        The name of the vault that should be updated.
        """
        return pulumi.get(self, "recovery_vault_name")

    @recovery_vault_name.setter
    def recovery_vault_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "recovery_vault_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the resource group where the vault that should be updated is located.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        In what region should the fabric be located.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the network mapping.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _FabricState:
    def __init__(__self__, *,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 recovery_vault_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Fabric resources.
        :param pulumi.Input[str] location: In what region should the fabric be located.
        :param pulumi.Input[str] name: The name of the network mapping.
        :param pulumi.Input[str] recovery_vault_name: The name of the vault that should be updated.
        :param pulumi.Input[str] resource_group_name: Name of the resource group where the vault that should be updated is located.
        """
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if recovery_vault_name is not None:
            pulumi.set(__self__, "recovery_vault_name", recovery_vault_name)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        In what region should the fabric be located.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the network mapping.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="recoveryVaultName")
    def recovery_vault_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the vault that should be updated.
        """
        return pulumi.get(self, "recovery_vault_name")

    @recovery_vault_name.setter
    def recovery_vault_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "recovery_vault_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the resource group where the vault that should be updated is located.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)


class Fabric(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 recovery_vault_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a Azure Site Recovery Replication Fabric within a Recovery Services vault. Only Azure fabrics are supported at this time. Replication Fabrics serve as a container within an Azure region for other Site Recovery resources such as protection containers, protected items, network mappings.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        primary = azure.core.ResourceGroup("primary", location="West US")
        secondary = azure.core.ResourceGroup("secondary", location="East US")
        vault = azure.recoveryservices.Vault("vault",
            location=secondary.location,
            resource_group_name=secondary.name,
            sku="Standard")
        fabric = azure.siterecovery.Fabric("fabric",
            resource_group_name=secondary.name,
            recovery_vault_name=vault.name,
            location=primary.location)
        ```

        ## Import

        Site Recovery Fabric can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:siterecovery/fabric:Fabric myfabric /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/resource-group-name/providers/Microsoft.RecoveryServices/vaults/recovery-vault-name/replicationFabrics/fabric-name
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: In what region should the fabric be located.
        :param pulumi.Input[str] name: The name of the network mapping.
        :param pulumi.Input[str] recovery_vault_name: The name of the vault that should be updated.
        :param pulumi.Input[str] resource_group_name: Name of the resource group where the vault that should be updated is located.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: FabricArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Azure Site Recovery Replication Fabric within a Recovery Services vault. Only Azure fabrics are supported at this time. Replication Fabrics serve as a container within an Azure region for other Site Recovery resources such as protection containers, protected items, network mappings.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        primary = azure.core.ResourceGroup("primary", location="West US")
        secondary = azure.core.ResourceGroup("secondary", location="East US")
        vault = azure.recoveryservices.Vault("vault",
            location=secondary.location,
            resource_group_name=secondary.name,
            sku="Standard")
        fabric = azure.siterecovery.Fabric("fabric",
            resource_group_name=secondary.name,
            recovery_vault_name=vault.name,
            location=primary.location)
        ```

        ## Import

        Site Recovery Fabric can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:siterecovery/fabric:Fabric myfabric /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/resource-group-name/providers/Microsoft.RecoveryServices/vaults/recovery-vault-name/replicationFabrics/fabric-name
        ```

        :param str resource_name: The name of the resource.
        :param FabricArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(FabricArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 recovery_vault_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = FabricArgs.__new__(FabricArgs)

            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            if recovery_vault_name is None and not opts.urn:
                raise TypeError("Missing required property 'recovery_vault_name'")
            __props__.__dict__["recovery_vault_name"] = recovery_vault_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
        super(Fabric, __self__).__init__(
            'azure:siterecovery/fabric:Fabric',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            recovery_vault_name: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None) -> 'Fabric':
        """
        Get an existing Fabric resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: In what region should the fabric be located.
        :param pulumi.Input[str] name: The name of the network mapping.
        :param pulumi.Input[str] recovery_vault_name: The name of the vault that should be updated.
        :param pulumi.Input[str] resource_group_name: Name of the resource group where the vault that should be updated is located.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _FabricState.__new__(_FabricState)

        __props__.__dict__["location"] = location
        __props__.__dict__["name"] = name
        __props__.__dict__["recovery_vault_name"] = recovery_vault_name
        __props__.__dict__["resource_group_name"] = resource_group_name
        return Fabric(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        In what region should the fabric be located.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the network mapping.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="recoveryVaultName")
    def recovery_vault_name(self) -> pulumi.Output[str]:
        """
        The name of the vault that should be updated.
        """
        return pulumi.get(self, "recovery_vault_name")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        Name of the resource group where the vault that should be updated is located.
        """
        return pulumi.get(self, "resource_group_name")

