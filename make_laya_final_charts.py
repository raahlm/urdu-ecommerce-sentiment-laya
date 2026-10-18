#!/usr/bin/env python3
"""
Fancy local charts for the LAYA fine-tuning project.

Run from ~/pk-collector:
    conda activate laya
    pip install matplotlib numpy
    python make_laya_final_charts.py

Outputs to:
    laya_work/checkpoints/silver_v1_ddp_run1/final_charts/

Includes:
- training loss by epoch
- original vs fine-tuned validation accuracy
- validation vs held-out test metrics
- calibration/risk comparisons
- inference latency
- selective accuracy
- fine-tuned per-question validation scores
- estimated Qwen vs LAYA time comparison
- a multi-page PDF dashboard
- CSV/JSON data used for plotting

Important:
- Qwen's ~4 rows/sec and ~32 min for 7,572 tasks were a prior benchmark/estimate,
  not a confirmed final wall-clock duration.
- LAYA wall-clock extrapolations use measured test-evaluation latency percentiles,
  multiplied by 7,572 tasks. This is a rough serial estimate, not a benchmark of a
  full Qwen-vs-LAYA run under identical prompts, batching, and output requirements.
- Both were run locally, so software/API usage cost is $0; electricity and hardware
  depreciation were not measured.
- The reported labels are silver labels, not independently human-verified gold labels.
"""

from pathlib import Path
import csv
import json
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

OUT = Path("laya_work/checkpoints/silver_v1_ddp_run1/final_charts")
OUT.mkdir(parents=True, exist_ok=True)

# ---- Values reported from the user's completed training/evaluations ----
training = {
    "epochs": [1, 2, 3, 4],
    "mean_loss": [0.9575, 0.8177, 0.6768, 0.5704],
}
baseline_val = {
    "choice_accuracy": 0.2205,
    "noul_accuracy": 0.7702,
    "brier": 0.3750,
    "ece": 0.3663,
    "aurc": 0.4150,
    "mean_confidence": 0.7899,
    "selective_accuracy@50": 0.5509,
    "selective_accuracy@80": 0.4527,
    "latency_p50_ms": 43.0987,
    "latency_p95_ms": 102.3659,
    "cost_per_decision_p50_ms": 15.0783,
    "cost_per_decision_p95_ms": 26.2941,
}
finetuned_val = {
    "choice_accuracy": 0.9340,
    "noul_accuracy": 0.9571,
    "brier": 0.0560,
    "ece": 0.0556,
    "aurc": 0.0529,
    "mean_confidence": 0.9980,
    "selective_accuracy@50": 0.9471,
    "selective_accuracy@80": 0.9471,
    "latency_p50_ms": 42.4001,
    "latency_p95_ms": 105.7503,
    "cost_per_decision_p50_ms": 15.3277,
    "cost_per_decision_p95_ms": 26.8807,
}
finetuned_test = {
    "choice_accuracy": 0.9350,
    "noul_accuracy": 0.9629,
    "brier": 0.0529,
    "ece": 0.0524,
    "aurc": 0.0496,
    "mean_confidence": 0.9977,
    "selective_accuracy@50": 0.9504,
    "selective_accuracy@80": 0.9504,
    "latency_p50_ms": 55.4196,
    "latency_p95_ms": 107.9091,
    "cost_per_decision_p50_ms": 15.0909,
    "cost_per_decision_p95_ms": 27.1751,
}
test_examples = 2503
qwen_batch_tasks = 7572
qwen_estimated_rows_per_sec = 4.0  # earlier reported benchmark estimate
qwen_estimated_seconds = qwen_batch_tasks / qwen_estimated_rows_per_sec
laya_test_p50_seconds = finetuned_test["latency_p50_ms"] / 1000
laya_test_p95_seconds = finetuned_test["latency_p95_ms"] / 1000
laya_estimated_seconds_p50 = qwen_batch_tasks * laya_test_p50_seconds
laya_estimated_seconds_p95 = qwen_batch_tasks * laya_test_p95_seconds

