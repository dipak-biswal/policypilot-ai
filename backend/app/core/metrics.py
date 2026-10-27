PRICES = {"gpt-4o-mini": {"input": 0.15, "output": 0.60}}


def estimate_cost(usage: dict) -> float:
    total = 0.0
    for model, u in usage.items():
        key = next((k for k in PRICES if model.startswith(k)), None)
        if not key:
            continue
        p = PRICES[key]
        total += u.get("input_tokens", 0) / 1e6 * p["input"]
        total += u.get("output_tokens", 0) / 1e6 * p["output"]
    return round(total, 6)
