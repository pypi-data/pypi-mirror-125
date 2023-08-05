# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'BackendAddressPoolBackendAddress',
    'BackendAddressPoolTunnelInterface',
    'LoadBalancerFrontendIpConfiguration',
    'OutboundRuleFrontendIpConfiguration',
    'GetBackendAddressPoolBackendAddressResult',
    'GetBackendAddressPoolBackendIpConfigurationResult',
    'GetLBFrontendIpConfigurationResult',
]

@pulumi.output_type
class BackendAddressPoolBackendAddress(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "ipAddress":
            suggest = "ip_address"
        elif key == "virtualNetworkId":
            suggest = "virtual_network_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in BackendAddressPoolBackendAddress. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        BackendAddressPoolBackendAddress.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        BackendAddressPoolBackendAddress.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 ip_address: str,
                 name: str,
                 virtual_network_id: str):
        """
        :param str name: Specifies the name of the Backend Address Pool.
        """
        pulumi.set(__self__, "ip_address", ip_address)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "virtual_network_id", virtual_network_id)

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> str:
        return pulumi.get(self, "ip_address")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Specifies the name of the Backend Address Pool.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="virtualNetworkId")
    def virtual_network_id(self) -> str:
        return pulumi.get(self, "virtual_network_id")


@pulumi.output_type
class BackendAddressPoolTunnelInterface(dict):
    def __init__(__self__, *,
                 identifier: int,
                 port: int,
                 protocol: str,
                 type: str):
        """
        :param int identifier: The unique identifier of this Gateway Lodbalancer Tunnel Interface.
        :param int port: The port number that this Gateway Lodbalancer Tunnel Interface listens to.
        :param str protocol: The protocol used for this Gateway Lodbalancer Tunnel Interface. Possible values are `Native` and `VXLAN`.
        :param str type: The traffic type of this Gateway Lodbalancer Tunnel Interface. Possible values are `Internal` and `External`.
        """
        pulumi.set(__self__, "identifier", identifier)
        pulumi.set(__self__, "port", port)
        pulumi.set(__self__, "protocol", protocol)
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def identifier(self) -> int:
        """
        The unique identifier of this Gateway Lodbalancer Tunnel Interface.
        """
        return pulumi.get(self, "identifier")

    @property
    @pulumi.getter
    def port(self) -> int:
        """
        The port number that this Gateway Lodbalancer Tunnel Interface listens to.
        """
        return pulumi.get(self, "port")

    @property
    @pulumi.getter
    def protocol(self) -> str:
        """
        The protocol used for this Gateway Lodbalancer Tunnel Interface. Possible values are `Native` and `VXLAN`.
        """
        return pulumi.get(self, "protocol")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The traffic type of this Gateway Lodbalancer Tunnel Interface. Possible values are `Internal` and `External`.
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class LoadBalancerFrontendIpConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "availabilityZone":
            suggest = "availability_zone"
        elif key == "gatewayLoadBalancerFrontendIpConfigurationId":
            suggest = "gateway_load_balancer_frontend_ip_configuration_id"
        elif key == "inboundNatRules":
            suggest = "inbound_nat_rules"
        elif key == "loadBalancerRules":
            suggest = "load_balancer_rules"
        elif key == "outboundRules":
            suggest = "outbound_rules"
        elif key == "privateIpAddress":
            suggest = "private_ip_address"
        elif key == "privateIpAddressAllocation":
            suggest = "private_ip_address_allocation"
        elif key == "privateIpAddressVersion":
            suggest = "private_ip_address_version"
        elif key == "publicIpAddressId":
            suggest = "public_ip_address_id"
        elif key == "publicIpPrefixId":
            suggest = "public_ip_prefix_id"
        elif key == "subnetId":
            suggest = "subnet_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in LoadBalancerFrontendIpConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        LoadBalancerFrontendIpConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        LoadBalancerFrontendIpConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 name: str,
                 availability_zone: Optional[str] = None,
                 gateway_load_balancer_frontend_ip_configuration_id: Optional[str] = None,
                 id: Optional[str] = None,
                 inbound_nat_rules: Optional[Sequence[str]] = None,
                 load_balancer_rules: Optional[Sequence[str]] = None,
                 outbound_rules: Optional[Sequence[str]] = None,
                 private_ip_address: Optional[str] = None,
                 private_ip_address_allocation: Optional[str] = None,
                 private_ip_address_version: Optional[str] = None,
                 public_ip_address_id: Optional[str] = None,
                 public_ip_prefix_id: Optional[str] = None,
                 subnet_id: Optional[str] = None,
                 zones: Optional[str] = None):
        """
        :param str name: Specifies the name of the frontend ip configuration.
        :param str availability_zone: A list of Availability Zones which the Load Balancer's IP Addresses should be created in. Possible values are `Zone-Redundant`, `1`, `2`, `3`, and `No-Zone`. Availability Zone can only be updated whenever the name of the front end ip configuration changes. Defaults to `Zone-Redundant`. 
               `No-Zones` - A `non-zonal` resource will be created and the resource will not be replicated or distributed to any Availability Zones.
        :param str gateway_load_balancer_frontend_ip_configuration_id: The Frontend IP Configuration ID of a Gateway Sku Load Balancer.
        :param str id: The id of the Frontend IP Configuration.
        :param Sequence[str] inbound_nat_rules: The list of IDs of inbound rules that use this frontend IP.
        :param Sequence[str] load_balancer_rules: The list of IDs of load balancing rules that use this frontend IP.
        :param Sequence[str] outbound_rules: The list of IDs outbound rules that use this frontend IP.
        :param str private_ip_address: Private IP Address to assign to the Load Balancer. The last one and first four IPs in any range are reserved and cannot be manually assigned.
        :param str private_ip_address_allocation: The allocation method for the Private IP Address used by this Load Balancer. Possible values as `Dynamic` and `Static`.
        :param str private_ip_address_version: The version of IP that the Private IP Address is. Possible values are `IPv4` or `IPv6`.
        :param str public_ip_address_id: The ID of a Public IP Address which should be associated with the Load Balancer.
        :param str public_ip_prefix_id: The ID of a Public IP Prefix which should be associated with the Load Balancer. Public IP Prefix can only be used with outbound rules.
        :param str subnet_id: The ID of the Subnet which should be associated with the IP Configuration.
        """
        pulumi.set(__self__, "name", name)
        if availability_zone is not None:
            pulumi.set(__self__, "availability_zone", availability_zone)
        if gateway_load_balancer_frontend_ip_configuration_id is not None:
            pulumi.set(__self__, "gateway_load_balancer_frontend_ip_configuration_id", gateway_load_balancer_frontend_ip_configuration_id)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if inbound_nat_rules is not None:
            pulumi.set(__self__, "inbound_nat_rules", inbound_nat_rules)
        if load_balancer_rules is not None:
            pulumi.set(__self__, "load_balancer_rules", load_balancer_rules)
        if outbound_rules is not None:
            pulumi.set(__self__, "outbound_rules", outbound_rules)
        if private_ip_address is not None:
            pulumi.set(__self__, "private_ip_address", private_ip_address)
        if private_ip_address_allocation is not None:
            pulumi.set(__self__, "private_ip_address_allocation", private_ip_address_allocation)
        if private_ip_address_version is not None:
            pulumi.set(__self__, "private_ip_address_version", private_ip_address_version)
        if public_ip_address_id is not None:
            pulumi.set(__self__, "public_ip_address_id", public_ip_address_id)
        if public_ip_prefix_id is not None:
            pulumi.set(__self__, "public_ip_prefix_id", public_ip_prefix_id)
        if subnet_id is not None:
            pulumi.set(__self__, "subnet_id", subnet_id)
        if zones is not None:
            pulumi.set(__self__, "zones", zones)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Specifies the name of the frontend ip configuration.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="availabilityZone")
    def availability_zone(self) -> Optional[str]:
        """
        A list of Availability Zones which the Load Balancer's IP Addresses should be created in. Possible values are `Zone-Redundant`, `1`, `2`, `3`, and `No-Zone`. Availability Zone can only be updated whenever the name of the front end ip configuration changes. Defaults to `Zone-Redundant`. 
        `No-Zones` - A `non-zonal` resource will be created and the resource will not be replicated or distributed to any Availability Zones.
        """
        return pulumi.get(self, "availability_zone")

    @property
    @pulumi.getter(name="gatewayLoadBalancerFrontendIpConfigurationId")
    def gateway_load_balancer_frontend_ip_configuration_id(self) -> Optional[str]:
        """
        The Frontend IP Configuration ID of a Gateway Sku Load Balancer.
        """
        return pulumi.get(self, "gateway_load_balancer_frontend_ip_configuration_id")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The id of the Frontend IP Configuration.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="inboundNatRules")
    def inbound_nat_rules(self) -> Optional[Sequence[str]]:
        """
        The list of IDs of inbound rules that use this frontend IP.
        """
        return pulumi.get(self, "inbound_nat_rules")

    @property
    @pulumi.getter(name="loadBalancerRules")
    def load_balancer_rules(self) -> Optional[Sequence[str]]:
        """
        The list of IDs of load balancing rules that use this frontend IP.
        """
        return pulumi.get(self, "load_balancer_rules")

    @property
    @pulumi.getter(name="outboundRules")
    def outbound_rules(self) -> Optional[Sequence[str]]:
        """
        The list of IDs outbound rules that use this frontend IP.
        """
        return pulumi.get(self, "outbound_rules")

    @property
    @pulumi.getter(name="privateIpAddress")
    def private_ip_address(self) -> Optional[str]:
        """
        Private IP Address to assign to the Load Balancer. The last one and first four IPs in any range are reserved and cannot be manually assigned.
        """
        return pulumi.get(self, "private_ip_address")

    @property
    @pulumi.getter(name="privateIpAddressAllocation")
    def private_ip_address_allocation(self) -> Optional[str]:
        """
        The allocation method for the Private IP Address used by this Load Balancer. Possible values as `Dynamic` and `Static`.
        """
        return pulumi.get(self, "private_ip_address_allocation")

    @property
    @pulumi.getter(name="privateIpAddressVersion")
    def private_ip_address_version(self) -> Optional[str]:
        """
        The version of IP that the Private IP Address is. Possible values are `IPv4` or `IPv6`.
        """
        return pulumi.get(self, "private_ip_address_version")

    @property
    @pulumi.getter(name="publicIpAddressId")
    def public_ip_address_id(self) -> Optional[str]:
        """
        The ID of a Public IP Address which should be associated with the Load Balancer.
        """
        return pulumi.get(self, "public_ip_address_id")

    @property
    @pulumi.getter(name="publicIpPrefixId")
    def public_ip_prefix_id(self) -> Optional[str]:
        """
        The ID of a Public IP Prefix which should be associated with the Load Balancer. Public IP Prefix can only be used with outbound rules.
        """
        return pulumi.get(self, "public_ip_prefix_id")

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> Optional[str]:
        """
        The ID of the Subnet which should be associated with the IP Configuration.
        """
        return pulumi.get(self, "subnet_id")

    @property
    @pulumi.getter
    def zones(self) -> Optional[str]:
        return pulumi.get(self, "zones")