# Fine-tuned validation per-question metrics (reported by LAYA evaluator).
per_question = {
    "aspect_AUTHENTICITY": 0.9816,
    "aspect_CUSTOMER_SUPPORT": 1.0000,
    "aspect_DELIVERY": 0.9710,
    "aspect_GENERAL_EXPERIENCE": 0.7672,
    "aspect_ORDER_FULFILLMENT": 0.8809,
    "aspect_OTHER": 0.9986,
    "aspect_PACKAGING": 0.9887,
    "aspect_PRICE_VALUE": 0.9484,
    "aspect_PRODUCT_AVAILABILITY": 0.9915,
    "aspect_PRODUCT_DESIGN": 0.9569,
    "aspect_PRODUCT_FUNCTIONALITY": 0.8741,
    "aspect_PRODUCT_QUALITY": 0.8013,
    "aspect_RETURN_REFUND": 0.9908,
    "aspect_SELLER_SERVICE": 0.9470,
    "aspect_SIZE_FIT": 0.9823,
    "code_switching": 0.9760,
    "intent_COMPARISON": 0.9859,
    "intent_COMPLAINT": 0.8897,
    "intent_EXPERIENCE_REPORT": 0.9215,
    "intent_GENERAL_REACTION": 0.9519,
    "intent_OTHER": 1.0000,
    "intent_PRAISE": 0.9144,
    "intent_QUESTION": 0.9894,
    "intent_RECOMMENDATION": 0.9031,
    "intent_RESOLUTION_REQUEST": 0.9965,
    "language": 0.9109,
    "relevance": 0.9166,
    "sentiment": 0.9178,
    "understandable": 1.0000,
}

plt.rcParams.update({
    "figure.figsize": (12, 7),
    "figure.dpi": 130,
    "savefig.dpi": 200,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "font.size": 10,
    "axes.titleweight": "bold",
    "legend.frameon": False,
})

def save(fig, filename):
    fig.tight_layout()
    fig.savefig(OUT / filename, bbox_inches="tight")
    plt.close(fig)

def grouped_bar(filename, title, labels, series, ylabel, percent=False, ylim=None, rotation=0):
    fig, ax = plt.subplots(figsize=(12, 7))
    x = np.arange(len(labels))
    width = 0.8 / len(series)
    containers = []
    for i, (name, values) in enumerate(series.items()):
        offset = (i - (len(series)-1)/2) * width
        containers.append(ax.bar(x + offset, values, width, label=name))
    fmt = "%.1f%%" if percent else "%.4f"
    for bars in containers:
        ax.bar_label(bars, fmt=fmt, padding=3, fontsize=8)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xticks(x, labels, rotation=rotation, ha="right" if rotation else "center")
    if ylim:
        ax.set_ylim(*ylim)
    ax.legend()
    save(fig, filename)

# 1. Training loss curve
fig, ax = plt.subplots(figsize=(11, 6.5))
ax.plot(training["epochs"], training["mean_loss"], marker="o", linewidth=3, markersize=9)
for x, y in zip(training["epochs"], training["mean_loss"]):
    ax.annotate(f"{y:.4f}", (x, y), xytext=(0, 10), textcoords="offset points",
                ha="center", fontsize=10, fontweight="bold")
ax.fill_between(training["epochs"], training["mean_loss"], alpha=0.12)
ax.set_title("LAYA Fine-Tuning — Training Loss Falls Across Epochs")
ax.set_xlabel("Training epoch")
ax.set_ylabel("Mean training loss (lower is better)")
ax.set_xticks(training["epochs"])
ax.set_ylim(0, 1.12)
save(fig, "01_training_loss.png")

# 2. Original vs fine-tuned validation accuracy
grouped_bar(
    "02_validation_accuracy.png",
    "Validation Accuracy — Fine-Tuning Produces a Large Gain",
    ["Choice accuracy", "NOUL accuracy"],
    {
        "Original LAYA": [baseline_val["choice_accuracy"]*100, baseline_val["noul_accuracy"]*100],
        "Fine-tuned LAYA": [finetuned_val["choice_accuracy"]*100, finetuned_val["noul_accuracy"]*100],
    },
    "Accuracy (%)", percent=True, ylim=(0, 112)
)

# 3. Validation vs held-out test: fine-tuned model
grouped_bar(
    "03_validation_vs_test.png",
    "Fine-Tuned Model — Validation vs Held-Out Test",
    ["Choice accuracy", "NOUL accuracy", "Selective @50", "Selective @80"],
    {
        "Validation (n=2,495)": [
            finetuned_val["choice_accuracy"]*100, finetuned_val["noul_accuracy"]*100,
            finetuned_val["selective_accuracy@50"]*100, finetuned_val["selective_accuracy@80"]*100,
        ],
        "Test (n=2,503)": [
            finetuned_test["choice_accuracy"]*100, finetuned_test["noul_accuracy"]*100,
            finetuned_test["selective_accuracy@50"]*100, finetuned_test["selective_accuracy@80"]*100,
        ],
    },
    "Accuracy (%)", percent=True, ylim=(0, 112)
)

