"""
Type annotations for codeartifact service client.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html)

Usage::

    ```python
    import boto3
    from mypy_boto3_codeartifact import CodeArtifactClient

    client: CodeArtifactClient = boto3.client("codeartifact")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import PackageFormatType, PackageVersionStatusType
from .paginator import (
    ListDomainsPaginator,
    ListPackagesPaginator,
    ListPackageVersionAssetsPaginator,
    ListPackageVersionsPaginator,
    ListRepositoriesInDomainPaginator,
    ListRepositoriesPaginator,
)
from .type_defs import (
    AssociateExternalConnectionResultTypeDef,
    CopyPackageVersionsResultTypeDef,
    CreateDomainResultTypeDef,
    CreateRepositoryResultTypeDef,
    DeleteDomainPermissionsPolicyResultTypeDef,
    DeleteDomainResultTypeDef,
    DeletePackageVersionsResultTypeDef,
    DeleteRepositoryPermissionsPolicyResultTypeDef,
    DeleteRepositoryResultTypeDef,
    DescribeDomainResultTypeDef,
    DescribePackageVersionResultTypeDef,
    DescribeRepositoryResultTypeDef,
    DisassociateExternalConnectionResultTypeDef,
    DisposePackageVersionsResultTypeDef,
    GetAuthorizationTokenResultTypeDef,
    GetDomainPermissionsPolicyResultTypeDef,
    GetPackageVersionAssetResultTypeDef,
    GetPackageVersionReadmeResultTypeDef,
    GetRepositoryEndpointResultTypeDef,
    GetRepositoryPermissionsPolicyResultTypeDef,
    ListDomainsResultTypeDef,
    ListPackagesResultTypeDef,
    ListPackageVersionAssetsResultTypeDef,
    ListPackageVersionDependenciesResultTypeDef,
    ListPackageVersionsResultTypeDef,
    ListRepositoriesInDomainResultTypeDef,
    ListRepositoriesResultTypeDef,
    ListTagsForResourceResultTypeDef,
    PutDomainPermissionsPolicyResultTypeDef,
    PutRepositoryPermissionsPolicyResultTypeDef,
    TagTypeDef,
    UpdatePackageVersionsStatusResultTypeDef,
    UpdateRepositoryResultTypeDef,
    UpstreamRepositoryTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("CodeArtifactClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class CodeArtifactClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CodeArtifactClient exceptions.
        """

    def associate_external_connection(
        self, *, domain: str, repository: str, externalConnection: str, domainOwner: str = ...
    ) -> AssociateExternalConnectionResultTypeDef:
        """
        Adds an existing external connection to a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.associate_external_connection)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#associate_external_connection)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.can_paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#can_paginate)
        """

    def copy_package_versions(
        self,
        *,
        domain: str,
        sourceRepository: str,
        destinationRepository: str,
        format: PackageFormatType,
        package: str,
        domainOwner: str = ...,
        namespace: str = ...,
        versions: Sequence[str] = ...,
        versionRevisions: Mapping[str, str] = ...,
        allowOverwrite: bool = ...,
        includeFromUpstream: bool = ...
    ) -> CopyPackageVersionsResultTypeDef:
        """
        Copies package versions from one repository to another repository in the same
        domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.copy_package_versions)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#copy_package_versions)
        """

    def create_domain(
        self, *, domain: str, encryptionKey: str = ..., tags: Sequence["TagTypeDef"] = ...
    ) -> CreateDomainResultTypeDef:
        """
        Creates a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.create_domain)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#create_domain)
        """

    def create_repository(
        self,
        *,
        domain: str,
        repository: str,
        domainOwner: str = ...,
        description: str = ...,
        upstreams: Sequence["UpstreamRepositoryTypeDef"] = ...,
        tags: Sequence["TagTypeDef"] = ...
    ) -> CreateRepositoryResultTypeDef:
        """
        Creates a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.create_repository)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#create_repository)
        """

    def delete_domain(self, *, domain: str, domainOwner: str = ...) -> DeleteDomainResultTypeDef:
        """
        Deletes a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.delete_domain)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#delete_domain)
        """

    def delete_domain_permissions_policy(
        self, *, domain: str, domainOwner: str = ..., policyRevision: str = ...
    ) -> DeleteDomainPermissionsPolicyResultTypeDef:
        """
        Deletes the resource policy set on a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.delete_domain_permissions_policy)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#delete_domain_permissions_policy)
        """

    def delete_package_versions(
        self,
        *,
        domain: str,
        repository: str,
        format: PackageFormatType,
        package: str,
        versions: Sequence[str],
        domainOwner: str = ...,
        namespace: str = ...,
        expectedStatus: PackageVersionStatusType = ...
    ) -> DeletePackageVersionsResultTypeDef:
        """
        Deletes one or more versions of a package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.delete_package_versions)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#delete_package_versions)
        """

    def delete_repository(
        self, *, domain: str, repository: str, domainOwner: str = ...
    ) -> DeleteRepositoryResultTypeDef:
        """
        Deletes a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.delete_repository)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#delete_repository)
        """

    def delete_repository_permissions_policy(
        self, *, domain: str, repository: str, domainOwner: str = ..., policyRevision: str = ...
    ) -> DeleteRepositoryPermissionsPolicyResultTypeDef:
        """
        Deletes the resource policy that is set on a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.delete_repository_permissions_policy)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#delete_repository_permissions_policy)
        """

    def describe_domain(
        self, *, domain: str, domainOwner: str = ...
    ) -> DescribeDomainResultTypeDef:
        """
        Returns a `DomainDescription <https://docs.aws.amazon.com/codeartifact/latest/AP
        IReference/API_DomainDescription.html>`__ object that contains information about
        the requested domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.describe_domain)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#describe_domain)
        """

    def describe_package_version(
        self,
        *,
        domain: str,
        repository: str,
        format: PackageFormatType,
        package: str,
        packageVersion: str,
        domainOwner: str = ...,
        namespace: str = ...
    ) -> DescribePackageVersionResultTypeDef:
        """
        Returns a `PackageVersionDescription <https://docs.aws.amazon.com/codeartifact/l
        atest/APIReference/API_PackageVersionDescription.html>`__ object that contains
        information about the requested package version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.describe_package_version)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#describe_package_version)
        """

    def describe_repository(
        self, *, domain: str, repository: str, domainOwner: str = ...
    ) -> DescribeRepositoryResultTypeDef:
        """
        Returns a `RepositoryDescription` object that contains detailed information
        about the requested repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.describe_repository)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#describe_repository)
        """

    def disassociate_external_connection(
        self, *, domain: str, repository: str, externalConnection: str, domainOwner: str = ...
    ) -> DisassociateExternalConnectionResultTypeDef:
        """
        Removes an existing external connection from a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.disassociate_external_connection)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#disassociate_external_connection)
        """

    def dispose_package_versions(
        self,
        *,
        domain: str,
        repository: str,
        format: PackageFormatType,
        package: str,
        versions: Sequence[str],
        domainOwner: str = ...,
        namespace: str = ...,
        versionRevisions: Mapping[str, str] = ...,
        expectedStatus: PackageVersionStatusType = ...
    ) -> DisposePackageVersionsResultTypeDef:
        """
        Deletes the assets in package versions and sets the package versions' status to
        `Disposed`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.dispose_package_versions)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#dispose_package_versions)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#generate_presigned_url)
        """

    def get_authorization_token(
        self, *, domain: str, domainOwner: str = ..., durationSeconds: int = ...
    ) -> GetAuthorizationTokenResultTypeDef:
        """
        Generates a temporary authorization token for accessing repositories in the
        domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.get_authorization_token)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#get_authorization_token)
        """

    def get_domain_permissions_policy(
        self, *, domain: str, domainOwner: str = ...
    ) -> GetDomainPermissionsPolicyResultTypeDef:
        """
        Returns the resource policy attached to the specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.get_domain_permissions_policy)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#get_domain_permissions_policy)
        """

    def get_package_version_asset(
        self,
        *,
        domain: str,
        repository: str,
        format: PackageFormatType,
        package: str,
        packageVersion: str,
        asset: str,
        domainOwner: str = ...,
        namespace: str = ...,
        packageVersionRevision: str = ...
    ) -> GetPackageVersionAssetResultTypeDef:
        """
        Returns an asset (or file) that is in a package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.get_package_version_asset)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#get_package_version_asset)
        """

    def get_package_version_readme(
        self,
        *,
        domain: str,
        repository: str,
        format: PackageFormatType,
        package: str,
        packageVersion: str,
        domainOwner: str = ...,
        namespace: str = ...
    ) -> GetPackageVersionReadmeResultTypeDef:
        """
        Gets the readme file or descriptive text for a package version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.get_package_version_readme)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#get_package_version_readme)
        """

    def get_repository_endpoint(
        self, *, domain: str, repository: str, format: PackageFormatType, domainOwner: str = ...
    ) -> GetRepositoryEndpointResultTypeDef:
        """
        Returns the endpoint of a repository for a specific package format.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.get_repository_endpoint)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#get_repository_endpoint)
        """

    def get_repository_permissions_policy(
        self, *, domain: str, repository: str, domainOwner: str = ...
    ) -> GetRepositoryPermissionsPolicyResultTypeDef:
        """
        Returns the resource policy that is set on a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.get_repository_permissions_policy)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#get_repository_permissions_policy)
        """

    def list_domains(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListDomainsResultTypeDef:
        """
        Returns a list of `DomainSummary <https://docs.aws.amazon.com/codeartifact/lates
        t/APIReference/API_PackageVersionDescription.html>`__ objects for all domains
        owned by the AWS account that makes this call.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.list_domains)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#list_domains)
        """

    def list_package_version_assets(
        self,
        *,
        domain: str,
        repository: str,
        format: PackageFormatType,
        package: str,
        packageVersion: str,
        domainOwner: str = ...,
        namespace: str = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListPackageVersionAssetsResultTypeDef:
        """
        Returns a list of `AssetSummary <https://docs.aws.amazon.com/codeartifact/latest
        /APIReference/API_AssetSummary.html>`__ objects for assets in a package version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.list_package_version_assets)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#list_package_version_assets)
        """

    def list_package_version_dependencies(
        self,
        *,
        domain: str,
        repository: str,
        format: PackageFormatType,
        package: str,
        packageVersion: str,
        domainOwner: str = ...,
        namespace: str = ...,
        nextToken: str = ...
    ) -> ListPackageVersionDependenciesResultTypeDef:
        """
        Returns the direct dependencies for a package version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.list_package_version_dependencies)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#list_package_version_dependencies)
        """

    def list_package_versions(
        self,
        *,
        domain: str,
        repository: str,
        format: PackageFormatType,
        package: str,
        domainOwner: str = ...,
        namespace: str = ...,
        status: PackageVersionStatusType = ...,
        sortBy: Literal["PUBLISHED_TIME"] = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListPackageVersionsResultTypeDef:
        """
        Returns a list of `PackageVersionSummary <https://docs.aws.amazon.com/codeartifa
        ct/latest/APIReference/API_PackageVersionSummary.html>`__ objects for package
        versions in a repository that match the request parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.list_package_versions)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#list_package_versions)
        """

    def list_packages(
        self,
        *,
        domain: str,
        repository: str,
        domainOwner: str = ...,
        format: PackageFormatType = ...,
        namespace: str = ...,
        packagePrefix: str = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListPackagesResultTypeDef:
        """
        Returns a list of `PackageSummary <https://docs.aws.amazon.com/codeartifact/late
        st/APIReference/API_PackageSummary.html>`__ objects for packages in a repository
        that match the request parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.list_packages)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#list_packages)
        """

    def list_repositories(
        self, *, repositoryPrefix: str = ..., maxResults: int = ..., nextToken: str = ...
    ) -> ListRepositoriesResultTypeDef:
        """
        Returns a list of `RepositorySummary <https://docs.aws.amazon.com/codeartifact/l
        atest/APIReference/API_RepositorySummary.html>`__ objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.list_repositories)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#list_repositories)
        """

    def list_repositories_in_domain(
        self,
        *,
        domain: str,
        domainOwner: str = ...,
        administratorAccount: str = ...,
        repositoryPrefix: str = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListRepositoriesInDomainResultTypeDef:
        """
        Returns a list of `RepositorySummary <https://docs.aws.amazon.com/codeartifact/l
        atest/APIReference/API_RepositorySummary.html>`__ objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.list_repositories_in_domain)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#list_repositories_in_domain)
        """

    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResultTypeDef:
        """
        Gets information about AWS tags for a specified Amazon Resource Name (ARN) in
        AWS CodeArtifact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#list_tags_for_resource)
        """

    def put_domain_permissions_policy(
        self, *, domain: str, policyDocument: str, domainOwner: str = ..., policyRevision: str = ...
    ) -> PutDomainPermissionsPolicyResultTypeDef:
        """
        Sets a resource policy on a domain that specifies permissions to access it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.put_domain_permissions_policy)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#put_domain_permissions_policy)
        """

    def put_repository_permissions_policy(
        self,
        *,
        domain: str,
        repository: str,
        policyDocument: str,
        domainOwner: str = ...,
        policyRevision: str = ...
    ) -> PutRepositoryPermissionsPolicyResultTypeDef:
        """
        Sets the resource policy on a repository that specifies permissions to access
        it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.put_repository_permissions_policy)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#put_repository_permissions_policy)
        """

    def tag_resource(self, *, resourceArn: str, tags: Sequence["TagTypeDef"]) -> Dict[str, Any]:
        """
        Adds or updates tags for a resource in AWS CodeArtifact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.tag_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#tag_resource)
        """

    def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes tags from a resource in AWS CodeArtifact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.untag_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#untag_resource)
        """

    def update_package_versions_status(
        self,
        *,
        domain: str,
        repository: str,
        format: PackageFormatType,
        package: str,
        versions: Sequence[str],
        targetStatus: PackageVersionStatusType,
        domainOwner: str = ...,
        namespace: str = ...,
        versionRevisions: Mapping[str, str] = ...,
        expectedStatus: PackageVersionStatusType = ...
    ) -> UpdatePackageVersionsStatusResultTypeDef:
        """
        Updates the status of one or more versions of a package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.update_package_versions_status)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#update_package_versions_status)
        """

    def update_repository(
        self,
        *,
        domain: str,
        repository: str,
        domainOwner: str = ...,
        description: str = ...,
        upstreams: Sequence["UpstreamRepositoryTypeDef"] = ...
    ) -> UpdateRepositoryResultTypeDef:
        """
        Update the properties of a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Client.update_repository)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/client.html#update_repository)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_domains"]) -> ListDomainsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Paginator.ListDomains)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/paginators.html#listdomainspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_package_version_assets"]
    ) -> ListPackageVersionAssetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Paginator.ListPackageVersionAssets)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/paginators.html#listpackageversionassetspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_package_versions"]
    ) -> ListPackageVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Paginator.ListPackageVersions)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/paginators.html#listpackageversionspaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_packages"]) -> ListPackagesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Paginator.ListPackages)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/paginators.html#listpackagespaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_repositories"]
    ) -> ListRepositoriesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Paginator.ListRepositories)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/paginators.html#listrepositoriespaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_repositories_in_domain"]
    ) -> ListRepositoriesInDomainPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/codeartifact.html#CodeArtifact.Paginator.ListRepositoriesInDomain)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/paginators.html#listrepositoriesindomainpaginator)
        """
