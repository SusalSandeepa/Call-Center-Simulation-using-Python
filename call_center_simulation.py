import simpy          # SimPy is a library for running time-based simulations
import random         # Random is used to make arrivals and service times random

# One caller process (a person who calls the center)
def customer(env, name, agents, service_time, stats):
    arrival_time = env.now
    print(f"{name} arrives at time {arrival_time:.2f}")

    # Ask for an available agent
    with agents.request() as request:
        yield request   # Wait until an agent is free

        # Calculate how long this caller waited
        wait = env.now - arrival_time
        stats["wait_times"].append(wait)
        print(f"{name} starts call at {env.now:.2f} (Waited {wait:.2f} min)")

        # Time taken to finish the call
        yield env.timeout(random.expovariate(1 / service_time))
        print(f"{name} ends call at {env.now:.2f}")

        # Increase the number of finished calls
        stats["finished_calls"] += 1

# This keeps creating new callers over time
def generate_customers(env, agents, arrival_gap, service_time, stats):
    i = 0
    while True:
        # Wait a random time before next caller comes
        yield env.timeout(random.expovariate(1 / arrival_gap))
        i += 1
        # Create a new caller and start their process
        env.process(customer(env, f"Caller {i}", agents, service_time, stats))
        stats["arrived_calls"] += 1

# This checks how many people are waiting in the queue
def watch_queue(env, agents, stats, sample_time=1.0):
    while True:
        # Record number of people waiting
        stats["queue_sizes"].append(len(agents.queue))
        yield env.timeout(sample_time)

# Main function that runs the whole simulation
def run_simulation(sim_time, num_agents, arrival_gap, service_time, seed=0):
    random.seed(seed)
    env = simpy.Environment()
    agents = simpy.Resource(env, capacity=num_agents)

    # Store all counts and averages here
    stats = {
        "arrived_calls": 0,
        "finished_calls": 0,
        "wait_times": [],
        "queue_sizes": []
    }

    env.process(generate_customers(env, agents, arrival_gap, service_time, stats))
    env.process(watch_queue(env, agents, stats))
    env.run(until=sim_time)

    print(stats)

if __name__ == "__main__":
    print("SIMPLE CALL CENTER SIMULATION\n")
    run_simulation(100, 2, 5, 8)
