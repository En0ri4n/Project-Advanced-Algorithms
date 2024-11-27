import src.variables as vars
from scipy.spatial.distance import cdist


class NNO:
    def __init__(self, customers):
        self.customers = customers.copy()
        self.depot = self.customers.pop(0)
        vars.distance_matrix = cdist([[customer.x_coord, customer.y_coord] for customer in customers], [[customer.x_coord, customer.y_coord] for customer in customers], 'euclidean')

    def run(self) -> float:
        """
        Solves the vehicle routing problem using the nearest neighbor heuristic.

        Returns:
        float: The total distance traveled by the truck.
        """
        unvisited = self.customers[:]
        total_distance = 0
        route = [self.depot]
        current = self.depot
        while unvisited:
            nearest = min(unvisited, key=lambda customer: current.distance_to(customer))
            route.append(nearest)
            total_distance += current.distance_to(nearest)
            current = nearest
            unvisited.remove(nearest)
        total_distance += current.distance_to(self.depot)

        print("-" * 50)
        print("Nearest Neighbor Solution:")
        print(f"Total distance traveled by the trucks: {total_distance:.2f}")
        print(f"Path: depot -> {' -> '.join([str(customer.cust_no) for customer in route[1:-1]])} -> depot")
        print("-" * 50)
        return total_distance
