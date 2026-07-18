"""Smoke tests for the health-assistant dataset.

No network, no API keys — validates the committed CSV only.
"""
from __future__ import annotations

import csv
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "health_assistant_dataset.csv"

EXPECTED_INTENTS = {
    "symptom_inquiry",
    "medication_info",
    "appointment_booking",
    "general_health",
    "emergency",
    "doctor_recommendation",
    "greeting",
    "goodbye",
}


def _rows() -> list[dict[str, str]]:
    with open(DATA, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def test_dataset_columns() -> None:
    rows = _rows()
    assert rows, "dataset is empty"
    assert set(rows[0].keys()) == {"text", "intent", "response"}


def test_dataset_size() -> None:
    assert len(_rows()) == 1250


def test_intent_set_matches_documentation() -> None:
    intents = {r["intent"] for r in _rows()}
    assert intents == EXPECTED_INTENTS


def test_emergency_intent_present() -> None:
    # Safety-relevant: the emergency intent must exist so it can be handled.
    assert any(r["intent"] == "emergency" for r in _rows())


def test_no_empty_text() -> None:
    for i, row in enumerate(_rows()):
        assert row["text"].strip(), f"row {i} has empty text"
