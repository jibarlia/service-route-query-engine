"""Sink kinds — the node kinds that count as a terminal datastore/queue.

Closed set: the graph's sinks are always an RDS datastore or an SQS queue. It's a
domain invariant tied to the node kinds present in the graph, not a deployment
knob, so it lives in code as an enum rather than in configuration.
"""

from __future__ import annotations

from enum import StrEnum


class SinkKind(StrEnum):
    RDS = "rds"
    SQS = "sqs"
