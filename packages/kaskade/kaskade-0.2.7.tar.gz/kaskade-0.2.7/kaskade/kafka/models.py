from typing import List


class Broker:
    def __init__(self, id: int = -1, host: str = "", port: int = -1) -> None:
        self.id = id
        self.host = host
        self.port = port

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return "{}:{}/{}".format(self.host, self.port, self.id)


class GroupPartition:
    def __init__(
        self,
        id: int = -1,
        topic: str = "",
        group: str = "",
        offset: int = 0,
        low: int = 0,
        high: int = 0,
    ) -> None:
        self.id = id
        self.topic = topic
        self.group = group
        self.offset = offset
        self.low = low
        self.high = high

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return str(
            {
                "id": self.id,
                "group": self.group,
                "topic": self.topic,
                "offset": self.offset,
                "low": self.low,
                "high": self.high,
            }
        )

    def lag_count(self) -> int:
        if self.high < 0:
            return 0
        elif self.offset < 0:
            return self.high - self.low
        else:
            return self.high - self.offset


class Group:
    def __init__(
        self,
        id: str = "",
        broker: Broker = Broker(),
        state: str = "",
        members: int = 0,
        partitions: List[GroupPartition] = [],
    ) -> None:
        self.broker = broker
        self.id = id
        self.state = state
        self.members = members
        self.partitions = partitions

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return self.id

    def lag_count(self) -> int:
        return (
            sum([partition.lag_count() for partition in self.partitions])
            if self.partitions is not None
            else 0
        )


class Partition:
    def __init__(
        self,
        id: int = -1,
        leader: int = -1,
        replicas: List[int] = [],
        isrs: List[int] = [],
    ) -> None:
        self.id = id
        self.leader = leader
        self.replicas = replicas
        self.isrs = isrs

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return str(self.id)


class Topic:
    def __init__(
        self,
        name: str = "",
        partitions: List[Partition] = [],
        groups: List[Group] = [],
    ) -> None:
        self.name = name
        self.partitions = partitions
        self.groups = groups

    def partitions_count(self) -> int:
        return len(self.partitions) if self.partitions is not None else 0

    def groups_count(self) -> int:
        return len(self.groups) if self.groups is not None else 0

    def replicas_count(self) -> int:
        return (
            max([len(partition.replicas) for partition in self.partitions], default=0)
            if self.partitions is not None
            else 0
        )

    def isrs_count(self) -> int:
        return (
            min([len(partition.isrs) for partition in self.partitions], default=0)
            if self.partitions is not None
            else 0
        )

    def lag_count(self) -> int:
        return (
            max([group.lag_count() for group in self.groups], default=0)
            if self.groups is not None
            else 0
        )

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return self.name


class Cluster:
    def __init__(
        self,
        brokers: List[Broker] = [],
        version: str = "",
        has_schemas: bool = False,
        protocol: str = "plain",
    ) -> None:
        self.brokers = brokers
        self.version = version
        self.has_schemas = has_schemas
        self.protocol = protocol

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return str(
            {
                "brokers": [str(broker) for broker in self.brokers],
                "version": self.version,
                "has_schemas": self.has_schemas,
                "protocol": self.protocol,
            }
        )

    def brokers_count(self) -> int:
        return len(self.brokers) if self.brokers is not None else 0
