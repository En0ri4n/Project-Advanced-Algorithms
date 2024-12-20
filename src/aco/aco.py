import concurrent.futures
import numpy as np
from scipy.spatial.distance import cdist
import src.variables as algo_vars
from src.aco.ant import Ant
from src.objects.truck import Truck


class ACO:
    costs: np.ndarray

    def __init__(self, customers, truck_count, truck_capacity, pheromone_importance=1.0, heuristic_importance=2.0, evaporation_rate=0.1, pheromone_init=1.0, iterations=100, ants_count=10,
                 do_stagnation_fuse=False, debug=False):
        algo_vars.distance_matrix = cdist([[customer.x_coord, customer.y_coord] for customer in customers], [[customer.x_coord, customer.y_coord] for customer in customers], 'euclidean')

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

        self.best_solution = None

        self.costs = np.array([])
        self.do_stagnation_fuse = do_stagnation_fuse
        self.debug = debug

    def remove_unused_trucks(self, solution):
        return [route for route in solution if len(route) > 2] if solution else []

    def run(self):
        print("Running ACO...")

        best_solution = None
        best_cost = float('inf')
        stagnation_count = 0
        max_stagnation = self.iterations // 10  # Number of iterations to allow without improvement

        for iteration in range(self.iterations):
            ants = [Ant(self.customers, self.depot, [Truck(self.truck_capacity) for _ in range(self.truck_count)]) for _ in range(self.ants_count)]

            iteration_best_cost = float('inf')
            iteration_best_solution = None

            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(self.construct_and_evaluate, ant) for ant in ants]

                for future in concurrent.futures.as_completed(futures):
                    cost, solution = future.result()

                    if self.debug:
                        print(f"Iteration {iteration + 1}, Solution found, Cost: {cost:.2f}")

                    self.costs = np.append(self.costs, cost)

                    if cost < iteration_best_cost:
                        iteration_best_cost = cost
                        iteration_best_solution = solution

            # Update global best solution if current iteration finds a better one
            if iteration_best_cost < best_cost:
                best_cost = iteration_best_cost
                best_solution = iteration_best_solution
                stagnation_count = 0  # Reset stagnation counter on improvement
            else:
                stagnation_count += 1

            self.update_pheromone(ants)

            # Check for stagnation at iteration level
            if stagnation_count >= max_stagnation and self.do_stagnation_fuse:
                print(f"Stagnation detected at iteration {iteration + 1}. Fusing pheromone matrices.")
                self.fuse_pheromone_matrices()
                stagnation_count = 0  # Reset stagnation counter

        self.best_solution = best_solution

    def fuse_pheromone_matrices(self):
        """
        Fuses the current pheromone matrix with a new, reset matrix to retain some learned behavior
        while encouraging exploration.
        """
        reset_pheromone = np.full(self.pheromone.shape, self.pheromone_init)  # Freshly reset pheromone matrix
        fusion_weight = 0.8  # Weight for combining old and new matrices (0.5 gives equal weight)

        self.pheromone = fusion_weight * self.pheromone + (1 - fusion_weight) * reset_pheromone

    def get_results(self):
        """
        Get the results of the ACO algorithm.\n
        /!\\\ You need to run the ACO algorithm first before calling this function. /!\\\\

        :return:
            costs (np.ndarray): The costs of the ACO algorithm at each iteration.
            best_solution (list): The best solution found by the ACO algorithm.
            truck_count (list): The number of trucks used in the best solution.
            total_distance (float): The total distance of the best solution.
            total_time (float): The total time of the best solution
        """

        best_solution_reduced = self.remove_unused_trucks(self.best_solution)

        truck_count = len([len(route) for route in best_solution_reduced if len(route) > 2])
        total_distance = sum(sum(route[i].distance_to(route[i + 1]) for i in range(len(route) - 1)) for route in best_solution_reduced)
        total_time = sum(sum(customer.service_time for customer in route[1:-1]) + sum(route[i].distance_to(route[i + 1]) for i in range(len(route) - 1)) for route in best_solution_reduced)

        return self.customers, self.depot, self.costs, best_solution_reduced, truck_count, total_distance, total_time

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
