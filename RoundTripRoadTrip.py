import sys
import time

from Graph import Graph


class RoadTrip:
    """
    A class representing a road trip.

    Attributes:
        startLoc (startLoc): Start location of the road trip.
        edges (dict): A dictionary of edges in the graph.
        location_visits (dict): Tracks number of visits to each location.
        edge_visits (dict): Tracks number of visits to each edge.
        required_locations (dict): A dictionary of required locations.
        forbidden_locations (dict): A dictionary of forbidden locations.
    """
    def __init__(self, startLoc, required_locations=None, forbidden_locations=None):
        self.startLoc = startLoc
        self.edges = []  # List of edges in the road trip
        self.location_visits = {}
        self.edge_visits = {}
        self.required_locations = required_locations if required_locations is not None else []
        self.forbidden_locations = forbidden_locations if forbidden_locations is not None else []

    def add_edge(self, edge):
        self.edges.append(edge)
        # Increment visit count for each location
        self.increment_visit(edge.location2.label)
        self.increment_edge_visit((edge.location1.label, edge.location2.label))

    def increment_visit(self, location_label):
        self.location_visits[location_label] = self.location_visits.get(location_label, 0) + 1

    def increment_edge_visit(self, edge_label):
        self.edge_visits[edge_label] = self.edge_visits.get(edge_label, 0) + 1

    def total_preference(self, graph):
        total_pref = 0

        for edge_label, visits in self.edge_visits.items():
            for i in range(visits):
                if i > 3:
                    continue
                total_pref += graph.edges[edge_label].preference * (1 - 0.25) ** (i)

        for location_label, visits in self.location_visits.items():
            for i in range(visits):
                total_pref += graph.locations[location_label].preference * (1 - 0.25) ** (i)

        return total_pref

    def time_estimate(self, speed):
        total = 0
        for edge in self.edges:
            total += edge.time_on_edge(speed)
            total += edge.location2.time_at_location()
        return total

    def print_edges(self, speed, graph, results_file, maxTime, count):
        with open(results_file, 'a') as f:
            print(
                f"Solution {count} | start_location: {self.startLoc} | max_time: {maxTime} hours | speed: {speed} mph")
            f.write(f"Solution {count} | start_location: {self.startLoc} | max_time: {maxTime} | speed: {speed}\n")

            for i, edge in enumerate(self.edges):
                inter_loc_label = edge.location2.label
                edge_time = edge.time_on_edge(speed)

                inter_loc_pref = graph.locations[inter_loc_label].preference
                inter_loc_time = graph.locations[inter_loc_label].time_at_location()

                print(
                    f"{i + 1}. {edge.location1.label} to {edge.location2.label} | label: {edge.label} | edge_pref: {edge.preference:.4f}, edge_time: {edge_time:.2f} hours, inter_loc_pref: {inter_loc_pref:.4f}, inter_loc_time: {inter_loc_time:.2f} hours")
                f.write(
                    f"{i + 1}. {edge.location1.label} to {edge.location2.label} | label: {edge.label} | edge_pref: {edge.preference:.4f}, edge_time: {edge_time:.2f} hours, inter_loc_pref: {inter_loc_pref:.4f}, inter_loc_time: {inter_loc_time:.2f} hours\n")

            total_trip_preference = self.total_preference(graph)
            total_trip_distance = sum(edge.distance for edge in self.edges)
            total_trip_time = self.time_estimate(speed)

            print(
                f"start_from: {self.startLoc} | total_trip_preference: {total_trip_preference:.4f} | total_distance: {total_trip_distance:.3f} miles | total_trip_time: {total_trip_time:.2f} hours")
            f.write(
                f"start_from: {self.startLoc} | total_trip_preference: {total_trip_preference:.4f} | total_distance: {total_trip_distance:.0f} miles | total_trip_time: {total_trip_time:.2f} hours\n\n")
            count += 1

    def is_valid(self, required_locations, forbidden_locations):
        # Check if all required locations are visited
        for loc in required_locations:
            if loc not in self.location_visits:
                return False
        # Check if any forbidden location is visited
        for loc in forbidden_locations:
            if loc in self.location_visits:
                return False
        return True


