# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import proto  # type: ignore

from google.cloud.dataproc_v1.types import shared
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.dataproc.v1",
    manifest={
        "CreateBatchRequest",
        "GetBatchRequest",
        "ListBatchesRequest",
        "ListBatchesResponse",
        "DeleteBatchRequest",
        "Batch",
        "PySparkBatch",
        "SparkBatch",
        "SparkRBatch",
        "SparkSqlBatch",
    },
)


class CreateBatchRequest(proto.Message):
    r"""A request to create a batch workload.

    Attributes:
        parent (str):
            Required. The parent resource where this
            batch will be created.
        batch (google.cloud.dataproc_v1.types.Batch):
            Required. The batch to create.
        batch_id (str):
            Optional. The ID to use for the batch, which will become the
            final component of the batch's resource name.

            This value must be 4-63 characters. Valid characters are
            ``/[a-z][0-9]-/``.
        request_id (str):
            Optional. A unique ID used to identify the request. If the
            service receives two
            `CreateBatchRequest <https://cloud.google.com/dataproc/docs/reference/rpc/google.cloud.dataproc.v1#google.cloud.dataproc.v1.CreateBatchRequest>`__\ s
            with the same request_id, the second request is ignored and
            the Operation that corresponds to the first Batch created
            and stored in the backend is returned.

            Recommendation: Set this value to a
            `UUID <https://en.wikipedia.org/wiki/Universally_unique_identifier>`__.

            The value must contain only letters (a-z, A-Z), numbers
            (0-9), underscores (_), and hyphens (-). The maximum length
            is 40 characters.
    """

    parent = proto.Field(proto.STRING, number=1,)
    batch = proto.Field(proto.MESSAGE, number=2, message="Batch",)
    batch_id = proto.Field(proto.STRING, number=3,)
    request_id = proto.Field(proto.STRING, number=4,)


class GetBatchRequest(proto.Message):
    r"""A request to get the resource representation for a batch
    workload.

    Attributes:
        name (str):
            Required. The name of the batch to retrieve.
    """

    name = proto.Field(proto.STRING, number=1,)


class ListBatchesRequest(proto.Message):
    r"""A request to list batch workloads in a project.

    Attributes:
        parent (str):
            Required. The parent, which owns this
            collection of batches.
        page_size (int):
            Optional. The maximum number of batches to
            return in each response. The service may return
            fewer than this value. The default page size is
            20; the maximum page size is 1000.
        page_token (str):
            Optional. A page token received from a previous
            ``ListBatches`` call. Provide this token to retrieve the
            subsequent page.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)


class ListBatchesResponse(proto.Message):
    r"""A list of batch workloads.

    Attributes:
        batches (Sequence[google.cloud.dataproc_v1.types.Batch]):
            The batches from the specified collection.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    batches = proto.RepeatedField(proto.MESSAGE, number=1, message="Batch",)
    next_page_token = proto.Field(proto.STRING, number=2,)


class DeleteBatchRequest(proto.Message):
    r"""A request to delete a batch workload.

    Attributes:
        name (str):
            Required. The name of the batch resource to
            delete.
    """

    name = proto.Field(proto.STRING, number=1,)


