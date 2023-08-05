"""
Type annotations for batch service client.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html)

Usage::

    ```python
    import boto3
    from mypy_boto3_batch import BatchClient

    client: BatchClient = boto3.client("batch")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    CEStateType,
    CETypeType,
    JobDefinitionTypeType,
    JobStatusType,
    JQStateType,
    PlatformCapabilityType,
)
from .paginator import (
    DescribeComputeEnvironmentsPaginator,
    DescribeJobDefinitionsPaginator,
    DescribeJobQueuesPaginator,
    ListJobsPaginator,
)
from .type_defs import (
    ArrayPropertiesTypeDef,
    ComputeEnvironmentOrderTypeDef,
    ComputeResourceTypeDef,
    ComputeResourceUpdateTypeDef,
    ContainerOverridesTypeDef,
    ContainerPropertiesTypeDef,
    CreateComputeEnvironmentResponseTypeDef,
    CreateJobQueueResponseTypeDef,
    DescribeComputeEnvironmentsResponseTypeDef,
    DescribeJobDefinitionsResponseTypeDef,
    DescribeJobQueuesResponseTypeDef,
    DescribeJobsResponseTypeDef,
    JobDependencyTypeDef,
    JobTimeoutTypeDef,
    KeyValuesPairTypeDef,
    ListJobsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    NodeOverridesTypeDef,
    NodePropertiesTypeDef,
    RegisterJobDefinitionResponseTypeDef,
    RetryStrategyTypeDef,
    SubmitJobResponseTypeDef,
    UpdateComputeEnvironmentResponseTypeDef,
    UpdateJobQueueResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("BatchClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ClientException: Type[BotocoreClientError]
    ServerException: Type[BotocoreClientError]


class BatchClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/batch.html#Batch.Client)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        BatchClient exceptions.
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/batch.html#Batch.Client.can_paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#can_paginate)
        """

    def cancel_job(self, *, jobId: str, reason: str) -> Dict[str, Any]:
        """
        Cancels a job in an Batch job queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/batch.html#Batch.Client.cancel_job)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#cancel_job)
        """

    def create_compute_environment(
        self,
        *,
        computeEnvironmentName: str,
        type: CETypeType,
        state: CEStateType = ...,
        computeResources: "ComputeResourceTypeDef" = ...,
        serviceRole: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateComputeEnvironmentResponseTypeDef:
        """
        Creates an Batch compute environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/batch.html#Batch.Client.create_compute_environment)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#create_compute_environment)
        """

    def create_job_queue(
        self,
        *,
        jobQueueName: str,
        priority: int,
        computeEnvironmentOrder: Sequence["ComputeEnvironmentOrderTypeDef"],
        state: JQStateType = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateJobQueueResponseTypeDef:
        """
        Creates an Batch job queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/batch.html#Batch.Client.create_job_queue)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#create_job_queue)
        """

    def delete_compute_environment(self, *, computeEnvironment: str) -> Dict[str, Any]:
        """
        Deletes an Batch compute environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/batch.html#Batch.Client.delete_compute_environment)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#delete_compute_environment)
        """

    def delete_job_queue(self, *, jobQueue: str) -> Dict[str, Any]:
        """
        Deletes the specified job queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/batch.html#Batch.Client.delete_job_queue)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#delete_job_queue)
        """

    def deregister_job_definition(self, *, jobDefinition: str) -> Dict[str, Any]:
        """
        Deregisters an Batch job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/batch.html#Batch.Client.deregister_job_definition)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#deregister_job_definition)
        """

    def describe_compute_environments(
        self,
        *,
        computeEnvironments: Sequence[str] = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> DescribeComputeEnvironmentsResponseTypeDef:
        """
        Describes one or more of your compute environments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/batch.html#Batch.Client.describe_compute_environments)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#describe_compute_environments)
        """

    def describe_job_definitions(
        self,
        *,
        jobDefinitions: Sequence[str] = ...,
        maxResults: int = ...,
        jobDefinitionName: str = ...,
        status: str = ...,
        nextToken: str = ...
    ) -> DescribeJobDefinitionsResponseTypeDef:
        """
        Describes a list of job definitions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/batch.html#Batch.Client.describe_job_definitions)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#describe_job_definitions)
        """

    def describe_job_queues(
        self, *, jobQueues: Sequence[str] = ..., maxResults: int = ..., nextToken: str = ...
    ) -> DescribeJobQueuesResponseTypeDef:
        """
        Describes one or more of your job queues.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/batch.html#Batch.Client.describe_job_queues)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#describe_job_queues)
        """

    def describe_jobs(self, *, jobs: Sequence[str]) -> DescribeJobsResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/batch.html#Batch.Client.describe_jobs)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#describe_jobs)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/batch.html#Batch.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#generate_presigned_url)
        """

    def list_jobs(
        self,
        *,
        jobQueue: str = ...,
        arrayJobId: str = ...,
        multiNodeJobId: str = ...,
        jobStatus: JobStatusType = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        filters: Sequence["KeyValuesPairTypeDef"] = ...
    ) -> ListJobsResponseTypeDef:
        """
        Returns a list of Batch jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/batch.html#Batch.Client.list_jobs)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#list_jobs)
        """

    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for an Batch resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/batch.html#Batch.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#list_tags_for_resource)
        """

    def register_job_definition(
        self,
        *,
        jobDefinitionName: str,
        type: JobDefinitionTypeType,
        parameters: Mapping[str, str] = ...,
        containerProperties: "ContainerPropertiesTypeDef" = ...,
        nodeProperties: "NodePropertiesTypeDef" = ...,
        retryStrategy: "RetryStrategyTypeDef" = ...,
        propagateTags: bool = ...,
        timeout: "JobTimeoutTypeDef" = ...,
        tags: Mapping[str, str] = ...,
        platformCapabilities: Sequence[PlatformCapabilityType] = ...
    ) -> RegisterJobDefinitionResponseTypeDef:
        """
        Registers an Batch job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/batch.html#Batch.Client.register_job_definition)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#register_job_definition)
        """

    def submit_job(
        self,
        *,
        jobName: str,
        jobQueue: str,
        jobDefinition: str,
        arrayProperties: "ArrayPropertiesTypeDef" = ...,
        dependsOn: Sequence["JobDependencyTypeDef"] = ...,
        parameters: Mapping[str, str] = ...,
        containerOverrides: "ContainerOverridesTypeDef" = ...,
        nodeOverrides: "NodeOverridesTypeDef" = ...,
        retryStrategy: "RetryStrategyTypeDef" = ...,
        propagateTags: bool = ...,
        timeout: "JobTimeoutTypeDef" = ...,
        tags: Mapping[str, str] = ...
    ) -> SubmitJobResponseTypeDef:
        """
        Submits an Batch job from a job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/batch.html#Batch.Client.submit_job)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#submit_job)
        """

    def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Associates the specified tags to a resource with the specified `resourceArn`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/batch.html#Batch.Client.tag_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#tag_resource)
        """

    def terminate_job(self, *, jobId: str, reason: str) -> Dict[str, Any]:
        """
        Terminates a job in a job queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/batch.html#Batch.Client.terminate_job)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#terminate_job)
        """

    def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Deletes specified tags from an Batch resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/batch.html#Batch.Client.untag_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#untag_resource)
        """

    def update_compute_environment(
        self,
        *,
        computeEnvironment: str,
        state: CEStateType = ...,
        computeResources: "ComputeResourceUpdateTypeDef" = ...,
        serviceRole: str = ...
    ) -> UpdateComputeEnvironmentResponseTypeDef:
        """
        Updates an Batch compute environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/batch.html#Batch.Client.update_compute_environment)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#update_compute_environment)
        """

    def update_job_queue(
        self,
        *,
        jobQueue: str,
        state: JQStateType = ...,
        priority: int = ...,
        computeEnvironmentOrder: Sequence["ComputeEnvironmentOrderTypeDef"] = ...
    ) -> UpdateJobQueueResponseTypeDef:
        """
        Updates a job queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/batch.html#Batch.Client.update_job_queue)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/client.html#update_job_queue)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_compute_environments"]
    ) -> DescribeComputeEnvironmentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/batch.html#Batch.Paginator.DescribeComputeEnvironments)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/paginators.html#describecomputeenvironmentspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_job_definitions"]
    ) -> DescribeJobDefinitionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/batch.html#Batch.Paginator.DescribeJobDefinitions)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/paginators.html#describejobdefinitionspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_job_queues"]
    ) -> DescribeJobQueuesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/batch.html#Batch.Paginator.DescribeJobQueues)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/paginators.html#describejobqueuespaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_jobs"]) -> ListJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.4/reference/services/batch.html#Batch.Paginator.ListJobs)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_batch/paginators.html#listjobspaginator)
        """
