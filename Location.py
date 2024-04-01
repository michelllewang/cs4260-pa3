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