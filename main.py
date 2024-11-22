import pandas as pd
import math
import matplotlib.pyplot as plt
import turtle
from time import sleep
from scipy.spatial.distance import cdist


class Node:
    def __init__(self, cust_no, x_coord, y_coord, demand, ready_time, due_date, service_time):
        self.cust_no = cust_no
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.demand = demand
        self.ready_time = ready_time
        self.due_date = due_date
        self.service_time = service_time

    def __str__(self):
        return f"Customer {self.cust_no} at ({self.x_coord}, {self.y_coord}) with demand {self.demand} and ready time {self.ready_time} to {self.due_date} and service time {self.service_time}"

    def distance_to(self, other: 'Node') -> float:
        return math.sqrt((self.x_coord - other.x_coord) ** 2 + (self.y_coord - other.y_coord) ** 2)


class Truck:
    def __init__(self, capa: int):
        self.capacity = capa


class ProjectAlgorithm:
    file_path: str
    turtle_draw_factor: int
    capacity: int
    customers: list
    trucks: list
    warehouse: Node
    screen: turtle.Screen

    def __init__(self, file_path: str, turtle_draw_factor=5):
        self.file_path = file_path
        self.turtle_draw_factor = turtle_draw_factor
        self.capacity = 0
        self.customers = []
        self.trucks = []
        self.screen = turtle.Screen()

    def initialize(self):
        # Reading the vehicle data (lines 3-4)
        vehicle_df = pd.read_csv(self.file_path, skiprows=4, nrows=1, sep='\s+', names=['Number', 'Capacity'])
        # Reading the customer data (after line 9)
        customers_df = pd.read_csv(self.file_path, skiprows=9, sep='\s+', names=['Cust No.', 'XCoord.', 'YCoord.', 'Demand', 'Ready Time', 'Due Date', 'Service Time'])

        # self.screen.setworldcoordinates(-100, -100, 700, 700)
        # self.screen.setup(800, 800, 0, 0)
        # self.draw_customers()
        # turtle.exitonclick()
        # plt.show()

        truck_count = vehicle_df['Number'][0]
        self.capacity = vehicle_df['Capacity'][0]
        self.trucks = [Truck(self.capacity) for _ in range(truck_count)]

        self.customers = [Node(row['Cust No.'], row['XCoord.'], row['YCoord.'], row['Demand'], row['Ready Time'], row['Due Date'], row['Service Time']) for index, row in customers_df.iterrows()]

        self.warehouse = self.customers.pop()

        a = cdist(list(map(lambda x: [x.x_coord, x.y_coord], self.customers)), list(map(lambda x: [x.x_coord, x.y_coord], self.customers)), metric='euclidean')
        print(a)

    def plot(self):
        # Plotting the graph
        plt.figure(figsize=(10, 8))
        plt.scatter([c.x_coord for c in self.customers], [c.y_coord for c in self.customers], c='blue', label='Customers', s=50)
        plt.scatter(self.warehouse.x_coord, self.warehouse.y_coord, c='red', label='Depot', s=100, marker='x')
        plt.title('Customer Locations (X vs Y Coordinates)')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.grid(True)
        plt.legend()

    def draw_customers(self):
        """
        Draw the customers on the screen with turtle
        :return: None
        """
        turtle.speed(0)
        turtle.hideturtle()
        turtle.penup()

        turtle.goto(self.warehouse.x_coord * self.turtle_draw_factor, self.warehouse.y_coord * self.turtle_draw_factor)
        turtle.pendown()
        turtle.dot(10, 'red')
        turtle.write("Depot")
        turtle.penup()
        for i in range(len(self.customers)):
            turtle.goto(self.customers[i].x_coord * self.turtle_draw_factor, self.customers[i].y_coord * self.turtle_draw_factor)
            turtle.pendown()
            turtle.dot(10, 'blue')
            turtle.penup()

    def run(self):
        time = 0
        last_customer = self.warehouse

        self.customers.sort(key=lambda x: x.ready_time)

        next_customer = self.customers.pop()
        while len(self.customers) > 0:
            # Calculate the time to go to the next customer
            time += last_customer.distance_to(next_customer)

            # Add the service time
            time += next_customer.service_time

            # Remove the demand from the truck
            self.trucks[0].capacity -= next_customer.demand

            # TURTLE
            turtle.goto(last_customer.x_coord * self.turtle_draw_factor, last_customer.y_coord * self.turtle_draw_factor)
            turtle.pendown()
            turtle.goto(next_customer.x_coord * self.turtle_draw_factor, next_customer.y_coord * self.turtle_draw_factor)
            turtle.penup()

            print("Serving customer", next_customer.cust_no, "at time", time)

            if time <= next_customer.ready_time:
                for i in range(len(self.customers)):
                    if time <= self.customers[i].ready_time:
                        last_customer = next_customer
                        next_customer = self.customers.pop(i)
                        break
            else:
                last_customer = next_customer
                next_customer = self.customers.pop()

            if self.trucks[0].capacity < next_customer.demand:
                print("Truck is full, returning to depot")
                time += last_customer.distance_to(self.warehouse)
                last_customer = self.warehouse
                next_customer = self.customers.pop()
                self.trucks[0].capacity = capacity

            sleep(0.01)

        turtle.exitonclick()
        plt.show()
        print("Time to visit all customers:", time)


if __name__ == '__main__':
    project = ProjectAlgorithm('r202.txt')
    project.initialize()