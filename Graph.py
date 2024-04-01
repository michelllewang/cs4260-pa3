import Edge
import Location
import csv


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

    def location_preference_assignments(self, locations_file):
        """
        Assigns preference values to each location in the graph.

        Args:
            locations_file (string): File containing locations.

        Returns:
            None
        """
        with open(locations_file, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                location_label = row['Location Label']
                utility = float(row['Utility'])
                self.locations[location_label].preference = utility

    def edge_preference_assignments(self, edges_file):
        """
        Assigns preference values to each edge in the graph.

        Args:
            edges_file (string): File containing edges.

        Returns:
            None
        """
        with open(edges_file, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                edge_label = row['edgeLabel']
                location1_label = row['locationA']
                location2_label = row['locationB']
                utility = float(row['Utility'])
                edge_key = (location1_label, location2_label)
                if edge_key in self.edges:
                    self.edges[edge_key].preference = utility
                else:
                    edge_key_reversed = (location2_label, location1_label)
                    if edge_key_reversed in self.edges:
                        self.edges[edge_key_reversed].preference = utility
                    else:
                        continue
                        # print(f"Edge not found for edge label: {edge_label}")

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
                location = Location.Location(label, float(latitude), float(longitude))
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
                    edge = Edge.Edge(label, self.locations[loc_a], self.locations[loc_b], float(distance))
                    edge1 = Edge.Edge(label, self.locations[loc_b], self.locations[loc_a], float(distance))
                    self.add_edge(edge)
                    self.add_edge(edge1)

    def get_edges_from_location(self, location_label):
        return [edge for (loc1, loc2), edge in self.edges.items() if loc1 == location_label]

    def get_direct_distance(self, location1: str, location2: str):
        return ((self.locations[location1].latitude - self.locations[location2].latitude) ** 2 + (
                    self.locations[location1].longitude - self.locations[location2].longitude) ** 2) ** 0.5