@pulumi.output_type
class OutboundRuleFrontendIpConfiguration(dict):
    def __init__(__self__, *,
                 name: str,
                 id: Optional[str] = None):
        """
        :param str name: The name of the Frontend IP Configuration.
        :param str id: The ID of the Load Balancer Outbound Rule.
        """
        pulumi.set(__self__, "name", name)
        if id is not None:
            pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the Frontend IP Configuration.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The ID of the Load Balancer Outbound Rule.
        """
        return pulumi.get(self, "id")


@pulumi.output_type
class GetBackendAddressPoolBackendAddressResult(dict):
    def __init__(__self__, *,
                 ip_address: str,
                 name: str,
                 virtual_network_id: str):
        """
        :param str ip_address: The Static IP address for this Load Balancer within the Virtual Network.
        :param str name: Specifies the name of the Backend Address Pool.
        :param str virtual_network_id: The ID of the Virtual Network where the Backend Address of the Load Balancer exists.
        """
        pulumi.set(__self__, "ip_address", ip_address)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "virtual_network_id", virtual_network_id)

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> str:
        """
        The Static IP address for this Load Balancer within the Virtual Network.
        """
        return pulumi.get(self, "ip_address")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Specifies the name of the Backend Address Pool.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="virtualNetworkId")
    def virtual_network_id(self) -> str:
        """
        The ID of the Virtual Network where the Backend Address of the Load Balancer exists.
        """
        return pulumi.get(self, "virtual_network_id")


@pulumi.output_type
class GetBackendAddressPoolBackendIpConfigurationResult(dict):
    def __init__(__self__, *,
                 id: str):
        """
        :param str id: The ID of the Backend Address Pool.
        """
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ID of the Backend Address Pool.
        """
        return pulumi.get(self, "id")


