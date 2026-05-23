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
Use ASCII variable names only.
For numeric and boolean problems, use only executable equation/compare steps.
Do not write prose outside JSON.
Allowed step types:
- equation: {"id":"s1","type":"equation","equation":"U = I*R","solves_for":"U","unit":"V"}
- compare: {"id":"s2","type":"compare","left":"XL","operator":"approximately_equal","right":"XC","output":"resonance"}"""


PREFERRED_SYMBOL_BY_TYPE = {
    "capacitance": "C",
    "voltage": "U",
    "current": "I",
    "resistance": "R",
    "inductance": "L",
    "frequency": "f",
    "angular_frequency": "omega",
    "charge": "q",
    "distance": "r",
    "area": "S",
    "energy": "W",
    "power": "P",
    "force": "F",
    "electric_field": "E",
    "magnetic_field": "B",
    "magnetic_flux": "Phi",
    "time": "t",
    "angle": "theta",
}


def safe_symbol(raw: Any, fallback: str) -> str:
    symbol = str(raw or "").strip()
    if not symbol or not symbol.replace("_", "").isalnum() or symbol[0].isdigit():
        return fallback
    return symbol


def unique_symbol(base: str, used: set[str]) -> str:
    if base not in used:
        used.add(base)
        return base
    index = 1
    while f"{base}{index}" in used:
        index += 1
    symbol = f"{base}{index}"
    used.add(symbol)
    return symbol


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


def executor_observations(trace_observations: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, str]]:
    used: set[str] = set()
    renamed: dict[str, str] = {}
    givens = []
    for obs in trace_observations:
        quantity_type = obs.get("quantity_type") or "unknown"
        raw_symbol = obs.get("symbol")
        preferred = PREFERRED_SYMBOL_BY_TYPE.get(quantity_type)
        if preferred is None:
            preferred = safe_symbol(raw_symbol, f"x{len(givens)}")
        # Keep explicit indexed physics symbols such as q1, q2, F13 when present,
        # but do not keep extractor placeholders like num_0.
        if (
            isinstance(raw_symbol, str)
            and raw_symbol
            and not raw_symbol.startswith("num_")
            and raw_symbol[0].isalpha()
            and any(ch.isdigit() for ch in raw_symbol)
        ):
            preferred = safe_symbol(raw_symbol, preferred)
        symbol = unique_symbol(preferred, used)
        if raw_symbol:
            renamed[str(raw_symbol)] = symbol
        givens.append(
            {
                "name": quantity_type,
                "symbol": symbol,
                "value": obs.get("value"),
                "unit": obs.get("unit") or "-",
            }
        )
    return givens, renamed


def clean_formula_text(formula: str | None, renamed: dict[str, str]) -> str | None:
    if not formula or "=" not in formula:
        return None
    text = str(formula).strip()
    # Remove explanatory suffixes from traces such as "I=U/R at resonance".
    text = text.split(" with ")[0].split(" at ")[0].split(";")[0].strip()
    text = text.replace("^", "**").replace("×", "*").replace("·", "*")
    text = text.replace("π", "pi")
    text = text.replace("sum(component powers)", "P1 + P2")
    # Common aliases from traces.
    text = text.replace("E=0.5", "W=0.5")
    text = text.replace("relative_error", "answer")
    for old, new in sorted(renamed.items(), key=lambda kv: -len(kv[0])):
        if old != new:
            text = text.replace(old, new)
    if not text or "=" not in text:
        return None
    if any(token in text.lower() for token in ["if ", "present", "state", "component"]):
        return None
    return text


def names_in_formula(formula: str) -> set[str]:
    return set(__import__("re").findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", formula)) - {
        "sqrt",
        "sin",
        "cos",
        "tan",
        "abs",
        "pi",
    }


def value_si_for_result(result: solver.SolveResult) -> float | None:
    trace = result.trace or {}
    if isinstance(trace.get("value_si"), (int, float)):
        return float(trace["value_si"])
    value = solver.parse_number(str(result.pred_answer))
    if value is None:
        return None
    value_si, _ = solver.unit_to_si(float(value), result.pred_unit)
    return value_si


def make_plan(row: dict[str, str], result: solver.SolveResult) -> dict[str, Any]:
    trace = result.trace or {}
    raw_observations = [compact_observation(obs) for obs in trace.get("observations", [])]
    observations, renamed = executor_observations(raw_observations)
    relations = trace.get("relations", [])
    formula = clean_formula_text(trace.get("formula"), renamed)
    pred_answer_type = result.answer_type

    if pred_answer_type in {"text", "math_expression", "yes_no"}:
        return {
            "problem_type": result.family,
            "answer_type": "boolean" if pred_answer_type == "yes_no" else pred_answer_type,
            "target": {
                "name": "answer",
                "symbol": "answer",
                "unit": result.pred_unit,
            },
            "givens": observations,
            "relations": relations,
            "steps": [],
            "final_answer": f"{result.pred_answer} {result.pred_unit}".strip(),
        }

    target_symbol = "answer"
    step_unit = result.pred_unit
    step: dict[str, Any]
    given_symbols = {item["symbol"] for item in observations}
    if formula:
        lhs = formula.split("=", 1)[0].strip()
        formula_names = names_in_formula(formula)
        if lhs and lhs.replace("_", "").isalnum() and lhs[0].isalpha() and formula_names <= (given_symbols | {lhs, "k", "eps0", "epsilon0", "mu0", "pi", "g"}):
            target_symbol = lhs
            step = {
                "id": "s1",
                "type": "equation",
                "equation": formula,
                "solves_for": target_symbol,
                "unit": result.pred_unit,
            }
        else:
            formula = None
    if not formula:
        value_si = value_si_for_result(result)
        if value_si is None:
            value_si = 0.0
        step = {
            "id": "s1",
            "type": "equation",
            "equation": f"answer = {value_si:.12g}",
            "solves_for": "answer",
            "unit": result.pred_unit,
        }

    return {
        "problem_type": result.family,
        "answer_type": result.answer_type,
        "target": {
            "name": "answer",
            "symbol": target_symbol,
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
