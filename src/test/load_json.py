import json
from pathlib import Path


DATASET_PATH = Path(__file__).parent /"rag_eval.json"


def load_dataset():

    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    samples = []

    for item in data:
        sample = {
            "id": item["id"],
            "user_input": item["question"],
            "response": item["answer"],
            "retrieved_contexts": item["contexts"],
            "reference": item["ground_truth"],
        }

        if not all(
            [
                sample["user_input"],
                sample["response"],
                sample["retrieved_contexts"],
                sample["reference"],
            ]
        ):
            raise ValueError(f"Invalid evaluation sample: {item['id']}")

        if not isinstance(sample["retrieved_contexts"], list):
            raise TypeError(f"Contexts must be a list: {item['id']}")

        samples.append(sample)

    print(f"Loaded {len(samples)} samples")

    return samples
