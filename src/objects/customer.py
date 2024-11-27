import src.variables as vars

class Customer:
    """
    Represents a customer in the vehicle routing problem.

    Attributes:
        cust_no (int): The customer number.
        x_coord (float): The x-coordinate of the customer's location.
        y_coord (float): The y-coordinate of the customer's location.
        demand (int): The demand of the customer.
        ready_time (int): The earliest time the customer is ready for service.
        due_date (int): The latest time the customer can be serviced.
        service_time (int): The time required to service the customer.
    """

    def __init__(self, cust_no, x_coord, y_coord, demand, ready_time, due_date, service_time):
        self.cust_no = cust_no
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.demand = demand
        self.ready_time = ready_time
        self.due_date = due_date
        self.service_time = service_time

    def distance_to(self, other):
        """
        Calculates the distance to another customer.

        Parameters:
            other (Customer): The other customer to calculate the distance to.

        Returns:
            float: The distance to the other customer.
        """
        return vars.distance_matrix[self.cust_no][other.cust_no]

    def __str__(self):
        return f"Customer {self.cust_no}"

    def __repr__(self):
        return self.__str__()