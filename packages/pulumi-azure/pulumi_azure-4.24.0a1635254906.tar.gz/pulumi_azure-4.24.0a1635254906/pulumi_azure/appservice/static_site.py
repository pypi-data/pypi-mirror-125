# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['StaticSiteArgs', 'StaticSite']

@pulumi.input_type
class StaticSiteArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 sku_size: Optional[pulumi.Input[str]] = None,
                 sku_tier: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a StaticSite resource.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Static Web App should exist. Changing this forces a new Static Web App to be created.
        :param pulumi.Input[str] location: The Azure Region where the Static Web App should exist. Changing this forces a new Static Web App to be created.
        :param pulumi.Input[str] name: The name which should be used for this Static Web App. Changing this forces a new Static Web App to be created.
        :param pulumi.Input[str] sku_size: Specifies the sku tier of the Static Web App. Possible values are "Free" or "Standard". Defaults to "Free".
        :param pulumi.Input[str] sku_tier: Specifies the sku tier of the Static Web App. Possible values are "Free" or "Standard". Defaults to "Free".
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if sku_size is not None:
            pulumi.set(__self__, "sku_size", sku_size)
        if sku_tier is not None:
            pulumi.set(__self__, "sku_tier", sku_tier)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the Resource Group where the Static Web App should exist. Changing this forces a new Static Web App to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The Azure Region where the Static Web App should exist. Changing this forces a new Static Web App to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Static Web App. Changing this forces a new Static Web App to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="skuSize")
    def sku_size(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the sku tier of the Static Web App. Possible values are "Free" or "Standard". Defaults to "Free".
        """
        return pulumi.get(self, "sku_size")

    @sku_size.setter
    def sku_size(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sku_size", value)

    @property
    @pulumi.getter(name="skuTier")
    def sku_tier(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the sku tier of the Static Web App. Possible values are "Free" or "Standard". Defaults to "Free".
        """
        return pulumi.get(self, "sku_tier")

    @sku_tier.setter
    def sku_tier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sku_tier", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _StaticSiteState:
    def __init__(__self__, *,
                 api_key: Optional[pulumi.Input[str]] = None,
                 default_host_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku_size: Optional[pulumi.Input[str]] = None,
                 sku_tier: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering StaticSite resources.
        :param pulumi.Input[str] api_key: The API key of this Static Web App, which is used for later interacting with this Static Web App from other clients, e.g. Github Action.
        :param pulumi.Input[str] default_host_name: The default host name of the Static Web App.
        :param pulumi.Input[str] location: The Azure Region where the Static Web App should exist. Changing this forces a new Static Web App to be created.
        :param pulumi.Input[str] name: The name which should be used for this Static Web App. Changing this forces a new Static Web App to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Static Web App should exist. Changing this forces a new Static Web App to be created.
        :param pulumi.Input[str] sku_size: Specifies the sku tier of the Static Web App. Possible values are "Free" or "Standard". Defaults to "Free".
        :param pulumi.Input[str] sku_tier: Specifies the sku tier of the Static Web App. Possible values are "Free" or "Standard". Defaults to "Free".
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        if api_key is not None:
            pulumi.set(__self__, "api_key", api_key)
        if default_host_name is not None:
            pulumi.set(__self__, "default_host_name", default_host_name)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if sku_size is not None:
            pulumi.set(__self__, "sku_size", sku_size)
        if sku_tier is not None:
            pulumi.set(__self__, "sku_tier", sku_tier)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="apiKey")
    def api_key(self) -> Optional[pulumi.Input[str]]:
        """
        The API key of this Static Web App, which is used for later interacting with this Static Web App from other clients, e.g. Github Action.
        """
        return pulumi.get(self, "api_key")

    @api_key.setter
    def api_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "api_key", value)

    @property
    @pulumi.getter(name="defaultHostName")
    def default_host_name(self) -> Optional[pulumi.Input[str]]:
        """
        The default host name of the Static Web App.
        """
        return pulumi.get(self, "default_host_name")

    @default_host_name.setter
    def default_host_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "default_host_name", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The Azure Region where the Static Web App should exist. Changing this forces a new Static Web App to be created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Static Web App. Changing this forces a new Static Web App to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Resource Group where the Static Web App should exist. Changing this forces a new Static Web App to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="skuSize")
    def sku_size(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the sku tier of the Static Web App. Possible values are "Free" or "Standard". Defaults to "Free".
        """
        return pulumi.get(self, "sku_size")

    @sku_size.setter
    def sku_size(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sku_size", value)

    @property
    @pulumi.getter(name="skuTier")
    def sku_tier(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the sku tier of the Static Web App. Possible values are "Free" or "Standard". Defaults to "Free".
        """
        return pulumi.get(self, "sku_tier")

    @sku_tier.setter
    def sku_tier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sku_tier", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class StaticSite(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku_size: Optional[pulumi.Input[str]] = None,
                 sku_tier: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Manages an App Service Static Site.

        ->**NOTE**: After the Static Site is provisioned, you'll need to associate your target repository, which contains your web app, to the Static Site, by following the [Azure Static Site document](https://docs.microsoft.com/en-us/azure/static-web-apps/github-actions-workflow).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.appservice.StaticSite("example",
            location="West Europe",
            resource_group_name="example")
        ```

        ## Import

        Static Web Apps can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:appservice/staticSite:StaticSite example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Web/staticSites/my-static-site1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: The Azure Region where the Static Web App should exist. Changing this forces a new Static Web App to be created.
        :param pulumi.Input[str] name: The name which should be used for this Static Web App. Changing this forces a new Static Web App to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Static Web App should exist. Changing this forces a new Static Web App to be created.
        :param pulumi.Input[str] sku_size: Specifies the sku tier of the Static Web App. Possible values are "Free" or "Standard". Defaults to "Free".
        :param pulumi.Input[str] sku_tier: Specifies the sku tier of the Static Web App. Possible values are "Free" or "Standard". Defaults to "Free".
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: StaticSiteArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages an App Service Static Site.

        ->**NOTE**: After the Static Site is provisioned, you'll need to associate your target repository, which contains your web app, to the Static Site, by following the [Azure Static Site document](https://docs.microsoft.com/en-us/azure/static-web-apps/github-actions-workflow).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example = azure.appservice.StaticSite("example",
            location="West Europe",
            resource_group_name="example")
        ```

        ## Import

        Static Web Apps can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:appservice/staticSite:StaticSite example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.Web/staticSites/my-static-site1
        ```

        :param str resource_name: The name of the resource.
        :param StaticSiteArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(StaticSiteArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku_size: Optional[pulumi.Input[str]] = None,
                 sku_tier: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
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
            __props__ = StaticSiteArgs.__new__(StaticSiteArgs)

            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["sku_size"] = sku_size
            __props__.__dict__["sku_tier"] = sku_tier
            __props__.__dict__["tags"] = tags
            __props__.__dict__["api_key"] = None
            __props__.__dict__["default_host_name"] = None
        super(StaticSite, __self__).__init__(
            'azure:appservice/staticSite:StaticSite',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            api_key: Optional[pulumi.Input[str]] = None,
            default_host_name: Optional[pulumi.Input[str]] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            sku_size: Optional[pulumi.Input[str]] = None,
            sku_tier: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'StaticSite':
        """
        Get an existing StaticSite resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_key: The API key of this Static Web App, which is used for later interacting with this Static Web App from other clients, e.g. Github Action.
        :param pulumi.Input[str] default_host_name: The default host name of the Static Web App.
        :param pulumi.Input[str] location: The Azure Region where the Static Web App should exist. Changing this forces a new Static Web App to be created.
        :param pulumi.Input[str] name: The name which should be used for this Static Web App. Changing this forces a new Static Web App to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Static Web App should exist. Changing this forces a new Static Web App to be created.
        :param pulumi.Input[str] sku_size: Specifies the sku tier of the Static Web App. Possible values are "Free" or "Standard". Defaults to "Free".
        :param pulumi.Input[str] sku_tier: Specifies the sku tier of the Static Web App. Possible values are "Free" or "Standard". Defaults to "Free".
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _StaticSiteState.__new__(_StaticSiteState)

        __props__.__dict__["api_key"] = api_key
        __props__.__dict__["default_host_name"] = default_host_name
        __props__.__dict__["location"] = location
        __props__.__dict__["name"] = name
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["sku_size"] = sku_size
        __props__.__dict__["sku_tier"] = sku_tier
        __props__.__dict__["tags"] = tags
        return StaticSite(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="apiKey")
    def api_key(self) -> pulumi.Output[str]:
        """
        The API key of this Static Web App, which is used for later interacting with this Static Web App from other clients, e.g. Github Action.
        """
        return pulumi.get(self, "api_key")

    @property
    @pulumi.getter(name="defaultHostName")
    def default_host_name(self) -> pulumi.Output[str]:
        """
        The default host name of the Static Web App.
        """
        return pulumi.get(self, "default_host_name")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The Azure Region where the Static Web App should exist. Changing this forces a new Static Web App to be created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name which should be used for this Static Web App. Changing this forces a new Static Web App to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the Resource Group where the Static Web App should exist. Changing this forces a new Static Web App to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="skuSize")
    def sku_size(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the sku tier of the Static Web App. Possible values are "Free" or "Standard". Defaults to "Free".
        """
        return pulumi.get(self, "sku_size")

    @property
    @pulumi.getter(name="skuTier")
    def sku_tier(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the sku tier of the Static Web App. Possible values are "Free" or "Standard". Defaults to "Free".
        """
        return pulumi.get(self, "sku_tier")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

