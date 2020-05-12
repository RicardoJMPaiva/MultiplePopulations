import random
import json
# knapsack

kp = {
    "V": 10,
    "R": 5,
    "NR_ITEMS": 250,    # 100, 250, 500
    # "C": 20,    # 2 * v or 0.5 * sum (weights)
}

def generate_uncor():
    weights = [random.uniform(1,kp["V"]) for i in range(kp["NR_ITEMS"])]
    values = [random.uniform(1,kp["V"]) for i in range(kp["NR_ITEMS"])]
    capacity = int(0.5 * sum(weights))
    return {'weights':weights, 'values':values, 'capacity': capacity}

def generate_weak_cor():
    weights = [random.uniform(1,kp["V"]) for i in range(kp["NR_ITEMS"])]
    values = []
    for i in range(kp["NR_ITEMS"]):
        value = weights[i] + random.uniform(-kp["R"],kp["R"])
        while value <= 0:
            value = weights[i] + random.uniform(-kp["R"],kp["R"])
        values.append(value)
    capacity = int(0.5 * sum(weights))
    return {'weights':weights, 'values':values, 'capacity': capacity}

def generate_strong_cor():
    weights = [random.uniform(1,kp["V"]) for i in range(kp["NR_ITEMS"])]
    values = [weights[i] + kp["R"] for i in range(kp["NR_ITEMS"])]
    capacity = int(0.5 * sum(weights))
    return {'weights':weights, 'values':values, 'capacity': capacity}

def perturbation():
    kp["N"] = kp["N"] + 1
    if kp["N"] > (len(kp["NR_ITEMS"]) - 1):
        kp["N"] = 0


if __name__ == "__main__":
    datasets = []
    for _ in range(10):
        datasets.append(generate_weak_cor())
    open("datasets/dataset1.json", 'w').write(json.dumps(datasets))