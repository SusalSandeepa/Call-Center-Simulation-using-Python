# Call-Center-Simulation-using-Python

Purpose 

  o This program simulates a small call center to study how the number of agents affects 

Performance. 

  o It helps understand how waiting time, queue size, and agent utilization change when more agents 
  are added. 

Requirements 

  o Python 3 installed on your computer 
  o The library SimPy (You can install it by running this command in your terminal or command 
  prompt) 

pip install simpy 

How to Run 

  o Open the Python file (call_center_simulation.py) in any IDE or text editor. 
  
  o Run the program by pressing Run or typing this in your terminal: 

python call_center_simulation.py 

  When you run the program, it will ask you to enter the number of agents for the simulation. 
  You can then change the service time or arrival gap directly in the code to test different conditions 
  and see how they affect performance. 

Results will be printed on the screen, showing: 

  o Average waiting time 
  o Average queue length 
  o Throughput 
  o Utilization 
  o Total calls arrived and finished 

How to Change Settings 

  You can easily change the test settings in the code:

    num_agents = int(input("Enter the number of agents for the simulation: ")) 

        # Run simulation for user input 
        
        result = run_simulation( 
        
            sim_time=100,       # you can change total time here to run the test  
            
            num_agents=num_agents, 
            
            arrival_gap=5,      # you can change arrival gap here 
            
            service_time=8,     # you can change average time to finish a call here 
            
            seed=10 
            
        ) 
 
 
Output Example 
 
  Results for  Agents=2, Service Time=8 and Arrival Gap =5 : 

    Average Wait (min): 14.22 
    
    Average Queue Length: 2.67 
  
    Throughput (calls/min): 0.15 
    
    Utilization: 0.6 
    
    Total Calls Arrived: 19 
    
    Total Calls Finished: 15 ---------------------------------