class Batch(proto.Message):
    r"""A representation of a batch workload in the service.

    Attributes:
        name (str):
            Output only. The resource name of the batch.
        uuid (str):
            Output only. A batch UUID (Unique Universal
            Identifier). The service generates this value
            when it creates the batch.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the batch was
            created.
        pyspark_batch (google.cloud.dataproc_v1.types.PySparkBatch):
            Optional. PySpark batch config.
        spark_batch (google.cloud.dataproc_v1.types.SparkBatch):
            Optional. Spark batch config.
        spark_r_batch (google.cloud.dataproc_v1.types.SparkRBatch):
            Optional. SparkR batch config.
        spark_sql_batch (google.cloud.dataproc_v1.types.SparkSqlBatch):
            Optional. SparkSql batch config.
        runtime_info (google.cloud.dataproc_v1.types.RuntimeInfo):
            Output only. Runtime information about batch
            execution.
        state (google.cloud.dataproc_v1.types.Batch.State):
            Output only. The state of the batch.
        state_message (str):
            Output only. Batch state details, such as a failure
            description if the state is ``FAILED``.
        state_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the batch entered
            a current state.
        creator (str):
            Output only. The email address of the user
            who created the batch.
        labels (Sequence[google.cloud.dataproc_v1.types.Batch.LabelsEntry]):
            Optional. The labels to associate with this batch. Label
            **keys** must contain 1 to 63 characters, and must conform
            to `RFC 1035 <https://www.ietf.org/rfc/rfc1035.txt>`__.
            Label **values** may be empty, but, if present, must contain
            1 to 63 characters, and must conform to `RFC
            1035 <https://www.ietf.org/rfc/rfc1035.txt>`__. No more than
            32 labels can be associated with a batch.
        runtime_config (google.cloud.dataproc_v1.types.RuntimeConfig):
            Optional. Runtime configuration for the batch
            execution.
        environment_config (google.cloud.dataproc_v1.types.EnvironmentConfig):
            Optional. Environment configuration for the
            batch execution.
        operation (str):
            Output only. The resource name of the
            operation associated with this batch.
        state_history (Sequence[google.cloud.dataproc_v1.types.Batch.StateHistory]):
            Output only. Historical state information for
            the batch.
    """

    class State(proto.Enum):
        r"""The batch state."""
        STATE_UNSPECIFIED = 0
        PENDING = 1
        RUNNING = 2
        CANCELLING = 3
        CANCELLED = 4
        SUCCEEDED = 5
        FAILED = 6

    class StateHistory(proto.Message):
        r"""Historical state information.

        Attributes:
            state (google.cloud.dataproc_v1.types.Batch.State):
                Output only. The state of the batch at this
                point in history.
            state_message (str):
                Output only. Details about the state at this
                point in history.
            state_start_time (google.protobuf.timestamp_pb2.Timestamp):
                Output only. The time when the batch entered
                the historical state.
        """

        state = proto.Field(proto.ENUM, number=1, enum="Batch.State",)
        state_message = proto.Field(proto.STRING, number=2,)
        state_start_time = proto.Field(
            proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,
        )

    name = proto.Field(proto.STRING, number=1,)
    uuid = proto.Field(proto.STRING, number=2,)
    create_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)
    pyspark_batch = proto.Field(
        proto.MESSAGE, number=4, oneof="batch_config", message="PySparkBatch",
    )
    spark_batch = proto.Field(
        proto.MESSAGE, number=5, oneof="batch_config", message="SparkBatch",
    )
    spark_r_batch = proto.Field(
        proto.MESSAGE, number=6, oneof="batch_config", message="SparkRBatch",
    )
    spark_sql_batch = proto.Field(
        proto.MESSAGE, number=7, oneof="batch_config", message="SparkSqlBatch",
    )
    runtime_info = proto.Field(proto.MESSAGE, number=8, message=shared.RuntimeInfo,)
    state = proto.Field(proto.ENUM, number=9, enum=State,)
    state_message = proto.Field(proto.STRING, number=10,)
    state_time = proto.Field(proto.MESSAGE, number=11, message=timestamp_pb2.Timestamp,)
    creator = proto.Field(proto.STRING, number=12,)
    labels = proto.MapField(proto.STRING, proto.STRING, number=13,)
    runtime_config = proto.Field(
        proto.MESSAGE, number=14, message=shared.RuntimeConfig,
    )
    environment_config = proto.Field(
        proto.MESSAGE, number=15, message=shared.EnvironmentConfig,
    )
    operation = proto.Field(proto.STRING, number=16,)
    state_history = proto.RepeatedField(proto.MESSAGE, number=17, message=StateHistory,)


class PySparkBatch(proto.Message):
    r"""A configuration for running an `Apache
    PySpark <https://spark.apache.org/docs/latest/api/python/getting_started/quickstart.html>`__
    batch workload.

    Attributes:
        main_python_file_uri (str):
            Required. The HCFS URI of the main Python
            file to use as the Spark driver. Must be a .py
            file.
        args (Sequence[str]):
            Optional. The arguments to pass to the driver. Do not
            include arguments that can be set as batch properties, such
            as ``--conf``, since a collision can occur that causes an
            incorrect batch submission.
        python_file_uris (Sequence[str]):
            Optional. HCFS file URIs of Python files to pass to the
            PySpark framework. Supported file types: ``.py``, ``.egg``,
            and ``.zip``.
        jar_file_uris (Sequence[str]):
            Optional. HCFS URIs of jar files to add to
            the classpath of the Spark driver and tasks.
        file_uris (Sequence[str]):
            Optional. HCFS URIs of files to be placed in
            the working directory of each executor.
        archive_uris (Sequence[str]):
            Optional. HCFS URIs of archives to be extracted into the
            working directory of each executor. Supported file types:
            ``.jar``, ``.tar``, ``.tar.gz``, ``.tgz``, and ``.zip``.
    """

    main_python_file_uri = proto.Field(proto.STRING, number=1,)
    args = proto.RepeatedField(proto.STRING, number=2,)
    python_file_uris = proto.RepeatedField(proto.STRING, number=3,)
    jar_file_uris = proto.RepeatedField(proto.STRING, number=4,)
    file_uris = proto.RepeatedField(proto.STRING, number=5,)
    archive_uris = proto.RepeatedField(proto.STRING, number=6,)


