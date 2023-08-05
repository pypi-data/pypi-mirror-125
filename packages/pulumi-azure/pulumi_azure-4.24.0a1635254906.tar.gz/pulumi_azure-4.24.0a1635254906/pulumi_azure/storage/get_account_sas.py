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
    'GetAccountSASResult',
    'AwaitableGetAccountSASResult',
    'get_account_sas',
    'get_account_sas_output',
]

@pulumi.output_type
class GetAccountSASResult:
    """
    A collection of values returned by getAccountSAS.
    """
    def __init__(__self__, connection_string=None, expiry=None, https_only=None, id=None, ip_addresses=None, permissions=None, resource_types=None, sas=None, services=None, signed_version=None, start=None):
        if connection_string and not isinstance(connection_string, str):
            raise TypeError("Expected argument 'connection_string' to be a str")
        pulumi.set(__self__, "connection_string", connection_string)
        if expiry and not isinstance(expiry, str):
            raise TypeError("Expected argument 'expiry' to be a str")
        pulumi.set(__self__, "expiry", expiry)
        if https_only and not isinstance(https_only, bool):
            raise TypeError("Expected argument 'https_only' to be a bool")
        pulumi.set(__self__, "https_only", https_only)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ip_addresses and not isinstance(ip_addresses, str):
            raise TypeError("Expected argument 'ip_addresses' to be a str")
        pulumi.set(__self__, "ip_addresses", ip_addresses)
        if permissions and not isinstance(permissions, dict):
            raise TypeError("Expected argument 'permissions' to be a dict")
        pulumi.set(__self__, "permissions", permissions)
        if resource_types and not isinstance(resource_types, dict):
            raise TypeError("Expected argument 'resource_types' to be a dict")
        pulumi.set(__self__, "resource_types", resource_types)
        if sas and not isinstance(sas, str):
            raise TypeError("Expected argument 'sas' to be a str")
        pulumi.set(__self__, "sas", sas)
        if services and not isinstance(services, dict):
            raise TypeError("Expected argument 'services' to be a dict")
        pulumi.set(__self__, "services", services)
        if signed_version and not isinstance(signed_version, str):
            raise TypeError("Expected argument 'signed_version' to be a str")
        pulumi.set(__self__, "signed_version", signed_version)
        if start and not isinstance(start, str):
            raise TypeError("Expected argument 'start' to be a str")
        pulumi.set(__self__, "start", start)

    @property
    @pulumi.getter(name="connectionString")
    def connection_string(self) -> str:
        return pulumi.get(self, "connection_string")

    @property
    @pulumi.getter
    def expiry(self) -> str:
        return pulumi.get(self, "expiry")

    @property
    @pulumi.getter(name="httpsOnly")
    def https_only(self) -> Optional[bool]:
        return pulumi.get(self, "https_only")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="ipAddresses")
    def ip_addresses(self) -> Optional[str]:
        return pulumi.get(self, "ip_addresses")

    @property
    @pulumi.getter
    def permissions(self) -> 'outputs.GetAccountSASPermissionsResult':
        return pulumi.get(self, "permissions")

    @property
    @pulumi.getter(name="resourceTypes")
    def resource_types(self) -> 'outputs.GetAccountSASResourceTypesResult':
        return pulumi.get(self, "resource_types")

    @property
    @pulumi.getter
    def sas(self) -> str:
        """
        The computed Account Shared Access Signature (SAS).
        """
        return pulumi.get(self, "sas")

    @property
    @pulumi.getter
    def services(self) -> 'outputs.GetAccountSASServicesResult':
        return pulumi.get(self, "services")

    @property
    @pulumi.getter(name="signedVersion")
    def signed_version(self) -> Optional[str]:
        return pulumi.get(self, "signed_version")

    @property
    @pulumi.getter
    def start(self) -> str:
        return pulumi.get(self, "start")