# 4. Calibration and risk
grouped_bar(
    "04_calibration_risk.png",
    "Calibration & Risk — Lower Is Better",
    ["Brier score", "ECE", "AURC"],
    {
        "Original validation": [baseline_val["brier"], baseline_val["ece"], baseline_val["aurc"]],
        "Fine-tuned validation": [finetuned_val["brier"], finetuned_val["ece"], finetuned_val["aurc"]],
        "Fine-tuned test": [finetuned_test["brier"], finetuned_test["ece"], finetuned_test["aurc"]],
    },
    "Metric value", ylim=(0, 0.49)
)

# 5. Latency
grouped_bar(
    "05_latency.png",
    "Inference Latency — Original, Fine-Tuned Validation, and Test",
    ["Latency p50", "Latency p95"],
    {
        "Original validation": [baseline_val["latency_p50_ms"], baseline_val["latency_p95_ms"]],
        "Fine-tuned validation": [finetuned_val["latency_p50_ms"], finetuned_val["latency_p95_ms"]],
        "Fine-tuned test": [finetuned_test["latency_p50_ms"], finetuned_test["latency_p95_ms"]],
    },
    "Milliseconds (lower is faster)"
)

# 6. Decision cost metrics
grouped_bar(
    "06_cost_per_decision.png",
    "Evaluator Cost per Decision",
    ["p50 cost", "p95 cost"],
    {
        "Original validation": [baseline_val["cost_per_decision_p50_ms"], baseline_val["cost_per_decision_p95_ms"]],
        "Fine-tuned validation": [finetuned_val["cost_per_decision_p50_ms"], finetuned_val["cost_per_decision_p95_ms"]],
        "Fine-tuned test": [finetuned_test["cost_per_decision_p50_ms"], finetuned_test["cost_per_decision_p95_ms"]],
    },
    "Milliseconds (lower is faster)"
)

# 7. Selective accuracy
grouped_bar(
    "07_selective_accuracy.png",
    "Selective Accuracy — Fine-Tuned Model Generalizes to Test",
    ["Selective @50", "Selective @80"],
    {
        "Original validation": [baseline_val["selective_accuracy@50"]*100, baseline_val["selective_accuracy@80"]*100],
        "Fine-tuned validation": [finetuned_val["selective_accuracy@50"]*100, finetuned_val["selective_accuracy@80"]*100],
        "Fine-tuned test": [finetuned_test["selective_accuracy@50"]*100, finetuned_test["selective_accuracy@80"]*100],
    },
    "Accuracy (%)", percent=True, ylim=(0, 112)
)

# 8. All per-question validation scores
items = sorted(per_question.items(), key=lambda item: item[1])
fig, ax = plt.subplots(figsize=(13, 12))
names = [k for k, _ in items]
values = [v*100 for _, v in items]
bars = ax.barh(names, values)
ax.bar_label(bars, labels=[f"{v:.1f}%" for v in values], padding=3, fontsize=8)
ax.axvline(90, linestyle="--", linewidth=1.4, label="90% reference")
ax.set_title("Fine-Tuned LAYA — Validation Performance Across All 29 Questions")
ax.set_xlabel("Reported evaluator accuracy (%)")
ax.set_xlim(0, 112)
ax.tick_params(axis="y", labelsize=8)
ax.legend(loc="lower right")
save(fig, "08_per_question_validation.png")

# 9. Qwen vs LAYA time estimate for 7,572 tasks.
# Qwen: prior estimate ~4 rows/s. LAYA: serial extrapolation from test latency percentiles.
labels = ["Qwen3-14B via Ollama\nprior estimate", "LAYA at test p50\nserial extrapolation", "LAYA at test p95\nserial extrapolation"]
minutes = [qwen_estimated_seconds/60, laya_estimated_seconds_p50/60, laya_estimated_seconds_p95/60]
fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.bar(labels, minutes)
ax.bar_label(bars, labels=[f"{v:.1f} min" for v in minutes], padding=5, fontsize=10, fontweight="bold")
ax.set_title("Estimated Time for 7,572 Annotation Tasks — Qwen vs LAYA")
ax.set_ylabel("Estimated elapsed time (minutes; lower is faster)")
ax.set_ylim(0, max(minutes)*1.25)
ax.text(
    0.01, -0.22,
    "Caution: Qwen's ~4 rows/s is a prior benchmark estimate; LAYA figures extrapolate measured test latency "
    "to a serial run. Different execution paths/batching mean this is indicative, not a controlled benchmark.",
    transform=ax.transAxes, fontsize=9, wrap=True
)
save(fig, "09_qwen_vs_laya_time_estimate.png")

