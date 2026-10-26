"""Data models for the HAWK concept simulator."""

from dataclasses import dataclass
from typing import Literal

Operation = Literal["inventory_scan", "pallet_move"]
Attachment = Literal["drone", "forklift"]


@dataclass(frozen=True)
class InventoryRecord:
    sku: str
    location: str
    quantity: int
    source: str


@dataclass(frozen=True)
class Task:
    task_id: str
    operation: Operation
    attachment: Attachment
    location: str | None = None
    load_kg: float | None = None


@dataclass(frozen=True)
class TaskResult:
    task_id: str
    status: str
    message: str
    records: tuple[InventoryRecord, ...] = ()
    load_kg: float | None = None
