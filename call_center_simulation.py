import simpy          # SimPy is a library for running time-based simulations
import random         # Random is used to make arrivals and service times random

# One caller process (a person who calls the center)
def customer(env, name, agents, service_time):
    arrival_time = env.now
    print(f"{name} arrives at time {arrival_time:.2f}")

    # Ask for an available agent
    with agents.request() as request:
        yield request   # Wait until an agent is free

        # Time taken to finish the call
        yield env.timeout(random.expovariate(1 / service_time))
        print(f"{name} ends call at {env.now:.2f}")

# This keeps creating new callers over time
def generate_customers(env, agents, arrival_gap, service_time):
    i = 0
    while True:
        # Wait a random time before next caller comes
        yield env.timeout(random.expovariate(1 / arrival_gap))
        i += 1
        # Create a new caller and start their process
        env.process(customer(env, f"Caller {i}", agents, service_time))

# MAIN PROGRAM
if __name__ == "__main__":
    print("SIMPLE CALL CENTER SIMULATION\n")

    env = simpy.Environment()                     # Create the simulation world
    agents = simpy.Resource(env, capacity=2)      # Number of available agents
    env.process(generate_customers(env, agents, 5, 8))
    env.run(until=30)                             # Run for 30 minutes
