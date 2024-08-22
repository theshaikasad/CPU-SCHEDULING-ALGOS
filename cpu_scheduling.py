import streamlit as st

# Process class
class Process:
    def __init__(self, name, burst_time, arrival_time, priority):
        self.name = name
        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.priority = priority

# FCFS Scheduling
def fcfs(processes):
    n = len(processes)
    completion_time = [0] * n
    waiting_time = [0] * n
    turnaround_time = [0] * n
    current_time = 0
    total_waiting_time = total_turnaround_time = 0
    
    for i in range(n):
        if current_time < processes[i].arrival_time:
            current_time = processes[i].arrival_time
        completion_time[i] = current_time + processes[i].burst_time
        turnaround_time[i] = completion_time[i] - processes[i].arrival_time
        waiting_time[i] = turnaround_time[i] - processes[i].burst_time
        total_waiting_time += waiting_time[i]
        total_turnaround_time += turnaround_time[i]
        current_time = completion_time[i]
    
    return completion_time, waiting_time, turnaround_time, total_waiting_time / n, total_turnaround_time / n

# SJF Scheduling
def sjf(processes):
    n = len(processes)
    completion_time = [0] * n
    waiting_time = [0] * n
    turnaround_time = [0] * n
    current_time = 0
    total_waiting_time = total_turnaround_time = 0
    completed = [False] * n
    
    for _ in range(n):
        idx = -1
        min_burst = float('inf')
        for i in range(n):
            if processes[i].arrival_time <= current_time and not completed[i]:
                if processes[i].burst_time < min_burst:
                    min_burst = processes[i].burst_time
                    idx = i
        if idx == -1:
            current_time += 1
            continue
        
        completion_time[idx] = current_time + processes[idx].burst_time
        turnaround_time[idx] = completion_time[idx] - processes[idx].arrival_time
        waiting_time[idx] = turnaround_time[idx] - processes[idx].burst_time
        total_waiting_time += waiting_time[idx]
        total_turnaround_time += turnaround_time[idx]
        current_time = completion_time[idx]
        completed[idx] = True
    
    return completion_time, waiting_time, turnaround_time, total_waiting_time / n, total_turnaround_time / n

# Priority Scheduling
def priority_scheduling(processes):
    n = len(processes)
    completion_time = [0] * n
    waiting_time = [0] * n
    turnaround_time = [0] * n
    current_time = 0
    total_waiting_time = total_turnaround_time = 0
    completed = [False] * n
    
    for _ in range(n):
        idx = -1
        highest_priority = float('inf')
        for i in range(n):
            if processes[i].arrival_time <= current_time and not completed[i]:
                if processes[i].priority < highest_priority:
                    highest_priority = processes[i].priority
                    idx = i
        if idx == -1:
            current_time += 1
            continue
        
        completion_time[idx] = current_time + processes[idx].burst_time
        turnaround_time[idx] = completion_time[idx] - processes[idx].arrival_time
        waiting_time[idx] = turnaround_time[idx] - processes[idx].burst_time
        total_waiting_time += waiting_time[idx]
        total_turnaround_time += turnaround_time[idx]
        current_time = completion_time[idx]
        completed[idx] = True
    
    return completion_time, waiting_time, turnaround_time, total_waiting_time / n, total_turnaround_time / n

# Round Robin Scheduling
def round_robin(processes, quantum):
    n = len(processes)
    remaining_burst_time = [proc.burst_time for proc in processes]
    waiting_time = [0] * n
    turnaround_time = [0] * n
    completion_time = [0] * n
    current_time = 0
    total_waiting_time = total_turnaround_time = 0
    start_time = [-1] * n
    process_count = 0
    
    while process_count < n:
        for i in range(n):
            if processes[i].arrival_time <= current_time and remaining_burst_time[i] > 0:
                if start_time[i] == -1:
                    start_time[i] = current_time
                
                if remaining_burst_time[i] > quantum:
                    current_time += quantum
                    remaining_burst_time[i] -= quantum
                else:
                    current_time += remaining_burst_time[i]
                    completion_time[i] = current_time
                    turnaround_time[i] = completion_time[i] - processes[i].arrival_time
                    waiting_time[i] = turnaround_time[i] - processes[i].burst_time
                    total_waiting_time += waiting_time[i]
                    total_turnaround_time += turnaround_time[i]
                    remaining_burst_time[i] = 0
                    process_count += 1
    
    return completion_time, waiting_time, turnaround_time, total_waiting_time / n, total_turnaround_time / n

# Streamlit GUI
def main():
    st.title("CPU Scheduling Algorithms Simulation")
    
    st.sidebar.header("Input Parameters")
    num_processes = st.sidebar.number_input("Number of Processes", min_value=1, max_value=10, value=5)
    
    processes = []
    for i in range(num_processes):
        st.sidebar.subheader(f"Process {i+1}")
        name = st.sidebar.text_input(f"Name - P{i+1}", value=f"P{i+1}")
        burst_time = st.sidebar.number_input(f"Burst Time (ms) - P{i+1}", min_value=1, value=5)
        arrival_time = st.sidebar.number_input(f"Arrival Time (ms) - P{i+1}", min_value=0, value=0)
        priority = st.sidebar.number_input(f"Priority (Lower is Higher) - P{i+1}", min_value=0, value=0)
        processes.append(Process(name, burst_time, arrival_time, priority))
    
    quantum = st.sidebar.number_input("Quantum for Round Robin (ms)", min_value=1, value=2)
    
    if st.sidebar.button("Run Scheduling Algorithms"):
        st.subheader("FCFS Scheduling")
        completion_time, waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time = fcfs(processes.copy())
        display_results(processes, completion_time, waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time)
        
        st.subheader("SJF Scheduling")
        completion_time, waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time = sjf(processes.copy())
        display_results(processes, completion_time, waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time)
        
        st.subheader("Priority Scheduling")
        completion_time, waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time = priority_scheduling(processes.copy())
        display_results(processes, completion_time, waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time)
        
        st.subheader("Round Robin Scheduling")
        completion_time, waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time = round_robin(processes.copy(), quantum)
        display_results(processes, completion_time, waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time)

def display_results(processes, completion_time, waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time):
    n = len(processes)
    st.write("Process\tBurst Time\tArrival Time\tCompletion Time\tWaiting Time\tTurnaround Time")
    for i in range(n):
        st.write(f"{processes[i].name}\t{processes[i].burst_time}\t\t{processes[i].arrival_time}\t\t{completion_time[i]}\t\t{waiting_time[i]}\t\t{turnaround_time[i]}")
    st.write(f"Average Waiting Time: {avg_waiting_time:.2f} ms")
    st.write(f"Average Turnaround Time: {avg_turnaround_time:.2f} ms")

if __name__ == "__main__":
    main()
