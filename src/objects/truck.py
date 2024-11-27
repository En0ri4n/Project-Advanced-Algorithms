class Truck:
    """
    Represents a truck in the vehicle routing problem.

    Attributes:
        capacity (int): The capacity of the truck.
        route (list): The route of the truck, which is a list of customers.
        load (int): The current load of the truck.
        time (int): The current time of the truck.
    """

    def __init__(self, capacity):
        self.capacity = capacity
        self.route = []
        self.load = 0
        self.time = 0
