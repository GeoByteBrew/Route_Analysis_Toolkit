"""Shared vehicle constraint model and transport templates."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class VehicleConstraints:
    length_m: float
    width_m: float
    height_m: float
    weight_t: float
    max_slope_pct: float = 8.0
    template_id: str = "custom"
    template_label: str = "Custom"


VEHICLE_TEMPLATES: dict[str, dict[str, Any]] = {
    "long_load": {
        "id": "long_load",
        "label": "Extra-long load",
        "description": "Extended trailer — length-critical",
        "length_m": 65.0,
        "width_m": 4.5,
        "height_m": 4.2,
        "weight_t": 40.0,
        "max_slope_pct": 7.0,
    },
    "wide_load": {
        "id": "wide_load",
        "label": "Wide & heavy load",
        "description": "Wide, heavy cylindrical load",
        "length_m": 30.0,
        "width_m": 4.8,
        "height_m": 4.8,
        "weight_t": 90.0,
        "max_slope_pct": 8.0,
    },
    "heavy_load": {
        "id": "heavy_load",
        "label": "Very heavy load",
        "description": "High weight, moderate envelope",
        "length_m": 14.0,
        "width_m": 4.2,
        "height_m": 4.5,
        "weight_t": 120.0,
        "max_slope_pct": 6.0,
    },
    "custom": {
        "id": "custom",
        "label": "Custom",
        "description": "Manual vehicle limits",
        "length_m": 45.0,
        "width_m": 4.5,
        "height_m": 4.2,
        "weight_t": 80.0,
        "max_slope_pct": 8.0,
    },
}


def list_templates() -> list[dict[str, Any]]:
    return list(VEHICLE_TEMPLATES.values())


def template_to_vehicle(template_id: str) -> VehicleConstraints:
    t = VEHICLE_TEMPLATES.get(template_id) or VEHICLE_TEMPLATES["custom"]
    return VehicleConstraints(
        length_m=float(t["length_m"]),
        width_m=float(t["width_m"]),
        height_m=float(t["height_m"]),
        weight_t=float(t["weight_t"]),
        max_slope_pct=float(t["max_slope_pct"]),
        template_id=str(t["id"]),
        template_label=str(t["label"]),
    )


def vehicle_as_dict(v: VehicleConstraints) -> dict[str, Any]:
    return asdict(v)
