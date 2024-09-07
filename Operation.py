import random
import numpy as np
import matplotlib.pyplot as plt

class MiningTruck():
    def __init__(self,id):
        self.id = id # Every Truck will have an ID
        self.state = 'unstarted' #initial state of truck
        self.time_mining = 0.0 # total time spent loading in the simulation
        self.time_traveling = 0.0 # total time spent 
        self.time_waiting = 0.0 # time waiting in queue to unload
        self.time_unloading = 0.0 # total time spent unloading
        self.time_remaining = 0.0 # Time remaining on current task
        self.current_station = None # keep track of the station bieng used when mining
        self.load_count = 0 # loads delivered

    def start_mine(self):
        
        self.state = "mining"
        mining_time = random.uniform(1, 5) # Mining trucks can spend a random duration between 1 to 5 hours mining at sites
        self.time_remaining = mining_time
        #print('Start mine for truck ', self.id)

    
    def start_travel_to_station(self):
        self.state = 'travel_to_station'
        self.time_remaining = 0.5 #30 minutes to travel to station
        #print('Start travel to station for truck ', self.id)

    def start_wait(self, wait_time):
        self.state = 'waiting'
        self.time_remaining = wait_time
        #print('Start wait for truck ', self.id,'waiting ', wait_time)

    def start_unload(self):
        self.state = 'unloading'
        self.time_remaining = 5.0/60.0 # 5 minutes to unload
        #print('Start unload for truck ', self.id)


    def start_travel_to_site(self):
        self.state = 'travel_to_mine'
        self.time_remaining = 0.5 # 30 minutes to travel to station
        #print('Start travel to Mine for truck ', self.id)

class UnloadStation():
    def __init__(self,id):
        self.id = id #Every Station will have an ID
        self.queue = [] # Queue of trucks waiting to Unload at that particular station
        self.trucks_unloaded_count = 0

    def add_truck(self,truck):
        self.queue.append(truck)

    def remove_truck(self): 
        self.queue.pop(0)

