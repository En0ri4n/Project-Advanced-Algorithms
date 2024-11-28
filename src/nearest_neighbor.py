import src.variables as algo_vars
from scipy.spatial.distance import cdist
from src.objects.truck import Truck


class NNO:
    def __init__(self, customers, truck_count, truck_capacity):
        self.customers = customers.copy()
        self.depot = self.customers.pop(0)
        self.trucks = [Truck(truck_capacity) for _ in range(truck_count)]
        algo_vars.distance_matrix = cdist([[customer.x_coord, customer.y_coord] for customer in customers], [[customer.x_coord, customer.y_coord] for customer in customers], 'euclidean')

    def run(self) -> float:
        """
        Solves the vehicle routing problem using the nearest neighbor heuristic with multiple trucks,
        respecting the capacity and time window constraints.

        Returns:
        float: The total distance traveled by the trucks.
        """
        unvisited = self.customers[:]
        total_distance = 0
        for truck in self.trucks:
            truck.route = [self.depot]
            truck.load = 0
            truck.time = 0
            current = self.depot
            while unvisited:
                feasible_customers = [
                    customer for customer in unvisited
                    if truck.load + customer.demand <= truck.capacity and
                       truck.time + current.distance_to(customer) <= customer.due_date
                ]
                if not feasible_customers:
                    break
                nearest = min(feasible_customers, key=lambda customer: current.distance_to(customer))
                travel_time = current.distance_to(nearest)
                arrival_time = truck.time + travel_time
                if arrival_time < nearest.ready_time:
                    arrival_time = nearest.ready_time  # Wait until the customer's ready time
                truck.route.append(nearest)
                truck.load += nearest.demand
                truck.time = arrival_time + nearest.service_time
                total_distance += travel_time
                current = nearest
                unvisited.remove(nearest)
            total_distance += current.distance_to(self.depot)
            truck.route.append(self.depot)  # Return to the depot

        print("-" * 50)
        print("Nearest Neighbor Solution with Multiple Trucks:")
        print(f"Number of trucks used: {len([truck for truck in self.trucks if len(truck.route) > 2])}")
        print(f"Total distance traveled by the trucks: {total_distance:.2f}")
        print("-" * 50)
        return total_distance
