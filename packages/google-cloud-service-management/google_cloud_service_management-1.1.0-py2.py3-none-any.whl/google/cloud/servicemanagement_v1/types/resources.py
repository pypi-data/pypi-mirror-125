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

from google.api import config_change_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.api.servicemanagement.v1",
    manifest={
        "ManagedService",
        "OperationMetadata",
        "Diagnostic",
        "ConfigSource",
        "ConfigFile",
        "ConfigRef",
        "ChangeReport",
        "Rollout",
    },
)


class ManagedService(proto.Message):
    r"""The full representation of a Service that is managed by
    Google Service Management.

    Attributes:
        service_name (str):
            The name of the service. See the
            `overview <https://cloud.google.com/service-management/overview>`__
            for naming requirements.
        producer_project_id (str):
            ID of the project that produces and owns this
            service.
    """

    service_name = proto.Field(proto.STRING, number=2,)
    producer_project_id = proto.Field(proto.STRING, number=3,)


class OperationMetadata(proto.Message):
    r"""The metadata associated with a long running operation
    resource.

    Attributes:
        resource_names (Sequence[str]):
            The full name of the resources that this
            operation is directly associated with.
        steps (Sequence[google.cloud.servicemanagement_v1.types.OperationMetadata.Step]):
            Detailed status information for each step.
            The order is undetermined.
        progress_percentage (int):
            Percentage of completion of this operation,
            ranging from 0 to 100.
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            The start time of the operation.
    """

    class Status(proto.Enum):
        r"""Code describes the status of the operation (or one of its
        steps).
        """
        STATUS_UNSPECIFIED = 0
        DONE = 1
        NOT_STARTED = 2
        IN_PROGRESS = 3
        FAILED = 4
        CANCELLED = 5

    class Step(proto.Message):
        r"""Represents the status of one operation step.

        Attributes:
            description (str):
                The short description of the step.
            status (google.cloud.servicemanagement_v1.types.OperationMetadata.Status):
                The status code.
        """

        description = proto.Field(proto.STRING, number=2,)
        status = proto.Field(proto.ENUM, number=4, enum="OperationMetadata.Status",)

    resource_names = proto.RepeatedField(proto.STRING, number=1,)
    steps = proto.RepeatedField(proto.MESSAGE, number=2, message=Step,)
    progress_percentage = proto.Field(proto.INT32, number=3,)
    start_time = proto.Field(proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,)


class Diagnostic(proto.Message):
    r"""Represents a diagnostic message (error or warning)

    Attributes:
        location (str):
            File name and line number of the error or
            warning.
        kind (google.cloud.servicemanagement_v1.types.Diagnostic.Kind):
            The kind of diagnostic information provided.
        message (str):
            Message describing the error or warning.
    """

    class Kind(proto.Enum):
        r"""The kind of diagnostic information possible."""
        WARNING = 0
        ERROR = 1

    location = proto.Field(proto.STRING, number=1,)
    kind = proto.Field(proto.ENUM, number=2, enum=Kind,)
    message = proto.Field(proto.STRING, number=3,)


class ConfigSource(proto.Message):
    r"""Represents a source file which is used to generate the service
    configuration defined by ``google.api.Service``.

    Attributes:
        id (str):
            A unique ID for a specific instance of this
            message, typically assigned by the client for
            tracking purpose. If empty, the server may
            choose to generate one instead.
        files (Sequence[google.cloud.servicemanagement_v1.types.ConfigFile]):
            Set of source configuration files that are used to generate
            a service configuration (``google.api.Service``).
    """

    id = proto.Field(proto.STRING, number=5,)
    files = proto.RepeatedField(proto.MESSAGE, number=2, message="ConfigFile",)


class ConfigFile(proto.Message):
    r"""Generic specification of a source configuration file

    Attributes:
        file_path (str):
            The file name of the configuration file (full
            or relative path).
        file_contents (bytes):
            The bytes that constitute the file.
        file_type (google.cloud.servicemanagement_v1.types.ConfigFile.FileType):
            The type of configuration file this
            represents.
    """

    class FileType(proto.Enum):
        r""""""
        FILE_TYPE_UNSPECIFIED = 0
        SERVICE_CONFIG_YAML = 1
        OPEN_API_JSON = 2
        OPEN_API_YAML = 3
        FILE_DESCRIPTOR_SET_PROTO = 4
        PROTO_FILE = 6

    file_path = proto.Field(proto.STRING, number=1,)
    file_contents = proto.Field(proto.BYTES, number=3,)
    file_type = proto.Field(proto.ENUM, number=4, enum=FileType,)


