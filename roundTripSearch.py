"""
    (a)
    Group 5: Program 3
    Team Members: Michelle Wang, Joanna Yi, Neelasha Bhattacharjee, Ethan Jeong

"""



import copy
import sys
import time

import random
import csv

class Edge:
    def __init__(self, label, location1, location2, distance):
        self.label = label
        self.location1 = location1
        self.location2 = location2
        self.distance = distance
        self.preference = 0  # This will be set using the preference assignment function

    def time_on_edge(self, speed):
        """
        Calculates the time taken to traverse the edge at the given speed.

        Args:
            speed (float): The speed at which the edge is traversed.

        Returns:
            float: The time taken to traverse the edge.
        """
        return self.distance / speed

class Location:
    def __init__(self, label, latitude, longitude):
        self.label = label
        self.latitude = latitude
        self.longitude = longitude
        self.preference = 0  # This will be set using the preference assignment function

    def time_at_location(self):
        """
        Calculates the time spent at the location based on the preference. Our team decides that
        the time spent at a location is twice the preference value.

        Returns:
            int: The calculated time spent at the location.
        """
        return self.preference * 2


class Graph:
    """
    A class representing a graph.

    Attributes:
        locations (dict): A dictionary of locations in the graph.
        edges (dict): A dictionary of edges in the graph.
    """

    def __init__(self):
        self.locations = {}  # key: location label, value: Location object
        self.edges = {}  # key: (location1, location2), value: Edge object

    def add_location(self, location):
        """
        Adds a location to the graph.

        Args:
            location (Location): The location object to be added.

        Returns:
            None
        """
        self.locations[location.label] = location

    def add_edge(self, edge):
        """
        Adds an edge to the graph.

        Args:
            edge (Edge): The edge object to be added.

        Returns:
            None
        """
        key = (edge.location1.label, edge.location2.label)
        self.edges[key] = edge

    def location_preference_assignments(self, a, b):
        """
        Assigns random preference values to each location in the graph.

        Args:
            a (float): The lower bound of the preference range.
            b (float): The upper bound of the preference range.

        Returns:
            None
        """
        for location in self.locations.values():
            location.preference = random.uniform(a, b)

    def edge_preference_assignments(self, a, b):
        """
        Assigns random preference values to each edge in the graph.

        Args:
            a (float): The lower bound of the preference range.
            b (float): The upper bound of the preference range.

        Returns:
            None
        """
        for edge in self.edges.values():
            edge.preference = random.uniform(a, b)

    def read_locations(self, file_name):
        """
        Reads locations from a CSV file and adds them to the graph.

        Args:
            file_name (str): The path to the CSV file.

        Returns:
            None
        """
        with open(file_name, newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                label, latitude, longitude = row[0], row[1], row[2]
                location = Location(label, float(latitude), float(longitude))
                self.add_location(location)

    def read_edges(self, file_name):
        """
        Reads edges from a CSV file and adds them to the graph.

        Args:
            file_name (str): The path to the CSV file.

        Returns:
            None
        """
        with open(file_name, newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                label, loc_a, loc_b, distance = row[0], row[1], row[2], row[3]
                if loc_a in self.locations and loc_b in self.locations and 50.0 < float(distance) < 200.0:
                    edge = Edge(label, self.locations[loc_a], self.locations[loc_b], float(distance))
                    edge1 = Edge(label, self.locations[loc_b], self.locations[loc_a], float(distance))
                    self.add_edge(edge)
                    self.add_edge(edge1)

    def get_edges_from_location(self, location_label):
        """
        Returns a list of edges connected to the specified location.

        Parameters:
            location_label (str): The label of the location.

        Returns:
            list: A list of edges connected to the specified location.
        """
        return [edge for (loc1, loc2), edge in self.edges.items() if loc1 == location_label]

    def get_direct_distance(self, location1: str, location2: str):
        """
        Calculates the direct distance between two locations.

        Args:
            location1 (str): The name of the first location.
            location2 (str): The name of the second location.

        Returns:
            float: The direct distance between the two locations.
        """
        return ((self.locations[location1].latitude - self.locations[location2].latitude) ** 2 + (
                    self.locations[location1].longitude - self.locations[location2].longitude) ** 2) ** 0.5



class RoadTrip:

    def __init__(self, startLoc):
        self.startLoc = startLoc
        self.edges = []  # List of edges in the road trip
        self.location_visits = {}  # Tracks the number of visits to each location
        self.edge_visits = {}  # Tracks the number of visits to each edge

    def add_edge(self, edge):
        """
        Adds an edge to the graph.

        Parameters:
        - edge: The edge to be added.

        """
        self.edges.append(edge)
        # Increment visit count for each location
        self.increment_visit(edge.location2.label)
        self.increment_edge_visit((edge.location1.label, edge.location2.label))

    def increment_visit(self, location_label):
        """
        Increments the visit count for a given location so taht we can track the number of times a location is visited.
        When a location is visited, we decrease its preference by 20 percent

        Args:
            location_label (str): The label of the location to increment the visit count for.
        """
        self.location_visits[location_label] = self.location_visits.get(location_label, 0) + 1

    def increment_edge_visit(self, edge_label):
        """
        Increments the visit count for a given edge label.

        Args:
            edge_label (str): The label of the edge to increment the visit count for.
        """
        self.edge_visits[edge_label] = self.edge_visits.get(edge_label, 0) + 1

    def total_preference(self, graph):
            """
            Calculates the total preference score for the round trip search. Visited locations and edges 
            have their preference decreased by 20 percent for each visit.

            Parameters:
            - graph (Graph): The graph object containing the edges and locations.

            Returns:
            - total_pref (float): The total preference score.
            """
            total_pref = 0

            for edge_label, visits in self.edge_visits.items():
                for i in range(visits):
                    if i > 3:
                        continue
                    total_pref += graph.edges[edge_label].preference * (1 - 0.80) ** (i)

            for location_label, visits in self.location_visits.items():
                for i in range(visits):
                    total_pref += graph.locations[location_label].preference * (1 - 0.80) ** (i)

            return total_pref

    def time_estimate(self, speed):
        """
        Calculates the estimated time for completing the round trip based on the given speed.

        Args:
            speed (float): The speed at which the round trip is being made.

        Returns:
            float: The estimated time for completing the round trip.
        """
        total = 0
        for edge in self.edges:
            total += edge.time_on_edge(speed)
            total += edge.location2.time_at_location()
        return total

    def print_edges(self, speed, graph, results_file, maxTime, count):
        """
        Print the edges of the round trip and write them to a results file.

        Parameters:
        - speed (float): The speed of the trip in mph.
        - graph (Graph): The graph containing the locations and edges.
        - results_file (str): The file path of the results file.
        - maxTime (int): The maximum time allowed for the trip in hours.
        - count (int): The solution count.

        Returns:
        None
        """
        with open(results_file, 'a') as f:
            print(f"Solution {count} | start_location: {self.startLoc} | max_time: {maxTime} hours | speed: {speed} mph")
            f.write(f"Solution {count} | start_location: {self.startLoc} | max_time: {maxTime} | speed: {speed}\n")

            for i, edge in enumerate(self.edges):
                inter_loc_label = edge.location2.label
                edge_time = edge.time_on_edge(speed)

                inter_loc_pref = graph.locations[inter_loc_label].preference
                inter_loc_time = graph.locations[inter_loc_label].time_at_location()

                print(f"{i + 1}. {edge.location1.label} to {edge.location2.label} | label: {edge.label} | edge_pref: {edge.preference:.4f}, edge_time: {edge_time:.2f} hours, inter_loc_pref: {inter_loc_pref:.4f}, inter_loc_time: {inter_loc_time:.2f} hours")
                f.write(
                    f"{i + 1}. {edge.location1.label} to {edge.location2.label} | label: {edge.label} | edge_pref: {edge.preference:.4f}, edge_time: {edge_time:.2f} hours, inter_loc_pref: {inter_loc_pref:.4f}, inter_loc_time: {inter_loc_time:.2f} hours\n")

            total_trip_preference = self.total_preference(graph)
            total_trip_distance = sum(edge.distance for edge in self.edges)
            total_trip_time = self.time_estimate(speed)

            print(f"start_from: {self.startLoc} | total_trip_preference: {total_trip_preference:.4f} | total_distance: {total_trip_distance:.3f} miles | total_trip_time: {total_trip_time:.2f} hours")
            f.write(f"start_from: {self.startLoc} | total_trip_preference: {total_trip_preference:.4f} | total_distance: {total_trip_distance:.0f} miles | total_trip_time: {total_trip_time:.2f} hours\n\n")
            count += 1


def RoundTripRoadTrip(startLoc, LocFile, EdgeFile, maxTime, x_mph, results_file):
    """
    Performs a round trip road trip search starting from a given location.

    Args:
        startLoc (str): The starting location for the road trip.
        LocFile (str): The file path to the location data file.
        EdgeFile (str): The file path to the edge data file.
        maxTime (float): The maximum time allowed for the road trip.
        x_mph (float): The speed in miles per hour.
        results_file (str): The file path to write the results.

    Returns:
        None
    """
    # Create a graph and read locations and edges from files
    graph = Graph()
    graph.read_locations(LocFile)
    graph.read_edges(EdgeFile)

    # Assign preferences to locations and edges
    graph.location_preference_assignments(0, 1)
    graph.edge_preference_assignments(0, 0.1)

    current_road_trip = RoadTrip(startLoc)
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
                        newRoadTrip = RoadTrip(startLoc=current_road_trip.startLoc)
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
                    newRoadTrip = RoadTrip(current_road_trip.startLoc)
                    newRoadTrip.edges = current_road_trip.edges.copy()
                    newRoadTrip.location_visits = current_road_trip.location_visits.copy()
                    newRoadTrip.edge_visits = current_road_trip.edge_visits.copy()
                    newRoadTrip.add_edge(edge)
                    if newRoadTrip.time_estimate(x_mph) < maxTime:
                        next_trips.append(newRoadTrip)

                # Sort the stack based on heuristic
                if current_road_trip.time_estimate(x_mph) < maxTime / 1.2:
                    next_trips.sort(key=lambda x: (
                            graph.get_direct_distance(current_road_trip.startLoc, x.edges[-1].location2.label) + (x.total_preference(graph) - current_road_trip.total_preference(graph)) * 100),reverse=False)
                else:
                    next_trips.sort(
                        key=lambda x: -graph.get_direct_distance(current_road_trip.startLoc, x.edges[-1].location2.label),
                        reverse=False)
                stack.extend(next_trips)


    return


if __name__ == '__main__':
    RoundTripRoadTrip('CharlotteNC', 'Locations.csv', 'Edges.csv', 100, 80, "results.txt")



"""
    (f)

    First Test Run Summary:
        Summary:
        Total Solutions: 4
        Average Instrumented Runtime: 1.1754133105278015 seconds
        Maximum TotalTripPreference: 9.951849868928267
        Average TotalTripPreference: 9.88461091828955
        Minimum TotalTripPreference: 9.817371967650832

    Second Test Run Summary:
        Summary:
        Total Solutions: 6
        Average Instrumented Runtime: 0.9235462745030721 seconds
        Maximum TotalTripPreference: 20.37008625831607
        Average TotalTripPreference: 17.503533464275634
        Minimum TotalTripPreference: 16.425904481262737

    Third Test Run Summary:
        Summary:
        Total Solutions: 5
        Average Instrumented Runtime: 0.6727949142456054 seconds
        Maximum TotalTripPreference: 17.4129207274496
        Average TotalTripPreference: 16.24065758696462
        Minimum TotalTripPreference: 14.200091512029376

"""