import matplotlib.pyplot as plt

colors = [
    "#0000FF",  # Blue
    "#FF0000",  # Red
    "#008000",  # Green
    "#FFA500",  # Orange
    "#800080",  # Purple
    "#00FFFF",  # Cyan
    "#FF00FF",  # Magenta
    "#FFFF00",  # Yellow
    "#FFC0CB",  # Pink
    "#A52A2A",  # Brown
    "#00FF00",  # Lime
    "#008080",  # Teal
    "#000080",  # Navy
    "#800000",  # Maroon
    "#FFD700",  # Gold
    "#EE82EE",  # Violet
    "#4B0082",  # Indigo
    "#808000",  # Olive
    "#40E0D0",  # Turquoise
    "#808080"  # Gray
]

def plot_routes(solution, depot):
    plt.figure(figsize=(10, 8))
    for i in range(len(solution)):
        route = solution[i]
        route_x = [depot.x_coord] + [customer.x_coord for customer in route[1:-1]] + [depot.x_coord]
        route_y = [depot.y_coord] + [customer.y_coord for customer in route[1:-1]] + [depot.y_coord]
        plt.plot(route_x, route_y, marker='o', color=colors[i % len(colors)], label=f'Truck {i + 1}', linestyle='--')
        # Show name on the point
        for i, customer in enumerate(route[1:-1]):
            plt.text(customer.x_coord, customer.y_coord, f"{customer.cust_no}", fontsize=9, ha='center', va='center')
    plt.scatter(depot.x_coord, depot.y_coord, c='red', label='Depot', s=100, marker='x')
    plt.title('Truck Routes')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.grid(True)
    plt.legend()
    plt.show()


def print_truck_usage(solution, depot, show_graphics=True):
    """
    Prints the capacity used by each truck, the total distance, and the total time for each route.
    Also plots the routes for each truck.

    Parameters:
    solution (list): A list of routes, where each route is a list of customers.
    depot (Customer): The depot (warehouse) object.
    """
    truck_count = 0  # Initialize the truck count
    max_global_time = 0  # Initialize the total time
    max_distance = 0  # Initialize the total distance

    for i, route in enumerate(solution):  # Iterate over each route in the solution
        load = sum(customer.demand for customer in route[1:-1])  # Calculate the load for the current route
        if load > 0:  # If the load is greater than 0
            truck_count += 1  # Increment the truck count

            # Calculate the total distance for the current route
            total_distance = sum(route[j].distance_to(route[j + 1]) for j in range(len(route) - 1))

            # Calculate the total time for the current route
            total_time = sum(customer.service_time for customer in route[1:-1]) + total_distance  # Assuming time is proportional to distance

            if max_global_time < total_time:
                max_global_time = total_time

            max_distance += total_distance

            if show_graphics:
                # Print the details for the current truck
                print('-' * 50)
                print(f"Truck #{i + 1}")
                print(f"Path: depot -> {''.join([f'{customer.cust_no} -> ' for customer in route[1:-1]])}depot")
                print(f"Capacity used = {load}")
                print(f"Total distance = {total_distance:.2f}")
                print(f"Total time = {total_time:.2f}")

                # Plot the route
                plt.figure()  # Create a new figure for each truck
                route_x = [depot.x_coord] + [customer.x_coord for customer in route[1:-1]] + [depot.x_coord]
                route_y = [depot.y_coord] + [customer.y_coord for customer in route[1:-1]] + [depot.y_coord]
                plt.plot(route_x, route_y, marker='o', color=colors[i % len(colors)], label=f'Truck {i + 1}')
                for customer in route[1:-1]:
                    plt.text(customer.x_coord, customer.y_coord, f"{customer.cust_no}", fontsize=9, ha='center', va='center')

                plt.scatter(depot.x_coord, depot.y_coord, c='red', label='Depot', s=100, marker='x')
                plt.title(f'Truck {i + 1} Route')
                plt.xlabel('X Coordinate')
                plt.ylabel('Y Coordinate')
                plt.grid(True)
                plt.legend()
                plt.show()

    print('-' * 100)
    print(f"Total number of trucks used: {truck_count}")  # Print the total number of trucks used
    print(f"Max distance: {max_distance:.2f}")  # Print the total number of trucks
    print(f"Max global time: {max_global_time:.2f}")  # Print the total number of trucks used
    print("\n" * 3)


# Plot the cost history of the ACO algorithm with each iteration
def print_costs_history(costs):
    plt.figure(figsize=(12, 6))
    plt.plot(
        range(1, len(costs) + 1), costs,
        marker='o', markersize=6,
        linestyle='', linewidth=1.5,
        color='b', label='Cost'
    )
    plt.title('Cost History', fontsize=16, fontweight='bold')
    plt.xlabel('Iteration', fontsize=14)
    plt.ylabel('Cost', fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True, linestyle=':', linewidth=0.7)
    plt.legend(fontsize=12)
    plt.tight_layout()
    plt.show()