class AwaitableGetAccountSASResult(GetAccountSASResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAccountSASResult(
            connection_string=self.connection_string,
            expiry=self.expiry,
            https_only=self.https_only,
            id=self.id,
            ip_addresses=self.ip_addresses,
            permissions=self.permissions,
            resource_types=self.resource_types,
            sas=self.sas,
            services=self.services,
            signed_version=self.signed_version,
            start=self.start)


def get_account_sas(connection_string: Optional[str] = None,
                    expiry: Optional[str] = None,
                    https_only: Optional[bool] = None,
                    ip_addresses: Optional[str] = None,
                    permissions: Optional[pulumi.InputType['GetAccountSASPermissionsArgs']] = None,
                    resource_types: Optional[pulumi.InputType['GetAccountSASResourceTypesArgs']] = None,
                    services: Optional[pulumi.InputType['GetAccountSASServicesArgs']] = None,
                    signed_version: Optional[str] = None,
                    start: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAccountSASResult:
    """
    Use this data source to obtain a Shared Access Signature (SAS Token) for an existing Storage Account.

    Shared access signatures allow fine-grained, ephemeral access control to various aspects of an Azure Storage Account.

    Note that this is an [Account SAS](https://docs.microsoft.com/en-us/rest/api/storageservices/constructing-an-account-sas)
    and *not* a [Service SAS](https://docs.microsoft.com/en-us/rest/api/storageservices/constructing-a-service-sas).

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
    example_account = azure.storage.Account("exampleAccount",
        resource_group_name=example_resource_group.name,
        location="westus",
        account_tier="Standard",
        account_replication_type="GRS",
        tags={
            "environment": "staging",
        })
    example_account_sas = example_account.primary_connection_string.apply(lambda primary_connection_string: azure.storage.get_account_sas(connection_string=primary_connection_string,
        https_only=True,
        signed_version="2017-07-29",
        resource_types=azure.storage.GetAccountSASResourceTypesArgs(
            service=True,
            container=False,
            object=False,
        ),
        services=azure.storage.GetAccountSASServicesArgs(
            blob=True,
            queue=False,
            table=False,
            file=False,
        ),
        start="2018-03-21T00:00:00Z",
        expiry="2020-03-21T00:00:00Z",
        permissions=azure.storage.GetAccountSASPermissionsArgs(
            read=True,
            write=True,
            delete=False,
            list=False,
            add=True,
            create=True,
            update=False,
            process=False,
        )))
    pulumi.export("sasUrlQueryString", example_account_sas.sas)
    ```


    :param str connection_string: The connection string for the storage account to which this SAS applies. Typically directly from the `primary_connection_string` attribute of a `storage.Account` resource.
    :param str expiry: The expiration time and date of this SAS. Must be a valid ISO-8601 format time/date string.
    :param bool https_only: Only permit `https` access. If `false`, both `http` and `https` are permitted. Defaults to `true`.
    :param str ip_addresses: IP address, or a range of IP addresses, from which to accept requests. When specifying a range, note that the range is inclusive.
    :param pulumi.InputType['GetAccountSASPermissionsArgs'] permissions: A `permissions` block as defined below.
    :param pulumi.InputType['GetAccountSASResourceTypesArgs'] resource_types: A `resource_types` block as defined below.
    :param pulumi.InputType['GetAccountSASServicesArgs'] services: A `services` block as defined below.
    :param str signed_version: Specifies the signed storage service version to use to authorize requests made with this account SAS. Defaults to `2017-07-29`.
    :param str start: The starting time and date of validity of this SAS. Must be a valid ISO-8601 format time/date string.
    """
    __args__ = dict()
    __args__['connectionString'] = connection_string
    __args__['expiry'] = expiry
    __args__['httpsOnly'] = https_only
    __args__['ipAddresses'] = ip_addresses
    __args__['permissions'] = permissions
    __args__['resourceTypes'] = resource_types
    __args__['services'] = services
    __args__['signedVersion'] = signed_version
    __args__['start'] = start
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:storage/getAccountSAS:getAccountSAS', __args__, opts=opts, typ=GetAccountSASResult).value

    return AwaitableGetAccountSASResult(
        connection_string=__ret__.connection_string,
        expiry=__ret__.expiry,
        https_only=__ret__.https_only,
        id=__ret__.id,
        ip_addresses=__ret__.ip_addresses,
        permissions=__ret__.permissions,
        resource_types=__ret__.resource_types,
        sas=__ret__.sas,
        services=__ret__.services,
        signed_version=__ret__.signed_version,
        start=__ret__.start)


@_utilities.lift_output_func(get_account_sas)
def get_account_sas_output(connection_string: Optional[pulumi.Input[str]] = None,
                           expiry: Optional[pulumi.Input[str]] = None,
                           https_only: Optional[pulumi.Input[Optional[bool]]] = None,
                           ip_addresses: Optional[pulumi.Input[Optional[str]]] = None,
                           permissions: Optional[pulumi.Input[pulumi.InputType['GetAccountSASPermissionsArgs']]] = None,
                           resource_types: Optional[pulumi.Input[pulumi.InputType['GetAccountSASResourceTypesArgs']]] = None,
                           services: Optional[pulumi.Input[pulumi.InputType['GetAccountSASServicesArgs']]] = None,
                           signed_version: Optional[pulumi.Input[Optional[str]]] = None,
                           start: Optional[pulumi.Input[str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAccountSASResult]:
    """
    Use this data source to obtain a Shared Access Signature (SAS Token) for an existing Storage Account.

    Shared access signatures allow fine-grained, ephemeral access control to various aspects of an Azure Storage Account.

    Note that this is an [Account SAS](https://docs.microsoft.com/en-us/rest/api/storageservices/constructing-an-account-sas)
    and *not* a [Service SAS](https://docs.microsoft.com/en-us/rest/api/storageservices/constructing-a-service-sas).

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
    example_account = azure.storage.Account("exampleAccount",
        resource_group_name=example_resource_group.name,
        location="westus",
        account_tier="Standard",
        account_replication_type="GRS",
        tags={
            "environment": "staging",
        })
    example_account_sas = example_account.primary_connection_string.apply(lambda primary_connection_string: azure.storage.get_account_sas(connection_string=primary_connection_string,
        https_only=True,
        signed_version="2017-07-29",
        resource_types=azure.storage.GetAccountSASResourceTypesArgs(
            service=True,
            container=False,
            object=False,
        ),
        services=azure.storage.GetAccountSASServicesArgs(
            blob=True,
            queue=False,
            table=False,
            file=False,
        ),
        start="2018-03-21T00:00:00Z",
        expiry="2020-03-21T00:00:00Z",
        permissions=azure.storage.GetAccountSASPermissionsArgs(
            read=True,
            write=True,
            delete=False,
            list=False,
            add=True,
            create=True,
            update=False,
            process=False,
        )))
    pulumi.export("sasUrlQueryString", example_account_sas.sas)
    ```


    :param str connection_string: The connection string for the storage account to which this SAS applies. Typically directly from the `primary_connection_string` attribute of a `storage.Account` resource.
    :param str expiry: The expiration time and date of this SAS. Must be a valid ISO-8601 format time/date string.
    :param bool https_only: Only permit `https` access. If `false`, both `http` and `https` are permitted. Defaults to `true`.
    :param str ip_addresses: IP address, or a range of IP addresses, from which to accept requests. When specifying a range, note that the range is inclusive.
    :param pulumi.InputType['GetAccountSASPermissionsArgs'] permissions: A `permissions` block as defined below.
    :param pulumi.InputType['GetAccountSASResourceTypesArgs'] resource_types: A `resource_types` block as defined below.
    :param pulumi.InputType['GetAccountSASServicesArgs'] services: A `services` block as defined below.
    :param str signed_version: Specifies the signed storage service version to use to authorize requests made with this account SAS. Defaults to `2017-07-29`.
    :param str start: The starting time and date of validity of this SAS. Must be a valid ISO-8601 format time/date string.
    """
    ...
