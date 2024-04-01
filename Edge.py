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