class SparkBatch(proto.Message):
    r"""A configuration for running an `Apache
    Spark <http://spark.apache.org/>`__ batch workload.

    Attributes:
        main_jar_file_uri (str):
            Optional. The HCFS URI of the jar file that
            contains the main class.
        main_class (str):
            Optional. The name of the driver main class. The jar file
            that contains the class must be in the classpath or
            specified in ``jar_file_uris``.
        args (Sequence[str]):
            Optional. The arguments to pass to the driver. Do not
            include arguments that can be set as batch properties, such
            as ``--conf``, since a collision can occur that causes an
            incorrect batch submission.
        jar_file_uris (Sequence[str]):
            Optional. HCFS URIs of jar files to add to
            the classpath of the Spark driver and tasks.
        file_uris (Sequence[str]):
            Optional. HCFS URIs of files to be placed in
            the working directory of each executor.
        archive_uris (Sequence[str]):
            Optional. HCFS URIs of archives to be extracted into the
            working directory of each executor. Supported file types:
            ``.jar``, ``.tar``, ``.tar.gz``, ``.tgz``, and ``.zip``.
    """

    main_jar_file_uri = proto.Field(proto.STRING, number=1, oneof="driver",)
    main_class = proto.Field(proto.STRING, number=2, oneof="driver",)
    args = proto.RepeatedField(proto.STRING, number=3,)
    jar_file_uris = proto.RepeatedField(proto.STRING, number=4,)
    file_uris = proto.RepeatedField(proto.STRING, number=5,)
    archive_uris = proto.RepeatedField(proto.STRING, number=6,)


class SparkRBatch(proto.Message):
    r"""A configuration for running an `Apache
    SparkR <https://spark.apache.org/docs/latest/sparkr.html>`__ batch
    workload.

    Attributes:
        main_r_file_uri (str):
            Required. The HCFS URI of the main R file to use as the
            driver. Must be a ``.R`` or ``.r`` file.
        args (Sequence[str]):
            Optional. The arguments to pass to the Spark driver. Do not
            include arguments that can be set as batch properties, such
            as ``--conf``, since a collision can occur that causes an
            incorrect batch submission.
        file_uris (Sequence[str]):
            Optional. HCFS URIs of files to be placed in
            the working directory of each executor.
        archive_uris (Sequence[str]):
            Optional. HCFS URIs of archives to be extracted into the
            working directory of each executor. Supported file types:
            ``.jar``, ``.tar``, ``.tar.gz``, ``.tgz``, and ``.zip``.
    """

    main_r_file_uri = proto.Field(proto.STRING, number=1,)
    args = proto.RepeatedField(proto.STRING, number=2,)
    file_uris = proto.RepeatedField(proto.STRING, number=3,)
    archive_uris = proto.RepeatedField(proto.STRING, number=4,)


class SparkSqlBatch(proto.Message):
    r"""A configuration for running `Apache Spark
    SQL <http://spark.apache.org/sql/>`__ queries as a batch workload.

    Attributes:
        query_file_uri (str):
            Required. The HCFS URI of the script that
            contains Spark SQL queries to execute.
        query_variables (Sequence[google.cloud.dataproc_v1.types.SparkSqlBatch.QueryVariablesEntry]):
            Optional. Mapping of query variable names to values
            (equivalent to the Spark SQL command:
            ``SET name="value";``).
        jar_file_uris (Sequence[str]):
            Optional. HCFS URIs of jar files to be added
            to the Spark CLASSPATH.
    """

    query_file_uri = proto.Field(proto.STRING, number=1,)
    query_variables = proto.MapField(proto.STRING, proto.STRING, number=2,)
    jar_file_uris = proto.RepeatedField(proto.STRING, number=3,)


__all__ = tuple(sorted(__protobuf__.manifest))
