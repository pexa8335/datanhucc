#!/usr/bin/env python
# coding: utf-8
"""Build planner-SFT JSONL data from deterministic solver traces.

This is Priority 2 scaffolding: instead of teaching Qwen to be a calculator,
teach it to emit a controlled plan/IR that a deterministic executor can verify
and run. Only rows solved correctly by the deterministic baseline are used.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

import physics_baseline_solver as solver


PLANNER_SYSTEM_PROMPT = """You are a physics planning model.
Given a physics question, output only a valid JSON plan.
The plan must expose answer_type, family, givens, relations, deterministic steps, and final target.
Do not write prose outside JSON."""


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def compact_observation(obs: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": obs.get("id"),
        "symbol": obs.get("symbol"),
        "value": obs.get("value"),
        "unit": obs.get("unit"),
        "value_si": obs.get("value_si"),
        "unit_si": obs.get("unit_si"),
        "quantity_type": obs.get("quantity_type"),
    }


def make_plan(row: dict[str, str], result: solver.SolveResult) -> dict[str, Any]:
    trace = result.trace or {}
    observations = [compact_observation(obs) for obs in trace.get("observations", [])]
    relations = trace.get("relations", [])
    formula = trace.get("formula")
    primitive = trace.get("planner") or f"deterministic_{result.family}"

    step: dict[str, Any] = {
        "id": "s1",
        "type": "deterministic_primitive",
        "primitive": primitive,
        "produces": "answer",
    }
    if formula:
        step["formula"] = formula

    return {
        "problem_type": result.family,
        "answer_type": result.answer_type,
        "target": {
            "name": "answer",
            "symbol": "answer",
            "unit": result.pred_unit,
        },
        "givens": observations,
        "relations": relations,
        "steps": [step],
        "final_answer": {
            "value": result.pred_answer,
            "unit": result.pred_unit,
        },
    }


def build_records(rows: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    records: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    for row in rows:
        result = solver.route_and_solve(row)
        expected_type = solver.classify_answer_type(row.get("answer", ""), row.get("unit", ""))
        if result.status != "ok":
            skipped.append({"id": row.get("id"), "status": result.status, "reason": result.failure_reason})
            continue
        ok, method = solver.compare_result(
            result.pred_answer,
            result.pred_unit,
            row.get("answer", ""),
            row.get("unit", ""),
            expected_type,
        )
        if not ok:
            skipped.append({"id": row.get("id"), "status": "wrong", "reason": method})
            continue

        plan = make_plan(row, result)
        messages = [
            {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
            {"role": "user", "content": row.get("question", "")},
            {"role": "assistant", "content": json.dumps(plan, ensure_ascii=False, sort_keys=True)},
        ]
        records.append({"id": row.get("id"), "family": result.family, "messages": messages, "plan": plan})
    return records, skipped


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build planner-SFT data from deterministic solver traces.")
    parser.add_argument("--train-csv", default="split_output/80.csv")
    parser.add_argument("--test-csv", default="split_output/20.csv")
    parser.add_argument("--output-dir", default="planner_sft")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    train_records, train_skipped = build_records(load_rows(Path(args.train_csv)))
    test_records, test_skipped = build_records(load_rows(Path(args.test_csv)))

    write_jsonl(output_dir / "planner_train.jsonl", train_records)
    write_jsonl(output_dir / "planner_test.jsonl", test_records)
    write_jsonl(output_dir / "planner_train_skipped.jsonl", train_skipped)
    write_jsonl(output_dir / "planner_test_skipped.jsonl", test_skipped)

    summary = {
        "train_source": args.train_csv,
        "test_source": args.test_csv,
        "train_planner_records": len(train_records),
        "test_planner_records": len(test_records),
        "train_skipped": len(train_skipped),
        "test_skipped": len(test_skipped),
        "note": "Planner data includes only rows solved correctly by deterministic baseline.",
    }
    (output_dir / "planner_sft_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
