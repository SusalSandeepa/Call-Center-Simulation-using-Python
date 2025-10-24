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
    random.seed(seed)                # Make random numbers repeatable
    env = simpy.Environment()        # Create the simulation world
    agents = simpy.Resource(env, capacity=num_agents)  # Number of available agents

    # Store all counts and averages here
    stats = {
        "arrived_calls": 0,
        "finished_calls": 0,
        "wait_times": [],
        "queue_sizes": []
    }

    # Start processes: callers and queue watcher
    env.process(generate_customers(env, agents, arrival_gap, service_time, stats))
    env.process(watch_queue(env, agents, stats))

    # Run the simulation for the set time
    env.run(until=sim_time)

    # Find average waiting time
    if stats["wait_times"]:
        avg_wait = sum(stats["wait_times"]) / len(stats["wait_times"])
    else:
        avg_wait = 0.0

    # Find average queue length
    if stats["queue_sizes"]:
        avg_queue = sum(stats["queue_sizes"]) / len(stats["queue_sizes"])
    else:
        avg_queue = 0.0

    # How many calls finished per minute
    throughput = stats["finished_calls"] / sim_time
    # How busy agents were on average
    utilization = throughput * service_time / num_agents

    # Return all results
    return {
        "Agents": num_agents,
        "Average Wait (min)": round(avg_wait, 2),
        "Average Queue Length": round(avg_queue, 2),
        "Throughput (calls/min)": round(throughput, 3),
        "Utilization": round(utilization, 3),
        "Arrived Calls": stats["arrived_calls"],
        "Finished Calls": stats["finished_calls"]
    }


# MAIN PROGRAM
if __name__ == "__main__":
    print("SIMPLE CALL CENTER SIMULATION\n")

    # Ask user for number of agents
    try:
        num_agents = int(input("Enter the number of agents for the simulation: "))

        # Run simulation for user input
        result = run_simulation(
            sim_time=100,       # Total time to run the test
            num_agents=num_agents,
            arrival_gap=5,      # Average minutes between new calls
            service_time=8,     # Average time to finish a call
            seed=10
        )

        # Print results
        print(f"\nResults for {result['Agents']} Agents:")
        print(f"  Average Wait (min): {result['Average Wait (min)']}")
        print(f"  Average Queue Length: {result['Average Queue Length']}")
        print(f"  Throughput (calls/min): {result['Throughput (calls/min)']}")
        print(f"  Utilization: {result['Utilization']}")
        print(f"  Total Calls Arrived: {result['Arrived Calls']}")
        print(f"  Total Calls Finished: {result['Finished Calls']}")
        print("----------------------------------\n")

    except ValueError:
        print("Please enter a valid number of agents.")
