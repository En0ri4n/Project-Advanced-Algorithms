import random


class Ant:
    def __init__(self, customers, depot, trucks):
        """
        Initializes an Ant object.

        Parameters:
        customers (list): List of customer objects.
        depot (object): The depot (warehouse) object.
        trucks (list): List of truck objects.
        """
        self.customers = customers
        self.depot = depot
        self.trucks = trucks
        self.solution = []

    def construct_solution(self, pheromone, pheromone_importance, heuristic_importance):
        """
        Constructs a solution for the ant by assigning customers to trucks.

        Parameters:
        pheromone (list): Pheromone levels between customers.
        pheromone_importance (float): Pheromone importance factor.
        heuristic_importance (float): Heuristic importance factor.
        """
        unvisited = self.customers[:]
        random.shuffle(unvisited)
        for truck in self.trucks:
            truck.route = [self.depot]
            truck.load = 0
            truck.time = 0
            while unvisited:
                next_customer = self.select_next_customer(truck, unvisited, pheromone, pheromone_importance, heuristic_importance)
                if next_customer is None:
                    break
                travel_time_to_next = truck.route[-1].distance_to(next_customer)
                travel_time_to_depot = next_customer.distance_to(self.depot)
                # Check if adding the next customer allows the truck to return on time
                if truck.time + travel_time_to_next + next_customer.service_time + travel_time_to_depot > self.depot.due_date:
                    break
                truck.route.append(next_customer)
                truck.load += next_customer.demand
                truck.time += travel_time_to_next + next_customer.service_time
                unvisited.remove(next_customer)
            truck.route.append(self.depot)  # Return to the depot
        self.solution = [truck.route for truck in self.trucks]

    def select_next_customer(self, truck, unvisited, pheromone, pheromone_importance, heuristic_importance):
        """
        Selects the next customer for the truck to visit based on pheromone levels and heuristic information.

        Parameters:
        truck (object): The current truck object.
        unvisited (list): List of unvisited customer objects.
        pheromone (list): Pheromone levels between customers.
        pheromone_importance (float): Pheromone importance factor.
        heuristic_importance (float): Heuristic importance factor.

        Returns:
        object: The next customer object to visit, or None if no feasible customer is found.
        """
        feasible_customers = [
            c for c in unvisited
            if truck.load + c.demand <= truck.capacity and truck.time + truck.route[-1].distance_to(c) + c.service_time + c.distance_to(self.depot) <= self.depot.due_date
        ]
        if not feasible_customers:
            return None
        probabilities = []
        for customer in feasible_customers:
            pheromone_level = pheromone[truck.route[-1].cust_no][customer.cust_no]
            heuristic_value = 1 / (truck.route[-1].distance_to(customer) + 1e-6)
            probabilities.append((pheromone_level ** pheromone_importance) * (heuristic_value ** heuristic_importance))
        total = sum(probabilities)
        probabilities = [p / total for p in probabilities]
        return random.choices(feasible_customers, probabilities)[0]
