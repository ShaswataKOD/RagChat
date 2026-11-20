import asyncio
import json
import random
import statistics
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

from src.config.config import config
from src.test.gemini_client_setup import METRICS
from src.test.load_json import load_dataset

RESULTS_DIR = Path(__file__).parent
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

RESULTS_PATH = RESULTS_DIR / "baseline_results.json"


async def evaluate_sample(sample, output):

    sample_result = next(
        (item for item in output["results"] if item["id"] == sample["id"]), None
    )

    if sample_result is None:
        sample_result = {"id": sample["id"], "scores": {}}
        output["results"].append(sample_result)

    metric_calls = {
        "faithfulness": lambda: METRICS["faithfulness"].ascore(
            response=sample["response"],
            retrieved_contexts=sample["retrieved_contexts"],
            user_input=sample["user_input"],
        ),
        "answer_relevancy": lambda: METRICS["answer_relevancy"].ascore(
            user_input=sample["user_input"],
            response=sample["response"],
        ),
        "context_precision": lambda: METRICS["context_precision"].ascore(
            user_input=sample["user_input"],
            reference=sample["reference"],
            retrieved_contexts=sample["retrieved_contexts"],
        ),
        "context_recall": lambda: METRICS["context_recall"].ascore(
            user_input=sample["user_input"],
            reference=sample["reference"],
            retrieved_contexts=sample["retrieved_contexts"],
        ),
    }

    for metric_name, metric_call in metric_calls.items():
        # Skip metrics already evaluated
        if metric_name in sample_result["scores"]:
            continue

        print(f"Starting {metric_name}...", flush=True)

        result = await execute_with_retry(metric_call)

        sample_result["scores"][metric_name] = {
            "score": result.value,
            "reason": result.reason,
        }

        # Save immediately after each successful metric
        save_results(output)

        print(
            f"{metric_name}: {result.value:.4f}",
            flush=True,
        )

        # Control the request rate
        await asyncio.sleep(5)

    return sample_result["scores"]


async def execute_with_retry(metric_call, max_attempts=5):
    for attempt in range(max_attempts):
        try:
            return await metric_call()

        except Exception as exc:
            error = str(exc).upper()

            retryable = any(
                term in error
                for term in [
                    "429",
                    "503",
                    "RESOURCE_EXHAUSTED",
                    "UNAVAILABLE",
                    "TOO MANY REQUESTS",
                ]
            )

            if not retryable or attempt == max_attempts - 1:
                raise

            delay = (2 ** (attempt + 1)) + random.uniform(0, 1)

            print(
                f"Temporary API error. Retrying in {delay:.1f}s "
                f"({attempt + 1}/{max_attempts})",
                flush=True,
            )

            await asyncio.sleep(delay)


def save_results(output):

    with open(RESULTS_PATH, "w", encoding="utf-8") as file:
        json.dump(output, file, indent=4, ensure_ascii=False)


async def main():

    samples = load_dataset()

    print(f"Loaded {len(samples)} samples", flush=True)

    BATCH_SIZE = 5
    BATCH_DELAY = 10

    run_id = datetime.now(timezone.utc).strftime("baseline_%Y%m%d_%H%M%S")

    output = {
        "run_id": run_id,
        "experiment": "baseline",
        "ragas_version": version("ragas"),
        "evaluator_model": config.GEMINI_MODEL,
        "dataset_size": len(samples),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "results": [],
    }

    # Resume from an existing compatible evaluation
    if RESULTS_PATH.exists():
        with open(RESULTS_PATH, "r", encoding="utf-8") as file:
            previous = json.load(file)

        if (
            previous.get("experiment") == "baseline"
            and previous.get("dataset_size") == len(samples)
            and previous.get("evaluator_model") == config.GEMINI_MODEL
        ):
            output = previous
            print("Resuming previous evaluation...", flush=True)

    total_batches = (len(samples) + BATCH_SIZE - 1) // BATCH_SIZE

    for batch_index in range(total_batches):
        start = batch_index * BATCH_SIZE
        batch = samples[start : start + BATCH_SIZE]

        print(
            f"\n========== BATCH {batch_index + 1}/{total_batches} ==========",
            flush=True,
        )

        for sample in batch:
            existing = next(
                (item for item in output["results"] if item["id"] == sample["id"]), None
            )

            required_metrics = set(METRICS.keys())

            if existing and set(existing["scores"].keys()) == required_metrics:
                print(f"Skipping completed sample: {sample['id']}")
                continue

            print(f"\nEvaluating {sample['id']}", flush=True)

            await evaluate_sample(sample, output)

        save_results(output)

        print(
            f"Batch {batch_index + 1} completed.",
            flush=True,
        )

        if batch_index < total_batches - 1:
            print(f"Waiting {BATCH_DELAY}s before next batch...")
            await asyncio.sleep(BATCH_DELAY)

    # Aggregate scores
    output["aggregate_scores"] = {}

    for metric in METRICS.keys():
        values = [
            item["scores"][metric]["score"]
            for item in output["results"]
            if metric in item["scores"]
        ]

        if values:
            output["aggregate_scores"][metric] = round(statistics.fmean(values), 4)

    save_results(output)

    print("\n========== FINAL EVALUATION RESULTS ==========")

    for metric, score in output["aggregate_scores"].items():
        print(f"{metric}: {score}")

    print(f"\nSaved results to: {RESULTS_PATH}")


if __name__ == "__main__":
    asyncio.run(main())
