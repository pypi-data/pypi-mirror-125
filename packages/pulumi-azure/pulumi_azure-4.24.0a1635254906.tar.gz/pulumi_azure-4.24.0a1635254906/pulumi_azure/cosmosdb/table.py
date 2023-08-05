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

__all__ = ['TableArgs', 'Table']

@pulumi.input_type
class TableArgs:
    def __init__(__self__, *,
                 account_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 autoscale_settings: Optional[pulumi.Input['TableAutoscaleSettingsArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 throughput: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a Table resource.
        :param pulumi.Input[str] account_name: The name of the Cosmos DB Table to create the table within. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which the Cosmos DB Table is created. Changing this forces a new resource to be created.
        :param pulumi.Input['TableAutoscaleSettingsArgs'] autoscale_settings: An `autoscale_settings` block as defined below. This must be set upon database creation otherwise it cannot be updated without a manual destroy-apply.
        :param pulumi.Input[str] name: Specifies the name of the Cosmos DB Table. Changing this forces a new resource to be created.
        :param pulumi.Input[int] throughput: The throughput of Table (RU/s). Must be set in increments of `100`. The minimum value is `400`. This must be set upon database creation otherwise it cannot be updated without a manual resource destroy-apply.
        """
        pulumi.set(__self__, "account_name", account_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if autoscale_settings is not None:
            pulumi.set(__self__, "autoscale_settings", autoscale_settings)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if throughput is not None:
            pulumi.set(__self__, "throughput", throughput)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> pulumi.Input[str]:
        """
        The name of the Cosmos DB Table to create the table within. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "account_name")

    @account_name.setter
    def account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "account_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group in which the Cosmos DB Table is created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="autoscaleSettings")
    def autoscale_settings(self) -> Optional[pulumi.Input['TableAutoscaleSettingsArgs']]:
        """
        An `autoscale_settings` block as defined below. This must be set upon database creation otherwise it cannot be updated without a manual destroy-apply.
        """
        return pulumi.get(self, "autoscale_settings")

    @autoscale_settings.setter
    def autoscale_settings(self, value: Optional[pulumi.Input['TableAutoscaleSettingsArgs']]):
        pulumi.set(self, "autoscale_settings", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Cosmos DB Table. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def throughput(self) -> Optional[pulumi.Input[int]]:
        """
        The throughput of Table (RU/s). Must be set in increments of `100`. The minimum value is `400`. This must be set upon database creation otherwise it cannot be updated without a manual resource destroy-apply.
        """
        return pulumi.get(self, "throughput")

    @throughput.setter
    def throughput(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "throughput", value)


@pulumi.input_type
class _TableState:
    def __init__(__self__, *,
                 account_name: Optional[pulumi.Input[str]] = None,
                 autoscale_settings: Optional[pulumi.Input['TableAutoscaleSettingsArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 throughput: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering Table resources.
        :param pulumi.Input[str] account_name: The name of the Cosmos DB Table to create the table within. Changing this forces a new resource to be created.
        :param pulumi.Input['TableAutoscaleSettingsArgs'] autoscale_settings: An `autoscale_settings` block as defined below. This must be set upon database creation otherwise it cannot be updated without a manual destroy-apply.
        :param pulumi.Input[str] name: Specifies the name of the Cosmos DB Table. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which the Cosmos DB Table is created. Changing this forces a new resource to be created.
        :param pulumi.Input[int] throughput: The throughput of Table (RU/s). Must be set in increments of `100`. The minimum value is `400`. This must be set upon database creation otherwise it cannot be updated without a manual resource destroy-apply.
        """
        if account_name is not None:
            pulumi.set(__self__, "account_name", account_name)
        if autoscale_settings is not None:
            pulumi.set(__self__, "autoscale_settings", autoscale_settings)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if throughput is not None:
            pulumi.set(__self__, "throughput", throughput)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Cosmos DB Table to create the table within. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "account_name")

    @account_name.setter
    def account_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_name", value)

    @property
    @pulumi.getter(name="autoscaleSettings")
    def autoscale_settings(self) -> Optional[pulumi.Input['TableAutoscaleSettingsArgs']]:
        """
        An `autoscale_settings` block as defined below. This must be set upon database creation otherwise it cannot be updated without a manual destroy-apply.
        """
        return pulumi.get(self, "autoscale_settings")

    @autoscale_settings.setter
    def autoscale_settings(self, value: Optional[pulumi.Input['TableAutoscaleSettingsArgs']]):
        pulumi.set(self, "autoscale_settings", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Cosmos DB Table. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource group in which the Cosmos DB Table is created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def throughput(self) -> Optional[pulumi.Input[int]]:
        """
        The throughput of Table (RU/s). Must be set in increments of `100`. The minimum value is `400`. This must be set upon database creation otherwise it cannot be updated without a manual resource destroy-apply.
        """
        return pulumi.get(self, "throughput")

    @throughput.setter
    def throughput(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "throughput", value)


class Table(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 autoscale_settings: Optional[pulumi.Input[pulumi.InputType['TableAutoscaleSettingsArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 throughput: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        Manages a Table within a Cosmos DB Account.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_account = azure.cosmosdb.get_account(name="tfex-cosmosdb-account",
            resource_group_name="tfex-cosmosdb-account-rg")
        example_table = azure.cosmosdb.Table("exampleTable",
            resource_group_name=example_account.resource_group_name,
            account_name=example_account.name,
            throughput=400)
        ```

        ## Import

        CosmosDB Tables can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:cosmosdb/table:Table table1 /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg1/providers/Microsoft.DocumentDB/databaseAccounts/account1/tables/table1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The name of the Cosmos DB Table to create the table within. Changing this forces a new resource to be created.
        :param pulumi.Input[pulumi.InputType['TableAutoscaleSettingsArgs']] autoscale_settings: An `autoscale_settings` block as defined below. This must be set upon database creation otherwise it cannot be updated without a manual destroy-apply.
        :param pulumi.Input[str] name: Specifies the name of the Cosmos DB Table. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which the Cosmos DB Table is created. Changing this forces a new resource to be created.
        :param pulumi.Input[int] throughput: The throughput of Table (RU/s). Must be set in increments of `100`. The minimum value is `400`. This must be set upon database creation otherwise it cannot be updated without a manual resource destroy-apply.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TableArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Table within a Cosmos DB Account.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_account = azure.cosmosdb.get_account(name="tfex-cosmosdb-account",
            resource_group_name="tfex-cosmosdb-account-rg")
        example_table = azure.cosmosdb.Table("exampleTable",
            resource_group_name=example_account.resource_group_name,
            account_name=example_account.name,
            throughput=400)
        ```

        ## Import

        CosmosDB Tables can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:cosmosdb/table:Table table1 /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg1/providers/Microsoft.DocumentDB/databaseAccounts/account1/tables/table1
        ```

        :param str resource_name: The name of the resource.
        :param TableArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TableArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 autoscale_settings: Optional[pulumi.Input[pulumi.InputType['TableAutoscaleSettingsArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 throughput: Optional[pulumi.Input[int]] = None,
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
            __props__ = TableArgs.__new__(TableArgs)

            if account_name is None and not opts.urn:
                raise TypeError("Missing required property 'account_name'")
            __props__.__dict__["account_name"] = account_name
            __props__.__dict__["autoscale_settings"] = autoscale_settings
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["throughput"] = throughput
        super(Table, __self__).__init__(
            'azure:cosmosdb/table:Table',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            account_name: Optional[pulumi.Input[str]] = None,
            autoscale_settings: Optional[pulumi.Input[pulumi.InputType['TableAutoscaleSettingsArgs']]] = None,
            name: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            throughput: Optional[pulumi.Input[int]] = None) -> 'Table':
        """
        Get an existing Table resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The name of the Cosmos DB Table to create the table within. Changing this forces a new resource to be created.
        :param pulumi.Input[pulumi.InputType['TableAutoscaleSettingsArgs']] autoscale_settings: An `autoscale_settings` block as defined below. This must be set upon database creation otherwise it cannot be updated without a manual destroy-apply.
        :param pulumi.Input[str] name: Specifies the name of the Cosmos DB Table. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which the Cosmos DB Table is created. Changing this forces a new resource to be created.
        :param pulumi.Input[int] throughput: The throughput of Table (RU/s). Must be set in increments of `100`. The minimum value is `400`. This must be set upon database creation otherwise it cannot be updated without a manual resource destroy-apply.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _TableState.__new__(_TableState)

        __props__.__dict__["account_name"] = account_name
        __props__.__dict__["autoscale_settings"] = autoscale_settings
        __props__.__dict__["name"] = name
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["throughput"] = throughput
        return Table(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> pulumi.Output[str]:
        """
        The name of the Cosmos DB Table to create the table within. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "account_name")

    @property
    @pulumi.getter(name="autoscaleSettings")
    def autoscale_settings(self) -> pulumi.Output[Optional['outputs.TableAutoscaleSettings']]:
        """
        An `autoscale_settings` block as defined below. This must be set upon database creation otherwise it cannot be updated without a manual destroy-apply.
        """
        return pulumi.get(self, "autoscale_settings")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the Cosmos DB Table. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the resource group in which the Cosmos DB Table is created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def throughput(self) -> pulumi.Output[int]:
        """
        The throughput of Table (RU/s). Must be set in increments of `100`. The minimum value is `400`. This must be set upon database creation otherwise it cannot be updated without a manual resource destroy-apply.
        """
        return pulumi.get(self, "throughput")