def RoundTripRoadTrip(startLoc, LocFile, EdgeFile, maxTime, x_mph, results_file, required_locations=[],
                      forbidden_locations=[]):
    """
    Returns road trips based on given constraints.

    Args:
        startLoc (Location): Start location of road trip.
        LocFile (CSV file): CSV file containing locations, themes, and utilities.
        EdgeFile (CSV file): CSV file containing edges, themes, and utilities.
        maxTime (int): Max hours wanted for road trip.
        x_mph (int): Average speed of road trip.
        results_file (txt file): File that records road trip results.
        required_locations (array): Locations required by user.
        forbidden_locations (array): Locations forbidden by user.

    Returns:
        None
    """
    # Create a graph and read locations and edges from files
    graph = Graph()
    graph.read_locations(LocFile)
    graph.read_edges(EdgeFile)

    # Assign preferences to locations and edges
    graph.location_preference_assignments(LocFile)
    graph.edge_preference_assignments(EdgeFile)

    current_road_trip = RoadTrip(startLoc, required_locations=required_locations, forbidden_locations=forbidden_locations)
    max_distance = maxTime * x_mph

    stack = [current_road_trip]

    # Collect statistics for summary
    solution_preferences = []
    max_preference = float('-inf')
    min_preference = float('inf')
    total_runtime = 0

    solutions = []

    user_input = "yes"
    start_time = time.time()
    total_time = 0
    with open(results_file, "w") as f:  # Open the file in write mode
        count = 1
        while stack and user_input.lower() == "yes":
            current_road_trip = stack.pop()

            # starting location, add all the roads from surrounding edges to stack
            if not current_road_trip.edges:
                surrounding_edges = graph.get_edges_from_location(current_road_trip.startLoc)
                # Sort array in descending order based on their preference
                surrounding_edges.sort(key=lambda x: x.preference, reverse=True)
                for edge in surrounding_edges:
                    # print(edge.location1.label, " to", edge.location2.label, " is being checked")
                    if edge.distance < max_distance:
                        newRoadTrip = RoadTrip(startLoc=current_road_trip.startLoc,
                                               required_locations=required_locations,
                                               forbidden_locations=forbidden_locations)
                        newRoadTrip.add_edge(edge)
                        stack.append(newRoadTrip)

            # if not starting location, add all the surrounding edges to stack
            else:
                # check if the last edge is the starting location
                lastEdge = current_road_trip.edges[-1]

                if lastEdge.location2.label == startLoc:

                    if current_road_trip.time_estimate(x_mph) < maxTime * 0.5:
                        continue

                    f = open(results_file, "a")
                    current_road_trip.print_edges(x_mph, graph, results_file, maxTime, count)
                    f.close()
                    solutions.append(current_road_trip)
                    return current_road_trip

                    end_time = time.time()
                    total_runtime += end_time - start_time
                    start_time = time.time()

                    user_input = input("Do you want to continue? (yes/no) ").lower()
                    count += 1

                    if user_input == "yes":
                        # Sort the stack based on road trip preference
                        stack.sort(key=lambda x: x.total_preference(graph))

                        # Pop half of the lowest preference elements on the stack
                        stack = stack[:int(len(stack) / 1.2)]
                        continue
                    else:
                        max_preference, min_preference = 0, float('inf')
                        total_preference = 0
                        for solution in solutions:
                            preference = solution.total_preference(graph)
                            total_preference += preference
                            if preference > max_preference:
                                max_preference = preference
                            if preference < min_preference:
                                min_preference = preference
                        average_preference = total_preference / len(solutions)
                        average_time = total_runtime / len(solutions)

                        print("\nSummary:")
                        print(f"Total Solutions: {len(solutions)}")
                        print(f"Average Instrumented Runtime: {average_time} seconds")
                        print(f"Maximum TotalTripPreference: {max_preference}")
                        print(f"Average TotalTripPreference: {average_preference}")
                        print(f"Minimum TotalTripPreference: {min_preference}")

                        # Print summary to screen and write to the file
                        with open(results_file, 'a') as f:
                            sys.stdout = f  # Redirect standard output to the file

                            print("\nSummary:")
                            print(f"Total Solutions: {len(solutions)}")
                            print(f"Average Instrumented Runtime: {average_time} seconds")
                            print(f"Maximum TotalTripPreference: {max_preference}")
                            print(f"Average TotalTripPreference: {average_preference}")
                            print(f"Minimum TotalTripPreference: {min_preference}")

                        # Reset standard output to the console
                        sys.stdout = sys.__stdout__
                        break

                surrounding_edges = graph.get_edges_from_location(lastEdge.location2.label)

                # Sort array in descending order based on their preference
                next_trips = []
                for edge in surrounding_edges:
                    if edge.location2.label in forbidden_locations:
                        continue  # Skip forbidden locations
                    newRoadTrip = RoadTrip(current_road_trip.startLoc, required_locations=required_locations,
                                           forbidden_locations=forbidden_locations)
                    newRoadTrip.edges = current_road_trip.edges.copy()
                    newRoadTrip.location_visits = current_road_trip.location_visits.copy()
                    newRoadTrip.edge_visits = current_road_trip.edge_visits.copy()
                    newRoadTrip.add_edge(edge)
                    if newRoadTrip.time_estimate(x_mph) < maxTime and newRoadTrip.is_valid(required_locations,
                                                                                           forbidden_locations):
                        next_trips.append(newRoadTrip)

                # Sort the stack based on heuristic
                if current_road_trip.time_estimate(x_mph) < maxTime / 1.2:
                    next_trips.sort(key=lambda x: (
                            graph.get_direct_distance(current_road_trip.startLoc, x.edges[-1].location2.label) + (
                                x.total_preference(graph) - current_road_trip.total_preference(graph)) * 100),
                                    reverse=False)
                else:
                    next_trips.sort(
                        key=lambda x: -graph.get_direct_distance(current_road_trip.startLoc,
                                                                 x.edges[-1].location2.label),
                        reverse=False)
                stack.extend(next_trips)

        if not solutions:  # If the solutions list is empty
            print("Error: No valid road trip could be found with the given constraints.")

    return solutions[0]


if __name__ == '__main__':
    startLoc = 'NewOrleansLA'
    LocFile = 'LocThemesUtil.csv'
    EdgeFile = 'EdgeThemesUtil.csv'
    maxTime = 30
    x_mph = 80
    results_file = "results.txt"

    required_input = input("Enter required locations (comma-separated, no spaces): ")
    forbidden_input = input("Enter forbidden locations (comma-separated, no spaces): ")

    required_locations = required_input.split(',') if required_input else []
    forbidden_locations = forbidden_input.split(',') if forbidden_input else []

    RoundTripRoadTrip(startLoc, LocFile, EdgeFile, maxTime, x_mph, results_file, required_locations,
                      forbidden_locations)