# 10. Cost comparison: local model/API usage and non-comparable power costs
fig, ax = plt.subplots(figsize=(11, 5.5))
ax.bar(["Qwen via local Ollama", "LAYA local checkpoint"], [0, 0])
ax.set_title("Software/API Cost for Local Inference")
ax.set_ylabel("Usage/API charges (USD)")
ax.set_ylim(0, 1)
ax.set_yticks([0])
ax.set_yticklabels(["$0"])
ax.text(
    0.5, 0.55,
    "Both run locally: no per-token API charge.\nElectricity, hardware depreciation, and engineering time were not measured.",
    ha="center", va="center", transform=ax.transAxes, fontsize=12,
    bbox=dict(boxstyle="round,pad=0.5", alpha=0.08)
)
save(fig, "10_local_usage_cost.png")

# Data exports.
data = {
    "training": training,
    "baseline_validation": baseline_val,
    "finetuned_validation": finetuned_val,
    "finetuned_test": finetuned_test,
    "finetuned_per_question_validation": per_question,
    "qwen_laya_comparison": {
        "task_count": qwen_batch_tasks,
        "qwen_model": "Qwen3-14B Q4_K_M via local Ollama",
        "qwen_estimated_rows_per_second": qwen_estimated_rows_per_sec,
        "qwen_estimated_seconds": qwen_estimated_seconds,
        "laya_test_p50_latency_ms": finetuned_test["latency_p50_ms"],
        "laya_test_p95_latency_ms": finetuned_test["latency_p95_ms"],
        "laya_estimated_seconds_at_p50_serial": laya_estimated_seconds_p50,
        "laya_estimated_seconds_at_p95_serial": laya_estimated_seconds_p95,
        "software_api_cost_usd": {"qwen_local": 0, "laya_local": 0},
        "caveat": "Not a controlled apples-to-apples benchmark; local power cost not measured."
    },
    "notes": [
        "Training loss values are epoch means transcribed from the training results.",
        "Validation and test metrics are transcribed from the reported LAYA evaluation outputs.",
        "Test set contains 2,503 examples; validation set contains 2,495 examples.",
        "The test labels are silver labels, not independently human-verified gold labels.",
        "Qwen time is an estimate from a previously reported ~4 rows/sec benchmark; actual full-run elapsed time was not provided.",
        "LAYA time estimates extrapolate reported test latency percentiles to 7,572 serial decisions and are not measured full-run times.",
        "Per-question chart shows the 29 reported fine-tuned validation question metrics; sample counts were not available."
    ]
}
(OUT / "chart_data.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

with (OUT / "comparison_metrics.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["metric", "original_validation", "finetuned_validation", "finetuned_test"])
    for key in [
        "choice_accuracy", "noul_accuracy", "brier", "ece", "aurc",
        "mean_confidence", "selective_accuracy@50", "selective_accuracy@80",
        "latency_p50_ms", "latency_p95_ms",
        "cost_per_decision_p50_ms", "cost_per_decision_p95_ms",
    ]:
        writer.writerow([key, baseline_val[key], finetuned_val[key], finetuned_test[key]])

# PDF dashboard: each generated PNG becomes a separate landscape page.
chart_files = sorted(OUT.glob("*.png"))
with PdfPages(OUT / "LAYA_Qwen_Final_Charts_Dashboard.pdf") as pdf:
    for chart_path in chart_files:
        img = plt.imread(chart_path)
        fig, ax = plt.subplots(figsize=(11.7, 8.3))
        ax.imshow(img)
        ax.axis("off")
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

print("\nCharts generated successfully.")
print(f"Output folder: {OUT.resolve()}")
print("\nFiles:")
for p in sorted(OUT.iterdir()):
    print(" ", p.name)
print("\nQwen/LAYA time comparison assumptions:")
print(f"  Qwen estimate: {qwen_estimated_seconds/60:.1f} minutes for {qwen_batch_tasks:,} tasks at ~{qwen_estimated_rows_per_sec:g} rows/s")
print(f"  LAYA p50 extrapolation: {laya_estimated_seconds_p50/60:.1f} minutes (serial, theoretical)")
print(f"  LAYA p95 extrapolation: {laya_estimated_seconds_p95/60:.1f} minutes (serial, theoretical)")
