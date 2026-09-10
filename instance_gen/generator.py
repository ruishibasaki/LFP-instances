import random
import sys
import math

def read_params(param_file):
    params = {}
    def parse_number(value):
        try:
            # Try integer first
            return int(value)
        except ValueError:
            try:
                # Then try float
                return float(value)
            except ValueError:
                # Fallback: return raw string
                return value

    with open(param_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if "=" in line:
                key, value = line.split("=", 1)
                value = value.strip()
                params[key.strip()] = parse_number(value)

    return params



def rand_float(a, b, decimals=2):
    """Generate a float between a and b with given precision."""
    return round(random.uniform(a, b), decimals)

def adjust_demands_to_delta(demands, capacities, lotq, delta1, delta):
    n_items = len(demands)
    n_periods = len(demands[0])
    n_bins = len(capacities)
	

 
    # Compute averages
    avg_lotq= sum(sum(lotq[i]) for i in range(n_items)) / (n_items*n_bins)
    avg_demand = sum(sum(demands[i]) for i in range(n_items)) / (n_items*n_periods)
    #max_capacity = max(capacities)

    # actual delta
    delta_real = avg_demand/(delta1*avg_lotq) 
    # scaling factor
    alpha = delta / delta_real
    
    # print for debugging
    print("Before correction: delta_real=", delta_real, "alpha=", alpha)

    # Apply correction
    for i in range(n_items):
        for t in range(n_periods):
            demands[i][t] = max(1, round(alpha*demands[i][t]))  # ensure positivity

    # Optional: recompute final delta
    avg_demand = sum(sum(demands[i]) for i in range(n_items)) / (n_items*n_periods)
    final_delta =  avg_demand/(delta1*avg_lotq) 
    print("After correction: delta_real=", final_delta)

    return demands


def adjust_capacities_to_delta(demands, capacities, delta):
    n_items = len(demands)
    n_periods = len(demands[0])
    n_bins = len(capacities)
	
    # Compute averages
    tt_capacity = sum(capacities) 
    #max_capacity = max(capacities)


    # actual delta
    delta_real = tt_capacity/n_items 
    # scaling factor
    alpha = delta / delta_real
    
    # print for debugging
    print("Before capa correction: delta_real=", delta_real, "alpha=", alpha)

    # Apply correction
    for k in range(n_bins):
    	capacities[k] = max(1, round(alpha*capacities[k]))

    # Optional: recompute final delta
    tt_capacity = sum(capacities) 
    final_delta = tt_capacity/n_items 
    print("After capa correction: delta_real=", final_delta)

    return capacities



def generate_instance_from_params(param_file, output_file):
    p = read_params(param_file)

    n_items = int(p["n_items"])
    n_periods = int(p["n_periods"])
    n_bins = int(p["n_bins"])

    # Storage
    prices = []
    hold_costs = []
    demands = []
    stock0 = []
    capacities = []
    lotq = []
    hand_costs = []

    # === Generate all data in memory first ===

    # Items section
    for i in range(n_items):
        price = random.randint(p["price_min"], p["price_max"])
        prices.append(price)

        hold_cost = math.ceil(rand_float(p["hold_cost_min"], p["hold_cost_max"]) * price)
        hold_costs.append(hold_cost)

        item_demands = [
            random.randint(p["demand_min"], p["demand_max"])
            for _ in range(n_periods)
        ]
        demands.append(item_demands)

        s0 = random.randint(p["stock0_min"], p["stock0_max"])
        stock0.append(s0)

    # Bins section
    for k in range(n_bins):
        capacity = random.randint(p["capacity_min"], p["capacity_max"])
        capacities.append(capacity)

    # Lotq section
    interval = (p["lotq_max"]-p["lotq_min"])/n_bins
    for i in range(n_items):
        line = [
            random.randint(int(p["lotq_min"]+interval*j), int(p["lotq_min"]+interval*(j+1)))
            for j in range(n_bins)
        ]
        lotq.append(line)

    # Hand cost section = b_i*(lot_ik)^\alpha + price_i*lot_ik
    base = random.randint(p["hand_cost_min"], p["hand_cost_max"])
    for i in range(n_items):
        avg_lot = sum(lotq[i])/n_bins
        b = base/avg_lot

        item_hand_costs = []
        for k in range(n_bins):
            hc = math.ceil(b*(lotq[i][k]**p["economies_scale"]) + prices[i]*lotq[i][k])
            item_hand_costs.append(hc)

        hand_costs.append(item_hand_costs)

    adjust_capacities_to_delta(demands, capacities, p["capacity_ratio1"])
    adjust_demands_to_delta(demands, capacities, lotq, p["capacity_ratio1"], p["capacity_ratio2"])
    # === Write everything to the file ===
    with open(output_file, "w") as f:

        # Header
        f.write(f"{n_items} {n_periods} {n_bins}\n")

        # Items
        for i in range(n_items):
            f.write(f"{hold_costs[i]} ")
            f.write(" ".join(map(str, demands[i])) + " ")
            f.write(f"{stock0[i]} {prices[i]}\n")

        # Capacities
        f.write(" ".join(map(str, capacities)) + "\n")

        # Lotq
        for i in range(n_items):
            f.write(" ".join(map(str, lotq[i])) + "\n")

        # Hand costs
        for i in range(n_items):
            f.write(" ".join(map(str, hand_costs[i])) + "\n")


# Example usage:
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generator.py <param_file> <output_instance>")
        sys.exit(1)

    param_file = sys.argv[1]
    output_file = sys.argv[2]

    generate_instance_from_params(param_file, output_file)
    print(f"Instance generated in: {output_file}")

