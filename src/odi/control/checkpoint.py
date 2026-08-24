"""Checkpoint persistence boundary for resumable execution."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from .state import WorkflowState


@dataclass(frozen=True)
class Checkpoint:
    id: str
    execution_id: str
    sequence: int
    state: dict[str, Any]
    created_at: datetime


class CheckpointStore:
    """Immutable in-memory checkpoint store with deterministic restore semantics."""

    def __init__(self) -> None:
        self._items: dict[str, list[Checkpoint]] = {}

    def save(self, state: WorkflowState) -> Checkpoint:
        execution_id = state.identity.execution_id
        history = self._items.setdefault(execution_id, [])
        checkpoint = Checkpoint(
            id=f"checkpoint-{uuid4().hex}",
            execution_id=execution_id,
            sequence=len(history) + 1,
            state=state.snapshot(),
            created_at=datetime.now(UTC),
        )
        history.append(checkpoint)
        state.checkpoint_id = checkpoint.id
        state.touch()
        return checkpoint

    def latest(self, execution_id: str) -> Checkpoint | None:
        history = self._items.get(execution_id, [])
        return history[-1] if history else None

    def history(self, execution_id: str) -> tuple[Checkpoint, ...]:
        return tuple(self._items.get(execution_id, ()))

    def restore(self, checkpoint: Checkpoint) -> dict[str, Any]:
        return dict(checkpoint.state)
