"""
Type annotations for discovery service client paginators.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_discovery/paginators.html)

Usage::

    ```python
    import boto3

    from mypy_boto3_discovery import ApplicationDiscoveryServiceClient
    from mypy_boto3_discovery.paginator import (
        DescribeAgentsPaginator,
        DescribeContinuousExportsPaginator,
        DescribeExportConfigurationsPaginator,
        DescribeExportTasksPaginator,
        DescribeTagsPaginator,
        ListConfigurationsPaginator,
    )

    client: ApplicationDiscoveryServiceClient = boto3.client("discovery")

    describe_agents_paginator: DescribeAgentsPaginator = client.get_paginator("describe_agents")
    describe_continuous_exports_paginator: DescribeContinuousExportsPaginator = client.get_paginator("describe_continuous_exports")
    describe_export_configurations_paginator: DescribeExportConfigurationsPaginator = client.get_paginator("describe_export_configurations")
    describe_export_tasks_paginator: DescribeExportTasksPaginator = client.get_paginator("describe_export_tasks")
    describe_tags_paginator: DescribeTagsPaginator = client.get_paginator("describe_tags")
    list_configurations_paginator: ListConfigurationsPaginator = client.get_paginator("list_configurations")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import ConfigurationItemTypeType
from .type_defs import (
    DescribeAgentsResponseTypeDef,
    DescribeContinuousExportsResponseTypeDef,
    DescribeExportConfigurationsResponseTypeDef,
    DescribeExportTasksResponseTypeDef,
    DescribeTagsResponseTypeDef,
    ExportFilterTypeDef,
    FilterTypeDef,
    ListConfigurationsResponseTypeDef,
    OrderByElementTypeDef,
    PaginatorConfigTypeDef,
    TagFilterTypeDef,
)

__all__ = (
    "DescribeAgentsPaginator",
    "DescribeContinuousExportsPaginator",
    "DescribeExportConfigurationsPaginator",
    "DescribeExportTasksPaginator",
    "DescribeTagsPaginator",
    "ListConfigurationsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeAgentsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/discovery.html#ApplicationDiscoveryService.Paginator.DescribeAgents)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_discovery/paginators.html#describeagentspaginator)
    """

    def paginate(
        self,
        *,
        agentIds: Sequence[str] = ...,
        filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeAgentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/discovery.html#ApplicationDiscoveryService.Paginator.DescribeAgents.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_discovery/paginators.html#describeagentspaginator)
        """


class DescribeContinuousExportsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/discovery.html#ApplicationDiscoveryService.Paginator.DescribeContinuousExports)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_discovery/paginators.html#describecontinuousexportspaginator)
    """

    def paginate(
        self, *, exportIds: Sequence[str] = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeContinuousExportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/discovery.html#ApplicationDiscoveryService.Paginator.DescribeContinuousExports.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_discovery/paginators.html#describecontinuousexportspaginator)
        """


class DescribeExportConfigurationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/discovery.html#ApplicationDiscoveryService.Paginator.DescribeExportConfigurations)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_discovery/paginators.html#describeexportconfigurationspaginator)
    """

    def paginate(
        self, *, exportIds: Sequence[str] = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeExportConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/discovery.html#ApplicationDiscoveryService.Paginator.DescribeExportConfigurations.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_discovery/paginators.html#describeexportconfigurationspaginator)
        """


class DescribeExportTasksPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/discovery.html#ApplicationDiscoveryService.Paginator.DescribeExportTasks)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_discovery/paginators.html#describeexporttaskspaginator)
    """

    def paginate(
        self,
        *,
        exportIds: Sequence[str] = ...,
        filters: Sequence["ExportFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeExportTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/discovery.html#ApplicationDiscoveryService.Paginator.DescribeExportTasks.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_discovery/paginators.html#describeexporttaskspaginator)
        """


class DescribeTagsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/discovery.html#ApplicationDiscoveryService.Paginator.DescribeTags)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_discovery/paginators.html#describetagspaginator)
    """

    def paginate(
        self,
        *,
        filters: Sequence["TagFilterTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/discovery.html#ApplicationDiscoveryService.Paginator.DescribeTags.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_discovery/paginators.html#describetagspaginator)
        """


class ListConfigurationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/discovery.html#ApplicationDiscoveryService.Paginator.ListConfigurations)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_discovery/paginators.html#listconfigurationspaginator)
    """

    def paginate(
        self,
        *,
        configurationType: ConfigurationItemTypeType,
        filters: Sequence["FilterTypeDef"] = ...,
        orderBy: Sequence["OrderByElementTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/discovery.html#ApplicationDiscoveryService.Paginator.ListConfigurations.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_discovery/paginators.html#listconfigurationspaginator)
        """
