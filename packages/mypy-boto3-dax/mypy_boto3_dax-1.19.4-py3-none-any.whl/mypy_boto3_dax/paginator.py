"""
Type annotations for dax service client paginators.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dax/paginators.html)

Usage::

    ```python
    import boto3

    from mypy_boto3_dax import DAXClient
    from mypy_boto3_dax.paginator import (
        DescribeClustersPaginator,
        DescribeDefaultParametersPaginator,
        DescribeEventsPaginator,
        DescribeParameterGroupsPaginator,
        DescribeParametersPaginator,
        DescribeSubnetGroupsPaginator,
        ListTagsPaginator,
    )

    client: DAXClient = boto3.client("dax")

    describe_clusters_paginator: DescribeClustersPaginator = client.get_paginator("describe_clusters")
    describe_default_parameters_paginator: DescribeDefaultParametersPaginator = client.get_paginator("describe_default_parameters")
    describe_events_paginator: DescribeEventsPaginator = client.get_paginator("describe_events")
    describe_parameter_groups_paginator: DescribeParameterGroupsPaginator = client.get_paginator("describe_parameter_groups")
    describe_parameters_paginator: DescribeParametersPaginator = client.get_paginator("describe_parameters")
    describe_subnet_groups_paginator: DescribeSubnetGroupsPaginator = client.get_paginator("describe_subnet_groups")
    list_tags_paginator: ListTagsPaginator = client.get_paginator("list_tags")
    ```
"""
from datetime import datetime
from typing import Generic, Iterator, Sequence, TypeVar, Union

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import SourceTypeType
from .type_defs import (
    DescribeClustersResponseTypeDef,
    DescribeDefaultParametersResponseTypeDef,
    DescribeEventsResponseTypeDef,
    DescribeParameterGroupsResponseTypeDef,
    DescribeParametersResponseTypeDef,
    DescribeSubnetGroupsResponseTypeDef,
    ListTagsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "DescribeClustersPaginator",
    "DescribeDefaultParametersPaginator",
    "DescribeEventsPaginator",
    "DescribeParameterGroupsPaginator",
    "DescribeParametersPaginator",
    "DescribeSubnetGroupsPaginator",
    "ListTagsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeClustersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/dax.html#DAX.Paginator.DescribeClusters)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dax/paginators.html#describeclusterspaginator)
    """

    def paginate(
        self, *, ClusterNames: Sequence[str] = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/dax.html#DAX.Paginator.DescribeClusters.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dax/paginators.html#describeclusterspaginator)
        """


class DescribeDefaultParametersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/dax.html#DAX.Paginator.DescribeDefaultParameters)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dax/paginators.html#describedefaultparameterspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeDefaultParametersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/dax.html#DAX.Paginator.DescribeDefaultParameters.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dax/paginators.html#describedefaultparameterspaginator)
        """


class DescribeEventsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/dax.html#DAX.Paginator.DescribeEvents)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dax/paginators.html#describeeventspaginator)
    """

    def paginate(
        self,
        *,
        SourceName: str = ...,
        SourceType: SourceTypeType = ...,
        StartTime: Union[datetime, str] = ...,
        EndTime: Union[datetime, str] = ...,
        Duration: int = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/dax.html#DAX.Paginator.DescribeEvents.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dax/paginators.html#describeeventspaginator)
        """


class DescribeParameterGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/dax.html#DAX.Paginator.DescribeParameterGroups)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dax/paginators.html#describeparametergroupspaginator)
    """

    def paginate(
        self,
        *,
        ParameterGroupNames: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeParameterGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/dax.html#DAX.Paginator.DescribeParameterGroups.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dax/paginators.html#describeparametergroupspaginator)
        """


class DescribeParametersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/dax.html#DAX.Paginator.DescribeParameters)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dax/paginators.html#describeparameterspaginator)
    """

    def paginate(
        self,
        *,
        ParameterGroupName: str,
        Source: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeParametersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/dax.html#DAX.Paginator.DescribeParameters.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dax/paginators.html#describeparameterspaginator)
        """


class DescribeSubnetGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/dax.html#DAX.Paginator.DescribeSubnetGroups)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dax/paginators.html#describesubnetgroupspaginator)
    """

    def paginate(
        self,
        *,
        SubnetGroupNames: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeSubnetGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/dax.html#DAX.Paginator.DescribeSubnetGroups.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dax/paginators.html#describesubnetgroupspaginator)
        """


class ListTagsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/dax.html#DAX.Paginator.ListTags)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dax/paginators.html#listtagspaginator)
    """

    def paginate(
        self, *, ResourceName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/dax.html#DAX.Paginator.ListTags.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dax/paginators.html#listtagspaginator)
        """
