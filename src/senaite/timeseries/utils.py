import json


def format_timeseries(obj, results):
    def safe_float(value, default):
        try:
            return float(value)
        except (TypeError, ValueError):
            return default
    min_range = safe_float(obj.ResultsRange.get("min"), -1000000)
    max_range = safe_float(obj.ResultsRange.get("max"), 1000000)

    values = []
    if results:
        values = json.loads(results)
    new_results = []
    for row in values:
        new_row = []
        for val in row:
            OOR = False
            try:
                new_val = float(val)
                if new_val < min_range or new_val > max_range:
                    OOR = True
            except Exception:
                new_val = val
            new_row.append({"val": val, "OOR": OOR})
        new_results.append(new_row)
    return json.dumps(new_results)
