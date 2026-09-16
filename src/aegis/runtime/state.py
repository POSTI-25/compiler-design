"""Runtime state for the minimal AEGIS interpreter."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class RuntimeState:
    battery: int | float = 100
    position: int | float = 0
    elapsed_time: int | float = 0
    camera_on: bool = False
    image_captured: bool = False
    safe_mode: bool = False
    trace: list[str] = field(default_factory=list)