class ConfigRef(proto.Message):
    r"""Represents a service configuration with its name and id.

    Attributes:
        name (str):
            Resource name of a service config. It must
            have the following format: "services/{service
            name}/configs/{config id}".
    """

    name = proto.Field(proto.STRING, number=1,)


class ChangeReport(proto.Message):
    r"""Change report associated with a particular service
    configuration.
    It contains a list of ConfigChanges based on the comparison
    between two service configurations.

    Attributes:
        config_changes (Sequence[google.api.config_change_pb2.ConfigChange]):
            List of changes between two service configurations. The
            changes will be alphabetically sorted based on the
            identifier of each change. A ConfigChange identifier is a
            dot separated path to the configuration. Example:
            visibility.rules[selector='LibraryService.CreateBook'].restriction
    """

    config_changes = proto.RepeatedField(
        proto.MESSAGE, number=1, message=config_change_pb2.ConfigChange,
    )


class Rollout(proto.Message):
    r"""A rollout resource that defines how service configuration
    versions are pushed to control plane systems. Typically, you
    create a new version of the service config, and then create a
    Rollout to push the service config.

    Attributes:
        rollout_id (str):
            Optional. Unique identifier of this Rollout. Must be no
            longer than 63 characters and only lower case letters,
            digits, '.', '_' and '-' are allowed.

            If not specified by client, the server will generate one.
            The generated id will have the form of , where "date" is the
            create date in ISO 8601 format. "revision number" is a
            monotonically increasing positive number that is reset every
            day for each service. An example of the generated rollout_id
            is '2016-02-16r1'
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Creation time of the rollout. Readonly.
        created_by (str):
            The user who created the Rollout. Readonly.
        status (google.cloud.servicemanagement_v1.types.Rollout.RolloutStatus):
            The status of this rollout. Readonly. In case
            of a failed rollout, the system will
            automatically rollback to the current Rollout
            version. Readonly.
        traffic_percent_strategy (google.cloud.servicemanagement_v1.types.Rollout.TrafficPercentStrategy):
            Google Service Control selects service
            configurations based on traffic percentage.
        delete_service_strategy (google.cloud.servicemanagement_v1.types.Rollout.DeleteServiceStrategy):
            The strategy associated with a rollout to delete a
            ``ManagedService``. Readonly.
        service_name (str):
            The name of the service associated with this
            Rollout.
    """

    class RolloutStatus(proto.Enum):
        r"""Status of a Rollout."""
        ROLLOUT_STATUS_UNSPECIFIED = 0
        IN_PROGRESS = 1
        SUCCESS = 2
        CANCELLED = 3
        FAILED = 4
        PENDING = 5
        FAILED_ROLLED_BACK = 6

    class TrafficPercentStrategy(proto.Message):
        r"""Strategy that specifies how clients of Google Service Controller
        want to send traffic to use different config versions. This is
        generally used by API proxy to split traffic based on your
        configured percentage for each config version.

        One example of how to gradually rollout a new service configuration
        using this strategy: Day 1

        ::

            Rollout {
              id: "example.googleapis.com/rollout_20160206"
              traffic_percent_strategy {
                percentages: {
                  "example.googleapis.com/20160201": 70.00
                  "example.googleapis.com/20160206": 30.00
                }
              }
            }

        Day 2

        ::

            Rollout {
              id: "example.googleapis.com/rollout_20160207"
              traffic_percent_strategy: {
                percentages: {
                  "example.googleapis.com/20160206": 100.00
                }
              }
            }

        Attributes:
            percentages (Sequence[google.cloud.servicemanagement_v1.types.Rollout.TrafficPercentStrategy.PercentagesEntry]):
                Maps service configuration IDs to their
                corresponding traffic percentage. Key is the
                service configuration ID, Value is the traffic
                percentage which must be greater than 0.0 and
                the sum must equal to 100.0.
        """

        percentages = proto.MapField(proto.STRING, proto.DOUBLE, number=1,)

    class DeleteServiceStrategy(proto.Message):
        r"""Strategy used to delete a service. This strategy is a
        placeholder only used by the system generated rollout to delete
        a service.

        """

    rollout_id = proto.Field(proto.STRING, number=1,)
    create_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    created_by = proto.Field(proto.STRING, number=3,)
    status = proto.Field(proto.ENUM, number=4, enum=RolloutStatus,)
    traffic_percent_strategy = proto.Field(
        proto.MESSAGE, number=5, oneof="strategy", message=TrafficPercentStrategy,
    )
    delete_service_strategy = proto.Field(
        proto.MESSAGE, number=200, oneof="strategy", message=DeleteServiceStrategy,
    )
    service_name = proto.Field(proto.STRING, number=8,)


__all__ = tuple(sorted(__protobuf__.manifest))
