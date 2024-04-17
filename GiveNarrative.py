from openai import OpenAI
from RoundTripRoadTrip import RoadTrip
from RoundTripRoadTrip import RoundTripRoadTrip

OPENAI_KEY = "REPLACE THIS WITH YOUR OWN KEY TO RUN THE CODE."

client = OpenAI(api_key=OPENAI_KEY)


def give_narrative(road_trip):
    """
    Generates a description of the attractions that could be visited based on a given road trip.

    :param road_trip: RoadTrip object.
    :return: None
    """

    locations = [road_trip.startLoc]  # Adds start location to list of locations

    # Iterates through road trip edges and adds locations to existing list
    for edge in road_trip.edges:
        locations.append(edge.location2.label)

    # Generates a message based on the locations list
    # Since the regression tree was built on user preferences for food, music, and nature, those user preferences
    # were incorporated into the message.
    message_content = (
        f"Give a description of the attractions that someone on a road trip from "
        f"{', '.join(locations)} may see in a paragraph form. "
        f"Also include attractions someone may see driving in between these locations. "
        f"The user prefers attractions related to food, music, and nature."
    )

    # Uses the OpenAI Chat Completion model to generate a response from the API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        max_tokens=1000,
        response_format={"type": "text"},
        messages=[
            {"role": "user", "content": message_content}
        ]
    )

    api_response_content = response.choices[0].message.content  # Stores the first text response returned by API

    # Writes the API response into the results.txt file
    with open(results_file, "a") as f:
        f.write(api_response_content + "\n")

    print(api_response_content)


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

    new_road_trip = RoundTripRoadTrip(startLoc, LocFile, EdgeFile, maxTime, x_mph, results_file, required_locations,
                      forbidden_locations)

    if new_road_trip:
        give_narrative(new_road_trip)