@pulumi.output_type
class GetLBFrontendIpConfigurationResult(dict):
    def __init__(__self__, *,
                 id: str,
                 name: str,
                 private_ip_address: str,
                 private_ip_address_allocation: str,
                 private_ip_address_version: str,
                 public_ip_address_id: str,
                 subnet_id: str,
                 zones: Sequence[str]):
        """
        :param str id: The id of the Frontend IP Configuration.
        :param str name: Specifies the name of the Load Balancer.
        :param str private_ip_address: Private IP Address to assign to the Load Balancer.
        :param str private_ip_address_allocation: The allocation method for the Private IP Address used by this Load Balancer.
        :param str private_ip_address_version: The Private IP Address Version, either `IPv4` or `IPv6`.
        :param str public_ip_address_id: The ID of a  Public IP Address which is associated with this Load Balancer.
        :param str subnet_id: The ID of the Subnet which is associated with the IP Configuration.
        :param Sequence[str] zones: A list of Availability Zones which the Load Balancer's IP Addresses should be created in.
        """
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "private_ip_address", private_ip_address)
        pulumi.set(__self__, "private_ip_address_allocation", private_ip_address_allocation)
        pulumi.set(__self__, "private_ip_address_version", private_ip_address_version)
        pulumi.set(__self__, "public_ip_address_id", public_ip_address_id)
        pulumi.set(__self__, "subnet_id", subnet_id)
        pulumi.set(__self__, "zones", zones)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The id of the Frontend IP Configuration.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Specifies the name of the Load Balancer.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="privateIpAddress")
    def private_ip_address(self) -> str:
        """
        Private IP Address to assign to the Load Balancer.
        """
        return pulumi.get(self, "private_ip_address")

    @property
    @pulumi.getter(name="privateIpAddressAllocation")
    def private_ip_address_allocation(self) -> str:
        """
        The allocation method for the Private IP Address used by this Load Balancer.
        """
        return pulumi.get(self, "private_ip_address_allocation")

    @property
    @pulumi.getter(name="privateIpAddressVersion")
    def private_ip_address_version(self) -> str:
        """
        The Private IP Address Version, either `IPv4` or `IPv6`.
        """
        return pulumi.get(self, "private_ip_address_version")

    @property
    @pulumi.getter(name="publicIpAddressId")
    def public_ip_address_id(self) -> str:
        """
        The ID of a  Public IP Address which is associated with this Load Balancer.
        """
        return pulumi.get(self, "public_ip_address_id")

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> str:
        """
        The ID of the Subnet which is associated with the IP Configuration.
        """
        return pulumi.get(self, "subnet_id")

    @property
    @pulumi.getter
    def zones(self) -> Sequence[str]:
        """
        A list of Availability Zones which the Load Balancer's IP Addresses should be created in.
        """
        return pulumi.get(self, "zones")


