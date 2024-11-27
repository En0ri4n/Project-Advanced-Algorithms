import concurrent.futures
import numpy as np
from scipy.spatial.distance import cdist
import src.variables as vars
from src.aco.ant import Ant
from src.objects.truck import Truck


class ACO:
    costs: np.ndarray

    def __init__(self, customers, truck_count, truck_capacity, pheromone_importance=1.0, heuristic_importance=2.0, evaporation_rate=0.1, pheromone_init=1.0, iterations=100, ants_count=10,
                 debug=False):
        vars.distance_matrix = cdist([[customer.x_coord, customer.y_coord] for customer in customers], [[customer.x_coord, customer.y_coord] for customer in customers], 'euclidean')

        self.depot = customers.pop(0)
        self.customers = customers
        self.truck_count = truck_count
        self.truck_capacity = truck_capacity
        self.pheromone_importance = pheromone_importance
        self.heuristic_importance = heuristic_importance
        self.evaporation_rate = evaporation_rate
        self.pheromone_init = pheromone_init
        self.iterations = iterations
        self.ants_count = ants_count
        self.pheromone = np.full((len(customers) + 1, len(customers) + 1), pheromone_init)

        self.costs = np.array([])
        self.debug = debug

    def remove_unused_trucks(self, solution):
        return [route for route in solution if len(route) > 2] if solution else []

    def run(self):
        print("Running ACO...")

        best_solution = None
        best_cost = float('inf')

        for _ in range(self.iterations):

            ants = [Ant(self.customers, self.depot, [Truck(self.truck_capacity) for _ in range(self.truck_count)]) for _ in range(self.ants_count)]

            with concurrent.futures.ThreadPoolExecutor() as executor:

                futures = [executor.submit(self.construct_and_evaluate, ant) for ant in ants]

                for future in concurrent.futures.as_completed(futures):
                    cost, solution = future.result()

                    if self.debug:
                        print(f"Solution found, Cost: {cost:.2f} ({int(cost < best_cost)})")

                    self.costs = np.append(self.costs, cost)

                    if cost < best_cost:
                        best_cost = cost
                        best_solution = solution

            self.update_pheromone(ants)

        return self.remove_unused_trucks(best_solution), best_cost  # Return the best solution and its cost (removing unused trucks)

    def construct_and_evaluate(self, ant):
        ant.construct_solution(self.pheromone, self.pheromone_importance, self.heuristic_importance)
        cost = self.calculate_distance_cost(ant.solution)

        return cost, ant.solution

    def calculate_distance_cost(self, solution):
        return sum(sum(route[i].distance_to(route[i + 1]) for i in range(len(route) - 1)) for route in solution)

    def update_pheromone(self, ants):

        self.pheromone *= (1 - self.evaporation_rate)
        best_ants = sorted(ants, key=lambda ant: self.calculate_distance_cost(ant.solution))[:self.ants_count // 2]

        for ant in best_ants:
            for route in ant.solution:
                for i in range(len(route) - 1):
                    self.pheromone[route[i].cust_no][route[i + 1].cust_no] += 1 / self.calculate_distance_cost(ant.solution)
