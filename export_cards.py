"""Export the supplied workbook's cards without rewriting their text.

Run locally with: python export_cards.py path/to/workbook.xlsx
The workbook itself is not required by the browser game.
"""

import json
import re
import sys
from pathlib import Path

import openpyxl


workbook = openpyxl.load_workbook(sys.argv[1], data_only=False)
out = {}


def records(sheet):
    rows = list(workbook[sheet].values)
    return [row for row in rows[1:] if row[0] is not None]


out["situationOriginal"] = [
    {"id": f"SO-{int(row[0]):02d}", "prompt": row[1]}
    for row in records("Situations Deck")
]
out["situationModern"] = [
    {
        "id": f"SM-{int(row[0]):02d}",
        "prompt": row[1],
        "question1": row[2],
        "choices1": list(row[3:7]),
        "question2": row[7],
        "choices2": list(row[8:12]),
        "suggestions1": list(row[13:16]),
        "suggestions2": list(row[17:20]),
    }
    for row in records("Situation Deck 2.0")
]
for key, sheet, prefix in [
    ("payoffOriginal", "PayoffConsequence Deck", "PO"),
    ("payoffModern", "PayoffConsequence Deck 2.0", "PM"),
]:
    out[key] = [
        {
            "id": f"{prefix}-{int(row[0]):02d}",
            "prompt": row[1],
            "options": list(row[2:5]),
            "teachingPoint": row[5],
        }
        for row in records(sheet)
    ]
for key, sheet, prefix in [
    ("plusOriginal", "+- Card Deck", "XO"),
    ("plusModern", "+- Card Deck 2.0", "XM"),
]:
    deck = []
    for row in records(sheet):
        effect = str(row[2] or "")
        match = re.search(r"(?:Gain|Lose)\s+(\d+)", effect, flags=re.I)
        if not match:
            raise ValueError(f"Missing point effect in {sheet}: {row!r}")
        amount = int(match.group(1)) * (1 if effect.lower().startswith("gain") else -1)
        deck.append({"id": f"{prefix}-{int(row[0]):02d}", "prompt": row[1], "effect": effect, "points": amount})
    out[key] = deck
out["power"] = [
    {"id": f"PT-{int(row[0]):02d}", "title": row[1], "prompt": row[2]}
    for row in records("Power Talk Formula Deck")
]

expected = {"situationOriginal": 16, "situationModern": 25, "payoffOriginal": 16,
            "payoffModern": 25, "plusOriginal": 27, "plusModern": 30, "power": 12}
assert {key: len(value) for key, value in out.items()} == expected
serialized = json.dumps(out, ensure_ascii=False, indent=2)
Path("data/cards.json").write_text(serialized, encoding="utf-8")
Path("data/cards.js").write_text("window.CARD_DATA = " + serialized + ";\n", encoding="utf-8")
print("Exported:", {key: len(value) for key, value in out.items()})