class Operation():
    def __init__(self, truck_count, station_count):
        self.trucks = [MiningTruck(i) for i in range(truck_count)]
        self.stations = [UnloadStation(i) for i in range(station_count)]
        self.simulation_time = 0.0 # Start at 0 
        self.time_step = 1.0/60.0 # 1 minute time steps
        self.max_time = 72.0 # 72 hour simulation
        
        # Data for plotting
        self.truck_times = {truck.id: {'mining': [], 'traveling': [], 'waiting': [], 'unloading': []} for truck in self.trucks}
        self.station_loads = {station.id: [] for station in self.stations}


    def simulate(self):
        while self.simulation_time < self.max_time:
            #print(self.simulation_time)
            
            for truck in self.trucks:
                # Pass a time step & update stats
                # truck.update_stats(time_step=self.time_step)

                truck.time_remaining -= self.time_step
                if truck.state == 'mining': 
                    truck.time_mining += self.time_step
                    self.truck_times[truck.id]['mining'].append(truck.time_mining)
                elif truck.state in ['travel_to_station', 'travel_to_mine']: 
                    truck.time_traveling += self.time_step
                    self.truck_times[truck.id]['traveling'].append(truck.time_traveling)
                elif truck.state == 'unloading': 
                    truck.time_unloading += self.time_step
                    self.truck_times[truck.id]['unloading'].append(truck.time_unloading)
                elif truck.state == 'waiting': 
                    truck.time_waiting += self.time_step
                    self.truck_times[truck.id]['waiting'].append(truck.time_waiting)

                # Current State has Ended
                if truck.time_remaining <= 0:
                    if truck.state == 'mining':
                        #Mining Completed - now travel to station
                        truck.start_travel_to_station()
                    elif truck.state == 'travel_to_station':
                        # Traveling
                        # Only Wait if assigned to a queue with a line
                        station = self.find_min_wait_station()
                        station.queue.append(truck)  # Add the truck to the station's queue
                        truck.current_station = station  # Track the station
            
                        # Check if the queue was empty (truck can start unloading immediately)
                        if len(station.queue) == 1:  
                            truck.start_unload()
                        else:
                            # Otherwise, calculate wait time and start wait in line
                            wait_time = self.calculate_wait_time(station)
                            truck.start_wait(wait_time)

                    elif truck.state == 'waiting':
                        # Done Waiting in Line - can start unload
                        truck.start_unload()
                    elif truck.state == 'unloading':
                        # Done Unloading - can head back to mining site
                        # Directly remove the truck from the tracked station's queue
                        station = truck.current_station
                        station.remove_truck() 
                        #print('UnloadingStation:', station.id)
                        truck.current_station = None  # Clear the station reference
                        truck.load_count += 1
                        station.trucks_unloaded_count += 1
                        self.station_loads[station.id].append(station.trucks_unloaded_count)
                        truck.start_travel_to_site()
                    elif truck.state in ['travel_to_mine', 'unstarted']: 
                        # Done traveling to mine, can start mininig again
                        # if truck.state == 'unstarted':
                        #     print('here We are')
                        truck.start_mine()

            self.simulation_time += self.time_step

    def find_min_wait_station(self):
        return min(self.stations, key=lambda station: len(station.queue))
    
    def calculate_wait_time(self, station):

        # Time remaining for the truck at the front of the queue
        front_truck = station.queue[0]
        front_truck_remaining_time = front_truck.time_remaining

        # Calculate the wait time for the current truck
        queue_length = len(station.queue)
        wait_time = front_truck_remaining_time + (queue_length - 1) * 5 / 60.0  # Convert minutes to hours

        return wait_time
    

    def report_statistics(self):
        #TODO - see what other truck stats may be good
        print("=== Truck Statistics ===")
        for truck in self.trucks:
            print(f"Truck {truck.id}:")
            print(f"  Loaded Count: {truck.load_count}")
            print(f"  Total Mining Time: {truck.time_mining:.2f} hours")
            print(f"  Total Travel Time: {truck.time_traveling:.2f} hours")
            print(f"  Total Unload Time: {truck.time_unloading:.4f} hours")
            print(f"  Total Wait Time: {truck.time_waiting:.4f} hours")
            total_time = truck.time_mining + truck.time_traveling + truck.time_unloading + truck.time_waiting
            print('total time:', total_time)
            # print(f"  Efficiency (Load/Total Time): {truck.loaded_count / total_time:.2f} loads/hour" if total_time > 0 else "  Efficiency: N/A")

        print("\n=== Station Statistics ===")
        for station in self.stations:
            print(f"Station {station.id}:")
            print(f" Number of times Trucks Unloaded Here: {station.trucks_unloaded_count}")

      # Plotting
        self.plot_statistics()

    # Update the plotting function
    def plot_statistics(self):
        # Plot Truck Times Distribution
        truck_ids = list(self.truck_times.keys())
        n_trucks = len(truck_ids)
        
        # Set up the bar chart parameters
        bar_width = 0.2
        index = np.arange(n_trucks)
        
        mining_times = [sum(self.truck_times[truck_id]['mining']) / 60 for truck_id in truck_ids]
        traveling_times = [sum(self.truck_times[truck_id]['traveling']) / 60 for truck_id in truck_ids]
        waiting_times = [sum(self.truck_times[truck_id]['waiting']) / 60 for truck_id in truck_ids]
        unloading_times = [sum(self.truck_times[truck_id]['unloading']) / 60 for truck_id in truck_ids]

        plt.figure(figsize=(14, 8))
        plt.bar(index - 1.5 * bar_width, mining_times, bar_width, label='Mining Time')
        plt.bar(index - 0.5 * bar_width, traveling_times, bar_width, label='Traveling Time')
        plt.bar(index + 0.5 * bar_width, waiting_times, bar_width, label='Waiting Time')
        plt.bar(index + 1.5 * bar_width, unloading_times, bar_width, label='Unloading Time')
        
        plt.xlabel('Truck ID')
        plt.ylabel('Minutes')
        plt.title('Distribution of Time Spent in Each State per Truck')
        plt.xticks(index, truck_ids)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        # Plot Number of Loads per Station
        station_ids = list(self.station_loads.keys())
        loads_per_station = [len(self.station_loads[station_id]) for station_id in station_ids]
        
        plt.figure(figsize=(12, 6))
        plt.bar(station_ids, loads_per_station, color='skyblue')
        
        plt.xlabel('Station ID')
        plt.ylabel('Number of Loads')
        plt.title('Number of Loads Handled per Station')
        plt.grid(axis='y')
        plt.tight_layout()
        plt.show()


    def run(self):
        self.simulate()
        self.report_statistics()

if __name__ == "__main__":
    operation = Operation(truck_count=200, station_count=15)
    operation.run()
