# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'AccountIdentityArgs',
    'AccountNetworkAclsArgs',
    'AccountNetworkAclsVirtualNetworkRuleArgs',
    'AccountStorageArgs',
]

@pulumi.input_type
class AccountIdentityArgs:
    def __init__(__self__, *,
                 identity_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 principal_id: Optional[pulumi.Input[str]] = None,
                 tenant_id: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] identity_ids: A list of IDs for User Assigned Managed Identity resources to be assigned.
        :param pulumi.Input[str] type: Specifies the type of Managed Service Identity that should be configured on the Cognitive Account. Possible values are `SystemAssigned`, `UserAssigned`, `SystemAssigned, UserAssigned` (to enable both).
        """
        if identity_ids is not None:
            pulumi.set(__self__, "identity_ids", identity_ids)
        if principal_id is not None:
            pulumi.set(__self__, "principal_id", principal_id)
        if tenant_id is not None:
            pulumi.set(__self__, "tenant_id", tenant_id)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="identityIds")
    def identity_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of IDs for User Assigned Managed Identity resources to be assigned.
        """
        return pulumi.get(self, "identity_ids")

    @identity_ids.setter
    def identity_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "identity_ids", value)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "principal_id")

    @principal_id.setter
    def principal_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "principal_id", value)

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "tenant_id")

    @tenant_id.setter
    def tenant_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tenant_id", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the type of Managed Service Identity that should be configured on the Cognitive Account. Possible values are `SystemAssigned`, `UserAssigned`, `SystemAssigned, UserAssigned` (to enable both).
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


@pulumi.input_type
class AccountNetworkAclsArgs:
    def __init__(__self__, *,
                 default_action: pulumi.Input[str],
                 ip_rules: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 virtual_network_rules: Optional[pulumi.Input[Sequence[pulumi.Input['AccountNetworkAclsVirtualNetworkRuleArgs']]]] = None,
                 virtual_network_subnet_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[str] default_action: The Default Action to use when no rules match from `ip_rules` / `virtual_network_subnet_ids`. Possible values are `Allow` and `Deny`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] ip_rules: One or more IP Addresses, or CIDR Blocks which should be able to access the Cognitive Account.
        :param pulumi.Input[Sequence[pulumi.Input['AccountNetworkAclsVirtualNetworkRuleArgs']]] virtual_network_rules: A `virtual_network_rules` block as defined below.
        """
        pulumi.set(__self__, "default_action", default_action)
        if ip_rules is not None:
            pulumi.set(__self__, "ip_rules", ip_rules)
        if virtual_network_rules is not None:
            pulumi.set(__self__, "virtual_network_rules", virtual_network_rules)
        if virtual_network_subnet_ids is not None:
            warnings.warn("""Deprecated in favour of `virtual_network_rules`""", DeprecationWarning)
            pulumi.log.warn("""virtual_network_subnet_ids is deprecated: Deprecated in favour of `virtual_network_rules`""")
        if virtual_network_subnet_ids is not None:
            pulumi.set(__self__, "virtual_network_subnet_ids", virtual_network_subnet_ids)

    @property
    @pulumi.getter(name="defaultAction")
    def default_action(self) -> pulumi.Input[str]:
        """
        The Default Action to use when no rules match from `ip_rules` / `virtual_network_subnet_ids`. Possible values are `Allow` and `Deny`.
        """
        return pulumi.get(self, "default_action")

    @default_action.setter
    def default_action(self, value: pulumi.Input[str]):
        pulumi.set(self, "default_action", value)

    @property
    @pulumi.getter(name="ipRules")
    def ip_rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        One or more IP Addresses, or CIDR Blocks which should be able to access the Cognitive Account.
        """
        return pulumi.get(self, "ip_rules")

    @ip_rules.setter
    def ip_rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "ip_rules", value)

    @property
    @pulumi.getter(name="virtualNetworkRules")
    def virtual_network_rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AccountNetworkAclsVirtualNetworkRuleArgs']]]]:
        """
        A `virtual_network_rules` block as defined below.
        """
        return pulumi.get(self, "virtual_network_rules")

    @virtual_network_rules.setter
    def virtual_network_rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AccountNetworkAclsVirtualNetworkRuleArgs']]]]):
        pulumi.set(self, "virtual_network_rules", value)

    @property
    @pulumi.getter(name="virtualNetworkSubnetIds")
    def virtual_network_subnet_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "virtual_network_subnet_ids")

    @virtual_network_subnet_ids.setter
    def virtual_network_subnet_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "virtual_network_subnet_ids", value)


@pulumi.input_type
class AccountNetworkAclsVirtualNetworkRuleArgs:
    def __init__(__self__, *,
                 subnet_id: pulumi.Input[str],
                 ignore_missing_vnet_service_endpoint: Optional[pulumi.Input[bool]] = None):
        """
        :param pulumi.Input[str] subnet_id: The ID of the subnet which should be able to access this Cognitive Account.
        :param pulumi.Input[bool] ignore_missing_vnet_service_endpoint: Whether ignore missing vnet service endpoint or not. Default to `false`.
        """
        pulumi.set(__self__, "subnet_id", subnet_id)
        if ignore_missing_vnet_service_endpoint is not None:
            pulumi.set(__self__, "ignore_missing_vnet_service_endpoint", ignore_missing_vnet_service_endpoint)

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> pulumi.Input[str]:
        """
        The ID of the subnet which should be able to access this Cognitive Account.
        """
        return pulumi.get(self, "subnet_id")

    @subnet_id.setter
    def subnet_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "subnet_id", value)

    @property
    @pulumi.getter(name="ignoreMissingVnetServiceEndpoint")
    def ignore_missing_vnet_service_endpoint(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether ignore missing vnet service endpoint or not. Default to `false`.
        """
        return pulumi.get(self, "ignore_missing_vnet_service_endpoint")

    @ignore_missing_vnet_service_endpoint.setter
    def ignore_missing_vnet_service_endpoint(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "ignore_missing_vnet_service_endpoint", value)


@pulumi.input_type
class AccountStorageArgs:
    def __init__(__self__, *,
                 storage_account_id: pulumi.Input[str],
                 identity_client_id: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] storage_account_id: Full resource id of a Microsoft.Storage resource.
        :param pulumi.Input[str] identity_client_id: The client ID of the managed identity associated with the storage resource.
        """
        pulumi.set(__self__, "storage_account_id", storage_account_id)
        if identity_client_id is not None:
            pulumi.set(__self__, "identity_client_id", identity_client_id)

    @property
    @pulumi.getter(name="storageAccountId")
    def storage_account_id(self) -> pulumi.Input[str]:
        """
        Full resource id of a Microsoft.Storage resource.
        """
        return pulumi.get(self, "storage_account_id")

    @storage_account_id.setter
    def storage_account_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "storage_account_id", value)

    @property
    @pulumi.getter(name="identityClientId")
    def identity_client_id(self) -> Optional[pulumi.Input[str]]:
        """
        The client ID of the managed identity associated with the storage resource.
        """
        return pulumi.get(self, "identity_client_id")

    @identity_client_id.setter
    def identity_client_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "identity_client_id", value)


