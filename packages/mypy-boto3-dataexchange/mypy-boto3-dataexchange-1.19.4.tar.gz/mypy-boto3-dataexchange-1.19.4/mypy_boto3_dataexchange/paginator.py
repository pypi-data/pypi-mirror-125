"""
Type annotations for dataexchange service client paginators.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/paginators.html)

Usage::

    ```python
    import boto3

    from mypy_boto3_dataexchange import DataExchangeClient
    from mypy_boto3_dataexchange.paginator import (
        ListDataSetRevisionsPaginator,
        ListDataSetsPaginator,
        ListEventActionsPaginator,
        ListJobsPaginator,
        ListRevisionAssetsPaginator,
    )

    client: DataExchangeClient = boto3.client("dataexchange")

    list_data_set_revisions_paginator: ListDataSetRevisionsPaginator = client.get_paginator("list_data_set_revisions")
    list_data_sets_paginator: ListDataSetsPaginator = client.get_paginator("list_data_sets")
    list_event_actions_paginator: ListEventActionsPaginator = client.get_paginator("list_event_actions")
    list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    list_revision_assets_paginator: ListRevisionAssetsPaginator = client.get_paginator("list_revision_assets")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ListDataSetRevisionsResponseTypeDef,
    ListDataSetsResponseTypeDef,
    ListEventActionsResponseTypeDef,
    ListJobsResponseTypeDef,
    ListRevisionAssetsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListDataSetRevisionsPaginator",
    "ListDataSetsPaginator",
    "ListEventActionsPaginator",
    "ListJobsPaginator",
    "ListRevisionAssetsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListDataSetRevisionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/dataexchange.html#DataExchange.Paginator.ListDataSetRevisions)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/paginators.html#listdatasetrevisionspaginator)
    """

    def paginate(
        self, *, DataSetId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDataSetRevisionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/dataexchange.html#DataExchange.Paginator.ListDataSetRevisions.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/paginators.html#listdatasetrevisionspaginator)
        """


class ListDataSetsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/dataexchange.html#DataExchange.Paginator.ListDataSets)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/paginators.html#listdatasetspaginator)
    """

    def paginate(
        self, *, Origin: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDataSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/dataexchange.html#DataExchange.Paginator.ListDataSets.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/paginators.html#listdatasetspaginator)
        """


class ListEventActionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/dataexchange.html#DataExchange.Paginator.ListEventActions)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/paginators.html#listeventactionspaginator)
    """

    def paginate(
        self, *, EventSourceId: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListEventActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/dataexchange.html#DataExchange.Paginator.ListEventActions.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/paginators.html#listeventactionspaginator)
        """


class ListJobsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/dataexchange.html#DataExchange.Paginator.ListJobs)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/paginators.html#listjobspaginator)
    """

    def paginate(
        self,
        *,
        DataSetId: str = ...,
        RevisionId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/dataexchange.html#DataExchange.Paginator.ListJobs.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/paginators.html#listjobspaginator)
        """


class ListRevisionAssetsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/dataexchange.html#DataExchange.Paginator.ListRevisionAssets)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/paginators.html#listrevisionassetspaginator)
    """

    def paginate(
        self, *, DataSetId: str, RevisionId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRevisionAssetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/dataexchange.html#DataExchange.Paginator.ListRevisionAssets.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/paginators.html#listrevisionassetspaginator)
        """
